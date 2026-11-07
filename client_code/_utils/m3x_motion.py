"""M3 motion for the custom theme: springs, the motion scheme and reduced motion.
See docs/components/Motion.md in the project library.

M3 Expressive motion is spring-based. Each spring token (stiffness and damping
ratio) is turned into a CSS linear() easing and a settling time by
tools/spring_to_linear.py, and stored in theme/assets/m3x/tokens.css. Components
use the six springs through these tokens:

    --m3x-motion-spatial-{fast,default,slow}-{easing,duration}   move, resize, reshape
    --m3x-motion-effects-{fast,default,slow}-{easing,duration}   colour, opacity

This module lets Python code use the same springs, choose the motion scheme,
and respect the device's reduced-motion setting.
"""
from anvil.js import window

SCHEMES = ("expressive", "standard")
SPRINGS = ("spatial-fast", "spatial-default", "spatial-slow",
           "effects-fast", "effects-default", "effects-slow")

_SCHEME_ATTRIBUTE = "data-m3x-motion"


def _root():
    return window.document.documentElement


def get_scheme():
    """The motion scheme in use: "expressive" (the default) or "standard"."""
    value = _root().getAttribute(_SCHEME_ATTRIBUTE)
    return value if value in SCHEMES else "expressive"


def set_scheme(scheme):
    """Choose the motion scheme for the whole app.

        expressive  lively springs with a little overshoot (the default).
        standard    calmer springs without overshoot.
    """
    if scheme not in SCHEMES:
        raise ValueError(f"Unknown motion scheme {scheme!r}. Choose one of {SCHEMES}")
    if scheme == "expressive":
        _root().removeAttribute(_SCHEME_ATTRIBUTE)
    else:
        _root().setAttribute(_SCHEME_ATTRIBUTE, scheme)


def reduced_motion():
    """True if the device asks for reduced motion."""
    return bool(window.matchMedia("(prefers-reduced-motion: reduce)").matches)


def spring(name="spatial-default"):
    """The (easing, duration in ms) of one of SPRINGS, as the page uses them."""
    if name not in SPRINGS:
        raise ValueError(f"Unknown spring {name!r}. Choose one of {SPRINGS}")
    kind, speed = name.split("-")
    style = window.getComputedStyle(_root())
    easing = str(style.getPropertyValue(f"--m3x-motion-{kind}-{speed}-easing")).strip()
    duration = str(
        style.getPropertyValue(f"--m3x-motion-{kind}-{speed}-duration")).strip()
    try:
        ms = float(duration.replace("ms", "")) if duration.endswith("ms") else (
            float(duration.replace("s", "")) * 1000)
    except ValueError:
        ms = 300.0
    return easing or "ease", ms


def animate(node, keyframes, name="spatial-default", **options):
    """Run a Web Animations API animation on node with one of the springs.

    keyframes is a list of dicts, as for element.animate(). With reduced
    motion the animation jumps straight to its last frame. Returns the
    Animation object.
    """
    easing, ms = spring(name)
    timing = {"duration": 0 if reduced_motion() else ms, "easing": easing,
              "fill": "both"}
    timing.update(options)
    return node.animate(keyframes, timing)
