from random import Random

import networkx as nx
from manim import BLUE, PURE_GREEN, RED, Dot, Scene, interpolate_color
from visits import FFG, RGG

from selma.graph import MGraph, gvlayout_factory

FFGC = nx.DiGraph(
  list(FFG.edges()) + [('Pazzi', 'Barbadori'), ('Lamberteschi', 'Ginori')]
)


def random_walk(scene, G, steps, wait, seed):
  rng = Random(seed)

  MG = MGraph(G, gvlayout_factory('neato', heightscale=0.6), node_scale=0.5)
  scene.add(MG.mgraph)

  dot = Dot(color=PURE_GREEN)
  nodes = list(MG.G.nodes())
  visits = {n: 0 for n in nodes}
  s = rng.choice(nodes)
  dot.move_to(MG.mnode(s).get_center())
  scene.add(dot)
  for _ in range(steps):
    visits[s] += 1
    MG.mnode(s)[0].set_fill(color=interpolate_color(BLUE, RED, min(visits[s] / 10, 1)))
    ts = list(MG.G.neighbors(s))
    if rng.random() < 0.2 or not ts:
      t = rng.choice(nodes)
      scene.remove(dot)
      dot.move_to(MG.mnode(s).get_center())
      scene.wait(wait)
      scene.add(dot)
    else:
      t = rng.choice(ts)
      scene.play(MG.movealong(dot, s, t), run_time=wait)
    s = t


class SlowWalk(Scene):
  def construct(self):
    random_walk(self, FFGC, 10, wait=1, seed=40)


class FastWalk(Scene):
  def construct(self):
    random_walk(self, FFGC, 300, wait=0.2, seed=40)


class LargeWalk(Scene):
  def construct(self):
    random_walk(self, RGG, 500, wait=0.1, seed=40)
