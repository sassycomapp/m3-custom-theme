"""M3 list item: one, two or three lines, with optional leading and trailing
elements. See docs/components/ListItem.md in the project library.
"""
from anvil import HtmlTemplate

from ..._utils.properties import ComponentTag, anvil_prop, role_property
from ._anvil_designer import ListItemTemplate

_SLOT = "list-item-trailing-slot"


class ListItem(ListItemTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self.init_components(**properties)
        node = self.dom_nodes["m3x-list-item"]
        node.addEventListener("click", self._on_click)
        node.addEventListener("keydown", self._on_keydown)

    def add_component(self, component, slot=_SLOT, **layout_props):
        """Add a control, such as a Switch or Checkbox, at the end of the item."""
        super().add_component(component, slot=slot, **layout_props)

    # ---- interaction ---------------------------------------------------------

    def _from_slot(self, event):
        # A click on a control in the trailing slot belongs to that control.
        return bool(event.target.closest(".m3x-list-item-trailing-slot"))

    def _on_click(self, event):
        if self.clickable and self.enabled and not self._from_slot(event):
            self.raise_event("click")

    def _on_keydown(self, event):
        if event.key in ("Enter", " ") and not self._from_slot(event):
            event.preventDefault()
            self._on_click(event)

    # ---- look ----------------------------------------------------------------

    def _set_text(self, name, value):
        node = self.dom_nodes[name]
        node.innerText = value or ""
        node.style.display = "" if value else "none"

    def _update_leading(self):
        icon = self.leading_icon or ""
        icon = icon[3:] if icon.startswith("mi:") else ""
        avatar = "" if icon else (self.leading_avatar_text or "")
        image = "" if (icon or avatar) else (self.leading_image or "")
        self._set_text("m3x-list-item-leading-icon", icon)
        self._set_text("m3x-list-item-avatar", avatar)
        img = self.dom_nodes["m3x-list-item-image"]
        if image:
            img.src = str(image)
        img.style.display = "" if image else "none"
        leading = self.dom_nodes["m3x-list-item-leading"]
        leading.style.display = "" if (icon or avatar or image) else "none"
        self._toggle("m3x-list-item-has-image", bool(image))

    def _update_state(self):
        node = self.dom_nodes["m3x-list-item"]
        interactive = bool(self.clickable)
        self._toggle("m3x-list-item-clickable", interactive)
        self._toggle("m3x-list-item-selected", self.selected)
        self._toggle("m3x-list-item-disabled", interactive and not self.enabled)
        if interactive:
            node.setAttribute("role", "button")
            node.setAttribute("tabindex", "0" if self.enabled else "-1")
            node.setAttribute("aria-disabled", "false" if self.enabled else "true")
        else:
            node.setAttribute("role", "listitem")
            node.removeAttribute("tabindex")
            node.removeAttribute("aria-disabled")
        if self.selected:
            node.setAttribute("aria-current", "true")
        else:
            node.removeAttribute("aria-current")

    def _toggle(self, name, value):
        self.dom_nodes["m3x-list-item"].classList.toggle(name, bool(value))

    @anvil_prop(default_value="List item")
    @property
    def headline(self, value) -> str:
        """The main text of the item."""
        self.dom_nodes["m3x-list-item-headline"].innerText = value or ""

    @anvil_prop(default_value="")
    @property
    def supporting_text(self, value) -> str:
        """A second line of text below the headline."""
        self._set_text("m3x-list-item-supporting-text", value)
        self._toggle("m3x-list-item-two-line", value)

    @anvil_prop(default_value="")
    @property
    def overline(self, value) -> str:
        """A small line of text above the headline."""
        self._set_text("m3x-list-item-overline", value)
        self._toggle("m3x-list-item-has-overline", value)

    @anvil_prop(default_value=False)
    @property
    def three_line(self, value) -> bool:
        """If True, the supporting text may take two lines."""
        self._toggle("m3x-list-item-three-line", value)

    @anvil_prop(default_value="")
    @property
    def leading_icon(self, value) -> str:
        """An icon at the start of the item."""
        self._update_leading()

    @anvil_prop(default_value="")
    @property
    def leading_avatar_text(self, value) -> str:
        """Text shown in a round avatar at the start of the item."""
        self._update_leading()

    @anvil_prop(default_value="")
    @property
    def leading_image(self, value) -> str:
        """An image shown at the start of the item."""
        self._update_leading()

    @anvil_prop(default_value="")
    @property
    def trailing_text(self, value) -> str:
        """A short text at the end of the item."""
        self._set_text("m3x-list-item-trailing-text", value)

    @anvil_prop(default_value="")
    @property
    def trailing_icon(self, value) -> str:
        """An icon at the end of the item."""
        name = value[3:] if value and value.startswith("mi:") else ""
        self._set_text("m3x-list-item-trailing-icon", name)

    @anvil_prop(default_value=False)
    @property
    def clickable(self, value) -> bool:
        """If True, the item reacts to the mouse and keyboard."""
        self._update_state()

    @anvil_prop(default_value=False)
    @property
    def selected(self, value) -> bool:
        """If True, the item is shown as selected."""
        self._update_state()

    @anvil_prop(default_value=True)
    @property
    def enabled(self, value) -> bool:
        """If True, a clickable item can be clicked."""
        self._update_state()

    @anvil_prop(default_value=False)
    @property
    def divider(self, value) -> bool:
        """If True, a thin line is drawn under the item."""
        self._toggle("m3x-list-item-divider", value)

    visible = HtmlTemplate.visible
    role = role_property("m3x-list-item")

    #!componentEvent(m3.ListItem)!1: {name: "click", description: "When a clickable ListItem is clicked."}
    #!componentEvent(m3.ListItem)!1: {name: "show", description: "When the ListItem is shown on the screen."}
    #!componentEvent(m3.ListItem)!1: {name: "hide", description: "When the ListItem is removed from the screen."}

    #!componentProp(m3.ListItem)!1: {name:"headline",type:"string",description:"The main text of the item."}
    #!componentProp(m3.ListItem)!1: {name:"supporting_text",type:"string",description:"A second line of text below the headline."}
    #!componentProp(m3.ListItem)!1: {name:"overline",type:"string",description:"A small line of text above the headline."}
    #!componentProp(m3.ListItem)!1: {name:"three_line",type:"boolean",description:"If True, the supporting text may take two lines."}
    #!componentProp(m3.ListItem)!1: {name:"leading_icon",type:"enum",description:"An icon at the start of the item."}
    #!componentProp(m3.ListItem)!1: {name:"leading_avatar_text",type:"string",description:"Text shown in a round avatar at the start of the item."}
    #!componentProp(m3.ListItem)!1: {name:"leading_image",type:"uri",description:"An image shown at the start of the item."}
    #!componentProp(m3.ListItem)!1: {name:"trailing_text",type:"string",description:"A short text at the end of the item."}
    #!componentProp(m3.ListItem)!1: {name:"trailing_icon",type:"enum",description:"An icon at the end of the item."}
    #!componentProp(m3.ListItem)!1: {name:"clickable",type:"boolean",description:"If True, the item reacts to the mouse and keyboard."}
    #!componentProp(m3.ListItem)!1: {name:"selected",type:"boolean",description:"If True, the item is shown as selected."}
    #!componentProp(m3.ListItem)!1: {name:"enabled",type:"boolean",description:"If True, a clickable item can be clicked."}
    #!componentProp(m3.ListItem)!1: {name:"divider",type:"boolean",description:"If True, a thin line is drawn under the item."}
    #!componentProp(m3.ListItem)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.ListItem)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.ListItem)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, ListItem, anvil.Component)!:
