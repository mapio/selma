from random import Random

import networkx as nx
from manim import Tex, UL, PURE_GREEN, VGroup, BLACK, Dot

from selma import BACKGROUND
from selma.mklm import clean_text
from selma.graph import MGraph, BORDER_COLOR, gvlayout_factory

HIGHLIGHT_COLOR = PURE_GREEN


def tokenize(corpus, by_char):
  return (
    [c for c in clean_text(corpus) if c != ' ']
    if by_char
    else clean_text(corpus).split()
  )


def make_text(tokens, color):
  T = Tex(*[ts for t in tokens for ts in (t, ' ')], color=color).scale(0.9)
  T.to_edge(UL)
  return T


def build_markov_chain(scene, tokens, layout, node_scale, order=1):
  T = make_text(tokens, BLACK)
  scene.add(T)

  nodes = (
    tokens
    if order == 1
    else [' '.join(tokens[i : i + order]) for i in range(len(tokens) - 1)]
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
    tg = VGroup(*T[highlight.step * 2 : (highlight.step + order) * 2])
    tg.set_color(HIGHLIGHT_COLOR)
    scene.add(mt)
    scene.wait(0.5)
    mt.set_stroke(color=BORDER_COLOR)
    tg.set_color(BLACK)
    highlight.step += 1

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


def random_walk(scene, weight, start, num, seed=None):
  G = nx.DiGraph(set(weight.keys()))
  G.remove_edges_from(nx.selfloop_edges(G))
  MG = MGraph(G, layout=gvlayout_factory('neato', heightscale=0.5), node_scale=0.8)
  for s, t in G.edges():
    me = MG.medge(s, t)
    me.z_index = 0
    me.set_stroke(width=weight[(s, t)] * 2)
  scene.add(MG.mgraph)
  rn = mk_rnd_next(next_weight(weight), seed)
  gen = generate(rn, start, num)
  T = make_text([g.split()[0] for g in gen], BACKGROUND)
  scene.add(T)
  s = gen[0]
  order = len(s.split())
  dot = Dot(color=PURE_GREEN)
  dot.move_to(MG.mnode(gen[0]))
  scene.add(dot)
  VGroup(*T[: order * 2]).set_color(PURE_GREEN)
  scene.wait(0.5)
  for pos, t in enumerate(gen[1:]):
    VGroup(*T[: pos * 2]).set_color(BLACK)
    if s != t:
      scene.play(MG.movealong(dot, s, t), run_time=0.5)
    else:
      scene.wait(0.5)
    VGroup(*T[pos * 2 : 2 * (pos + order) + 1]).set_color(PURE_GREEN)
    s = t
