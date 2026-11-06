"""M3 search: a search bar that opens a search view of suggestions.
See docs/components/SearchBar.md in the project library.

The view drops down from the bar (docked search view) on wide screens and
fills the screen (full-screen search view) on screens narrower than 600 px.
"""
from anvil import HtmlTemplate
from anvil.js import window

from ..._utils.properties import ComponentTag, anvil_prop, role_property
from ._anvil_designer import SearchBarTemplate

_SLOT = "search-trailing-slot"
_counter = [0]


class SearchBar(SearchBarTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._open = False
        self._active = -1
        self._shown = []
        _counter[0] += 1
        self._id = f"m3x-search-{_counter[0]}"
        self.init_components(**properties)
        nodes = self.dom_nodes
        nodes["m3x-search-view"].id = f"{self._id}-view"
        nodes["m3x-search-input"].setAttribute("aria-controls", f"{self._id}-view")
        nodes["m3x-search-input"].addEventListener("input", self._on_input)
        nodes["m3x-search-input"].addEventListener("focus", lambda e: self._open_view())
        nodes["m3x-search-input"].addEventListener("keydown", self._on_key)
        nodes["m3x-search-clear"].addEventListener("click", self._on_clear)
        nodes["m3x-search-back"].addEventListener("click", lambda e: self._close_view())
        nodes["m3x-search-view"].addEventListener("click", self._on_view_click)
        # Pressing on a suggestion would blur the input before the click; keep focus.
        nodes["m3x-search-view"].addEventListener(
            "pointerdown", lambda e: e.preventDefault())
        self._outside = self._on_document_pointer
        self._update_clear()

    def add_component(self, component, slot=_SLOT, **layout_props):
        """Add a component, such as an Avatar or IconButton, at the end of the bar."""
        super().add_component(component, slot=slot, **layout_props)

    # ---- view ----------------------------------------------------------------

    def _matches(self):
        text = (self.text or "").strip().lower()
        items = [s for s in list(self.suggestions or []) if text in s.lower()]
        return items[: int(self.max_suggestions or 8)]

    def _render_view(self):
        view = self.dom_nodes["m3x-search-view"]
        view.innerHTML = ""
        self._shown = self._matches()
        doc = window.document
        for i, suggestion in enumerate(self._shown):
            item = doc.createElement("div")
            item.className = "m3x-search-item"
            item.id = f"{self._id}-item-{i}"
            item.setAttribute("role", "option")
            item.setAttribute("data-index", str(i))
            item.setAttribute("aria-selected", "true" if i == self._active else "false")
            if i == self._active:
                item.classList.add("m3x-search-item-active")
            icon = doc.createElement("i")
            icon.className = "material-symbols-outlined m3x-search-item-icon"
            icon.setAttribute("aria-hidden", "true")
            icon.innerText = "search"
            label = doc.createElement("span")
            label.innerText = suggestion
            item.appendChild(icon)
            item.appendChild(label)
            view.appendChild(item)
        has_items = bool(self._shown) and self._open
        self.dom_nodes["m3x-search"].classList.toggle(
            "m3x-search-has-items", has_items)
        input_node = self.dom_nodes["m3x-search-input"]
        input_node.setAttribute("aria-expanded", "true" if has_items else "false")
        if 0 <= self._active < len(self._shown):
            input_node.setAttribute("aria-activedescendant",
                                    f"{self._id}-item-{self._active}")
        else:
            input_node.removeAttribute("aria-activedescendant")

    def _open_view(self):
        if not self.enabled or self._open:
            return
        self._open = True
        self._active = -1
        self.dom_nodes["m3x-search"].classList.add("m3x-search-open")
        window.document.addEventListener("pointerdown", self._outside, True)
        self._render_view()

    def _close_view(self):
        if not self._open:
            return
        self._open = False
        self._active = -1
        self.dom_nodes["m3x-search"].classList.remove("m3x-search-open")
        window.document.removeEventListener("pointerdown", self._outside, True)
        self._render_view()
        self.dom_nodes["m3x-search-input"].blur()

    def _on_document_pointer(self, event):
        if not self.dom_nodes["m3x-search"].contains(event.target):
            self._close_view()

    # ---- interaction ---------------------------------------------------------

    def _update_clear(self):
        self.dom_nodes["m3x-search"].classList.toggle(
            "m3x-search-has-text", bool(self.text))

    def _on_input(self, event):
        self._props["text"] = self.dom_nodes["m3x-search-input"].value
        self._active = -1
        self._update_clear()
        if not self._open:
            self._open_view()
        else:
            self._render_view()
        self.raise_event("change")

    def _on_clear(self, event):
        self.text = ""
        self.raise_event("change")
        self.dom_nodes["m3x-search-input"].focus()
        self._render_view()

    def _search(self, query):
        self.text = query
        self._close_view()
        self.raise_event("search", query=query)

    def _on_key(self, event):
        key = event.key
        if key == "Escape":
            event.preventDefault()
            self._close_view()
        elif key in ("ArrowDown", "ArrowUp") and self._shown:
            event.preventDefault()
            if not self._open:
                self._open_view()
            step = 1 if key == "ArrowDown" else -1
            self._active = (self._active + step) % len(self._shown)
            self._render_view()
        elif key == "Enter":
            event.preventDefault()
            if 0 <= self._active < len(self._shown):
                self._search(self._shown[self._active])
            else:
                self._search(self.text or "")

    def _on_view_click(self, event):
        item = event.target.closest("[data-index]")
        if item:
            self._search(self._shown[int(item.getAttribute("data-index"))])

    # ---- properties ----------------------------------------------------------

    @anvil_prop(default_value="")
    @property
    def text(self, value) -> str:
        """The text in the search bar."""
        self.dom_nodes["m3x-search-input"].value = value or ""
        self._update_clear()

    @anvil_prop(default_value="Search")
    @property
    def placeholder(self, value) -> str:
        """The text shown in the empty search bar."""
        node = self.dom_nodes["m3x-search-input"]
        node.placeholder = value or ""
        node.setAttribute("aria-label", value or "Search")

    @anvil_prop(default_value=[])
    @property
    def suggestions(self, value) -> list:
        """Suggestions shown below the bar while the user types."""
        if self._open:
            self._render_view()

    @anvil_prop(default_value=8)
    @property
    def max_suggestions(self, value) -> int:
        """The largest number of suggestions shown at once."""

    @anvil_prop(default_value=True)
    @property
    def enabled(self, value) -> bool:
        """If True, the user can type in the search bar."""
        self.dom_nodes["m3x-search-input"].disabled = not value
        self.dom_nodes["m3x-search"].classList.toggle("m3x-search-disabled", not value)

    def focus(self):
        """Put the keyboard focus in the search bar."""
        self.dom_nodes["m3x-search-input"].focus()

    visible = HtmlTemplate.visible
    role = role_property("m3x-search")

    #!componentEvent(m3.SearchBar)!1: {name: "search", description: "When the user presses Enter or chooses a suggestion.", parameters:[{name: "query", description: "The text searched for."}]}
    #!componentEvent(m3.SearchBar)!1: {name: "change", description: "When the user changes the text."}
    #!componentEvent(m3.SearchBar)!1: {name: "show", description: "When the search bar is shown on the screen."}
    #!componentEvent(m3.SearchBar)!1: {name: "hide", description: "When the search bar is removed from the screen."}

    #!componentProp(m3.SearchBar)!1: {name:"text",type:"string",description:"The text in the search bar."}
    #!componentProp(m3.SearchBar)!1: {name:"placeholder",type:"string",description:"The text shown in the empty search bar."}
    #!componentProp(m3.SearchBar)!1: {name:"suggestions",type:"text[]",description:"Suggestions shown below the bar while the user types."}
    #!componentProp(m3.SearchBar)!1: {name:"max_suggestions",type:"number",description:"The largest number of suggestions shown at once."}
    #!componentProp(m3.SearchBar)!1: {name:"enabled",type:"boolean",description:"If True, the user can type in the search bar."}
    #!componentProp(m3.SearchBar)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.SearchBar)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.SearchBar)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, SearchBar, anvil.Component)!:
