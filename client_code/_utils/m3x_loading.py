"""The shapes of the M3 Expressive loading indicator.
See docs/components/LoadingIndicator.md in the project library.

The indicator morphs through seven shapes in the order Jetpack Compose uses:
soft burst, 9-sided cookie, pentagon, pill, sunny, 4-sided cookie, oval. Each
shape is drawn with the same number of points, so the browser can morph one into
the next. Each morph takes 650 ms and turns the shape a quarter turn further; the
whole indicator also turns once every 4666 ms.
"""
from math import cos, pi, sin

POINTS = 96
MORPH_MS = 650
ROTATION_MS = 4666
_RADIUS = 19  # The 38 px active indicator in its 48 px box.
_CENTRE = 24


def _lobes(count, depth):
    return lambda t: 1 + depth * cos(count * t)


def _polygon(sides, rounding):
    def r(t):
        sector = 2 * pi / sides
        edge = cos(pi / sides) / cos((t % sector) - pi / sides)
        return edge * (1 - rounding) + rounding
    return r


def _superellipse(a, b, power, turn):
    def r(t):
        t = t - turn
        x = abs(cos(t) / a) ** power
        y = abs(sin(t) / b) ** power
        return (x + y) ** (-1 / power)
    return r


_SHAPES = (
    ("soft_burst", _lobes(10, 0.09)),
    ("cookie_9", _lobes(9, 0.07)),
    ("pentagon", _polygon(5, 0.25)),
    ("pill", _superellipse(1.0, 0.6, 2.8, pi / 4)),
    ("sunny", _lobes(8, 0.13)),
    ("cookie_4", _lobes(4, 0.12)),
    ("oval", _superellipse(1.0, 0.78, 2.0, -pi / 4)),
)


def _path(radius_of):
    raw = [radius_of(2 * pi * i / POINTS) for i in range(POINTS)]
    scale = _RADIUS / max(raw)
    parts = []
    for i, r in enumerate(raw):
        t = 2 * pi * i / POINTS
        x = _CENTRE + scale * r * sin(t)
        y = _CENTRE - scale * r * cos(t)
        parts.append(f"{x:.1f} {y:.1f}")
    return "M" + " L".join(parts) + " Z"


_cache = []


def shape_paths():
    """The seven shapes as SVG path data, in morph order."""
    if not _cache:
        _cache.extend(_path(radius_of) for _, radius_of in _SHAPES)
    return list(_cache)


def morph_values(cycles=4):
    """Path values for one seamless loop: four passes through the seven shapes
    make 28 quarter turns, which is seven whole turns, so the loop restarts
    without a jump."""
    paths = shape_paths()
    sequence = paths * cycles
    return sequence + [sequence[0]]


def rotation_values(cycles=4):
    steps = len(_SHAPES) * cycles
    return [f"{90 * i} {_CENTRE} {_CENTRE}" for i in range(steps + 1)]
