"""M3 bottom sheet: a surface that slides up from the bottom of the screen and
holds any components.
See docs/components/BottomSheet.md in the project library.

Put a BottomSheet on a form in the designer and add components to it. It takes
no space on the page. Call open() to show it and close() to hide it.

A modal sheet (modal=True) covers the page with a scrim. A standard sheet
(modal=False) leaves the page usable.
"""
from anvil import HtmlTemplate
from anvil.designer import in_designer
from anvil.js import window

from ..._utils.properties import ComponentTag, anvil_prop, role_property
from ._anvil_designer import BottomSheetTemplate

_SLOT = "bottom-sheet-content-slot"
_EXIT_MS = 250  # Slightly longer than the exit transition (short4, 200 ms).
_DISMISS_SHARE = 0.25  # Dragged down by a quarter of its height: the sheet closes.
_DISMISS_SPEED = 0.5  # Or flicked down faster than 0.5 px per ms.
_FOCUSABLE = ('a[href], button:not([disabled]), input:not([disabled]), '
              'select:not([disabled]), textarea:not([disabled]), '
              '[tabindex]:not([tabindex="-1"])')


class BottomSheet(BottomSheetTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._open = False
        self._timer = None
        self._return_focus = None
        self._drag = None
        self._ignore_click = False
        self._body_overflow = ""
        self.init_components(**properties)
        nodes = self.dom_nodes
        self._host = nodes["m3x-bottom-sheet-host"]
        self._sheet = nodes["m3x-bottom-sheet"]
        self._handle = nodes["m3x-bottom-sheet-handle"]
        self._home = self._host.parentElement
        if in_designer:
            # In the designer the sheet is drawn in place so components can be
            # dropped into it.
            self._host.classList.add("m3x-bottom-sheet-in-designer")
        nodes["m3x-bottom-sheet-scrim"].addEventListener("click", self._on_scrim)
        self._handle.addEventListener("click", self._on_handle_click)
        self._handle.addEventListener("pointerdown", self._on_drag_start)
        self._move_handler = self._on_drag_move
        self._up_handler = self._on_drag_end
        self._key_handler = self._on_key
        # A sheet left open on the page body is removed when the form goes away.
        self.add_event_handler("x-anvil-page-removed", lambda **e: self._finish_close())

    def add_component(self, component, slot=_SLOT, **layout_props):
        """Add a component to the sheet."""
        super().add_component(component, slot=slot, **layout_props)

    # ---- opening and closing -------------------------------------------------

    @property
    def is_open(self):
        """True while the sheet is open."""
        return self._open

    def open(self):
        """Slide the sheet up from the bottom of the screen."""
        if self._open or in_designer:
            return
        self._open = True
        window.clearTimeout(self._timer)
        self._return_focus = window.document.activeElement
        # The sheet is drawn on the page body, outside Anvil's containers, which
        # cut off anything that reaches outside a component.
        window.document.body.appendChild(self._host)
        self._sheet.style.removeProperty("--m3x-bottom-sheet-drag")
        self._host.classList.add("m3x-bottom-sheet-open")
        self._host.offsetHeight  # Start the slide from below the screen.
        self._host.classList.add("m3x-bottom-sheet-shown")
        if self.modal:
            self._body_overflow = window.document.body.style.overflow
            window.document.body.style.overflow = "hidden"
        window.document.addEventListener("keydown", self._key_handler, True)
        self._sheet.focus({"preventScroll": True})
        self.raise_event("opened")

    def close(self):
        """Slide the sheet down and hide it."""
        if not self._open:
            return
        self._open = False
        self._host.classList.remove("m3x-bottom-sheet-shown")
        window.document.removeEventListener("keydown", self._key_handler, True)
        if self.modal:
            window.document.body.style.overflow = self._body_overflow
        window.clearTimeout(self._timer)
        self._timer = window.setTimeout(self._finish_close, _EXIT_MS)
        if self.modal and self._return_focus:
            try:
                self._return_focus.focus({"preventScroll": True})
            except Exception:
                pass
        self.raise_event("closed")

    def _finish_close(self, *args):
        if self._open:
            # The form was removed while the sheet was open.
            self._open = False
            window.document.removeEventListener("keydown", self._key_handler, True)
            if self.modal:
                window.document.body.style.overflow = self._body_overflow
        self._host.classList.remove("m3x-bottom-sheet-open", "m3x-bottom-sheet-shown")
        self._sheet.style.removeProperty("--m3x-bottom-sheet-drag")
        if not self._home.isSameNode(self._host.parentElement):
            self._home.appendChild(self._host)

    # ---- user actions --------------------------------------------------------

    def _on_scrim(self, event):
        if self.dismissible:
            self.close()

    def _on_handle_click(self, event):
        if self._ignore_click:
            self._ignore_click = False
            return
        if self.dismissible:
            self.close()

    def _on_key(self, event):
        if event.key == "Escape" and self.dismissible:
            event.stopPropagation()
            self.close()
        elif event.key == "Tab" and self.modal:
            self._keep_focus_inside(event)

    def _keep_focus_inside(self, event):
        nodes = [n for n in self._sheet.querySelectorAll(_FOCUSABLE)
                 if n.offsetParent is not None]
        if not nodes:
            event.preventDefault()
            return
        first, last = nodes[0], nodes[-1]
        active = window.document.activeElement
        inside = self._sheet.contains(active)
        at_first = first.isSameNode(active) or self._sheet.isSameNode(active)
        if event.shiftKey and (at_first or not inside):
            event.preventDefault()
            last.focus()
        elif not event.shiftKey and (last.isSameNode(active) or not inside):
            event.preventDefault()
            first.focus()

    # ---- dragging the sheet down ---------------------------------------------

    def _on_drag_start(self, event):
        if not self._open or not self.dismissible or event.button != 0:
            return
        self._drag = {"start": event.clientY, "y": event.clientY,
                      "t": event.timeStamp, "speed": 0, "moved": False}
        self._handle.setPointerCapture(event.pointerId)
        self._host.classList.add("m3x-bottom-sheet-dragging")
        window.addEventListener("pointermove", self._move_handler)
        window.addEventListener("pointerup", self._up_handler)
        window.addEventListener("pointercancel", self._up_handler)

    def _on_drag_move(self, event):
        drag = self._drag
        if not drag:
            return
        distance = max(0, event.clientY - drag["start"])
        if distance > 4:
            drag["moved"] = True
        elapsed = event.timeStamp - drag["t"]
        if elapsed > 0:
            drag["speed"] = (event.clientY - drag["y"]) / elapsed
        drag["y"], drag["t"] = event.clientY, event.timeStamp
        self._sheet.style.setProperty("--m3x-bottom-sheet-drag", f"{distance}px")

    def _on_drag_end(self, event):
        drag = self._drag
        self._drag = None
        window.removeEventListener("pointermove", self._move_handler)
        window.removeEventListener("pointerup", self._up_handler)
        window.removeEventListener("pointercancel", self._up_handler)
        self._host.classList.remove("m3x-bottom-sheet-dragging")
        if not drag or not drag["moved"]:
            return
        self._ignore_click = True  # The click that ends a drag does not close.
        distance = max(0, drag["y"] - drag["start"])
        far = distance > self._sheet.offsetHeight * _DISMISS_SHARE
        if far or drag["speed"] > _DISMISS_SPEED:
            self.close()
        else:
            self._sheet.style.removeProperty("--m3x-bottom-sheet-drag")

    # ---- properties ----------------------------------------------------------

    @anvil_prop(default_value=True)
    @property
    def modal(self, value) -> bool:
        """If True, a scrim covers the page while the sheet is open."""
        nodes = self.dom_nodes  # Set before __init__ has named the nodes.
        nodes["m3x-bottom-sheet-host"].classList.toggle("m3x-bottom-sheet-modal",
                                                        bool(value))
        nodes["m3x-bottom-sheet"].setAttribute("aria-modal",
                                               "true" if value else "false")

    @anvil_prop(default_value=True)
    @property
    def dismissible(self, value) -> bool:
        """If True, the user can close the sheet."""
        nodes = self.dom_nodes
        nodes["m3x-bottom-sheet-handle"].disabled = not value
        nodes["m3x-bottom-sheet-host"].classList.toggle("m3x-bottom-sheet-fixed",
                                                        not value)

    @anvil_prop(default_value=True)
    @property
    def show_drag_handle(self, value) -> bool:
        """If True, a drag handle is shown at the top of the sheet."""
        self.dom_nodes["m3x-bottom-sheet-host"].classList.toggle(
            "m3x-bottom-sheet-no-handle", not value)

    @anvil_prop(default_value="Sheet")
    @property
    def label(self, value) -> str:
        """A name for the sheet that screen readers announce."""
        self.dom_nodes["m3x-bottom-sheet"].setAttribute("aria-label",
                                                        value or "Sheet")

    visible = HtmlTemplate.visible
    role = role_property("m3x-bottom-sheet")

    #!componentEvent(m3.BottomSheet)!1: {name: "opened", description: "When the sheet has opened."}
    #!componentEvent(m3.BottomSheet)!1: {name: "closed", description: "When the sheet has closed."}
    #!componentEvent(m3.BottomSheet)!1: {name: "show", description: "When the component is shown on the screen."}
    #!componentEvent(m3.BottomSheet)!1: {name: "hide", description: "When the component is removed from the screen."}

    #!componentProp(m3.BottomSheet)!1: {name:"modal",type:"boolean",description:"If True, a scrim covers the page while the sheet is open."}
    #!componentProp(m3.BottomSheet)!1: {name:"dismissible",type:"boolean",description:"If True, the user can close the sheet."}
    #!componentProp(m3.BottomSheet)!1: {name:"show_drag_handle",type:"boolean",description:"If True, a drag handle is shown at the top of the sheet."}
    #!componentProp(m3.BottomSheet)!1: {name:"label",type:"string",description:"A name for the sheet that screen readers announce."}
    #!componentProp(m3.BottomSheet)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.BottomSheet)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.BottomSheet)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, BottomSheet, anvil.Component)!:
