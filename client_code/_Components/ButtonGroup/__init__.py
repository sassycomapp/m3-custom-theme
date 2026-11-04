"""M3 Expressive button group: connected (replacing segmented buttons) or
standard. See docs/components/ButtonGroup.md in the project library.
"""
from anvil import HtmlTemplate
from anvil.js import window

from ..._utils.properties import ComponentTag, anvil_prop, role_property
from ._anvil_designer import ButtonGroupTemplate

_SELECTIONS = ("none", "single", "multiple")


class ButtonGroup(ButtonGroupTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._buttons = []
        self._selected = set()
        self.init_components(**properties)

    # ---- building ------------------------------------------------------------

    def _build(self):
        container = self.dom_nodes["m3x-button-group"]
        container.innerHTML = ""
        self._buttons = []
        doc = window.document
        icons = list(self.icons or [])
        for i, text in enumerate(list(self.items or [])):
            button = doc.createElement("button")
            button.type = "button"
            button.className = "m3x-button-group-button"
            icon = icons[i] if i < len(icons) else ""
            if icon and icon.startswith("mi:"):
                node = doc.createElement("i")
                node.className = "m3x-button-group-icon material-symbols-outlined"
                node.setAttribute("aria-hidden", "true")
                node.innerText = icon[3:]
                button.appendChild(node)
            if text:
                label = doc.createElement("span")
                label.innerText = text
                button.appendChild(label)
            elif icon:
                button.setAttribute("aria-label", icon[3:])
            button.addEventListener("click", lambda event, i=i: self._on_click(i))
            container.appendChild(button)
            self._buttons.append(button)
        self._clean_selection()
        self._show()

    def _clean_selection(self):
        count = len(self._buttons)
        if not count:
            return  # The buttons are not built yet: keep the requested selection.
        mode = self._mode()
        selected = {i for i in self._selected if 0 <= i < count}
        if mode == "none":
            selected = set()
        elif mode == "single":
            first = min(selected) if selected else 0
            selected = {first}
        self._selected = selected

    def _mode(self):
        return self.selection if self.selection in _SELECTIONS else "single"

    def _show(self):
        mode = self._mode()
        for i, button in enumerate(self._buttons):
            selected = i in self._selected
            button.classList.toggle("m3x-button-group-selected", selected)
            if mode == "none":
                button.removeAttribute("aria-pressed")
            else:
                button.setAttribute("aria-pressed", "true" if selected else "false")
            if self.enabled:
                button.removeAttribute("disabled")
            else:
                button.setAttribute("disabled", "")

    # ---- interaction ---------------------------------------------------------

    def _on_click(self, index):
        if not self.enabled:
            return
        mode = self._mode()
        if mode == "single" and index not in self._selected:
            self._selected = {index}
            self._store()
            self.raise_event("change")
        elif mode == "multiple":
            self._selected ^= {index}
            self._store()
            self.raise_event("change")
        self.raise_event("click", index=index)

    def _store(self):
        """Copy the selection into the two selection properties."""
        ordered = sorted(self._selected)
        self._props["selected_indices"] = ordered
        self._props["selected_index"] = ordered[0] if ordered else None
        self._show()

    # ---- properties ----------------------------------------------------------

    @anvil_prop(default_value=["Day", "Week", "Month"])
    @property
    def items(self, value) -> list:
        """The label of each button."""
        self._build()

    @anvil_prop(default_value=[])
    @property
    def icons(self, value) -> list:
        """Optional: one mi: icon per button."""
        self._build()

    @anvil_prop(default_value="connected")
    @property
    def type(self, value) -> str:
        """connected or standard."""
        node = self.dom_nodes["m3x-button-group"]
        node.classList.toggle("m3x-button-group-connected", value != "standard")
        node.classList.toggle("m3x-button-group-standard", value == "standard")

    @anvil_prop(default_value="single")
    @property
    def selection(self, value) -> str:
        """none, single or multiple."""
        self._clean_selection()
        self._store()

    def _get_selected_index(self):
        return self._props.get("selected_index")

    def _set_selected_index(self, value):
        self._selected = set() if value is None else {int(value)}
        self._clean_selection()
        self._store()

    selected_index = property(_get_selected_index, _set_selected_index)

    def _get_selected_indices(self):
        return list(self._props.get("selected_indices", []) or [])

    def _set_selected_indices(self, value):
        self._selected = {int(i) for i in (value or [])}
        self._clean_selection()
        self._store()

    selected_indices = property(_get_selected_indices, _set_selected_indices)

    @anvil_prop(default_value="filled")
    @property
    def appearance(self, value) -> str:
        """filled, tonal or outlined."""
        node = self.dom_nodes["m3x-button-group"]
        for option in ("filled", "tonal", "outlined"):
            node.classList.toggle(f"m3x-button-group-{option}", option == value)

    @anvil_prop(default_value=False)
    @property
    def full_width(self, value) -> bool:
        """If True, the group fills the width of its container."""
        self.dom_nodes["m3x-button-group"].classList.toggle(
            "m3x-button-group-full-width", bool(value)
        )

    @anvil_prop(default_value=True)
    @property
    def enabled(self, value) -> bool:
        """If True, the buttons can be clicked."""
        self._show()

    visible = HtmlTemplate.visible
    role = role_property("m3x-button-group")

    #!componentEvent(m3.ButtonGroup)!1: {name: "change", description: "When the selection changes."}
    #!componentEvent(m3.ButtonGroup)!1: {name: "click", description: "When any button in the group is clicked.", parameters:[{name: "index", description: "The position of the button, counting from 0."}]}
    #!componentEvent(m3.ButtonGroup)!1: {name: "show", description: "When the group is shown on the screen."}
    #!componentEvent(m3.ButtonGroup)!1: {name: "hide", description: "When the group is removed from the screen."}

    #!componentProp(m3.ButtonGroup)!1: {name:"items",type:"text[]",description:"The label of each button."}
    #!componentProp(m3.ButtonGroup)!1: {name:"icons",type:"text[]",description:"Optional: one mi: icon per button."}
    #!componentProp(m3.ButtonGroup)!1: {name:"type",type:"enum",options:["connected", "standard"],description:"connected or standard."}
    #!componentProp(m3.ButtonGroup)!1: {name:"selection",type:"enum",options:["none", "single", "multiple"],description:"none, single or multiple."}
    #!componentProp(m3.ButtonGroup)!1: {name:"selected_index",type:"number",description:"The position of the selected button."}
    #!componentProp(m3.ButtonGroup)!1: {name:"selected_indices",type:"object",description:"The positions of all selected buttons."}
    #!componentProp(m3.ButtonGroup)!1: {name:"appearance",type:"enum",options:["filled", "tonal", "outlined"],description:"The colours of the buttons."}
    #!componentProp(m3.ButtonGroup)!1: {name:"full_width",type:"boolean",description:"If True, the group fills the width of its container."}
    #!componentProp(m3.ButtonGroup)!1: {name:"enabled",type:"boolean",description:"If True, the buttons can be clicked."}
    #!componentProp(m3.ButtonGroup)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.ButtonGroup)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.ButtonGroup)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, ButtonGroup, anvil.Component)!:
