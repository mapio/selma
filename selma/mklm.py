from collections import defaultdict
import random
import re

def clean_text(corpus):
  res = [' ']
  for c in corpus:
    l = c.lower()
    if l.isalpha():
      res.append(l)
    elif l == ' ' and res[-1] != ' ':
      res.append(' ')
  return ''.join(res[1:])

class MarkovChainTextGenerator:
  def __init__(
    self, order=2, token_type='word', smoothing_alpha=0.001, interpolation=True
  ):
    """
    Markov Chain Text Generator with variable order and tokenization type.

    Parameters:
        order (int): Order of the Markov chain (n-gram size)
        token_type (str): 'word' for word-level, 'char' for character-level
        smoothing_alpha (float): Laplace smoothing factor
        interpolation (bool): Use backoff interpolation for unseen sequences
    """
    self.order = order
    self.token_type = token_type
    self.smoothing_alpha = smoothing_alpha
    self.interpolation = interpolation
    self.ngram_counts = defaultdict(lambda: defaultdict(int))
    self.total_counts = defaultdict(int)
    self.vocab = set()

  def tokenize(self, text):
    """Tokenizes text into words or characters based on user preference."""
    if self.token_type == 'word':
      return re.findall(r'\b\w+\b', text.lower())  # Simple word tokenization
    elif self.token_type == 'char':
      return list(text.lower())  # Character-level tokenization
    else:
      raise ValueError("token_type must be 'word' or 'char'")

  def train(self, corpus):
    """Trains the Markov chain model on a given corpus."""
    tokens = self.tokenize(corpus)
    self.vocab.update(tokens)
    self.vocab.add('<UNK>')  # Handle unknown words

    for i in range(len(tokens) - self.order):
      prefix = tuple(tokens[i : i + self.order])  # n-gram prefix
      next_token = tokens[i + self.order]  # next token

      self.ngram_counts[prefix][next_token] += 1
      self.total_counts[prefix] += 1

  def get_next_token_probs(self, prefix):
    """
    Retrieves transition probabilities using interpolation.
    """
    prefix = tuple(prefix)
    if prefix in self.ngram_counts:
      total = self.total_counts[prefix] + self.smoothing_alpha * len(self.vocab)
      return {
        token: (count + self.smoothing_alpha) / total
        for token, count in self.ngram_counts[prefix].items()
      }

    # Backoff: Try shorter prefixes
    if self.interpolation:
      for k in range(self.order - 1, 0, -1):
        shorter_prefix = prefix[-k:]
        if shorter_prefix in self.ngram_counts:
          total = self.total_counts[shorter_prefix] + self.smoothing_alpha * len(
            self.vocab
          )
          return {
            token: (count + self.smoothing_alpha) / total
            for token, count in self.ngram_counts[shorter_prefix].items()
          }

    # If no known transitions, return uniform probabilities over vocab
    return {token: 1 / len(self.vocab) for token in self.vocab}

  def generate(self, seed=None, length=50):
    """
    Generates text based on the trained model.
    """
    if not self.ngram_counts:
      raise ValueError('Model is not trained. Call `train(corpus)` first.')

    tokens = (
      list(self.tokenize(seed))
      if seed
      else [random.choice(list(self.vocab - {'<UNK>'}))]
    )

    while len(tokens) < length:
      prefix = tuple(tokens[-self.order :])
      probs = self.get_next_token_probs(prefix)

      next_token = random.choices(list(probs.keys()), weights=list(probs.values()))[0]
      tokens.append(next_token)

    return ' '.join(tokens) if self.token_type == 'word' else ''.join(tokens)
