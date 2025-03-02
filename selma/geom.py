import warnings

import numpy as np


def arctan2(p):  # in [-π, π]
  return np.arctan2(p[1], p[0])


def shortest_arc(θp, θq):  # in [-π, π]
  return (θq - θp + np.pi) % (2 * np.pi) - np.pi


def in_arc_range(θ, start_angle, arc_angle):
  # θ, start_angle, arc_angle = map(lambda x: x % (2 * np.pi), [θ, start_angle, arc_angle])
  return 0 <= (θ - start_angle) % (2 * np.pi) <= arc_angle  # % (2 * np.pi)


def in_range(val, low, high, eps=1e-9):
  return low - eps <= val <= high + eps


def rect_bounds(rect):
  v = rect.get_vertices()
  minx, miny, _ = np.min(v, axis=0)
  maxx, maxy, _ = np.max(v, axis=0)
  return minx, maxx, miny, maxy


def rect_intersect(r0, r1):
  """
  Returns the intersection point between the sides of rectangle
  r0 and the line from r0.get_center() to r1.get_center().
  """
  center = np.array(r0.get_center())
  direction = np.array(r1.get_center()) - center
  x_min, x_max, y_min, y_max = rect_bounds(r0)

  intersections = []

  # Check intersections with vertical boundaries (x = x_min and x_max)
  for x_bound in (x_min, x_max):
    if abs(direction[0]) < 1e-9:
      continue
    t = (x_bound - center[0]) / direction[0]
    y_hit = center[1] + t * direction[1]
    if y_min <= y_hit <= y_max:
      intersections.append((t, np.array([x_bound, y_hit, 0])))

  # Check intersections with horizontal boundaries (y = y_min and y_max)
  for y_bound in (y_min, y_max):
    if abs(direction[1]) < 1e-9:
      continue
    t = (y_bound - center[1]) / direction[1]
    x_hit = center[0] + t * direction[0]
    if x_min <= x_hit <= x_max:
      intersections.append((t, np.array([x_hit, y_bound, 0])))

  # Filter for intersections in the forward direction (0 <= t <= 1)
  valid = [(t, pt) for t, pt in intersections if 0 <= t <= 1]
  if not valid:
    return center

  # Return the intersection point closest to the center
  return min(valid, key=lambda tup: tup[0])[1]


def compute_arc(P, Q, r):
  """
  Given two 3D points P, Q (each [x,y,0]) and a *signed* radius r,
  return:
    - center : the circle center as [x, y] (the side is decided by the sign of r)
    - start_angle : the starting angle in [-π, π) for point P
    - arc_angle : the angle in [-π, π) from P to Q.
  """
  P = np.asarray(P, dtype=float)[:2]
  Q = np.asarray(Q, dtype=float)[:2]
  chord = Q - P
  d = np.linalg.norm(chord)
  if d > 2 * abs(r):
    raise ValueError(f'No real circle of radius {r} passes through P, Q (distance={d:.2f}).')

  # Midpoint of the chord
  M = (P + Q) / 2

  # Distance from midpoint to the circle center
  h = np.sqrt(r * r - (d / 2) ** 2)

  # Unit vector along chord
  u = chord / d
  # Perp vector (rotate +90°)
  n = np.array([-u[1], u[0]])

  # Circle center is M ± h * n
  center = M + np.sign(r) * h * n

  # Angles for P and Q (in [0, 2π))
  θp = arctan2(P - center)
  θq = arctan2(Q - center)

  return center, θp, shortest_arc(θp, θq)


def circle_intersect(center, radius, rect):
  """
  Returns all intersections between the circle (center, radius>0)
  and the boundary of an axis-aligned rectangle rect.

  Each intersection is (theta, point) where:
    - theta in [0, 2π) (angle from center in XY-plane),
    - point is [x, y].
  """
  r = abs(radius)

  x_min, x_max, y_min, y_max = rect_bounds(rect)
  results = []

  # ---- Vertical boundaries: x = x_min, x_max ----
  for x_bound in (x_min, x_max):
    dx = x_bound - center[0]
    if abs(dx) > r:
      continue
    # length in the perpendicular direction
    dy_mag = np.sqrt(r**2 - dx * dx)

    # The intersection points are (x_bound, center[1] ± dy_mag)
    for sign_ in (+1, -1):
      y_hit = center[1] + sign_ * dy_mag
      if in_range(y_hit, y_min, y_max):
        pt = np.array([x_bound, y_hit])
        th = arctan2(pt - center)
        results.append((th, pt))

  # ---- Horizontal boundaries: y = y_min, y_max ----
  for y_bound in (y_min, y_max):
    dy = y_bound - center[1]
    if abs(dy) > r:
      continue
    # length in the perpendicular direction
    dx_mag = np.sqrt(r**2 - dy * dy)

    # The intersection points are (center[0] ± dx_mag, y_bound)
    for sign_ in (+1, -1):
      x_hit = center[0] + sign_ * dx_mag
      if in_range(x_hit, x_min, x_max):
        pt = np.array([x_hit, y_bound])
        th = arctan2(pt - center)
        results.append((th, pt))

  # Remove duplicates (possible at corners)
  unique = {}
  for theta, pt in results:
    key = (round(theta, 6), round(pt[0], 6), round(pt[1], 6))
    if key not in unique:
      unique[key] = (theta, pt)
  return list(unique.values())


def arc_intersect(center, radius, start_angle, arc_angle, rect):
  candidate = [
    (th, pt) for (th, pt) in circle_intersect(center, radius, rect) if in_arc_range(th, start_angle, arc_angle)
  ]
  if len(candidate) != 1:
    warnings.warn(f'Expected 1 intersection with {rect}, got {len(candidate)}.')
    return rect.get_center()
  return candidate[0][0]
