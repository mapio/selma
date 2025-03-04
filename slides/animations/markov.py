from pathlib import Path
from random import Random

import networkx as nx
from manim import BLACK, PURE_GREEN, UL, Dot, Scene, Tex, VGroup, config

from selma import BACKGROUND
from selma.graph import BORDER_COLOR, MGraph, gvlayout_factory
from selma.mklm import clean_text

config.background_color = BACKGROUND

HIGHLIGHT_COLOR = PURE_GREEN

CORPORA = {
  'gadda': 'Come poco pepe a coppia cuoce e scoppia',  # Gadda
  'giovanni': 'In principio era il Verbo, e il Verbo era presso Dio, e il Verbo era Dio',  # Vangelo di Giovanni, 1:1
}

# Training


def tokenize(corpus, by_char):
  return [c for c in clean_text(corpus) if c != ' '] if by_char else clean_text(corpus).split()


def make_text(tokens, color):
  T = Tex(*[ts for t in tokens for ts in (t, ' ')], color=color).scale(0.9)
  T.to_edge(UL)
  return T


def build_markov_chain(tokens, order=1):
  nodes = tokens if order == 1 else [' '.join(tokens[i : i + order]) for i in range(len(tokens) - 1)]

  pairs = list(zip(nodes, nodes[1:]))
  edges = set(pairs)
  weight = {e: 0 for e in edges}
  for s, t in pairs:
    weight[(s, t)] += 1
  G = nx.DiGraph(edges)
  G.remove_edges_from(nx.selfloop_edges(G))

  return G, pairs, weight


def animate_training(scene, tokens, layout, node_scale, order=1):
  T = make_text(tokens, BLACK)
  scene.add(T)

  G, pairs, weight = build_markov_chain(tokens, order)
  weight = {e: 0 for e in set(pairs)}

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

  highlight(pairs[0][0])
  for s, t in pairs:
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


class TrainByCharGadda1(Scene):
  def construct(self):
    animate_training(
      self,
      tokenize(CORPORA['gadda'], by_char=True),
      layout=gvlayout_factory('neato', heightscale=0.5),
      node_scale=0.8,
      order=1,
    )


class TrainByCharGadda2(Scene):
  def construct(self):
    animate_training(
      self,
      tokenize(CORPORA['gadda'], by_char=True),
      layout=gvlayout_factory('neato', heightscale=0.5),
      node_scale=0.8,
      order=2,
    )


class TrainByCharGadda3(Scene):
  def construct(self):
    animate_training(
      self,
      tokenize(CORPORA['gadda'], by_char=True),
      layout=gvlayout_factory('neato', heightscale=0.5),
      node_scale=0.8,
      order=3,
    )


class TrainByWordGiovanni1(Scene):
  def construct(self):
    animate_training(
      self,
      tokenize(CORPORA['giovanni'], by_char=False),
      layout=gvlayout_factory('neato', heightscale=0.6),
      node_scale=0.6,
      order=1,
    )


class TrainByWordGiovanni2(Scene):
  def construct(self):
    animate_training(
      self,
      tokenize(CORPORA['giovanni'], by_char=False),
      layout=gvlayout_factory('neato', heightscale=0.6),
      node_scale=0.6,
      order=2,
    )


# Generation


def next_weight(weight):
  return {s: tuple(sorted((t, weight[(s, t)]) for ss, t in weight.keys() if ss == s)) for s, _ in weight}


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


def random_walk(scene, tokens, order, start, num, seed=None):
  G, _, weight = build_markov_chain(tokens, order)
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


class GenerateByCharGadda1(Scene):
  def construct(self):
    random_walk(self, tokenize(CORPORA['gadda'], by_char=True), 1, 'c', 20, seed=41)


class GenerateByCharGadda2(Scene):
  def construct(self):
    random_walk(self, tokenize(CORPORA['gadda'], by_char=True), 2, 'c o', 20, seed=42)


class GenerateByCharGadda3(Scene):
  def construct(self):
    random_walk(self, tokenize(CORPORA['gadda'], by_char=True), 3, 'c o p', 20, seed=42)


class GenerateByWordGiovanni1(Scene):
  def construct(self):
    random_walk(self, tokenize(CORPORA['giovanni'], by_char=False), 1, 'era', 17, seed=43)


class GenerateByWordGiovanni2(Scene):
  def construct(self):
    random_walk(self, tokenize(CORPORA['giovanni'], by_char=False), 2, 'era il', 16, seed=38)
