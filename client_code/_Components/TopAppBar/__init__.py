"""M3 Expressive top app bar: small (optionally centred), medium flexible and
large flexible. See docs/components/TopAppBar.md in the project library.
"""
from anvil import HtmlTemplate
from anvil.js import window

from ..._utils.properties import ComponentTag, anvil_prop, role_property
from ._anvil_designer import TopAppBarTemplate

_SLOT = "top-app-bar-actions-slot"
_SIZES = ("small", "medium", "large")


class TopAppBar(TopAppBarTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._listening = False
        # One handler object, so that the same function is added and removed.
        self._scroll_handler = self._on_scroll
        self.init_components(**properties)
        self.dom_nodes["m3x-top-app-bar-navigation"].addEventListener(
            "click", lambda event: self.raise_event("navigation_click")
        )
        self.add_event_handler("show", self._on_show)
        self.add_event_handler("hide", self._on_hide)

    def add_component(self, component, slot=_SLOT, **layout_props):
        """Add an action, normally an IconButton, at the end of the bar."""
        super().add_component(component, slot=slot, **layout_props)

    # ---- scrolled look -------------------------------------------------------

    def _on_scroll(self, event):
        target = event.target
        if target.nodeType == 9:  # The document itself scrolled.
            target = window.document.scrollingElement
        try:
            scrolled = target.scrollTop > 0
        except Exception:
            return
        if target.contains(self.dom_nodes["m3x-top-app-bar"]):
            self._toggle("m3x-top-app-bar-scrolled", scrolled)

    def _on_show(self, **event_args):
        if not self._listening:
            # Capture scroll events from whichever element scrolls the page.
            window.addEventListener("scroll", self._scroll_handler, True)
            self._listening = True

    def _on_hide(self, **event_args):
        if self._listening:
            window.removeEventListener("scroll", self._scroll_handler, True)
            self._listening = False

    # ---- properties ----------------------------------------------------------

    def _toggle(self, name, value):
        self.dom_nodes["m3x-top-app-bar"].classList.toggle(name, bool(value))

    @anvil_prop(default_value="Title")
    @property
    def title(self, value) -> str:
        """The title of the page."""
        self.dom_nodes["m3x-top-app-bar-title"].innerText = value or ""

    @anvil_prop(default_value="")
    @property
    def subtitle(self, value) -> str:
        """A smaller line of text below the title."""
        node = self.dom_nodes["m3x-top-app-bar-subtitle"]
        node.innerText = value or ""
        node.style.display = "" if value else "none"
        self._toggle("m3x-top-app-bar-has-subtitle", value)

    @anvil_prop(default_value="small")
    @property
    def size(self, value) -> str:
        """small, medium or large."""
        value = value if value in _SIZES else "small"
        for size in _SIZES:
            self._toggle(f"m3x-top-app-bar-{size}", size == value)

    @anvil_prop(default_value=False)
    @property
    def centered(self, value) -> bool:
        """If True, the title of a small bar is centred."""
        self._toggle("m3x-top-app-bar-centered", value)

    @anvil_prop(default_value="")
    @property
    def navigation_icon(self, value) -> str:
        """An icon button at the start of the bar."""
        name = value[3:] if value and value.startswith("mi:") else ""
        self.dom_nodes["m3x-top-app-bar-navigation-icon"].innerText = name
        button = self.dom_nodes["m3x-top-app-bar-navigation"]
        button.style.display = "" if name else "none"
        self._toggle("m3x-top-app-bar-has-navigation", name)

    @anvil_prop(default_value="")
    @property
    def navigation_label(self, value) -> str:
        """The name of the navigation icon for screen readers."""
        button = self.dom_nodes["m3x-top-app-bar-navigation"]
        if value:
            button.setAttribute("aria-label", value)
        else:
            button.removeAttribute("aria-label")

    @anvil_prop(default_value=True)
    @property
    def sticky(self, value) -> bool:
        """If True, the bar stays at the top of the window when the page scrolls."""
        self._toggle("m3x-top-app-bar-sticky", value)

    visible = HtmlTemplate.visible
    role = role_property("m3x-top-app-bar")

    #!componentEvent(m3.TopAppBar)!1: {name: "navigation_click", description: "When the navigation icon at the start of the bar is clicked."}
    #!componentEvent(m3.TopAppBar)!1: {name: "show", description: "When the top app bar is shown on the screen."}
    #!componentEvent(m3.TopAppBar)!1: {name: "hide", description: "When the top app bar is removed from the screen."}

    #!componentProp(m3.TopAppBar)!1: {name:"title",type:"string",description:"The title of the page."}
    #!componentProp(m3.TopAppBar)!1: {name:"subtitle",type:"string",description:"A smaller line of text below the title."}
    #!componentProp(m3.TopAppBar)!1: {name:"size",type:"enum",options:["small", "medium", "large"],description:"small, medium or large."}
    #!componentProp(m3.TopAppBar)!1: {name:"centered",type:"boolean",description:"If True, the title of a small bar is centred."}
    #!componentProp(m3.TopAppBar)!1: {name:"navigation_icon",type:"enum",description:"An icon button at the start of the bar."}
    #!componentProp(m3.TopAppBar)!1: {name:"navigation_label",type:"string",description:"The name of the navigation icon for screen readers."}
    #!componentProp(m3.TopAppBar)!1: {name:"sticky",type:"boolean",description:"If True, the bar stays at the top of the window when the page scrolls."}
    #!componentProp(m3.TopAppBar)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.TopAppBar)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.TopAppBar)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, TopAppBar, anvil.Component)!:
