import networkx as nx
import numpy as np

from manim import VGroup, Tex, SurroundingRectangle, MoveAlongPath, Arc, BLACK, BLUE

from selma.geom import compute_arc, circle_intersect, shortest_arc, in_arc_range
from selma.animations import AnimationGroup

MANIM_WIDTH = 16
MANIM_HEIGHT = 9
EDGE_RADIUS = 10
TIP_SIZE = 0.15
ARROW_STROKE = 2


def gvlayout_factory(algo='dot', fontsize=32, heightscale=1):
  def gvlayout(G):
    A = nx.nx_agraph.to_agraph(G)
    A.node_attr.update(fontsize='12', shape='box')
    A.layout(algo)

    pos_array = np.array(
      [A.get_node(node).attr['pos'].split(',') for node in G.nodes()], dtype=float
    ).T

    height = MANIM_HEIGHT * heightscale
    width = MANIM_WIDTH / MANIM_HEIGHT * height

    min_x, min_y = np.min(pos_array, axis=1)
    max_x, max_y = np.max(pos_array, axis=1)

    # Map the positions to the new rectangle
    pos_array[0] = (pos_array[0] - min_x) / (max_x - min_x) * width - width / 2
    pos_array[1] = (pos_array[1] - min_y) / (max_y - min_y) * height - height / 2

    return {
      node: np.array([pos_array[0, i], pos_array[1, i], 0])
      for i, node in enumerate(G.nodes())
    }

  return gvlayout


def _medge(R, S, radius):
  center, start_angle, arc_angle = compute_arc(R.get_center(), S.get_center(), radius)
  r = abs(radius)

  # The "full arc"
  arc = Arc(radius=r, start_angle=start_angle, angle=arc_angle).move_arc_center_to(
    [center[0], center[1], 0]
  )

  def _filter(rect):
    candidate = [
      (th, pt)
      for (th, pt) in circle_intersect(center, r, rect)
      if in_arc_range(th, start_angle, arc_angle)
    ]
    if len(candidate) != 1:
      raise ValueError(f'Expected 1 intersection with {R}, got {len(candidate)}.')
    return candidate[0][0]

  θr = _filter(R)
  θs = _filter(S)

  arrow = Arc(radius=r, start_angle=θr, angle=shortest_arc(θr, θs)).move_arc_center_to(
    [center[0], center[1], 0]
  )
  arrow.set(stroke_width=ARROW_STROKE)
  arrow.add_tip(tip_width=TIP_SIZE, tip_length=TIP_SIZE)

  return arc, arrow


class MGraph:
  def __init__(self, G, layout, stroke_color=BLUE, fill_color=BLACK):
    self.G = G
    self.layout = layout
    pos = layout(G)
    self._nodes = {}
    rect = {}
    for node in G.nodes():
      t = Tex(node, font_size=32)
      t.move_to(pos[node])
      r = SurroundingRectangle(
        t, fill_color=fill_color, fill_opacity=1, color=stroke_color
      )
      r.set_z_index(t.z_index - 1)
      rect[node] = r
      self._nodes[node] = VGroup(t, r)
    self._edges = {}
    self._edgearcs = {}
    for s, t in G.edges():
      arc, arrow = _medge(rect[s], rect[t], EDGE_RADIUS)
      arrow.set_z_index(min(rect[s].z_index, rect[t].z_index) - 1)
      self._edges[(s, t)] = arrow
      self._edgearcs[(s, t)] = arc
    self.mnodes = VGroup(list(self._nodes.values()))
    self.medges = VGroup(list(self._edges.values()))

  def mnode(self, node):
    return self._nodes[node]

  def medge(self, s, t):
    return self._edges[(s, t)]

  def mpath(self, s, t):
    return self._edgearcs[(s, t)]

  def movealong(self, mobject, s, t) -> AnimationGroup:
    ag = AnimationGroup()
    mobject.move_to(self._nodes[s])
    ag.append([MoveAlongPath(mobject, self.mpath(s, t))])
    return ag
