"""M3 floating action button (FAB) and extended FAB.
See docs/components/FloatingActionButton.md in the project library.
"""
from anvil import HtmlTemplate

from ..._utils.properties import (
    ComponentTag,
    anvil_prop,
    role_property,
    tooltip_property,
)
from ._anvil_designer import FloatingActionButtonTemplate

_SIZES = ("regular", "medium", "large")
_APPEARANCES = (
    "primary_container", "secondary_container", "tertiary_container",
    "primary", "secondary", "tertiary",
)


class FloatingActionButton(FloatingActionButtonTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._tooltip_node = None
        self.init_components(**properties)
        self.dom_nodes["m3x-fab"].addEventListener("click", self._on_click)

    def _on_click(self, event):
        if self.enabled:
            self.raise_event("click")

    def _set_class(self, prefix, options, value, default):
        node = self.dom_nodes["m3x-fab"]
        value = value if value in options else default
        for option in options:
            css_class = prefix + option.replace("_", "-")
            node.classList.toggle(css_class, option == value)

    @anvil_prop(default_value="mi:add")
    @property
    def icon(self, value) -> str:
        """The icon on the button."""
        name = value[3:] if value and value.startswith("mi:") else ""
        node = self.dom_nodes["m3x-fab-icon"]
        node.innerText = name
        node.style.display = "" if name else "none"

    @anvil_prop(default_value="")
    @property
    def text(self, value) -> str:
        """A label after the icon. With a label, the button is an extended FAB."""
        node = self.dom_nodes["m3x-fab-label"]
        node.innerText = value or ""
        node.style.display = "" if value else "none"
        self.dom_nodes["m3x-fab"].classList.toggle("m3x-fab-extended", bool(value))

    @anvil_prop(default_value="regular")
    @property
    def size(self, value) -> str:
        """regular (56 px), medium (80 px) or large (96 px)."""
        self._set_class("m3x-fab-", _SIZES, value, "regular")

    @anvil_prop(default_value="primary_container")
    @property
    def appearance(self, value) -> str:
        """The colour of the button."""
        self._set_class("m3x-fab-", _APPEARANCES, value, "primary_container")

    @anvil_prop(default_value=False)
    @property
    def floating(self, value) -> bool:
        """If True, the button floats in the bottom right corner of the window."""
        self.dom_nodes["m3x-fab"].classList.toggle("m3x-fab-floating", bool(value))

    @anvil_prop(default_value=True)
    @property
    def enabled(self, value) -> bool:
        """If True, the button can be clicked."""
        node = self.dom_nodes["m3x-fab"]
        if value:
            node.removeAttribute("disabled")
        else:
            node.setAttribute("disabled", "")

    # The tooltip is also the button's name for screen readers, which an
    # icon-only button needs (Section 5.9 of the plan).
    _base_tooltip = tooltip_property("m3x-fab")

    def _get_tooltip(self):
        return self._base_tooltip

    def _set_tooltip(self, value):
        self._base_tooltip = value
        node = self.dom_nodes["m3x-fab"]
        if value:
            node.setAttribute("aria-label", value)
        else:
            node.removeAttribute("aria-label")

    tooltip = property(_get_tooltip, _set_tooltip)

    visible = HtmlTemplate.visible
    role = role_property("m3x-fab")

    #!componentEvent(m3.FloatingActionButton)!1: {name: "click", description: "When the button is clicked."}
    #!componentEvent(m3.FloatingActionButton)!1: {name: "show", description: "When the button is shown on the screen."}
    #!componentEvent(m3.FloatingActionButton)!1: {name: "hide", description: "When the button is removed from the screen."}

    #!componentProp(m3.FloatingActionButton)!1: {name:"icon",type:"enum",description:"The icon on the button."}
    #!componentProp(m3.FloatingActionButton)!1: {name:"text",type:"string",description:"A label after the icon. With a label, the button is an extended FAB."}
    #!componentProp(m3.FloatingActionButton)!1: {name:"size",type:"enum",options:["regular", "medium", "large"],description:"The size of the button."}
    #!componentProp(m3.FloatingActionButton)!1: {name:"appearance",type:"enum",options:["primary_container", "secondary_container", "tertiary_container", "primary", "secondary", "tertiary"],description:"The colour of the button."}
    #!componentProp(m3.FloatingActionButton)!1: {name:"floating",type:"boolean",description:"If True, the button floats in the bottom right corner of the window."}
    #!componentProp(m3.FloatingActionButton)!1: {name:"tooltip",type:"string",description:"A description of the action."}
    #!componentProp(m3.FloatingActionButton)!1: {name:"enabled",type:"boolean",description:"If True, the button can be clicked."}
    #!componentProp(m3.FloatingActionButton)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.FloatingActionButton)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.FloatingActionButton)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, FloatingActionButton, anvil.Component)!:
