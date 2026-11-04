"""The M3 Expressive wavy variant of the base theme's progress indicators.
See docs/components/WavyProgress.md in the project library.

LinearProgressIndicator and CircularProgressIndicator have a wavy property. When
it is True, the component hides its own drawing and this module draws the wavy
one in its place. Every setter of those components calls update_linear or
update_circular, so the wavy drawing always follows the component's properties.
"""
from math import cos, pi, sin

from anvil.js import window

from .properties import theme_color_to_css

# Circular: 48 px box, 20 px radius, 1.6 px amplitude, about 15 px wavelength.
_CENTRE = 24
_RADIUS = 20
_AMPLITUDE = 1.6
_WAVES = 8
_POINTS = 120
_FRAMES = 8
# The 4 px gap between indicator and track, in units of pathLength 100.
_GAP = 4 / (2 * pi * _RADIUS) * 100

_SVG_NS = "http://www.w3.org/2000/svg"
_paths = {}


def _reduced_motion():
    return bool(window.matchMedia("(prefers-reduced-motion: reduce)").matches)


def _progress(component):
    try:
        return max(0.0, min(float(component.progress or 0), 100.0))
    except (TypeError, ValueError):
        return 0.0


def _flat(progress):
    # M3: the wave is flat below 10 % and from 95 % of the progress.
    return progress <= 10 or progress >= 95


def _set_colours(node, component, active_prop, track_prop=None):
    for name, prop in (("active", active_prop), ("track", track_prop)):
        value = getattr(component, prop, None) if prop else None
        var = f"--m3x-wavy-{name}-color"
        if value:
            node.style.setProperty(var, theme_color_to_css(value))
        else:
            node.style.removeProperty(var)


def _element(tag, cls=None, svg=False):
    doc = window.document
    node = doc.createElementNS(_SVG_NS, tag) if svg else doc.createElement(tag)
    if cls:
        node.setAttribute("class", cls)
    return node


# ---- linear ------------------------------------------------------------------


def update_linear(component):
    root = component.dom_nodes["anvil-m3-progressindicator-linear"]
    host = getattr(component, "_m3x_wavy_host", None)
    if not component.wavy:
        root.classList.remove("m3x-progress-wavy")
        if host is not None:
            host.remove()
            component._m3x_wavy_host = None
        return
    if host is None:
        host = _element("div", "m3x-wavy-linear")
        host.setAttribute("role", "progressbar")
        for cls in ("m3x-wavy-linear-track", "m3x-wavy-linear-active",
                    "m3x-wavy-linear-active m3x-wavy-linear-active-2",
                    "m3x-wavy-linear-stop"):
            host.appendChild(_element("div", cls))
        root.appendChild(host)
        component._m3x_wavy_host = host
    root.classList.add("m3x-progress-wavy")
    determinate = component.type == "determinate"
    progress = _progress(component)
    host.classList.toggle("m3x-wavy-indeterminate", not determinate)
    host.classList.toggle("m3x-wavy-flat", determinate and _flat(progress))
    host.classList.toggle("m3x-wavy-still", _reduced_motion())
    host.style.setProperty("--m3x-wavy-progress", f"{progress}%")
    if determinate:
        host.setAttribute("aria-valuenow", str(round(progress)))
        host.setAttribute("aria-valuemin", "0")
        host.setAttribute("aria-valuemax", "100")
    else:
        host.removeAttribute("aria-valuenow")
    _set_colours(host, component, "progress_color", "track_color")


# ---- circular ----------------------------------------------------------------


def _circle_path(amplitude, phase):
    """A closed path around the centre, as one wave per 1/_WAVES of the circle."""
    points = []
    for i in range(_POINTS):
        theta = 2 * pi * i / _POINTS
        r = _RADIUS + amplitude * sin(_WAVES * theta + phase)
        x = _CENTRE + r * sin(theta)
        y = _CENTRE - r * cos(theta)
        points.append(f"{x:.2f} {y:.2f}")
    return "M" + " L".join(points) + " Z"


def _frames(amplitude):
    key = amplitude
    if key not in _paths:
        _paths[key] = [_circle_path(amplitude, 2 * pi * f / _FRAMES)
                       for f in range(_FRAMES)]
    return _paths[key]


def update_circular(component):
    root = component.dom_nodes["anvil-m3-progressindicator"]
    host = getattr(component, "_m3x_wavy_host", None)
    if not component.wavy:
        root.classList.remove("m3x-progress-wavy")
        if host is not None:
            host.remove()
            component._m3x_wavy_host = None
        return
    determinate = component.type == "determinate"
    progress = _progress(component)
    flat = determinate and _flat(progress)
    still = _reduced_motion()
    state = (determinate, flat, still)
    if host is None or getattr(component, "_m3x_wavy_state", None) != state:
        if host is not None:
            host.remove()
        host = _build_circular(flat, still)
        root.appendChild(host)
        component._m3x_wavy_host = host
        component._m3x_wavy_state = state
    root.classList.add("m3x-progress-wavy")
    host.classList.toggle("m3x-wavy-indeterminate", not determinate)
    active = host.querySelector(".m3x-wavy-circular-active")
    track = host.querySelector(".m3x-wavy-circular-track")
    if determinate:
        active.setAttribute("stroke-dasharray", f"{progress:.2f} 100")
        rest = max(0.0, 100 - progress - 2 * _GAP)
        track.setAttribute("stroke-dasharray", f"{rest:.2f} 100")
        track.setAttribute("stroke-dashoffset", f"{-(progress + _GAP):.2f}")
        host.setAttribute("aria-valuenow", str(round(progress)))
        host.setAttribute("aria-valuemin", "0")
        host.setAttribute("aria-valuemax", "100")
    else:
        active.removeAttribute("stroke-dasharray")
        host.removeAttribute("aria-valuenow")
    _set_colours(host, component, "color")


def _build_circular(flat, still):
    svg = _element("svg", "m3x-wavy-circular", svg=True)
    svg.setAttribute("viewBox", "0 0 48 48")
    svg.setAttribute("role", "progressbar")
    frames = _frames(0 if flat else _AMPLITUDE)
    track = _element("path", "m3x-wavy-circular-track", svg=True)
    track.setAttribute("d", _frames(0)[0])
    track.setAttribute("pathLength", "100")
    svg.appendChild(track)
    active = _element("path", "m3x-wavy-circular-active", svg=True)
    active.setAttribute("d", frames[0])
    active.setAttribute("pathLength", "100")
    if not flat and not still:
        # The wave travels round the circle, one wavelength per second.
        animate = _element("animate", svg=True)
        animate.setAttribute("attributeName", "d")
        animate.setAttribute("dur", "1s")
        animate.setAttribute("repeatCount", "indefinite")
        animate.setAttribute("values", ";".join(frames + [frames[0]]))
        active.appendChild(animate)
    svg.appendChild(active)
    return svg
