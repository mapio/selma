import networkx as nx
import numpy as np

from manim import VGroup, Tex, SurroundingRectangle, Arrow, BLACK, BLUE

from selma.geom import get_rect_edge_intersection

MANIM_WIDTH = 16
MANIM_HEIGHT = 9


def gvlayout_factory(algo='dot', fontsize=32, heightscale=1):
  def gvlayout(G):
    A = nx.nx_agraph.to_agraph(G)
    for node in A.nodes():
      n = A.get_node(node)
      n.attr['shape'] = 'box'
      n.attr['fontsize'] = str(fontsize)
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
    iss = []
    for s, t in G.edges():
      ss = get_rect_edge_intersection(rect[s], rect[t])
      tt = get_rect_edge_intersection(rect[t], rect[s])
      iss.append(ss)
      iss.append(tt)
      a = Arrow(
        ss,
        tt,
        max_stroke_width_to_length_ratio=float('inf'),
        max_tip_length_to_length_ratio=float('inf'),
        stroke_width=2,
        tip_length=0.1,
        buff=0,
        path_arc=0.3,
      )
      a.set_z_index(min(rect[s].z_index, rect[t].z_index) - 1)
      self._edges[(s, t)] = a
      self.iss = iss

  def mnode(self, node):
    return self._nodes[node]

  def mnodes(self):
    return VGroup(list(self._nodes.values()))

  def medge(self, s, t):
    return self._edges[(s, t)]

  def medges(self):
    return VGroup(list(self._edges.values()))
