"""M3 FAB menu: a floating action button that opens a short stack of related
actions above it. While open, the button turns into a round close button.
See docs/components/FabMenu.md in the project library.

Choosing an action raises item_click with the action's text (item) and
position (index).
"""
from anvil import HtmlTemplate
from anvil.designer import in_designer
from anvil.js import window

from ..._utils import fui
from ..._utils.properties import ComponentTag, anvil_prop, role_property
from ._anvil_designer import FabMenuTemplate

_COLORS = ("primary", "secondary", "tertiary")
_SIZES = ("regular", "medium", "large")
_EXIT_MS = 200  # Slightly longer than the closing transition.
_counter = [0]


class FabMenu(FabMenuTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._open = False
        self._active = -1
        self._cleanup = None
        self._timer = None
        _counter[0] += 1
        self._id = f"m3x-fab-menu-{_counter[0]}"
        self.init_components(**properties)
        nodes = self.dom_nodes
        self._list = nodes["m3x-fab-menu-list"]
        self._list.id = f"{self._id}-list"
        self._home = self._list.parentElement
        toggle = nodes["m3x-fab-menu-toggle"]
        toggle.setAttribute("aria-controls", self._list.id)
        toggle.addEventListener("click", self._on_toggle)
        toggle.addEventListener("keydown", self._on_toggle_key)
        self._list.addEventListener("click", self._on_list_click)
        self._list.addEventListener("keydown", self._on_list_key)
        self._outside = self._on_document_pointer
        self._escape = self._on_document_key
        self.add_event_handler("x-anvil-page-removed", lambda **e: self._finish_close())

    # ---- opening and closing -------------------------------------------------

    def _on_toggle(self, event):
        if self._open:
            self._close(refocus=False)
        else:
            self._open_menu(focus_index=0 if event.detail == 0 else None)

    def _on_toggle_key(self, event):
        # Lesson 21: the arrow keys open the menu, or move into an open one.
        if event.key not in ("ArrowUp", "ArrowDown"):
            return
        event.preventDefault()
        index = -1 if event.key == "ArrowUp" else 0
        if self._open:
            self._focus(index)
        else:
            self._open_menu(focus_index=index)

    def _render_list(self):
        self._list.innerHTML = ""
        items = list(self.items or [])
        icons = list(self.item_icons or [])
        count = len(items)
        for i, text in enumerate(items):
            button = window.document.createElement("button")
            button.type = "button"
            button.className = "m3x-fab-menu-item"
            button.setAttribute("role", "menuitem")
            button.setAttribute("tabindex", "-1")
            button.setAttribute("data-index", str(i))
            # The action nearest the button appears first.
            button.style.setProperty("--m3x-fab-menu-item-order", str(count - 1 - i))
            icon = icons[i] if i < len(icons) else ""
            if icon and icon.startswith("mi:"):
                glyph = window.document.createElement("i")
                glyph.className = "m3x-fab-menu-item-icon material-symbols-outlined"
                glyph.setAttribute("aria-hidden", "true")
                glyph.textContent = icon[3:]
                button.appendChild(glyph)
            label = window.document.createElement("span")
            label.textContent = text
            button.appendChild(label)
            self._list.appendChild(button)

    def _items(self):
        return list(self._list.querySelectorAll(".m3x-fab-menu-item"))

    def _open_menu(self, focus_index=None):
        if not self.enabled or not self.items or in_designer:
            return
        window.clearTimeout(self._timer)
        self._open = True
        self._active = -1
        self._render_list()
        root = self.dom_nodes["m3x-fab-menu"]
        # The list is drawn on the page body, outside Anvil's containers, which
        # cut off anything that reaches outside a component.
        for name in _COLORS:
            self._list.classList.toggle(f"m3x-fab-menu-{name}",
                                        root.classList.contains(f"m3x-fab-menu-{name}"))
        window.document.body.appendChild(self._list)
        self._list.classList.add("m3x-fab-menu-list-open")
        root.classList.add("m3x-fab-menu-expanded")
        self.dom_nodes["m3x-fab-menu-toggle"].setAttribute("aria-expanded", "true")
        self._cleanup = fui.auto_update(
            self.dom_nodes["m3x-fab-menu-toggle"], self._list,
            placement="top-end", strategy="fixed", offset=8)
        self._list.offsetHeight  # Start the items' entrance from hidden.
        self._list.classList.add("m3x-fab-menu-list-shown")
        window.document.addEventListener("pointerdown", self._outside, True)
        # Escape closes the menu wherever the focus is: a menu opened with the
        # mouse leaves the focus on the button, outside the list.
        window.document.addEventListener("keydown", self._escape, True)
        if focus_index is not None:
            self._focus(focus_index)
        self.raise_event("opened")

    def _close(self, refocus=True):
        if not self._open:
            return
        self._open = False
        self._active = -1
        window.document.removeEventListener("pointerdown", self._outside, True)
        window.document.removeEventListener("keydown", self._escape, True)
        self._list.classList.remove("m3x-fab-menu-list-shown")
        self.dom_nodes["m3x-fab-menu"].classList.remove("m3x-fab-menu-expanded")
        self.dom_nodes["m3x-fab-menu-toggle"].setAttribute("aria-expanded", "false")
        if refocus:
            self.dom_nodes["m3x-fab-menu-toggle"].focus()
        window.clearTimeout(self._timer)
        self._timer = window.setTimeout(self._finish_close, _EXIT_MS)
        self.raise_event("closed")

    def _finish_close(self, *args):
        if self._open:
            # The form was removed while the menu was open.
            self._open = False
            window.document.removeEventListener("pointerdown", self._outside, True)
            window.document.removeEventListener("keydown", self._escape, True)
            self.dom_nodes["m3x-fab-menu"].classList.remove("m3x-fab-menu-expanded")
        if self._cleanup:
            self._cleanup()
            self._cleanup = None
        self._list.classList.remove("m3x-fab-menu-list-open", "m3x-fab-menu-list-shown")
        if not self._home.isSameNode(self._list.parentElement):
            self._home.appendChild(self._list)

    def close(self):
        """Close the menu."""
        self._close(refocus=False)

    # ---- choosing --------------------------------------------------------------

    def _focus(self, index):
        items = self._items()
        if items:
            self._active = index % len(items)
            items[self._active].focus()

    def _choose(self, index):
        items = list(self.items or [])
        if 0 <= index < len(items):
            self._close()
            self.raise_event("item_click", item=items[index], index=index)

    def _on_list_click(self, event):
        item = event.target.closest("[data-index]")
        if item:
            self._choose(int(item.getAttribute("data-index")))

    def _on_list_key(self, event):
        key = event.key
        if key == "ArrowDown":
            event.preventDefault()
            self._focus(self._active + 1)
        elif key == "ArrowUp":
            event.preventDefault()
            self._focus(self._active - 1)
        elif key == "Home":
            event.preventDefault()
            self._focus(0)
        elif key == "End":
            event.preventDefault()
            self._focus(len(self._items()) - 1)
        elif key == "Tab":
            self._close(refocus=False)

    def _on_document_key(self, event):
        if event.key == "Escape":
            event.preventDefault()
            event.stopPropagation()
            self._close()

    def _on_document_pointer(self, event):
        inside = (self.dom_nodes["m3x-fab-menu"].contains(event.target)
                  or self._list.contains(event.target))
        if not inside:
            self._close(refocus=False)

    # ---- properties ------------------------------------------------------------

    @anvil_prop(default_value="mi:add")
    @property
    def icon(self, value) -> str:
        """The icon on the button while the menu is closed."""
        name = value[3:] if value and value.startswith("mi:") else "add"
        self.dom_nodes["m3x-fab-menu-icon"].innerText = name

    @anvil_prop(default_value=[])
    @property
    def items(self, value) -> list:
        """The actions in the menu, from top to bottom."""
        if getattr(self, "_open", False):
            self._render_list()

    @anvil_prop(default_value=[])
    @property
    def item_icons(self, value) -> list:
        """Optional: one mi: icon per action."""
        if getattr(self, "_open", False):
            self._render_list()

    @anvil_prop(default_value="primary")
    @property
    def color(self, value) -> str:
        """primary, secondary or tertiary."""
        node = self.dom_nodes["m3x-fab-menu"]  # Set before __init__ ends.
        for name in _COLORS:
            node.classList.toggle(f"m3x-fab-menu-{name}", name == (value or "primary"))

    @anvil_prop(default_value="regular")
    @property
    def size(self, value) -> str:
        """regular, medium or large: the button's size while closed."""
        node = self.dom_nodes["m3x-fab-menu"]
        for name in _SIZES:
            node.classList.toggle(f"m3x-fab-menu-{name}", name == (value or "regular"))

    @anvil_prop(default_value=False)
    @property
    def floating(self, value) -> bool:
        """If True, the button floats in the bottom right corner of the window."""
        self.dom_nodes["m3x-fab-menu"].classList.toggle("m3x-fab-menu-floating",
                                                        bool(value))

    @anvil_prop(default_value="Actions")
    @property
    def label(self, value) -> str:
        """A name for the button and its menu that screen readers announce."""
        self.dom_nodes["m3x-fab-menu-toggle"].setAttribute("aria-label",
                                                           value or "Actions")
        self.dom_nodes["m3x-fab-menu-list"].setAttribute("aria-label",
                                                         value or "Actions")

    @anvil_prop(default_value=True)
    @property
    def enabled(self, value) -> bool:
        """If True, the button can be clicked."""
        self.dom_nodes["m3x-fab-menu-toggle"].disabled = not value
        if not value and getattr(self, "_open", False):
            self._close(refocus=False)

    visible = HtmlTemplate.visible
    role = role_property("m3x-fab-menu")

    #!componentEvent(m3.FabMenu)!1: {name: "item_click", description: "When the user chooses an action from the menu.", parameters:[{name: "item", description: "The action's text."}, {name: "index", description: "The action's position, from 0."}]}
    #!componentEvent(m3.FabMenu)!1: {name: "opened", description: "When the menu has opened."}
    #!componentEvent(m3.FabMenu)!1: {name: "closed", description: "When the menu has closed."}
    #!componentEvent(m3.FabMenu)!1: {name: "show", description: "When the button is shown on the screen."}
    #!componentEvent(m3.FabMenu)!1: {name: "hide", description: "When the button is removed from the screen."}

    #!componentProp(m3.FabMenu)!1: {name:"icon",type:"enum",description:"The icon on the button while the menu is closed."}
    #!componentProp(m3.FabMenu)!1: {name:"items",type:"text[]",description:"The actions in the menu, from top to bottom."}
    #!componentProp(m3.FabMenu)!1: {name:"item_icons",type:"text[]",description:"Optional: one mi: icon per action."}
    #!componentProp(m3.FabMenu)!1: {name:"color",type:"enum",options:["primary", "secondary", "tertiary"],description:"The colour set."}
    #!componentProp(m3.FabMenu)!1: {name:"size",type:"enum",options:["regular", "medium", "large"],description:"The button's size while the menu is closed."}
    #!componentProp(m3.FabMenu)!1: {name:"floating",type:"boolean",description:"If True, the button floats in the bottom right corner of the window."}
    #!componentProp(m3.FabMenu)!1: {name:"label",type:"string",description:"A name for the button and its menu that screen readers announce."}
    #!componentProp(m3.FabMenu)!1: {name:"enabled",type:"boolean",description:"If True, the button can be clicked."}
    #!componentProp(m3.FabMenu)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.FabMenu)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.FabMenu)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, FabMenu, anvil.Component)!:
