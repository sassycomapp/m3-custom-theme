"""M3 date picker: a text field with a calendar dialog.
See docs/components/DatePicker.md in the project library.
"""
import datetime
import re

from anvil import HtmlTemplate
from anvil.js import window

from ..._utils import m3x_picker
from ..._utils.properties import ComponentTag, anvil_prop, role_property
from ..TextInput.TextBox import TextBox
from ._anvil_designer import DatePickerTemplate

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
        "Sunday"]
_ICON_BUTTON = (
    '<button anvil-name="{name}" type="button" class="m3x-date-picker-icon-button"'
    ' aria-label="{label}"><i class="material-symbols-outlined" aria-hidden="true">'
    "{icon}</i></button>"
)
_PANEL_HTML = (
    '<div class="m3x-date-picker-panel">'
    '<div class="m3x-date-picker-supporting">Select date</div>'
    '<div class="m3x-date-picker-header">'
    '<div anvil-name="headline" class="m3x-date-picker-headline"></div>'
    + _ICON_BUTTON.format(name="mode", label="", icon="")
    + "</div>"
    '<div class="m3x-date-picker-divider"></div>'
    '<div anvil-name="nav" class="m3x-date-picker-nav">'
    '<button anvil-name="month-year" type="button"'
    ' class="m3x-date-picker-month-year"></button>'
    '<span class="m3x-date-picker-nav-space"></span>'
    + _ICON_BUTTON.format(name="previous", label="Previous month", icon="chevron_left")
    + _ICON_BUTTON.format(name="next", label="Next month", icon="chevron_right")
    + "</div>"
    '<div anvil-name="body" class="m3x-date-picker-body"></div>'
    '<div anvil-slot="input" class="m3x-date-picker-input"></div></div>'
)
_FIRST_YEAR = 1900
_LAST_YEAR = 2100


def _first_of_month(day):
    return datetime.date(day.year, day.month, 1)


def _add_months(day, months):
    index = day.year * 12 + day.month - 1 + months
    return datetime.date(index // 12, index % 12 + 1, 1)


def _days_in_month(day):
    return (_add_months(day, 1) - datetime.timedelta(days=1)).day


class DatePicker(m3x_picker.PickerFieldMixin, DatePickerTemplate):
    _ICON = "mi:calendar_today"
    _ICON_LABEL = "Choose a date in a calendar"
    _DIALOG_CLASS = "m3x-date-picker-dialog"

    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._value = None
        self._field = None
        self.init_components(**properties)
        self._setup_field()
        for name in m3x_picker.FIELD_PROPERTIES:
            m3x_picker.apply_field_property(self, name, getattr(self, name))
        self._value = self._clean(self._props.get("date"))
        self._show_value()

    # ---- format --------------------------------------------------------------

    @property
    def _HINT(self):
        """An example of a date as the field expects it: today's date."""
        return self._format(datetime.date.today())

    @property
    def _ERROR(self):
        low, high = self._clean(self.min_date), self._clean(self.max_date)
        message = f"Enter a date like {self._HINT}."
        if low and high:
            message += f" Choose from {self._format(low)} to {self._format(high)}."
        elif low:
            message += f" Choose {self._format(low)} or later."
        elif high:
            message += f" Choose {self._format(high)} or earlier."
        return message

    def _format(self, day):
        out = self.format or "%d/%m/%Y"
        for code, text in (("%d", f"{day.day:02d}"), ("%m", f"{day.month:02d}"),
                           ("%Y", f"{day.year:04d}"), ("%y", f"{day.year % 100:02d}"),
                           ("%B", MONTHS[day.month - 1]),
                           ("%b", MONTHS[day.month - 1][:3])):
            out = out.replace(code, text)
        return out

    def _parse(self, text):
        pattern, order = "", []
        fmt = self.format or "%d/%m/%Y"
        i = 0
        while i < len(fmt):
            if fmt[i] == "%" and i + 1 < len(fmt):
                code = fmt[i + 1]
                pattern += {"d": r"(\d{1,2})", "m": r"(\d{1,2})", "Y": r"(\d{4})",
                            "y": r"(\d{2})", "B": r"([A-Za-z]+)",
                            "b": r"([A-Za-z]+)"}.get(code, re.escape(fmt[i:i + 2]))
                if code in "dmYyBb":
                    order.append(code)
                i += 2
            else:
                pattern += r"\s*" if fmt[i] == " " else re.escape(fmt[i])
                i += 1
        match = re.match(r"^\s*" + pattern + r"\s*$", text)
        if not match:
            return None
        parts = dict(zip(order, match.groups()))
        try:
            year = int(parts["Y"]) if "Y" in parts else 2000 + int(parts["y"])
            if "m" in parts:
                month = int(parts["m"])
            else:
                name = parts.get("B") or parts.get("b") or ""
                month = [m[:3].lower() for m in MONTHS].index(name[:3].lower()) + 1
            return datetime.date(year, month, int(parts["d"]))
        except (KeyError, ValueError):
            return None

    def _clean(self, value):
        if isinstance(value, datetime.datetime):
            return value.date()
        return value if isinstance(value, datetime.date) else None

    def _in_range(self, month):
        """The month itself, or the nearest month that has allowed days."""
        low, high = self._clean(self.min_date), self._clean(self.max_date)
        if low and month.replace(day=_days_in_month(month)) < low:
            return _first_of_month(low)
        if high and month > high:
            return _first_of_month(high)
        return month

    def _allowed(self, day):
        low, high = self._clean(self.min_date), self._clean(self.max_date)
        return not ((low and day < low) or (high and day > high))

    # ---- dialog --------------------------------------------------------------

    def _build_dialog_content(self, dialog):
        today = datetime.date.today()
        start = self._value or today
        low, high = self._clean(self.min_date), self._clean(self.max_date)
        if low and start < low:
            start = low
        if high and start > high:
            start = high
        self._pending = self._value
        self._focus_day = start
        self._view = _first_of_month(start)
        self._mode = "calendar"
        panel = HtmlTemplate(html=_PANEL_HTML)
        self._panel = panel
        self._input = TextBox(appearance="outlined", label="Date",
                              placeholder=self._HINT)
        self._input.add_event_handler("change", self._on_input_change)
        panel.add_component(self._input, slot="input")
        nodes = panel.dom_nodes
        self._repeat_timer = None
        self._pointer_used = False
        for name, step in (("previous", -1), ("next", 1)):
            button = nodes[name]
            button.addEventListener(
                "pointerdown", lambda e, step=step: self._start_repeat(e, step))
            button.addEventListener("pointerup", lambda e: self._stop_repeat())
            for end in ("pointerleave", "pointercancel"):
                # No click follows a press that leaves the button.
                button.addEventListener(end, lambda e: self._stop_repeat(True))
            button.addEventListener(
                "click", lambda e, step=step: self._on_arrow_click(step))
        nodes["month-year"].addEventListener("click", lambda e: self._toggle_years())
        nodes["mode"].addEventListener("click", lambda e: self._toggle_mode())
        nodes["body"].addEventListener("click", self._on_body_click)
        nodes["body"].addEventListener("keydown", self._on_body_key)
        self._render()
        return panel

    def _render(self, focus=False):
        nodes = self._panel.dom_nodes
        shown = self._pending
        nodes["headline"].innerText = (
            f"{DAYS[shown.weekday()][:3]}, {shown.day} {MONTHS[shown.month - 1][:3]}"
            if shown else "Select a date"
        )
        typing = self._mode == "input"
        mode_icon = nodes["mode"].querySelector("i")
        mode_icon.innerText = "calendar_today" if typing else "edit"
        nodes["mode"].setAttribute(
            "aria-label", "Choose in the calendar" if typing else "Type the date"
        )
        nodes["nav"].style.display = "none" if typing else ""
        nodes["body"].style.display = "none" if typing else ""
        self._panel.get_components()[0].visible = typing
        if typing:
            self._input.text = self._format(shown) if shown else ""
            return
        years = self._mode == "years"
        nodes["month-year"].innerHTML = ""
        label = window.document.createElement("span")
        label.innerText = f"{MONTHS[self._view.month - 1]} {self._view.year}"
        arrow = window.document.createElement("i")
        arrow.className = "material-symbols-outlined"
        arrow.setAttribute("aria-hidden", "true")
        arrow.innerText = "arrow_drop_up" if years else "arrow_drop_down"
        nodes["month-year"].appendChild(label)
        nodes["month-year"].appendChild(arrow)
        nodes["month-year"].setAttribute("aria-expanded", "true" if years else "false")
        for name, months in (("previous", -1), ("next", 1)):
            nodes[name].style.visibility = "hidden" if years else ""
            nodes[name].disabled = not self._can_move(months)
        body = nodes["body"]
        body.innerHTML = ""
        if years:
            self._render_years(body)
        else:
            self._render_month(body, focus)

    def _render_month(self, body, focus):
        doc = window.document
        sunday_first = self.week_starts_on == "sunday"
        order = [6, 0, 1, 2, 3, 4, 5] if sunday_first else list(range(7))
        grid = doc.createElement("div")
        grid.className = "m3x-date-picker-grid"
        grid.setAttribute("role", "grid")
        for index in order:
            head = doc.createElement("span")
            head.className = "m3x-date-picker-weekday"
            head.setAttribute("aria-label", DAYS[index])
            head.innerText = DAYS[index][0]
            grid.appendChild(head)
        first = self._view
        offset = order.index(first.weekday())
        for _ in range(offset):
            grid.appendChild(doc.createElement("span"))
        today = datetime.date.today()
        focus_node = None
        for number in range(1, _days_in_month(first) + 1):
            day = datetime.date(first.year, first.month, number)
            cell = doc.createElement("button")
            cell.type = "button"
            cell.className = "m3x-date-picker-day"
            cell.innerText = str(number)
            cell.setAttribute("data-day", day.isoformat())
            cell.setAttribute(
                "aria-label", f"{DAYS[day.weekday()]} {number} {MONTHS[day.month - 1]}"
            )
            if day == today:
                cell.classList.add("m3x-date-picker-today")
                cell.setAttribute("aria-current", "date")
            if day == self._pending:
                cell.classList.add("m3x-date-picker-selected")
                cell.setAttribute("aria-selected", "true")
            if not self._allowed(day):
                cell.disabled = True
            is_focus = day == self._focus_day
            cell.setAttribute("tabindex", "0" if is_focus else "-1")
            if is_focus:
                focus_node = cell
            grid.appendChild(cell)
        body.appendChild(grid)
        if focus and focus_node is not None:
            focus_node.focus()

    def _render_years(self, body):
        doc = window.document
        low, high = self._clean(self.min_date), self._clean(self.max_date)
        first = low.year if low else _FIRST_YEAR
        last = high.year if high else _LAST_YEAR
        grid = doc.createElement("div")
        grid.className = "m3x-date-picker-years"
        current = None
        for year in range(first, last + 1):
            cell = doc.createElement("button")
            cell.type = "button"
            cell.className = "m3x-date-picker-year"
            cell.innerText = str(year)
            cell.setAttribute("data-year", str(year))
            if year == self._view.year:
                cell.classList.add("m3x-date-picker-selected")
                current = cell
            grid.appendChild(cell)
        body.appendChild(grid)
        if current is not None:
            window.setTimeout(lambda: current.scrollIntoView({"block": "center"}), 0)
            current.focus()

    # ---- interaction ---------------------------------------------------------

    def _can_move(self, months):
        """True if the month the arrows would show has any allowed day."""
        target = _add_months(self._view, months)
        low, high = self._clean(self.min_date), self._clean(self.max_date)
        last = target.replace(day=_days_in_month(target))
        return not ((low and last < low) or (high and target > high))

    def _on_arrow_click(self, months):
        # A mouse or touch press already moved the month on pointerdown; a
        # keyboard press (Enter or Space) arrives only as a click.
        if self._pointer_used:
            self._pointer_used = False
            return
        self._move_month(months)

    def _start_repeat(self, event, months):
        if event.button != 0 or not self._can_move(months):
            return
        self._pointer_used = True
        self._move_month(months)
        # Held down: wait 400 ms, then move a month every 120 ms.
        self._repeat_timer = window.setTimeout(
            lambda: self._repeat(months, 120), 400)

    def _repeat(self, months, interval):
        if not self._can_move(months):
            self._stop_repeat()
            return
        self._move_month(months)
        self._repeat_timer = window.setTimeout(
            lambda: self._repeat(months, interval), interval)

    def _stop_repeat(self, cancelled=False):
        if cancelled:
            self._pointer_used = False
        if self._repeat_timer is not None:
            window.clearTimeout(self._repeat_timer)
            self._repeat_timer = None

    def _move_month(self, months):
        if not self._can_move(months):
            return
        self._view = _add_months(self._view, months)
        day = min(self._focus_day.day, _days_in_month(self._view))
        self._focus_day = datetime.date(self._view.year, self._view.month, day)
        self._render()

    def _toggle_years(self):
        self._mode = "calendar" if self._mode == "years" else "years"
        self._render(focus=True)

    def _toggle_mode(self):
        self._mode = "calendar" if self._mode == "input" else "input"
        self._render(focus=True)

    def _on_body_click(self, event):
        target = event.target
        year = target.closest("[data-year]")
        if year:
            self._view = self._in_range(datetime.date(
                int(year.getAttribute("data-year")), self._view.month, 1))
            self._mode = "calendar"
            self._render(focus=True)
            return
        cell = target.closest("[data-day]")
        if cell and not cell.disabled:
            year, month, number = cell.getAttribute("data-day").split("-")
            day = datetime.date(int(year), int(month), int(number))
            self._pending = day
            self._focus_day = day
            self._render(focus=True)

    def _on_body_key(self, event):
        if self._mode != "calendar":
            return
        moves = {"ArrowLeft": -1, "ArrowRight": 1, "ArrowUp": -7, "ArrowDown": 7}
        if event.key in moves:
            target = self._focus_day + datetime.timedelta(days=moves[event.key])
        elif event.key == "PageUp":
            target = _add_months(self._focus_day, -1).replace(
                day=min(self._focus_day.day, 28))
        elif event.key == "PageDown":
            target = _add_months(self._focus_day, 1).replace(
                day=min(self._focus_day.day, 28))
        else:
            return
        event.preventDefault()
        self._focus_day = target
        self._view = _first_of_month(target)
        self._render(focus=True)

    def _on_input_change(self, **event_args):
        text = (self._input.text or "").strip()
        if not text:
            self._input.error = False
            self._input.supporting_text = ""
            return
        day = self._parse(text)
        ok = day is not None and self._allowed(day)
        self._input.error = not ok
        self._input.supporting_text = "" if ok else self._ERROR
        if ok:
            self._pending = day
            self._focus_day = day
            self._view = _first_of_month(day)
            self._panel.dom_nodes["headline"].innerText = (
                f"{DAYS[day.weekday()][:3]}, {day.day} {MONTHS[day.month - 1][:3]}"
            )

    # ---- properties ----------------------------------------------------------

    def _get_date(self):
        return self._value

    def _set_date(self, value):
        self._value = self._clean(value)
        self._props["date"] = self._value
        self._show_value()

    date = property(_get_date, _set_date)

    def _store(self, value):
        self._props["date"] = value
        super()._store(value)

    @anvil_prop(default_value="Date")
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
        """If True, the date can be changed."""
        m3x_picker.apply_field_property(self, "enabled", value)

    @anvil_prop(default_value="%d/%m/%Y")
    @property
    def format(self, value) -> str:
        """How the date is written in the field."""
        self._show_value()

    @anvil_prop(default_value=None)
    @property
    def min_date(self, value) -> object:
        """The earliest date that can be chosen."""

    @anvil_prop(default_value=None)
    @property
    def max_date(self, value) -> object:
        """The latest date that can be chosen."""

    @anvil_prop(default_value="monday")
    @property
    def week_starts_on(self, value) -> str:
        """monday or sunday."""

    visible = HtmlTemplate.visible
    role = role_property("m3x-date-picker")

    #!componentEvent(m3.DatePicker)!1: {name: "change", description: "When the user changes the date."}
    #!componentEvent(m3.DatePicker)!1: {name: "show", description: "When the date picker is shown on the screen."}
    #!componentEvent(m3.DatePicker)!1: {name: "hide", description: "When the date picker is removed from the screen."}

    #!componentProp(m3.DatePicker)!1: {name:"date",type:"object",description:"The chosen date, as a datetime.date. None when empty."}
    #!componentProp(m3.DatePicker)!1: {name:"label",type:"string",description:"The label of the field."}
    #!componentProp(m3.DatePicker)!1: {name:"format",type:"string",description:"How the date is written in the field."}
    #!componentProp(m3.DatePicker)!1: {name:"min_date",type:"object",description:"The earliest date that can be chosen."}
    #!componentProp(m3.DatePicker)!1: {name:"max_date",type:"object",description:"The latest date that can be chosen."}
    #!componentProp(m3.DatePicker)!1: {name:"week_starts_on",type:"enum",options:["monday", "sunday"],description:"The first day of the week in the calendar."}
    #!componentProp(m3.DatePicker)!1: {name:"appearance",type:"enum",options:["filled", "outlined"],description:"The look of the field."}
    #!componentProp(m3.DatePicker)!1: {name:"supporting_text",type:"string",description:"A line of help text below the field."}
    #!componentProp(m3.DatePicker)!1: {name:"enabled",type:"boolean",description:"If True, the date can be changed."}
    #!componentProp(m3.DatePicker)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.DatePicker)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.DatePicker)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, DatePicker, anvil.Component)!:
