"""M3 split button: a main action on the left and an arrow on the right that
opens a menu of related actions.
See docs/components/SplitButton.md in the project library.

The main part raises click. Choosing a menu option raises item_click with the
option's text (item) and position (index).
"""
from anvil import HtmlTemplate
from anvil.js import window

from ..._utils import fui
from ..._utils.properties import ComponentTag, anvil_prop, role_property
from ._anvil_designer import SplitButtonTemplate

_SIZES = ("xsmall", "small", "medium", "large", "xlarge")
_APPEARANCES = ("filled", "tonal", "elevated", "outlined")
_counter = [0]


class SplitButton(SplitButtonTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._open = False
        self._active = -1
        self._cleanup = None
        _counter[0] += 1
        self._id = f"m3x-split-{_counter[0]}"
        self.init_components(**properties)
        nodes = self.dom_nodes
        self._menu = nodes["m3x-split-menu"]
        self._menu.id = f"{self._id}-menu"
        self._home = self._menu.parentElement
        nodes["m3x-split-trailing"].setAttribute("aria-controls", self._menu.id)
        nodes["m3x-split-leading"].addEventListener("click", self._on_leading)
        nodes["m3x-split-trailing"].addEventListener("click", self._on_trailing)
        nodes["m3x-split-trailing"].addEventListener("keydown", self._on_trailing_key)
        self._menu.addEventListener("click", self._on_menu_click)
        self._menu.addEventListener("keydown", self._on_menu_key)
        self._outside = self._on_document_pointer
        self.add_event_handler("x-anvil-page-removed", lambda **e: self._close())

    # ---- main action -----------------------------------------------------------

    def _on_leading(self, event):
        self._close()
        self.raise_event("click")

    # ---- menu ----------------------------------------------------------------

    def _on_trailing(self, event):
        if self._open:
            self._close()
        else:
            self._open_menu(focus_first=event.detail == 0)  # 0: from the keyboard.

    def _on_trailing_key(self, event):
        if event.key in ("ArrowDown", "ArrowUp") and not self._open:
            event.preventDefault()
            self._open_menu(focus_first=True,
                            index=-1 if event.key == "ArrowUp" else 0)

    def _render_menu(self):
        menu = self._menu
        menu.innerHTML = ""
        for i, text in enumerate(self.menu_items or []):
            item = window.document.createElement("div")
            item.className = "m3x-split-menu-item"
            item.setAttribute("role", "menuitem")
            item.setAttribute("tabindex", "-1")
            item.setAttribute("data-index", str(i))
            item.textContent = text
            menu.appendChild(item)

    def _items(self):
        return list(self._menu.querySelectorAll(".m3x-split-menu-item"))

    def _open_menu(self, focus_first=False, index=0):
        if not self.enabled or not self.menu_items:
            return
        self._open = True
        self._render_menu()
        # The menu is drawn on the page body, outside Anvil's containers, which
        # cut off anything that reaches outside a component.
        window.document.body.appendChild(self._menu)
        self._menu.classList.add("m3x-split-menu-open")
        self.dom_nodes["m3x-split"].classList.add("m3x-split-selected")
        self.dom_nodes["m3x-split-trailing"].setAttribute("aria-expanded", "true")
        self._cleanup = fui.auto_update(
            self.dom_nodes["m3x-split"], self._menu,
            placement="bottom-end", strategy="fixed", offset=4)
        window.document.addEventListener("pointerdown", self._outside, True)
        if focus_first:
            items = self._items()
            self._focus(index % len(items))

    def _close(self, refocus=False):
        if not self._open:
            return
        self._open = False
        self._active = -1
        if self._cleanup:
            self._cleanup()
            self._cleanup = None
        window.document.removeEventListener("pointerdown", self._outside, True)
        self._menu.classList.remove("m3x-split-menu-open")
        self.dom_nodes["m3x-split"].classList.remove("m3x-split-selected")
        self.dom_nodes["m3x-split-trailing"].setAttribute("aria-expanded", "false")
        self._home.appendChild(self._menu)
        if refocus:
            self.dom_nodes["m3x-split-trailing"].focus()

    def _focus(self, index):
        items = self._items()
        if items:
            self._active = index % len(items)
            items[self._active].focus()

    def _choose(self, index):
        items = self.menu_items or []
        if 0 <= index < len(items):
            self._close(refocus=True)
            self.raise_event("item_click", item=items[index], index=index)

    def _on_menu_click(self, event):
        item = event.target.closest("[data-index]")
        if item:
            self._choose(int(item.getAttribute("data-index")))

    def _on_menu_key(self, event):
        key = event.key
        count = len(self._items())
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
            self._focus(count - 1)
        elif key in ("Enter", " "):
            event.preventDefault()
            self._choose(self._active)
        elif key in ("Escape", "Tab"):
            if key == "Escape":
                event.preventDefault()
            self._close(refocus=key == "Escape")

    def _on_document_pointer(self, event):
        root = self.dom_nodes["m3x-split"]
        if not (root.contains(event.target) or self._menu.contains(event.target)):
            self._close()

    # ---- properties ----------------------------------------------------------

    @anvil_prop(default_value="Save")
    @property
    def text(self, value) -> str:
        """The label of the main action."""
        self.dom_nodes["m3x-split-label"].innerText = value or ""

    @anvil_prop(default_value="")
    @property
    def icon(self, value) -> str:
        """An optional icon before the label."""
        name = value[3:] if value and value.startswith("mi:") else ""
        node = self.dom_nodes["m3x-split-icon"]
        node.innerText = name
        node.style.display = "" if name else "none"

    @anvil_prop(default_value=[])
    @property
    def menu_items(self, value) -> list:
        """The options in the menu that the arrow opens."""
        if getattr(self, "_open", False):
            self._render_menu()

    @anvil_prop(default_value="filled")
    @property
    def appearance(self, value) -> str:
        """filled, tonal, elevated or outlined."""
        node = self.dom_nodes["m3x-split"]  # Set before __init__ ends.
        for name in _APPEARANCES:
            node.classList.toggle(f"m3x-split-{name}", name == (value or "filled"))

    @anvil_prop(default_value="small")
    @property
    def size(self, value) -> str:
        """xsmall, small, medium, large or xlarge."""
        node = self.dom_nodes["m3x-split"]
        for name in _SIZES:
            node.classList.toggle(f"m3x-split-{name}", name == (value or "small"))

    @anvil_prop(default_value=True)
    @property
    def enabled(self, value) -> bool:
        """If True, the button can be clicked."""
        self.dom_nodes["m3x-split-leading"].disabled = not value
        self.dom_nodes["m3x-split-trailing"].disabled = not value
        if not value and getattr(self, "_open", False):
            self._close()

    visible = HtmlTemplate.visible
    role = role_property("m3x-split")

    #!componentEvent(m3.SplitButton)!1: {name: "click", description: "When the main (left) part of the button is clicked."}
    #!componentEvent(m3.SplitButton)!1: {name: "item_click", description: "When the user chooses an option from the menu.", parameters:[{name: "item", description: "The option's text."}, {name: "index", description: "The option's position, from 0."}]}
    #!componentEvent(m3.SplitButton)!1: {name: "show", description: "When the button is shown on the screen."}
    #!componentEvent(m3.SplitButton)!1: {name: "hide", description: "When the button is removed from the screen."}

    #!componentProp(m3.SplitButton)!1: {name:"text",type:"string",description:"The label of the main action."}
    #!componentProp(m3.SplitButton)!1: {name:"icon",type:"enum",description:"An optional icon before the label."}
    #!componentProp(m3.SplitButton)!1: {name:"menu_items",type:"text[]",description:"The options in the menu that the arrow opens."}
    #!componentProp(m3.SplitButton)!1: {name:"appearance",type:"enum",options:["filled", "tonal", "elevated", "outlined"],description:"The colours of the button."}
    #!componentProp(m3.SplitButton)!1: {name:"size",type:"enum",options:["xsmall", "small", "medium", "large", "xlarge"],description:"The size of the button."}
    #!componentProp(m3.SplitButton)!1: {name:"enabled",type:"boolean",description:"If True, the button can be clicked."}
    #!componentProp(m3.SplitButton)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.SplitButton)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.SplitButton)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, SplitButton, anvil.Component)!:
