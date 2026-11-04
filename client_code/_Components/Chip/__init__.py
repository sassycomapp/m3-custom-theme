"""M3 Chip: assist, filter, input and suggestion chips in one component.
See docs/components/Chip.md in the project library.
"""
from anvil import HtmlTemplate

from ..._utils.properties import (
    ComponentTag,
    anvil_prop,
    innerText_property,
    role_property,
    tooltip_property,
)
from ._anvil_designer import ChipTemplate

_TYPES = ("assist", "filter", "input", "suggestion")
_SELECTABLE = ("filter", "input")


class Chip(ChipTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._tooltip_node = None
        self.init_components(**properties)
        self.dom_nodes["m3x-chip-action"].addEventListener("click", self._on_click)
        self.dom_nodes["m3x-chip-remove"].addEventListener("click", self._on_remove)

    def _on_click(self, event):
        if not self.enabled:
            return
        if self.type in _SELECTABLE:
            self.selected = not self.selected
            self.raise_event("change")
        self.raise_event("click")

    def _on_remove(self, event):
        event.stopPropagation()
        if self.enabled:
            self.raise_event("remove")

    def _toggle(self, name, value):
        self.dom_nodes["m3x-chip"].classList.toggle(name, bool(value))

    def _update_look(self):
        """Classes and icons that depend on more than one property."""
        chip_type = self.type if self.type in _TYPES else "assist"
        for t in _TYPES:
            self._toggle(f"m3x-chip-{t}", t == chip_type)
        selectable = chip_type in _SELECTABLE
        selected = bool(self.selected) and selectable
        self._toggle("m3x-chip-selected", selected)
        self._toggle("m3x-chip-elevated", self.elevated and chip_type != "input")
        self._toggle("m3x-chip-removable", self.removable)
        self._toggle("m3x-chip-disabled", not self.enabled)
        # A selected filter Chip without its own icon shows a check mark.
        leading = self.leading_icon or ""
        icon = leading[3:] if leading.startswith("mi:") else ""
        if not icon and selected and chip_type == "filter":
            icon = "check"
        node = self.dom_nodes["m3x-chip-leading-icon"]
        node.innerText = icon
        node.style.display = "" if icon else "none"
        self._toggle("m3x-chip-has-leading-icon", icon)
        action = self.dom_nodes["m3x-chip-action"]
        if selectable:
            action.setAttribute("aria-pressed", "true" if selected else "false")
        else:
            action.removeAttribute("aria-pressed")
        for name in ("m3x-chip-action", "m3x-chip-remove"):
            if self.enabled:
                self.dom_nodes[name].removeAttribute("disabled")
            else:
                self.dom_nodes[name].setAttribute("disabled", "")

    @anvil_prop(default_value="assist")
    @property
    def type(self, value) -> str:
        """The kind of Chip: assist, filter, input or suggestion."""
        self._update_look()

    @anvil_prop(default_value=False)
    @property
    def selected(self, value) -> bool:
        """If True, a filter or input Chip is selected."""
        self._update_look()

    @anvil_prop(default_value="")
    @property
    def leading_icon(self, value) -> str:
        """An icon shown before the text."""
        self._update_look()

    @anvil_prop(default_value=False)
    @property
    def elevated(self, value) -> bool:
        """If True, the Chip is raised with a shadow instead of an outline."""
        self._update_look()

    @anvil_prop(default_value=False)
    @property
    def removable(self, value) -> bool:
        """If True, the Chip shows a remove icon."""
        self._update_look()

    @anvil_prop(default_value=True)
    @property
    def enabled(self, value) -> bool:
        """If True, the Chip can be clicked."""
        self._update_look()

    text = innerText_property("m3x-chip-label", "text")
    visible = HtmlTemplate.visible
    role = role_property("m3x-chip")
    tooltip = tooltip_property("m3x-chip")

    #!componentEvent(m3.Chip)!1: {name: "click", description: "When the Chip is clicked."}
    #!componentEvent(m3.Chip)!1: {name: "change", description: "When a filter or input Chip is selected or unselected by a click."}
    #!componentEvent(m3.Chip)!1: {name: "remove", description: "When the remove icon of a removable Chip is clicked."}
    #!componentEvent(m3.Chip)!1: {name: "show", description: "When the Chip is shown on the screen."}
    #!componentEvent(m3.Chip)!1: {name: "hide", description: "When the Chip is removed from the screen."}

    #!componentProp(m3.Chip)!1: {name:"text",type:"string",description:"The text displayed on the Chip."}
    #!componentProp(m3.Chip)!1: {name:"type",type:"enum",options:["assist", "filter", "input", "suggestion"],description:"The kind of Chip."}
    #!componentProp(m3.Chip)!1: {name:"selected",type:"boolean",description:"If True, a filter or input Chip is selected."}
    #!componentProp(m3.Chip)!1: {name:"leading_icon",type:"enum",description:"An icon shown before the text."}
    #!componentProp(m3.Chip)!1: {name:"elevated",type:"boolean",description:"If True, the Chip is raised with a shadow instead of an outline."}
    #!componentProp(m3.Chip)!1: {name:"removable",type:"boolean",description:"If True, the Chip shows a remove icon."}
    #!componentProp(m3.Chip)!1: {name:"enabled",type:"boolean",description:"If True, the Chip can be clicked."}
    #!componentProp(m3.Chip)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.Chip)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.Chip)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
    #!componentProp(m3.Chip)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, Chip, anvil.Component)!:
