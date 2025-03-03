from collections import Counter

from manim import BLACK, PURE_GREEN, UL, Dot, Scene, VGroup
from markov import CORPORA, clean_text, make_text, mk_rnd_next

from selma.graph import make_node


def generate(rnd_next, num=100):
  return [rnd_next(None) for _ in range(num)]

def next_weight(corpus):
  c = Counter(corpus)
  return {None: tuple(sorted((t, f) for t, f in c.items()))}

CORPUS = list(clean_text(CORPORA['gadda']).replace(' ', '␣'))

weights_set = next_weight(set(CORPUS))
weights = next_weight(CORPUS)


def animate_generate(scene, weights, num, seed):
  gen = ''.join(generate(mk_rnd_next(weights, seed), num))
  nodes = {c: make_node(c).scale(s/4 + 1) for c, s in weights[None]}
  G = VGroup(*nodes.values())
  G.arrange_in_grid(2)
  scene.add(*G)
  T = make_text(gen, BLACK).scale(1.5).to_edge(UL)
  scene.add(T)
  dot = Dot(color=PURE_GREEN)
  dot.move_to(nodes[gen[0]])
  scene.add(dot)
  for pos, t in enumerate(gen):
    VGroup(*T[: pos * 2]).set_color(BLACK)
    VGroup(*T[pos * 2 : 2 * (pos ) + 1]).set_color(PURE_GREEN)
    scene.play(dot.animate.move_to(nodes[t]), run_time=.5)

class SimplerGenerate(Scene):
  def construct(self):
    animate_generate(self, weights_set, 20, 34)

class SimpleGenerate(Scene):
  def construct(self):
    animate_generate(self, weights, 20, 48)


