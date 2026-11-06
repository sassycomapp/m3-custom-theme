"""M3 carousel: a row of items, usually images, that the user moves through.
See docs/components/Carousel.md in the project library.

Add components (an Image, or a Card holding one) to the carousel; each becomes
one item. In the contained layouts the items change width as the carousel
moves: large items in front, a medium and a small item hinting at what comes
next. The user moves the carousel by dragging, swiping, scrolling sideways with
a trackpad or the mouse wheel (with Shift), or with the arrow keys.
"""
from anvil import HtmlTemplate
from anvil.designer import in_designer
from anvil.js import get_dom_node, window
from anvil.js.window import ResizeObserver

from ..._utils.properties import ComponentTag, anvil_prop, role_property
from ._anvil_designer import CarouselTemplate

_SLOT = "carousel-slot"
_LAYOUTS = ("multi_browse", "hero", "center_hero", "uncontained", "full_width")
# Fallbacks; the values in use are read from the --m3x-carousel-* tokens.
_TOKENS = {"gap": ("--m3x-carousel-gap", 8),
           "padding": ("--m3x-carousel-padding", 16),
           "small": ("--m3x-carousel-small-item-width", 56),
           "small_narrow": ("--m3x-carousel-small-item-min-width", 40)}
_NARROW = 360     # Carousels narrower than this get the narrow small width.
_DRAG_STEP = 48   # Pixels dragged to move one item.
_WHEEL_STEP = 60  # Wheel distance to move one item.
_WHEEL_PAUSE_MS = 250


def _fit_multi_browse(avail, target, small, gap):
    """Large, medium and small widths for a multi-browse carousel: the number of
    large items whose width comes closest to target, then a medium item about
    half a large one, then a small item, filling avail exactly."""
    best = None
    for large_count in range(1, 9):
        large = (avail - small - (large_count + 1) * gap) / (large_count + 0.5)
        medium = large / 2
        if medium < small:
            medium = small
            large = (avail - small - medium - (large_count + 1) * gap) / large_count
        if large < small * 2 and large_count > 1:
            break
        score = abs(large - target)
        if best is None or score < best[0]:
            best = (score, large_count, large, medium)
    _, large_count, large, medium = best
    return large_count, max(large, small), medium


class Carousel(CarouselTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._width = 0
        self._gap, self._padding = 8, 16
        self._small_wide, self._small_narrow = 56, 40
        self._drag = None
        self._suppress_click = False
        self._wheel = 0
        self._wheel_paused = False
        self.init_components(**properties)
        root = self.dom_nodes["m3x-carousel"]
        track = self.dom_nodes["m3x-carousel-track"]
        root.addEventListener("keydown", self._on_key)
        track.addEventListener("click", self._on_click, True)
        if not in_designer:
            track.addEventListener("pointerdown", self._on_pointer_down)
            root.addEventListener("wheel", self._on_wheel, {"passive": False})
        self._move = self._on_pointer_move
        self._up = self._on_pointer_up
        self._observer = ResizeObserver(lambda *a: self._measure())
        self.add_event_handler("x-anvil-page-added", self._on_page_added)
        self.add_event_handler("x-anvil-page-removed", self._on_page_removed)

    def add_component(self, component, slot=_SLOT, **layout_props):
        """Add an item (any component, usually an Image) to the carousel."""
        super().add_component(component, slot=slot, **layout_props)
        get_dom_node(component).classList.add("m3x-carousel-item")
        self._arrange()

    # ---- size and arrangement -------------------------------------------------

    def _on_page_added(self, **event_args):
        self._observer.observe(self.dom_nodes["m3x-carousel"])
        self._measure()

    def _on_page_removed(self, **event_args):
        self._observer.disconnect()

    def _read_tokens(self):
        style = window.getComputedStyle(self.dom_nodes["m3x-carousel"])
        values = {}
        for key, (token, fallback) in _TOKENS.items():
            try:
                values[key] = float(str(style.getPropertyValue(token)).strip()
                                    .replace("px", ""))
            except ValueError:
                values[key] = fallback
        self._gap, self._padding = values["gap"], values["padding"]
        self._small_wide, self._small_narrow = values["small"], values["small_narrow"]

    def _measure(self):
        self._read_tokens()
        width = self.dom_nodes["m3x-carousel"].clientWidth
        if width and width != self._width:
            self._width = width
            self._arrange()

    def _items(self):
        return [get_dom_node(c) for c in self.get_components()]

    def _last_index(self):
        """The highest value index can take in the current layout."""
        count = len(self._items())
        layout = self.layout
        if layout == "multi_browse" and self._width:
            avail = self._width - 2 * self._padding
            large_count, _, _ = _fit_multi_browse(avail, self.item_width or 186,
                                                  self._small(avail), self._gap)
            return max(0, count - large_count - 1)
        if layout == "uncontained":
            return 0
        return max(0, count - 1)

    def _small(self, avail):
        return self._small_wide if avail >= _NARROW else self._small_narrow

    def _widths(self, count, avail):
        """The width of each item at the current index; 0 hides an item."""
        layout = self.layout
        index = min(max(0, int(self.index or 0)), self._last_index())
        widths = [0] * count
        if count == 0:
            return widths
        small = self._small(avail)
        if layout == "full_width":
            widths[index] = avail
            return widths
        if layout == "multi_browse":
            large_count, large, medium = _fit_multi_browse(
                avail, self.item_width or 186, small, self._gap)
            sizes = [large] * large_count + [medium, small]
        elif layout == "hero":
            sizes = [avail - small - self._gap, small]
        else:  # center_hero
            sizes = [small, avail - 2 * small - 2 * self._gap, small]
        slots = len(sizes)
        if count <= slots - 1:
            # Too few items for the layout: share the width equally.
            share = (avail - (count - 1) * self._gap) / count
            return [share] * count
        if layout == "center_hero":
            large = sizes[1]
            if index == 0:
                first, sizes = 0, [large, small, small]
            elif index >= count - 1:
                first, sizes = count - 3, [small, small, large]
            else:
                first = index - 1
        else:
            first = index
            if first + slots > count:
                # The end: the arrangement turns round so the last item is large.
                first, sizes = count - slots, list(reversed(sizes))
        for offset, size in enumerate(sizes):
            if 0 <= first + offset < count:
                widths[first + offset] = size
        return widths

    def _arrange(self):
        items = self._items()
        root = self.dom_nodes["m3x-carousel"]
        if self.layout == "uncontained":
            for node in items:
                node.style.width = f"{self.item_width or 186}px"
                node.style.marginInlineEnd = f"{self._gap}px"
                node.removeAttribute("aria-hidden")
            return
        if not self._width:
            return
        avail = self._width - 2 * self._padding
        widths = self._widths(len(items), avail)
        shown = [i for i, w in enumerate(widths) if w > 0]
        for i, (node, width) in enumerate(zip(items, widths)):
            node.style.width = f"{width}px"
            node.style.marginInlineEnd = (
                f"{self._gap}px" if width and shown and i != shown[-1] else "0px")
            node.setAttribute("role", "group")
            node.setAttribute("aria-roledescription", "slide")
            node.setAttribute("aria-label", f"{i + 1} of {len(items)}")
            if width:
                node.removeAttribute("aria-hidden")
                node.classList.remove("m3x-carousel-item-hidden")
            else:
                node.setAttribute("aria-hidden", "true")
                node.classList.add("m3x-carousel-item-hidden")
        root.classList.toggle("m3x-carousel-at-start", int(self.index or 0) <= 0)

    # ---- moving -----------------------------------------------------------------

    def _go(self, index):
        index = min(max(0, index), self._last_index())
        if index != int(self.index or 0):
            self.index = index
            self.raise_event("change", index=index)

    def next(self):
        """Move one item forward."""
        self._go(int(self.index or 0) + 1)

    def previous(self):
        """Move one item back."""
        self._go(int(self.index or 0) - 1)

    def _on_key(self, event):
        if self.layout == "uncontained":
            track = self.dom_nodes["m3x-carousel-track"]
            steps = {"ArrowRight": 1, "ArrowLeft": -1}
            if event.key in steps:
                event.preventDefault()
                track.scrollBy({"left": steps[event.key] * ((self.item_width or 186) + self._gap),
                                "behavior": "smooth"})
            return
        moves = {"ArrowRight": 1, "ArrowLeft": -1}
        if event.key in moves:
            event.preventDefault()
            self._go(int(self.index or 0) + moves[event.key])
        elif event.key == "Home":
            event.preventDefault()
            self._go(0)
        elif event.key == "End":
            event.preventDefault()
            self._go(self._last_index())

    def _on_wheel(self, event):
        sideways = event.deltaX if abs(event.deltaX) > abs(event.deltaY) else 0
        if not sideways and event.shiftKey:
            sideways = event.deltaY
        if not sideways:
            return  # Up and down scrolling stays with the page.
        event.preventDefault()
        if self.layout == "uncontained":
            self.dom_nodes["m3x-carousel-track"].scrollLeft += sideways
            return
        if self._wheel_paused:
            return
        self._wheel += sideways
        if abs(self._wheel) >= _WHEEL_STEP:
            self._go(int(self.index or 0) + (1 if self._wheel > 0 else -1))
            self._wheel = 0
            self._wheel_paused = True
            window.setTimeout(self._resume_wheel, _WHEEL_PAUSE_MS)

    def _resume_wheel(self, *args):
        self._wheel_paused = False
        self._wheel = 0

    def _on_pointer_down(self, event):
        if event.button != 0:
            return
        self._drag = {"x": event.clientX, "moved": False,
                      "scroll": self.dom_nodes["m3x-carousel-track"].scrollLeft,
                      "start": event.clientX, "id": event.pointerId}
        window.addEventListener("pointermove", self._move)
        window.addEventListener("pointerup", self._up)
        window.addEventListener("pointercancel", self._up)

    def _on_pointer_move(self, event):
        drag = self._drag
        if not drag:
            return
        if abs(event.clientX - drag["start"]) > 4 and not drag["moved"]:
            drag["moved"] = True
            self.dom_nodes["m3x-carousel"].classList.add("m3x-carousel-dragging")
        if self.layout == "uncontained":
            self.dom_nodes["m3x-carousel-track"].scrollLeft = (
                drag["scroll"] - (event.clientX - drag["start"]))
            return
        moved = event.clientX - drag["x"]
        if abs(moved) >= _DRAG_STEP:
            self._go(int(self.index or 0) + (1 if moved < 0 else -1))
            drag["x"] = event.clientX

    def _on_pointer_up(self, event):
        drag = self._drag
        self._drag = None
        window.removeEventListener("pointermove", self._move)
        window.removeEventListener("pointerup", self._up)
        window.removeEventListener("pointercancel", self._up)
        self.dom_nodes["m3x-carousel"].classList.remove("m3x-carousel-dragging")
        self._suppress_click = bool(drag and drag["moved"])

    def _on_click(self, event):
        if self._suppress_click:
            # The click that ends a drag is not a click on an item.
            self._suppress_click = False
            event.stopPropagation()
            event.preventDefault()
            return
        items = self._items()
        components = self.get_components()
        for i, node in enumerate(items):
            if node.contains(event.target):
                self.raise_event("item_click", index=i, component=components[i])
                return

    # ---- properties ---------------------------------------------------------------

    @anvil_prop(default_value="multi_browse")
    @property
    def layout(self, value) -> str:
        """multi_browse, hero, center_hero, uncontained or full_width."""
        node = self.dom_nodes["m3x-carousel"]  # Set before __init__ ends.
        for name in _LAYOUTS:
            node.classList.toggle(f"m3x-carousel-{name}", name == (value or "multi_browse"))
        if hasattr(self, "_width"):
            self._arrange()

    @anvil_prop(default_value=186)
    @property
    def item_width(self, value) -> float:
        """The width large items aim for (or every item's width, uncontained)."""
        if hasattr(self, "_width"):
            self._arrange()

    @anvil_prop(default_value=220)
    @property
    def item_height(self, value) -> float:
        """The height of the items in pixels."""
        self.dom_nodes["m3x-carousel"].style.setProperty(
            "--m3x-carousel-item-height", f"{value or 220}px")

    @anvil_prop(default_value=0)
    @property
    def index(self, value) -> int:
        """The position of the first large item, from 0."""
        if hasattr(self, "_width"):
            self._arrange()

    @anvil_prop(default_value="Carousel")
    @property
    def label(self, value) -> str:
        """A name for the carousel that screen readers announce."""
        self.dom_nodes["m3x-carousel"].setAttribute("aria-label", value or "Carousel")

    visible = HtmlTemplate.visible
    role = role_property("m3x-carousel")

    #!componentEvent(m3.Carousel)!1: {name: "item_click", description: "When an item is clicked.", parameters:[{name: "index", description: "The item's position, from 0."}, {name: "component", description: "The item."}]}
    #!componentEvent(m3.Carousel)!1: {name: "change", description: "When the carousel moves to another item.", parameters:[{name: "index", description: "The new index."}]}
    #!componentEvent(m3.Carousel)!1: {name: "show", description: "When the carousel is shown on the screen."}
    #!componentEvent(m3.Carousel)!1: {name: "hide", description: "When the carousel is removed from the screen."}

    #!componentProp(m3.Carousel)!1: {name:"layout",type:"enum",options:["multi_browse", "hero", "center_hero", "uncontained", "full_width"],description:"How the items are sized and arranged."}
    #!componentProp(m3.Carousel)!1: {name:"item_width",type:"number",description:"The width large items aim for, or every item's width when uncontained."}
    #!componentProp(m3.Carousel)!1: {name:"item_height",type:"number",description:"The height of the items in pixels."}
    #!componentProp(m3.Carousel)!1: {name:"index",type:"number",description:"The position of the first large item, from 0."}
    #!componentProp(m3.Carousel)!1: {name:"label",type:"string",description:"A name for the carousel that screen readers announce."}
    #!componentProp(m3.Carousel)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.Carousel)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.Carousel)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, Carousel, anvil.Component)!:
