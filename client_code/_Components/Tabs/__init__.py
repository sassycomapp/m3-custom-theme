"""M3 Tabs: primary and secondary tabs, fixed or scrollable.
See docs/components/Tabs.md in the project library.

The Tabs component shows the row of tabs only. The app shows the content of the
selected tab, normally by making one of several panels visible in the change
event.
"""
from anvil import HtmlTemplate
from anvil.js import window

from ..._utils.properties import ComponentTag, anvil_prop, role_property
from ._anvil_designer import TabsTemplate


class Tabs(TabsTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._buttons = []
        self.init_components(**properties)

    # ---- building the row --------------------------------------------------

    def _build(self):
        container = self.dom_nodes["m3x-tabs"]
        container.innerHTML = ""
        self._buttons = []
        items = list(self.items or [])
        icons = list(self.icons or [])
        has_icons = any(icon for icon in icons)
        container.classList.toggle("m3x-tabs-with-icons", has_icons)
        doc = window.document
        for i, text in enumerate(items):
            button = doc.createElement("button")
            button.type = "button"
            button.className = "m3x-tab"
            button.setAttribute("role", "tab")
            content = doc.createElement("span")
            content.className = "m3x-tab-content"
            icon = icons[i] if i < len(icons) else ""
            if icon and icon.startswith("mi:"):
                node = doc.createElement("i")
                node.className = "m3x-tab-icon material-symbols-outlined"
                node.setAttribute("aria-hidden", "true")
                node.innerText = icon[3:]
                content.appendChild(node)
            label = doc.createElement("span")
            label.className = "m3x-tab-label"
            label.innerText = text
            content.appendChild(label)
            indicator = doc.createElement("span")
            indicator.className = "m3x-tab-indicator"
            content.appendChild(indicator)
            button.appendChild(content)
            button.addEventListener("click", lambda event, i=i: self._select(i))
            button.addEventListener("keydown", self._on_keydown)
            container.appendChild(button)
            self._buttons.append(button)
        self._show_selected()

    def _show_selected(self):
        index = self._clamped(self.selected_index)
        for i, button in enumerate(self._buttons):
            selected = i == index
            button.classList.toggle("m3x-tab-selected", selected)
            button.setAttribute("aria-selected", "true" if selected else "false")
            button.setAttribute("tabindex", "0" if selected else "-1")

    def _clamped(self, index):
        if not self._buttons:
            return None
        try:
            index = int(index or 0)
        except (TypeError, ValueError):
            index = 0
        return max(0, min(index, len(self._buttons) - 1))

    # ---- interaction ---------------------------------------------------------

    def _select(self, index, focus=False):
        index = self._clamped(index)
        if index is None:
            return
        if focus:
            self._buttons[index].focus()
        if index != self._clamped(self.selected_index):
            self.selected_index = index
            self.raise_event("change")
        self._buttons[index].scrollIntoView({"block": "nearest", "inline": "nearest"})

    def _on_keydown(self, event):
        # The ARIA tabs pattern: arrow keys, Home and End move the selection.
        current = self._clamped(self.selected_index)
        if current is None:
            return
        last = len(self._buttons) - 1
        moves = {"ArrowRight": current + 1, "ArrowLeft": current - 1,
                 "Home": 0, "End": last}
        if event.key not in moves:
            return
        event.preventDefault()
        target = moves[event.key]
        if target > last:
            target = 0
        elif target < 0:
            target = last
        self._select(target, focus=True)

    # ---- properties ----------------------------------------------------------

    @anvil_prop(default_value=["Tab 1", "Tab 2", "Tab 3"])
    @property
    def items(self, value) -> list:
        """The label of each tab."""
        self._build()

    @anvil_prop(default_value=[])
    @property
    def icons(self, value) -> list:
        """Optional: one mi: icon per tab, in the same order as the items."""
        self._build()

    @anvil_prop(default_value=0)
    @property
    def selected_index(self, value) -> int:
        """The position of the selected tab, counting from 0."""
        self._show_selected()

    @anvil_prop(default_value="primary")
    @property
    def type(self, value) -> str:
        """primary or secondary."""
        node = self.dom_nodes["m3x-tabs"]
        node.classList.toggle("m3x-tabs-primary", value != "secondary")
        node.classList.toggle("m3x-tabs-secondary", value == "secondary")

    @anvil_prop(default_value=False)
    @property
    def scrollable(self, value) -> bool:
        """If True, tabs keep their natural width and the row scrolls sideways."""
        self.dom_nodes["m3x-tabs"].classList.toggle("m3x-tabs-scrollable", bool(value))

    @property
    def selected_text(self):
        """The label of the selected tab, or None if there are no tabs."""
        index = self._clamped(self.selected_index)
        return None if index is None else list(self.items)[index]

    visible = HtmlTemplate.visible
    role = role_property("m3x-tabs")

    #!componentEvent(m3.Tabs)!1: {name: "change", description: "When the user selects a different tab."}
    #!componentEvent(m3.Tabs)!1: {name: "show", description: "When the Tabs are shown on the screen."}
    #!componentEvent(m3.Tabs)!1: {name: "hide", description: "When the Tabs are removed from the screen."}

    #!componentProp(m3.Tabs)!1: {name:"items",type:"text[]",description:"The label of each tab."}
    #!componentProp(m3.Tabs)!1: {name:"icons",type:"text[]",description:"Optional: one mi: icon per tab."}
    #!componentProp(m3.Tabs)!1: {name:"selected_index",type:"number",description:"The position of the selected tab, counting from 0."}
    #!componentProp(m3.Tabs)!1: {name:"selected_text",type:"string",description:"The label of the selected tab."}
    #!componentProp(m3.Tabs)!1: {name:"type",type:"enum",options:["primary", "secondary"],description:"primary or secondary."}
    #!componentProp(m3.Tabs)!1: {name:"scrollable",type:"boolean",description:"If True, the row scrolls sideways."}
    #!componentProp(m3.Tabs)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.Tabs)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.Tabs)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, Tabs, anvil.Component)!:
