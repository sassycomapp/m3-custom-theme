"""M3 rich tooltip: a small card with an optional subhead, supporting text and
an optional action, attached to any component.
See docs/components/RichTooltip.md in the project library.

The plain M3 tooltip is the base theme's tooltip property, which every base
component has. The rich tooltip is attached in code:

    m3.RichTooltip("Text", subhead="Title", action_text="Learn more",
                   on_action=open_help).attach(self.button_1)

A rich tooltip without persistent appears while the pointer rests on the
component or the component has keyboard focus. A persistent rich tooltip opens
when the component is clicked and stays until the user clicks elsewhere,
presses Escape or uses the action.
"""
from anvil.js import get_dom_node, window

from . import fui

_SHOW_DELAY_MS = 500
_HIDE_DELAY_MS = 150
_counter = [0]


class RichTooltip:
    def __init__(self, text, subhead=None, action_text=None, on_action=None,
                 persistent=False):
        self.text = text
        self.subhead = subhead
        self.action_text = action_text
        self.on_action = on_action
        self.persistent = persistent
        self._anchor = None
        self._node = None
        self._cleanup = None
        self._timer = None
        self._listeners = []

    # ---- attaching -----------------------------------------------------------

    def attach(self, component):
        """Attach the tooltip to a component. Returns the tooltip."""
        self.detach()
        anchor = get_dom_node(component)
        self._anchor = anchor
        _counter[0] += 1
        self._id = f"m3x-rich-tooltip-{_counter[0]}"
        # Capture phase: base components such as Button stop the click from
        # reaching their outer element, so the tooltip listens on the way in.
        if self.persistent:
            self._listen(anchor, "click", self._on_anchor_click, True)
            anchor.setAttribute("aria-haspopup", "dialog")
        else:
            for event in ("mouseenter", "focusin"):
                self._listen(anchor, event, lambda e: self._show_later())
            for event in ("mouseleave", "focusout"):
                self._listen(anchor, event, lambda e: self._hide_later())
            anchor.setAttribute("aria-describedby", self._id)
        return self

    def detach(self):
        """Remove the tooltip from its component."""
        self.hide()
        for node, event, handler, capture in self._listeners:
            node.removeEventListener(event, handler, capture)
        self._listeners = []
        if self._anchor is not None:
            self._anchor.removeAttribute("aria-describedby")
            self._anchor.removeAttribute("aria-haspopup")
            self._anchor = None

    def _listen(self, node, event, handler, capture=False):
        node.addEventListener(event, handler, capture)
        self._listeners.append((node, event, handler, capture))

    # ---- showing -------------------------------------------------------------

    def _clear_timer(self):
        if self._timer is not None:
            window.clearTimeout(self._timer)
            self._timer = None

    def _show_later(self):
        self._clear_timer()
        if self._node is None:
            self._timer = window.setTimeout(lambda: self.show(), _SHOW_DELAY_MS)

    def _hide_later(self):
        self._clear_timer()
        self._timer = window.setTimeout(lambda: self.hide(), _HIDE_DELAY_MS)

    def show(self):
        """Show the tooltip now."""
        self._clear_timer()
        if self._node is not None or self._anchor is None:
            return
        doc = window.document
        node = doc.createElement("div")
        node.className = "m3x-rich-tooltip"
        node.id = self._id
        node.setAttribute("role", "dialog" if self.persistent else "tooltip")
        if self.subhead:
            head = doc.createElement("div")
            head.className = "m3x-rich-tooltip-subhead"
            head.innerText = self.subhead
            node.appendChild(head)
        body = doc.createElement("div")
        body.className = "m3x-rich-tooltip-text"
        body.innerText = self.text
        node.appendChild(body)
        if self.action_text:
            actions = doc.createElement("div")
            actions.className = "m3x-rich-tooltip-actions"
            button = doc.createElement("button")
            button.type = "button"
            button.className = "m3x-rich-tooltip-action"
            button.innerText = self.action_text
            button.addEventListener("click", self._on_action_click)
            actions.appendChild(button)
            node.appendChild(actions)
        if not self.persistent:
            # The pointer may move onto the tooltip, for example to its action.
            node.addEventListener("mouseenter", lambda e: self._clear_timer())
            node.addEventListener("mouseleave", lambda e: self._hide_later())
        doc.body.appendChild(node)
        self._node = node
        self._cleanup = fui.auto_update(self._anchor, node, placement="bottom-start")
        window.requestAnimationFrame(
            lambda t: node.classList.add("m3x-rich-tooltip-shown"))
        if self.persistent:
            self._outside = self._on_document_pointer
            self._escape = self._on_document_key
            doc.addEventListener("pointerdown", self._outside, True)
            doc.addEventListener("keydown", self._escape, True)

    def hide(self):
        """Hide the tooltip now."""
        self._clear_timer()
        if self._node is None:
            return
        if self._cleanup is not None:
            self._cleanup()
            self._cleanup = None
        self._node.remove()
        self._node = None
        if self.persistent:
            window.document.removeEventListener("pointerdown", self._outside, True)
            window.document.removeEventListener("keydown", self._escape, True)

    # ---- events --------------------------------------------------------------

    def _on_anchor_click(self, event):
        if self._node is None:
            self.show()
        else:
            self.hide()

    def _on_document_pointer(self, event):
        inside = self._node is not None and self._node.contains(event.target)
        on_anchor = self._anchor is not None and self._anchor.contains(event.target)
        if not inside and not on_anchor:
            self.hide()

    def _on_document_key(self, event):
        if event.key == "Escape":
            self.hide()
            if self._anchor is not None:
                self._anchor.focus()

    def _on_action_click(self, event):
        self.hide()
        if self.on_action is not None:
            self.on_action()
