from manim import config, Scene, Dot, UP, DOWN, PURE_GREEN, GRAY_B, GRAY, BLACK
import networkx as nx

from selma import BACKGROUND
from selma.bags import SBag, QBag
from selma.graph import gvlayout_factory, MGraph


config.background_color = BACKGROUND


# Ronald L. Breiger and Philippa E. Pattison
# Cumulated social roles: The duality of persons and their algebras,
# 1 Social Networks, Volume 8, Issue 3, September 1986, Pages 215-256

FFG = nx.DiGraph(
  [
    ('Acciaiuoli', 'Medici'),
    ('Medici', 'Barbadori'),
    ('Medici', 'Ridolfi'),
    ('Medici', 'Tornabuoni'),
    ('Medici', 'Albizzi'),
    ('Medici', 'Salviati'),
    ('Castellani', 'Peruzzi'),
    ('Castellani', 'Strozzi'),
    ('Peruzzi', 'Strozzi'),
    ('Peruzzi', 'Bischeri'),
    ('Strozzi', 'Ridolfi'),
    ('Strozzi', 'Bischeri'),
    ('Ridolfi', 'Tornabuoni'),
    ('Tornabuoni', 'Guadagni'),
    ('Albizzi', 'Ginori'),
    ('Albizzi', 'Guadagni'),
    ('Salviati', 'Pazzi'),
    ('Bischeri', 'Guadagni'),
    ('Guadagni', 'Lamberteschi'),
    ('Ginori', 'Acciaiuoli'),  # added
    ('Barbadori', 'Castellani'),  # reversed
  ]
)

ff_layout = gvlayout_factory('neato', heightscale=0.7)


class FlorentineFamilyGraph(Scene):
  def construct(self):
    MG = MGraph(FFG, ff_layout, node_scale=0.6)
    self.add(MG.mgraph)


class FlorentineFamilyMarkedGraph(Scene):
  def construct(self):
    MG = MGraph(FFG, ff_layout, node_scale=0.6)
    self.add(MG.mgraph)

    def mark(n):
      mn = MG.mnode(n)
      mn[0].set_fill(color=GRAY_B, opacity=1)
      mn.set(stroke_color=GRAY)

    def highlight(s, color):
      ms = MG.mnode(s)
      ms.set(stroke_color=color)
      for t in FFG.neighbors(s):
        MG.medge(s, t).set_color(color)

    mark('Strozzi')
    highlight('Medici', PURE_GREEN)


def animate_visit(scene, bag, graph, start):
  dot = Dot(color=PURE_GREEN)

  def highlight(s, turnon):
    color = PURE_GREEN if turnon else BLACK
    ms = graph.mnode(s)
    ms.set(stroke_color=color)
    if turnon:
      dot.move_to(ms.get_center())
      scene.add(dot)
      scene.wait(1)
    for t in graph.G.neighbors(s):
      graph.medge(s, t).set_color(color)
    if not turnon:
      scene.remove(dot)

  def give(n):
    if n in give.nodes:
      return
    give.nodes.add(n)
    mn = graph.mnode(n)
    mn[0].set_fill(color=GRAY_B, opacity=1)
    mn.set(stroke_color=GRAY_B)
    scene.play(bag.give(mn.copy()), run_time=0.5)

  give.nodes = set()

  give(start)
  while not bag.is_empty():
    s = bag.peek()
    scene.play(bag.take(), run_time=0.5)
    highlight(s, True)
    for t in graph.G.neighbors(s):
      scene.play(graph.movealong(dot, s, t), run_time=0.5)
      give(t)
    highlight(s, False)


class FlorentineFamilyBFS(Scene):
  def construct(self):
    bag = QBag(width=12, scale=0.6)
    bag.container.rect.to_edge(UP)
    self.add(bag.container.rect)

    graph = MGraph(FFG, ff_layout, scale=0.8, node_scale=0.6)
    graph.shift(DOWN / 2)
    self.add(graph.mgraph)

    animate_visit(self, bag, graph, 'Medici')


class FlorentineFamilyDFS(Scene):
  def construct(self):
    bag = SBag(width=12, scale=0.6)
    bag.container.rect.to_edge(UP)
    self.add(bag.container.rect)

    graph = MGraph(FFG, ff_layout, scale=0.8, node_scale=0.6)
    graph.shift(DOWN / 2)
    self.add(graph.mgraph)

    animate_visit(self, bag, graph, 'Medici')


# Random Geometric Graph


def largest_reachable_subgraph(G):
  m, am, sm = None, 0, None
  for n in G.nodes():
    sp = nx.shortest_path(G, n)
    if len(sp) > am:
      m, am, sm = n, len(sp), sp
  GG = nx.subgraph(G, set(sm) | {m})
  return m, GG


RGG = nx.random_geometric_graph(180, 0.11, seed=5)
RGG = nx.DiGraph(RGG.edges())
RGG = nx.relabel_nodes(RGG, str)
rgg_start, RGG = largest_reachable_subgraph(RGG)

rgg_remap = {o: str(n) for n, o in enumerate(RGG.nodes())}
RGG = nx.relabel_nodes(RGG, rgg_remap.get)
rgg_start = rgg_remap[rgg_start]

rgg_layout = gvlayout_factory('neato', heightscale=0.8)


def fast_visit(scene, bag, graph, start, wait):
  def highlight(s, turnon):
    color = PURE_GREEN if turnon else BLACK
    ms = graph.mnode(s)
    ms.set(stroke_color=color)
    for t in graph.G.neighbors(s):
      graph.medge(s, t).set_color(color)
    if turnon:
      scene.wait(wait)

  def give(n):
    if n in give.nodes:
      return
    give.nodes.add(n)
    mn = graph.mnode(n)
    mn[0].set_fill(color=GRAY_B, opacity=1)
    mn.set(stroke_color=GRAY_B)
    bag.give(mn.copy())

  give.nodes = set()

  give(start)
  while not bag.is_empty():
    s = bag.peek()
    bag.take()
    highlight(s, True)
    for t in graph.G.neighbors(s):
      give(t)
    highlight(s, False)


class RGGBFS(Scene):
  def construct(self):
    MG = MGraph(RGG, rgg_layout, node_scale=0.5)
    self.add(MG.mgraph)
    fast_visit(self, QBag(1, 0.6), MG, rgg_start, 0.5)


class RGGDFS(Scene):
  def construct(self):
    MG = MGraph(RGG, rgg_layout, node_scale=0.5)
    self.add(MG.mgraph)
    fast_visit(self, SBag(1, 0.6), MG, rgg_start, 0.5)
