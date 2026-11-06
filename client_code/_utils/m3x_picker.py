"""The text field shared by the m3x DatePicker and TimePicker.
See docs/components/DatePicker.md and docs/components/TimePicker.md in the
project library.

Each picker is an M3 text field with an icon at its end. The user either types
the value into the field, or clicks the icon to choose it in a dialog. A typed
value is checked when the user presses Enter or leaves the field: a value that
cannot be read puts the field into its error state and keeps the last good value.
"""
from anvil.js import window

from .._Components.Button import Button
from .._Components.Dialog import Dialog
from .._Components.TextInput.TextBox import TextBox

FIELD_PROPERTIES = ("label", "appearance", "supporting_text", "enabled")


class PickerFieldMixin:
    """Mixed into DatePicker and TimePicker. The class sets _ICON, _HINT and
    _ERROR, and defines _format(value), _parse(text) and _build_dialog_content()."""

    def _setup_field(self):
        self._field = TextBox(trailing_icon=self._ICON, appearance="outlined")
        self._field.add_event_handler("trailing_icon_click", self._on_icon_click)
        self._field.add_event_handler("pressed_enter", self._on_commit)
        self._field.add_event_handler("lost_focus", self._on_commit)
        self.add_component(self._field, slot="default")
        icon = self._field.dom_nodes["anvil-m3-trailing-icon"]
        icon.setAttribute("role", "button")
        icon.setAttribute("tabindex", "0")
        icon.setAttribute("aria-label", self._ICON_LABEL)
        icon.style.cursor = "pointer"
        icon.addEventListener("keydown", self._on_icon_key)

    # ---- field ---------------------------------------------------------------

    def _show_value(self):
        if getattr(self, "_field", None) is None:
            return
        self._field.text = self._format(self._value) if self._value else ""
        self._field.placeholder = f"e.g. {self._HINT}"
        self._set_error(False)

    def _set_error(self, on):
        self._field.error = on
        normal = self.supporting_text or ""
        self._field.supporting_text = self._ERROR if on else normal

    def _on_commit(self, **event_args):
        text = (self._field.text or "").strip()
        if not text:
            self._store(None)
            return
        value = self._parse(text)
        if value is None or not self._allowed(value):
            self._set_error(True)
            return
        self._store(value)

    def _store(self, value):
        changed = value != self._value
        self._value = value
        self._show_value()
        if changed:
            self.raise_event("change")

    def _allowed(self, value):
        return True

    # ---- dialog --------------------------------------------------------------

    def _on_icon_key(self, event):
        if event.key in ("Enter", " "):
            event.preventDefault()
            self._on_icon_click()

    def _on_icon_click(self, **event_args):
        if not self.enabled:
            return
        dialog = Dialog()
        content = self._build_dialog_content(dialog)
        dialog.add_component(content)
        dialog.add_action("Cancel", value=None)
        # OK returns the value chosen in the dialog, so it is a Button of its own.
        ok = Button(text="OK", appearance="text")
        ok.add_event_handler("click", lambda **e: dialog.close(self._pending))
        dialog.add_component(ok, slot="dialog-actions-slot")
        dialog.dom_nodes["m3x-dialog"].classList.add(self._DIALOG_CLASS)
        result = dialog.show()
        if result is not None:
            self._store(result)
        window.setTimeout(lambda: self._field.focus(), 0)


def apply_field_property(component, name, value):
    field = getattr(component, "_field", None)
    if field is None:
        return
    if name == "supporting_text":
        field.supporting_text = value or ""
    else:
        setattr(field, name, value)
