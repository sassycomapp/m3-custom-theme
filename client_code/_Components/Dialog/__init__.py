"""M3 Dialog. See docs/components/Dialog.md in the project library.

A Dialog is a container with a headline, supporting text, an optional icon, a
content slot and an actions slot. show() opens it through Anvil's alert(), so
Anvil's own focus, backdrop and Escape handling apply. show() returns the value
passed to close(), or None when the user dismisses the Dialog.
"""
from anvil import HtmlTemplate, alert
from anvil.js import window

from ..._utils.properties import (
    ComponentTag,
    anvil_prop,
    property_without_callback,
    role_property,
)
from ..Button import Button
from ._anvil_designer import DialogTemplate

_CONTENT_SLOT = "dialog-content-slot"
_ACTIONS_SLOT = "dialog-actions-slot"


class Dialog(DialogTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._alert_content = None
        self.init_components(**properties)
        self.dom_nodes["m3x-dialog-close"].addEventListener(
            "click", self._on_close_click
        )
        self.add_event_handler("show", self._on_show)

    def add_component(self, component, slot=_CONTENT_SLOT, **layout_props):
        super().add_component(component, slot=slot, **layout_props)

    def add_action(self, text, value=None, appearance="text", **properties):
        """Add a button to the actions. Clicking it closes the Dialog, and show()
        returns value. Returns the Button."""
        button = Button(text=text, appearance=appearance, **properties)
        button.add_event_handler("click", lambda **event_args: self.close(value))
        self.add_component(button, slot=_ACTIONS_SLOT)
        return button

    def show(self):
        """Open the Dialog. Returns the value passed to close(), or None if the
        user dismissed it. If the Dialog sits inside a form, the whole form is
        shown, so a form built around a Dialog works the same way."""
        content = self
        while content.parent is not None:
            content = content.parent
        self._alert_content = content
        role = "m3x-dialog-full-screen" if self.full_screen else "m3x-dialog"
        try:
            return alert(
                content=content, buttons=[], dismissible=self.dismissible, role=role
            )
        finally:
            self._alert_content = None

    def close(self, value=None):
        """Close the Dialog. show() returns value."""
        if self._alert_content is not None:
            self._alert_content.raise_event("x-close-alert", value=value)

    def _on_close_click(self, event):
        self.close(None)

    def _on_show(self, **event_args):
        if self._alert_content is None:
            return
        # Anvil adds a backdrop for each open alert. The newest one belongs to
        # this Dialog and takes the M3 scrim colour.
        backdrops = window.document.querySelectorAll(".anvil-modal-backdrop")
        if backdrops.length:
            backdrops[backdrops.length - 1].classList.add("m3x-dialog-scrim")

    def _set_text(self, node_name, value):
        node = self.dom_nodes[node_name]
        node.innerText = value or ""
        node.style.display = "" if value else "none"

    @anvil_prop
    @property
    def headline(self, value) -> str:
        """The headline (title) of the Dialog."""
        self._set_text("m3x-dialog-headline", value)

    @anvil_prop
    @property
    def supporting_text(self, value) -> str:
        """The supporting text below the headline."""
        self._set_text("m3x-dialog-supporting-text", value)

    @anvil_prop
    @property
    def icon(self, value) -> str:
        """An icon shown above the headline. Basic dialogs only."""
        name = value[3:] if value and value.startswith("mi:") else ""
        self._set_text("m3x-dialog-icon", name)
        self.dom_nodes["m3x-dialog"].classList.toggle("m3x-dialog-has-icon", bool(name))

    @anvil_prop
    @property
    def full_screen(self, value) -> bool:
        """If True, the Dialog fills the whole screen."""
        self.dom_nodes["m3x-dialog"].classList.toggle(
            "m3x-dialog-full-screen", bool(value)
        )

    dismissible = property_without_callback("dismissible", True)
    visible = HtmlTemplate.visible
    role = role_property("m3x-dialog")

    #!componentEvent(m3.Dialog)!1: {name: "show", description: "When the Dialog is shown on the screen."}
    #!componentEvent(m3.Dialog)!1: {name: "hide", description: "When the Dialog is removed from the screen."}

    #!componentProp(m3.Dialog)!1: {name:"headline",type:"string",description:"The headline (title) of the Dialog."}
    #!componentProp(m3.Dialog)!1: {name:"supporting_text",type:"string",description:"The supporting text below the headline."}
    #!componentProp(m3.Dialog)!1: {name:"icon",type:"enum",description:"An icon shown above the headline. Basic dialogs only."}
    #!componentProp(m3.Dialog)!1: {name:"full_screen",type:"boolean",description:"If True, the Dialog fills the whole screen."}
    #!componentProp(m3.Dialog)!1: {name:"dismissible",type:"boolean",description:"If True, the user can dismiss the Dialog."}
    #!componentProp(m3.Dialog)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.Dialog)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.Dialog)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, Dialog, anvil.Component)!:
