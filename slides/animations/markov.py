from random import Random

import networkx as nx
from manim import Tex, UL, PURE_GREEN, VGroup, BLACK

from selma.mklm import clean_text
from selma.graph import MGraph, BORDER_COLOR

HIGHLIGHT_COLOR = PURE_GREEN


def tokenize(corpus, by_char):
  return (
    [c for c in clean_text(corpus) if c != ' ']
    if by_char
    else clean_text(corpus).split()
  )


def build_markov_chain(scene, tokens, layout, node_scale, order=1):
  T = Tex(*[ts for t in tokens for ts in (t, ' ')], color=BLACK).scale(0.9)
  T.to_edge(UL)
  scene.add(T)

  nodes = (
    tokens
    if order == 1
    else [
      ' '.join(tokens[i : i + order])
      for i in range(len(tokens) - 1)
    ]
  )

  edges = list(zip(nodes, nodes[1:]))
  G = nx.DiGraph(set(edges))
  weight = {e: 0 for e in G.edges()}
  G.remove_edges_from(nx.selfloop_edges(G))

  MG = MGraph(G, layout=layout, node_scale=node_scale)

  def highlight(t):
    mt = MG.mnode(t)
    mt.z_index = 1
    mt.set_stroke(color=HIGHLIGHT_COLOR)
    tg = VGroup(*[T[i] for i in range(highlight.step, highlight.step + 1 + order)])
    tg.set_color(HIGHLIGHT_COLOR)
    scene.add(mt)
    scene.wait(0.5)
    mt.set_stroke(color=BORDER_COLOR)
    tg.set_color(BLACK)
    highlight.step += 2

  highlight.step = 0

  highlight(edges[0][0])
  for s, t in edges:
    weight[(s, t)] += 1
    if s != t:
      me = MG.medge(s, t)
      me.z_index = 0
      me.set_stroke(width=weight[(s, t)] * 2, color=HIGHLIGHT_COLOR)
      scene.add(me)
    else:
      me = None
    highlight(t)
    if me:
      me.set_stroke(color=BLACK)

  return weight


def next_weight(weight):
  return {
    s: tuple(sorted((t, weight[(s, t)]) for ss, t in weight.keys() if ss == s))
    for s, _ in weight
  }


def next_weight0(corpus):
  return {None: tuple((c, 1) for c in set(corpus))}


def mk_rnd_next(next_weight, seed=None):
  rng = Random(seed)

  def rnd_next(s):
    if s not in next_weight:
      return None
    total = sum(w for _, w in next_weight[s])
    r = rng.uniform(0, total)
    upto = 0
    for t, w in next_weight[s]:
      if upto + w >= r:
        return t
      upto += w

  return rnd_next


def generate(rnd_next, start, num=100):
  res = [start]
  while len(res) <= num:
    n = rnd_next(res[-1])
    if n is None:
      break
    res.append(n)
  return res

def generate0(rnd_next, num=100):
  return [rnd_next(None) for _ in range(num)]