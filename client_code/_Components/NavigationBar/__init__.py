"""M3 navigation bar: three to five destinations at the bottom of the screen.
See docs/components/NavigationBar.md in the project library.

The navigation bar shows the destinations. The app shows the selected
destination, normally by opening a form or showing a panel in the change event.
"""
from anvil import HtmlTemplate
from anvil.js import window

from ..._utils.properties import ComponentTag, anvil_prop, role_property
from ._anvil_designer import NavigationBarTemplate


class NavigationBar(NavigationBarTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._buttons = []
        self.init_components(**properties)

    def _build(self):
        bar = self.dom_nodes["m3x-navigation-bar"]
        bar.innerHTML = ""
        self._buttons = []
        doc = window.document
        icons = list(self.icons or [])
        badges = list(self.badges or [])
        for i, text in enumerate(list(self.items or [])):
            button = doc.createElement("button")
            button.type = "button"
            button.className = "m3x-navigation-bar-item"
            indicator = doc.createElement("span")
            indicator.className = "m3x-navigation-bar-indicator"
            icon = icons[i] if i < len(icons) else ""
            node = doc.createElement("i")
            node.className = "m3x-navigation-bar-icon material-symbols-outlined"
            node.setAttribute("aria-hidden", "true")
            node.innerText = icon[3:] if icon and icon.startswith("mi:") else ""
            indicator.appendChild(node)
            badge = badges[i] if i < len(badges) else None
            if badge is not None:
                count = int(badge)
                size = "large" if count > 0 else "small"
                mark = doc.createElement("span")
                mark.className = f"m3x-badge m3x-badge-{size} m3x-navigation-bar-badge"
                if count > 0:
                    mark.innerText = "999+" if count > 999 else str(count)
                button.setAttribute(
                    "aria-description", f"{count} new" if count > 0 else "new"
                )
                indicator.appendChild(mark)
            button.appendChild(indicator)
            label = doc.createElement("span")
            label.className = "m3x-navigation-bar-label"
            label.innerText = text
            button.appendChild(label)
            button.addEventListener("click", lambda event, i=i: self._select(i))
            bar.appendChild(button)
            self._buttons.append(button)
        self._show_selected()

    def _show_selected(self):
        for i, button in enumerate(self._buttons):
            selected = i == self.selected_index
            button.classList.toggle("m3x-navigation-bar-selected", selected)
            if selected:
                button.setAttribute("aria-current", "page")
            else:
                button.removeAttribute("aria-current")

    def _select(self, index):
        if index != self.selected_index:
            self.selected_index = index
            self.raise_event("change")

    @anvil_prop(default_value=["Home", "Search", "Profile"])
    @property
    def items(self, value) -> list:
        """The label of each destination."""
        self._build()

    @anvil_prop(default_value=["mi:home", "mi:search", "mi:person"])
    @property
    def icons(self, value) -> list:
        """One mi: icon per destination."""
        self._build()

    @anvil_prop(default_value=None)
    @property
    def badges(self, value) -> list:
        """One badge per destination: None, 0 for a dot, or a number."""
        self._build()

    @anvil_prop(default_value=0)
    @property
    def selected_index(self, value) -> int:
        """The position of the selected destination, counting from 0."""
        self._show_selected()

    @anvil_prop(default_value=False)
    @property
    def fixed(self, value) -> bool:
        """If True, the bar is fixed to the bottom edge of the window."""
        self.dom_nodes["m3x-navigation-bar"].classList.toggle(
            "m3x-navigation-bar-fixed", bool(value)
        )

    @property
    def selected_text(self):
        """The label of the selected destination."""
        items = list(self.items or [])
        index = self.selected_index
        return items[index] if index is not None and 0 <= index < len(items) else None

    visible = HtmlTemplate.visible
    role = role_property("m3x-navigation-bar")

    #!componentEvent(m3.NavigationBar)!1: {name: "change", description: "When the user selects a different destination."}
    #!componentEvent(m3.NavigationBar)!1: {name: "show", description: "When the navigation bar is shown on the screen."}
    #!componentEvent(m3.NavigationBar)!1: {name: "hide", description: "When the navigation bar is removed from the screen."}

    #!componentProp(m3.NavigationBar)!1: {name:"items",type:"text[]",description:"The label of each destination."}
    #!componentProp(m3.NavigationBar)!1: {name:"icons",type:"text[]",description:"One mi: icon per destination."}
    #!componentProp(m3.NavigationBar)!1: {name:"badges",type:"object",description:"One badge per destination: None, 0 for a dot, or a number."}
    #!componentProp(m3.NavigationBar)!1: {name:"selected_index",type:"number",description:"The position of the selected destination."}
    #!componentProp(m3.NavigationBar)!1: {name:"selected_text",type:"string",description:"The label of the selected destination."}
    #!componentProp(m3.NavigationBar)!1: {name:"fixed",type:"boolean",description:"If True, the bar is fixed to the bottom edge of the window."}
    #!componentProp(m3.NavigationBar)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.NavigationBar)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.NavigationBar)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, NavigationBar, anvil.Component)!:
