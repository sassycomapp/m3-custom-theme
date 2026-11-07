"""M3 window size classes for the custom theme.
See docs/components/PaneLayout.md in the project library.

M3 adapts layouts to the width of the window, in five classes:

    compact      under 600 px    (phones)
    medium       600 to 839 px   (small tablets, folded phones)
    expanded     840 to 1199 px  (tablets, small laptops)
    large        1200 to 1599 px (laptops, desktops)
    extra_large  1600 px and up  (large desktops)

The class in use is also written to the page's root element as
data-m3x-window, so CSS can follow it.
"""
from anvil.js import window

CLASSES = ("compact", "medium", "expanded", "large", "extra_large")
_STARTS = (0, 600, 840, 1200, 1600)  # The width (px) where each class starts.
_ATTRIBUTE = "data-m3x-window"
_listeners = []
_queries = []


def width_class(width=None):
    """The window size class for width (px), or for the window now."""
    _track()
    if width is None:
        width = window.innerWidth
    name = CLASSES[0]
    for cls, start in zip(CLASSES, _STARTS):
        if width >= start:
            name = cls
    return name


def is_single_pane():
    """True in the compact and medium classes, where M3 shows one pane at a time."""
    return width_class() in ("compact", "medium")


def on_change(callback):
    """Call callback(width_class) whenever the window moves to another class.
    Returns a function that stops the calls."""
    _track()
    _listeners.append(callback)

    def stop():
        if callback in _listeners:
            _listeners.remove(callback)
    return stop


def _changed(*args):
    name = width_class()
    window.document.documentElement.setAttribute(_ATTRIBUTE, name)
    for callback in list(_listeners):
        callback(name)


def _track():
    """Watch the class boundaries once, through matchMedia."""
    if _queries:
        return
    for start in _STARTS[1:]:
        query = window.matchMedia(f"(min-width: {start}px)")
        query.addEventListener("change", _changed)
        _queries.append(query)
    window.document.documentElement.setAttribute(
        _ATTRIBUTE, width_class(window.innerWidth))
