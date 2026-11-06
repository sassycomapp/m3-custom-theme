"""M3 toolbar: a row (or column) of actions, usually icon buttons, with an
optional floating action button beside it.
See docs/components/Toolbar.md in the project library.

Two variants:
    floating  a rounded bar that floats over the content, horizontal or vertical.
    docked    a full-width bar along the bottom of the screen. It replaces the
              M3 bottom app bar.

Add IconButtons (or other buttons) to the toolbar. Add a FloatingActionButton
with slot="toolbar-fab-slot" to put it beside a floating toolbar or at the end
of a docked one.
"""
from anvil import HtmlTemplate
from anvil.designer import in_designer
from anvil.js import window

from ..._utils.properties import ComponentTag, anvil_prop, role_property
from ._anvil_designer import ToolbarTemplate

_SLOT = "toolbar-slot"
_FAB_SLOT = "toolbar-fab-slot"
_SCROLL_THRESHOLD = 40  # px scrolled before the toolbar hides or comes back.


class Toolbar(ToolbarTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._scroll_target = None
        self._anchor = 0
        self._listening = False
        self._scroll_handler = self._on_scroll
        self.init_components(**properties)
        if in_designer:
            # In the designer the toolbar is drawn in place, never pinned.
            self.dom_nodes["m3x-toolbar"].classList.add("m3x-toolbar-in-designer")
        self.add_event_handler("x-anvil-page-added", self._on_page_added)
        self.add_event_handler("x-anvil-page-removed", self._on_page_removed)

    def add_component(self, component, slot=_SLOT, **layout_props):
        """Add a component to the toolbar. Use slot="toolbar-fab-slot" for a
        FloatingActionButton."""
        super().add_component(component, slot=slot, **layout_props)
        if slot == _FAB_SLOT:
            self.dom_nodes["m3x-toolbar"].classList.add("m3x-toolbar-has-fab")

    # ---- hiding on scroll ------------------------------------------------------

    def _on_page_added(self, **event_args):
        self._update_scroll_listener()

    def _on_page_removed(self, **event_args):
        self._stop_listening()

    def _update_scroll_listener(self):
        wanted = (self.hide_on_scroll and self.pin_to_screen and not in_designer)
        if wanted and not self._listening:
            window.addEventListener("scroll", self._scroll_handler, True)
            self._listening = True
        elif not wanted:
            self._stop_listening()

    def _stop_listening(self):
        if self._listening:
            window.removeEventListener("scroll", self._scroll_handler, True)
            self._listening = False
        self._set_hidden(False)

    def _on_scroll(self, event):
        target = event.target
        if target is None or target.nodeType == 9:  # The page itself.
            target = window.document.scrollingElement
        if self.dom_nodes["m3x-toolbar"].contains(target):
            return
        y = target.scrollTop or 0
        if self._scroll_target is None or not self._scroll_target.isSameNode(target):
            self._scroll_target = target
            self._anchor = y
            return
        hidden = self.dom_nodes["m3x-toolbar"].classList.contains("m3x-toolbar-hidden")
        if y <= 0:
            self._set_hidden(False)
            self._anchor = 0
        elif not hidden and y - self._anchor > _SCROLL_THRESHOLD:
            self._set_hidden(True)
            self._anchor = y
        elif hidden and self._anchor - y > _SCROLL_THRESHOLD:
            self._set_hidden(False)
            self._anchor = y
        elif (hidden and y > self._anchor) or (not hidden and y < self._anchor):
            self._anchor = y  # Keep counting from the furthest point.

    def _set_hidden(self, hidden):
        self.dom_nodes["m3x-toolbar"].classList.toggle("m3x-toolbar-hidden", hidden)

    # ---- properties ------------------------------------------------------------

    @anvil_prop(default_value="floating")
    @property
    def variant(self, value) -> str:
        """floating or docked."""
        node = self.dom_nodes["m3x-toolbar"]  # Set before __init__ ends.
        node.classList.toggle("m3x-toolbar-docked", value == "docked")
        node.classList.toggle("m3x-toolbar-floating", value != "docked")

    @anvil_prop(default_value="standard")
    @property
    def color_style(self, value) -> str:
        """standard or vibrant."""
        self.dom_nodes["m3x-toolbar"].classList.toggle(
            "m3x-toolbar-vibrant", value == "vibrant")

    @anvil_prop(default_value=False)
    @property
    def vertical(self, value) -> bool:
        """If True, a floating toolbar is a vertical column."""
        self.dom_nodes["m3x-toolbar"].classList.toggle("m3x-toolbar-vertical",
                                                       bool(value))
        self.dom_nodes["m3x-toolbar-bar"].setAttribute(
            "aria-orientation", "vertical" if value else "horizontal")

    @anvil_prop(default_value=False)
    @property
    def pin_to_screen(self, value) -> bool:
        """If True, the toolbar is fixed to the window."""
        self.dom_nodes["m3x-toolbar"].classList.toggle("m3x-toolbar-pinned",
                                                       bool(value))
        if hasattr(self, "_listening"):
            self._update_scroll_listener()

    @anvil_prop(default_value=False)
    @property
    def hide_on_scroll(self, value) -> bool:
        """If True, a pinned toolbar slides away while the user scrolls down."""
        if hasattr(self, "_listening"):
            self._update_scroll_listener()

    @anvil_prop(default_value="Toolbar")
    @property
    def label(self, value) -> str:
        """A name for the toolbar that screen readers announce."""
        self.dom_nodes["m3x-toolbar-bar"].setAttribute("aria-label",
                                                       value or "Toolbar")

    visible = HtmlTemplate.visible
    role = role_property("m3x-toolbar")

    #!componentEvent(m3.Toolbar)!1: {name: "show", description: "When the toolbar is shown on the screen."}
    #!componentEvent(m3.Toolbar)!1: {name: "hide", description: "When the toolbar is removed from the screen."}

    #!componentProp(m3.Toolbar)!1: {name:"variant",type:"enum",options:["floating", "docked"],description:"floating: a rounded bar over the content. docked: a full-width bar along the bottom."}
    #!componentProp(m3.Toolbar)!1: {name:"color_style",type:"enum",options:["standard", "vibrant"],description:"standard: a quiet surface colour. vibrant: the primary container colour."}
    #!componentProp(m3.Toolbar)!1: {name:"vertical",type:"boolean",description:"If True, a floating toolbar is a vertical column."}
    #!componentProp(m3.Toolbar)!1: {name:"pin_to_screen",type:"boolean",description:"If True, the toolbar is fixed to the window."}
    #!componentProp(m3.Toolbar)!1: {name:"hide_on_scroll",type:"boolean",description:"If True, a pinned toolbar slides away while the user scrolls down."}
    #!componentProp(m3.Toolbar)!1: {name:"label",type:"string",description:"A name for the toolbar that screen readers announce."}
    #!componentProp(m3.Toolbar)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.Toolbar)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.Toolbar)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, Toolbar, anvil.Component)!:
