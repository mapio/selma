import networkx as nx
import numpy as np

from manim import VGroup, Text, Rectangle, MoveAlongPath, Arc, Animation, DARK_BROWN

from selma import BACKGROUND, FOREGROUND, MANIM_HEIGHT, MANIM_WIDTH
from selma.geom import compute_arc, arc_intersect, shortest_arc

EDGE_RADIUS = 10
TIP_SIZE = 0.15
ARROW_STROKE = 2
BORDER = 0.3
BORDER_COLOR = DARK_BROWN


def test_draw(G, layout):
  pos = {node: (pos[0], pos[1]) for node, pos in layout(G).items()}
  nx.draw_networkx_edges(
    G, pos, edge_color='black', connectionstyle='arc3,rad=0.1', arrows=True
  )
  _ = nx.draw_networkx_labels(G, pos)


def rescale_pos(pos_array, heightscale=1):
  height = MANIM_HEIGHT * heightscale
  width = MANIM_WIDTH / MANIM_HEIGHT * height

  min_x, min_y = np.min(pos_array, axis=0)
  max_x, max_y = np.max(pos_array, axis=0)

  # Map the positions to the new rectangle
  pos_array[:, 0] = (pos_array[:, 0] - min_x) / (max_x - min_x) * width - width / 2
  pos_array[:, 1] = (pos_array[:, 1] - min_y) / (max_y - min_y) * height - height / 2

  return pos_array


def gvlayout_factory(algo='dot', fontsize=32, heightscale=1):
  def gvlayout(G):
    A = nx.nx_agraph.to_agraph(G)
    A.node_attr.update(fontsize=fontsize, shape='box')
    A.layout(algo)

    pos_array = rescale_pos(
      np.array(
        [A.get_node(node).attr['pos'].split(',') for node in G.nodes()], dtype=float
      ),
      heightscale,
    )

    return {
      node: np.array([pos_array[i, 0], pos_array[i, 1], 0])
      for i, node in enumerate(G.nodes())
    }

  return gvlayout


def _medge(R, S, radius, color=FOREGROUND):
  center, start_angle, arc_angle = compute_arc(R.get_center(), S.get_center(), radius)
  radius = abs(radius)

  arc = Arc(
    radius=radius, start_angle=start_angle, angle=arc_angle, stroke_color=BACKGROUND
  ).move_arc_center_to([center[0], center[1], 0])

  θr = arc_intersect(center, radius, start_angle, arc_angle, R)
  θs = arc_intersect(center, radius, start_angle, arc_angle, S)

  arrow = Arc(
    radius=radius, start_angle=θr, angle=shortest_arc(θr, θs), stroke_color=color
  ).move_arc_center_to([center[0], center[1], 0])
  arrow.set_stroke(width=ARROW_STROKE)
  arrow.add_tip(tip_width=TIP_SIZE, tip_length=TIP_SIZE)

  return arc, arrow


class MGraph:
  def __init__(
    self,
    G,
    layout,
    stroke_color=BORDER_COLOR,
    fill_color=BACKGROUND,
    node_scale=1,
    scale=1,
  ):
    self.G = G
    self.layout = layout
    pos = layout(G)
    self._nodes = {}
    rect = {}
    for node in G.nodes():
      t = Text(node, color=FOREGROUND, font_size=32)
      t.move_to(pos[node])
      r = Rectangle(
        width=t.width + BORDER,
        height=t.height + BORDER,
        fill_color=fill_color,
        fill_opacity=1,
        color=stroke_color,
      ).move_to(t.get_center())
      # r.set_z_index(t.z_index - 1)
      rect[node] = r
      self._nodes[node] = VGroup(r, t).scale(node_scale)
    self._edges = {}
    self._paths = {}
    for s, t in G.edges():
      arc, arrow = _medge(rect[s], rect[t], EDGE_RADIUS)
      # arrow.set_z_index(min(rect[s].z_index, rect[t].z_index) - 1)
      self._edges[(s, t)] = arrow
      self._paths[(s, t)] = arc
    self.mnodes = VGroup(list(self._nodes.values()))
    self.medges = VGroup(list(self._edges.values()))
    self.mgraph = VGroup(self.medges, self.mnodes)
    self.mpaths = VGroup(list(self._paths.values()))
    self.scale(scale)

  def shift(self, pos):
    self.mgraph.shift(pos)
    self.mpaths.shift(pos)

  def scale(self, scale):
    self.mgraph.scale(scale)
    self.mpaths.scale(scale)

  def mnode(self, node):
    return self._nodes[node]

  def medge(self, s, t):
    return self._edges[(s, t)]

  def mpath(self, s, t):
    return self._paths[(s, t)]

  def movealong(self, mobject, s, t) -> Animation:
    mobject.move_to(self._nodes[s])
    return MoveAlongPath(mobject, self.mpath(s, t))
