"""M3 time picker: a text field with a clock dial dialog.
See docs/components/TimePicker.md in the project library.
"""
import datetime
import re
from math import atan2, cos, hypot, pi, sin

from anvil import HtmlTemplate
from anvil.js import window

from ..._utils import m3x_picker
from ..._utils.properties import ComponentTag, anvil_prop, role_property
from ._anvil_designer import TimePickerTemplate

_SVG_NS = "http://www.w3.org/2000/svg"
# Dial geometry (Compose TimePicker): 256 px dial, labels and the 48 px
# selector on an outer ring of radius 101 px and, for 24-hour hours, an inner
# ring of radius 69 px.
_SIZE = 256
_CENTRE = 128
_OUTER = 101
_INNER = 69

_PANEL_HTML = (
    '<div class="m3x-time-picker-panel">'
    '<div class="m3x-time-picker-supporting">Select time</div>'
    '<div class="m3x-time-picker-selectors">'
    '<input anvil-name="hour" class="m3x-time-picker-box" inputmode="numeric"'
    ' maxlength="2" aria-label="Hour" readonly>'
    '<span class="m3x-time-picker-separator">:</span>'
    '<input anvil-name="minute" class="m3x-time-picker-box" inputmode="numeric"'
    ' maxlength="2" aria-label="Minute" readonly>'
    '<div anvil-name="period" class="m3x-time-picker-period" role="group"'
    ' aria-label="AM or PM">'
    '<button type="button" data-period="am">AM</button>'
    '<button type="button" data-period="pm">PM</button></div></div>'
    '<div anvil-name="dial" class="m3x-time-picker-dial" tabindex="0"'
    ' role="slider"></div>'
    '<button anvil-name="mode" type="button" class="m3x-time-picker-mode">'
    '<i class="material-symbols-outlined" aria-hidden="true"></i></button></div>'
)


class TimePicker(m3x_picker.PickerFieldMixin, TimePickerTemplate):
    _ICON = "mi:schedule"
    _ICON_LABEL = "Choose a time on a clock"
    _DIALOG_CLASS = "m3x-time-picker-dialog"

    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._value = None
        self._field = None
        self.init_components(**properties)
        self._setup_field()
        for name in m3x_picker.FIELD_PROPERTIES:
            m3x_picker.apply_field_property(self, name, getattr(self, name))
        self._value = self._clean(self._props.get("time"))
        self._show_value()

    # ---- format --------------------------------------------------------------

    @property
    def _HINT(self):
        return "HH:MM" if self.format_24h else "H:MM AM"

    @property
    def _ERROR(self):
        return f"Enter a time as {self._HINT}."

    def _format(self, value):
        if self.format_24h:
            return f"{value.hour:02d}:{value.minute:02d}"
        hour = value.hour % 12 or 12
        return f"{hour}:{value.minute:02d} {'AM' if value.hour < 12 else 'PM'}"

    def _parse(self, text):
        pattern = r"^\s*(\d{1,2})\s*[:.h]?\s*(\d{2})\s*([AaPp])?\.?[Mm]?\.?\s*$"
        match = re.match(pattern, text)
        if not match:
            return None
        hour, minute = int(match.group(1)), int(match.group(2))
        period = (match.group(3) or "").lower()
        if period:
            if not 1 <= hour <= 12:
                return None
            hour = hour % 12 + (12 if period == "p" else 0)
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            return None
        return datetime.time(hour, minute)

    def _clean(self, value):
        if isinstance(value, datetime.datetime):
            return value.time().replace(second=0, microsecond=0)
        if isinstance(value, datetime.time):
            return value.replace(second=0, microsecond=0)
        return None

    # ---- dialog --------------------------------------------------------------

    def _build_dialog_content(self, dialog):
        now = datetime.datetime.now()
        self._pending = self._value or datetime.time(now.hour, now.minute)
        self._unit = "hour"
        self._typing = False
        self._dragging = False
        panel = HtmlTemplate(html=_PANEL_HTML)
        self._panel = panel
        nodes = panel.dom_nodes
        nodes["period"].style.display = "none" if self.format_24h else ""
        for unit in ("hour", "minute"):
            box = nodes[unit]
            box.addEventListener("click", lambda e, u=unit: self._choose_unit(u))
            box.addEventListener("input", lambda e, u=unit: self._on_typed(u))
        nodes["period"].addEventListener("click", self._on_period_click)
        nodes["mode"].addEventListener("click", lambda e: self._toggle_typing())
        dial = nodes["dial"]
        dial.addEventListener("pointerdown", self._on_pointer_down)
        dial.addEventListener("pointermove", self._on_pointer_move)
        dial.addEventListener("pointerup", self._on_pointer_up)
        dial.addEventListener("keydown", self._on_dial_key)
        self._render()
        return panel

    def _render(self, skip=None):
        """Redraw the dialog. skip names a box the user is typing in, which keeps
        its text."""
        nodes = self._panel.dom_nodes
        value = self._pending
        hour = value.hour if self.format_24h else (value.hour % 12 or 12)
        for unit, number in (("hour", hour), ("minute", value.minute)):
            box = nodes[unit]
            padded = unit == "minute" or self.format_24h
            if unit != skip:
                box.value = f"{number:02d}" if padded else str(number)
            box.classList.toggle("m3x-time-picker-selected",
                                 unit == self._unit and not self._typing)
            if self._typing:
                box.removeAttribute("readonly")
            else:
                box.setAttribute("readonly", "")
        nodes["hour"].parentElement.classList.toggle(
            "m3x-time-picker-24h", bool(self.format_24h))
        for button in nodes["period"].querySelectorAll("button"):
            pm = button.getAttribute("data-period") == "pm"
            selected = pm == (value.hour >= 12)
            button.classList.toggle("m3x-time-picker-selected", selected)
            button.setAttribute("aria-pressed", "true" if selected else "false")
        icon = nodes["mode"].querySelector("i")
        icon.innerText = "schedule" if self._typing else "keyboard"
        nodes["mode"].setAttribute(
            "aria-label", "Choose on the clock" if self._typing else "Type the time")
        dial = nodes["dial"]
        dial.style.display = "none" if self._typing else ""
        if not self._typing:
            self._draw_dial(dial)

    def _draw_dial(self, dial):
        doc = window.document
        dial.innerHTML = ""
        svg = doc.createElementNS(_SVG_NS, "svg")
        svg.setAttribute("viewBox", f"0 0 {_SIZE} {_SIZE}")
        svg.setAttribute("class", "m3x-time-picker-dial-svg")
        svg.setAttribute("aria-hidden", "true")
        value = self._pending
        if self._unit == "hour":
            current = value.hour if self.format_24h else value.hour % 12
            labels = self._hour_labels()
            count = 12
            selected_index = current % 12
            radius = _INNER if (self.format_24h and current >= 12) else _OUTER
            dial.setAttribute("aria-label", "Hour")
            dial.setAttribute("aria-valuenow", str(value.hour))
        else:
            labels = [(i * 5, f"{i * 5:02d}", _OUTER) for i in range(12)]
            count = 60
            selected_index = value.minute
            radius = _OUTER
            dial.setAttribute("aria-label", "Minute")
            dial.setAttribute("aria-valuenow", str(value.minute))
        angle = 2 * pi * selected_index / count
        x = _CENTRE + radius * sin(angle)
        y = _CENTRE - radius * cos(angle)
        line = doc.createElementNS(_SVG_NS, "line")
        for name, val in (("x1", _CENTRE), ("y1", _CENTRE), ("x2", x), ("y2", y)):
            line.setAttribute(name, f"{val:.1f}")
        line.setAttribute("class", "m3x-time-picker-hand")
        svg.appendChild(line)
        for cls, r, cx, cy in (("m3x-time-picker-centre", 4, _CENTRE, _CENTRE),
                               ("m3x-time-picker-handle", 24, x, y)):
            circle = doc.createElementNS(_SVG_NS, "circle")
            circle.setAttribute("cx", f"{cx:.1f}")
            circle.setAttribute("cy", f"{cy:.1f}")
            circle.setAttribute("r", str(r))
            circle.setAttribute("class", cls)
            svg.appendChild(circle)
        for number, text, ring in labels:
            position = number % 12 if self._unit == "hour" else number
            a = 2 * pi * position / count
            label = doc.createElementNS(_SVG_NS, "text")
            label.setAttribute("x", f"{_CENTRE + ring * sin(a):.1f}")
            label.setAttribute("y", f"{_CENTRE - ring * cos(a):.1f}")
            label.setAttribute("class", "m3x-time-picker-label")
            if hypot(_CENTRE + ring * sin(a) - x, _CENTRE - ring * cos(a) - y) < 1:
                label.classList.add("m3x-time-picker-label-selected")
            label.textContent = text
            svg.appendChild(label)
        dial.appendChild(svg)

    def _hour_labels(self):
        if self.format_24h:
            outer = [(h, f"{h:02d}", _OUTER) for h in range(12)]
            inner = [(h, f"{h:02d}", _INNER) for h in range(12, 24)]
            return outer + inner
        return [(h, str(h or 12), _OUTER) for h in range(12)]

    # ---- interaction ---------------------------------------------------------

    def _choose_unit(self, unit):
        if self._typing:
            return
        self._unit = unit
        self._render()

    def _pick(self, event):
        rect = self._panel.dom_nodes["dial"].getBoundingClientRect()
        scale = _SIZE / rect.width
        dx = (event.clientX - rect.left) * scale - _CENTRE
        dy = (event.clientY - rect.top) * scale - _CENTRE
        angle = atan2(dx, -dy) % (2 * pi)
        value = self._pending
        if self._unit == "hour":
            step = round(angle / (2 * pi) * 12) % 12
            if self.format_24h:
                inner = hypot(dx, dy) < (_OUTER + _INNER) / 2
                hour = step + 12 if inner else step
            else:
                hour = step + (12 if value.hour >= 12 else 0)
            self._pending = value.replace(hour=hour)
        else:
            self._pending = value.replace(minute=round(angle / (2 * pi) * 60) % 60)
        self._render()

    def _on_pointer_down(self, event):
        self._dragging = True
        self._panel.dom_nodes["dial"].setPointerCapture(event.pointerId)
        self._pick(event)

    def _on_pointer_move(self, event):
        if self._dragging:
            self._pick(event)

    def _on_pointer_up(self, event):
        if not self._dragging:
            return
        self._dragging = False
        self._pick(event)
        if self._unit == "hour":
            # M3: choosing the hour moves on to the minutes.
            self._unit = "minute"
            self._render()

    def _on_dial_key(self, event):
        steps = {"ArrowUp": 1, "ArrowRight": 1, "ArrowDown": -1, "ArrowLeft": -1}
        if event.key not in steps:
            return
        event.preventDefault()
        value = self._pending
        if self._unit == "hour":
            self._pending = value.replace(hour=(value.hour + steps[event.key]) % 24)
        else:
            self._pending = value.replace(
                minute=(value.minute + steps[event.key]) % 60)
        self._render()

    def _on_period_click(self, event):
        button = event.target.closest("[data-period]")
        if not button:
            return
        pm = button.getAttribute("data-period") == "pm"
        hour = self._pending.hour % 12 + (12 if pm else 0)
        self._pending = self._pending.replace(hour=hour)
        self._render()

    def _toggle_typing(self):
        self._typing = not self._typing
        self._render()
        if self._typing:
            self._panel.dom_nodes["hour"].focus()

    def _on_typed(self, unit):
        box = self._panel.dom_nodes[unit]
        text = (box.value or "").strip()
        if not text.isdigit():
            box.classList.add("m3x-time-picker-error")
            return
        number = int(text)
        value = self._pending
        if unit == "minute":
            ok = 0 <= number <= 59
            if ok:
                self._pending = value.replace(minute=number)
        elif self.format_24h:
            ok = 0 <= number <= 23
            if ok:
                self._pending = value.replace(hour=number)
        else:
            ok = 1 <= number <= 12
            if ok:
                pm = value.hour >= 12
                self._pending = value.replace(hour=number % 12 + (12 if pm else 0))
        box.classList.toggle("m3x-time-picker-error", not ok)
        self._render(skip=unit)

    # ---- properties ----------------------------------------------------------

    def _get_time(self):
        return self._value

    def _set_time(self, value):
        self._value = self._clean(value)
        self._props["time"] = self._value
        self._show_value()

    time = property(_get_time, _set_time)

    def _store(self, value):
        self._props["time"] = value
        super()._store(value)

    @anvil_prop(default_value="Time")
    @property
    def label(self, value) -> str:
        """The label of the field."""
        m3x_picker.apply_field_property(self, "label", value)

    @anvil_prop(default_value="outlined")
    @property
    def appearance(self, value) -> str:
        """filled or outlined."""
        m3x_picker.apply_field_property(self, "appearance", value)

    @anvil_prop(default_value="")
    @property
    def supporting_text(self, value) -> str:
        """A line of help text below the field."""
        m3x_picker.apply_field_property(self, "supporting_text", value)

    @anvil_prop(default_value=True)
    @property
    def enabled(self, value) -> bool:
        """If True, the time can be changed."""
        m3x_picker.apply_field_property(self, "enabled", value)

    @anvil_prop(default_value=True)
    @property
    def format_24h(self, value) -> bool:
        """If True, the 24-hour clock; if False, the 12-hour clock with AM and PM."""
        self._show_value()

    visible = HtmlTemplate.visible
    role = role_property("m3x-time-picker")

    #!componentEvent(m3.TimePicker)!1: {name: "change", description: "When the user changes the time."}
    #!componentEvent(m3.TimePicker)!1: {name: "show", description: "When the time picker is shown on the screen."}
    #!componentEvent(m3.TimePicker)!1: {name: "hide", description: "When the time picker is removed from the screen."}

    #!componentProp(m3.TimePicker)!1: {name:"time",type:"object",description:"The chosen time, as a datetime.time. None when empty."}
    #!componentProp(m3.TimePicker)!1: {name:"label",type:"string",description:"The label of the field."}
    #!componentProp(m3.TimePicker)!1: {name:"format_24h",type:"boolean",description:"If True, the 24-hour clock; if False, the 12-hour clock with AM and PM."}
    #!componentProp(m3.TimePicker)!1: {name:"appearance",type:"enum",options:["filled", "outlined"],description:"The look of the field."}
    #!componentProp(m3.TimePicker)!1: {name:"supporting_text",type:"string",description:"A line of help text below the field."}
    #!componentProp(m3.TimePicker)!1: {name:"enabled",type:"boolean",description:"If True, the time can be changed."}
    #!componentProp(m3.TimePicker)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.TimePicker)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.TimePicker)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, TimePicker, anvil.Component)!:
