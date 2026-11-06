"""Demo and test form for the M3 custom theme.

Shows every existing component in each of its variants and states. It is the
test harness for every later step (see m3-custom-theme.md, Step 3). Add each new
component here, in every variant and state, before merging it.
"""
import datetime

from anvil import *
import m3.components as m3

from anvil.js import get_dom_node
from m3._utils import m3x_theming
from m3._utils.properties import theme_color_to_css

from ._anvil_designer import Form1Template

BUTTON_APPEARANCES = ["filled", "elevated", "tonal", "outlined", "text"]
ICON_BUTTON_APPEARANCES = ["standard", "filled", "tonal", "outlined"]
CARD_APPEARANCES = ["elevated", "filled", "outlined"]
AVATAR_APPEARANCES = ["filled", "tonal", "outlined"]
TEXT_INPUT_APPEARANCES = ["filled", "outlined"]
SCALES = ["small", "medium", "large"]

# Token reference (Step 5). Every value comes from theme/assets/m3x/tokens.css.
COLOUR_ROLES = [
    "primary", "on-primary", "primary-container", "on-primary-container",
    "inverse-primary", "primary-fixed", "primary-fixed-dim", "on-primary-fixed",
    "on-primary-fixed-variant", "secondary", "on-secondary",
    "secondary-container", "on-secondary-container", "secondary-fixed",
    "secondary-fixed-dim", "on-secondary-fixed", "on-secondary-fixed-variant",
    "tertiary", "on-tertiary", "tertiary-container", "on-tertiary-container",
    "tertiary-fixed", "tertiary-fixed-dim", "on-tertiary-fixed",
    "on-tertiary-fixed-variant", "error", "on-error", "error-container",
    "on-error-container", "background", "on-background", "surface",
    "on-surface", "surface-variant", "on-surface-variant", "surface-dim",
    "surface-bright", "surface-container-lowest", "surface-container-low",
    "surface-container", "surface-container-high", "surface-container-highest",
    "surface-tint", "inverse-surface", "inverse-on-surface", "outline",
    "outline-variant", "scrim", "shadow",
]
TYPE_STYLES = [
    f"{group}-{size}"
    for group in ("display", "headline", "title", "body", "label")
    for size in ("large", "medium", "small")
]
SHAPES = [
    "none", "extra-small", "small", "medium", "large", "large-increased",
    "extra-large", "extra-large-increased", "extra-extra-large", "full",
]
EASINGS = [
    "emphasized", "emphasized-decelerate", "emphasized-accelerate", "standard",
    "standard-decelerate", "standard-accelerate", "legacy", "legacy-decelerate",
    "legacy-accelerate", "linear",
]
SPACES = [4, 8, 12, 16, 24, 32, 48, 64]

# Each section: (title, component class, list of keyword-argument dicts).
SECTIONS = [
    (
        "Button",
        m3.Button,
        [dict(text=a.title(), appearance=a) for a in BUTTON_APPEARANCES]
        + [
            dict(text="Disabled " + a, appearance=a, enabled=False)
            for a in BUTTON_APPEARANCES
        ]
        + [
            dict(text="Icon left", appearance="filled", icon="mi:add"),
            dict(
                text="Icon right",
                appearance="tonal",
                icon="mi:add",
                icon_align="right",
            ),
        ],
    ),
    (
        "IconButton",
        m3.IconButton,
        [dict(icon="mi:favorite", appearance=a) for a in ICON_BUTTON_APPEARANCES]
        + [
            dict(icon="mi:favorite", appearance=a, enabled=False)
            for a in ICON_BUTTON_APPEARANCES
        ],
    ),
    (
        "ToggleIconButton",
        m3.ToggleIconButton,
        [
            dict(icon="mi:favorite", appearance=a, selected=s)
            for a in ICON_BUTTON_APPEARANCES
            for s in (False, True)
        ],
    ),
    (
        "Checkbox",
        m3.Checkbox,
        [
            dict(text="Unchecked"),
            dict(text="Checked", checked=True),
            dict(text="Error", error=True),
            dict(text="Disabled", enabled=False),
            dict(text="Disabled, checked", checked=True, enabled=False),
        ],
    ),
    (
        "Switch",
        m3.Switch,
        [
            dict(),
            dict(selected=True),
            dict(enabled=False),
            dict(selected=True, enabled=False),
        ],
    ),
    (
        "TextBox",
        m3.TextBox,
        [
            dict(
                label="Label " + a,
                placeholder="Placeholder",
                supporting_text="Supporting text",
                appearance=a,
            )
            for a in TEXT_INPUT_APPEARANCES
        ]
        + [
            dict(label="Error", appearance="outlined", error=True,
                 supporting_text="Error text"),
            dict(label="Disabled", appearance="outlined", enabled=False),
        ],
    ),
    (
        "TextArea",
        m3.TextArea,
        [
            dict(label="Label " + a, supporting_text="Supporting text", appearance=a)
            for a in TEXT_INPUT_APPEARANCES
        ],
    ),
    (
        "Slider",
        m3.Slider,
        [
            dict(value=30, min=0, max=100, show_label=True),
            dict(value=60, min=0, max=100, step=20, show_markers=True),
            dict(value=30, min=0, max=100, enabled=False),
        ],
    ),
    (
        "Avatar",
        m3.Avatar,
        [dict(user_name="Ada Lovelace", appearance=a) for a in AVATAR_APPEARANCES],
    ),
    (
        "Link",
        m3.Link,
        [dict(text="A link", url="#"), dict(text="A link with icon", url="#",
                                             icon="mi:open_in_new")],
    ),
]


class Form1(Form1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        super().__init__(**properties)

        m3x_theming.apply_saved()
        self._heading("M3 custom theme: demo and test form", "display", "small")
        self._build_theme_controls()
        for title, cls, variants in SECTIONS:
            row = self._section(title)
            for kwargs in variants:
                row.add_component(cls(**kwargs))
        self._build_radio_buttons()
        self._build_menus()
        self._build_dropdown_menus()
        self._build_file_loaders()
        self._build_navigation_links()
        self._build_typography()
        self._build_cards()
        self._build_progress()
        self._build_dividers()
        self._build_dialogs()
        self._build_chips()
        self._build_badges()
        self._build_snackbars()
        self._build_tabs()
        self._build_fabs()
        self._build_list_items()
        self._build_button_groups()
        self._build_app_bars()
        self._build_navigation_bars()
        self._build_wavy_progress()
        self._build_loading_indicators()
        self._build_pickers()
        self._build_tooltips()
        self._build_search()
        self._build_bottom_sheets()
        self._build_toolbars()
        self._build_split_buttons()
        self._build_fab_menus()
        self._build_tokens()

    # ---- helpers -------------------------------------------------------

    def _heading(self, text, style="headline", scale="small"):
        self.add_component(m3.Heading(text=text, style=style, scale=scale))

    def _section(self, title):
        self._heading(title)
        row = FlowPanel(spacing="medium")
        self.add_component(row)
        return row

    # ---- sections that need more than a row of components ------------------

    def _build_radio_buttons(self):
        # RadioButtons join a group by sitting inside a RadioGroupPanel. Do not
        # pass the group property: it must be a RadioGroup object, not a string.
        row = self._section("RadioGroupPanel and RadioButton")
        panel = m3.RadioGroupPanel()
        panel.add_component(m3.RadioButton(text="Option A", value="a", selected=True))
        panel.add_component(m3.RadioButton(text="Option B", value="b"))
        panel.add_component(m3.RadioButton(text="Disabled", value="c", enabled=False))
        row.add_component(panel)

    def _build_theme_controls(self):
        row = self._section("Palette and mode")
        self._palette_menu = m3.DropdownMenu(
            label="Palette", items=list(m3x_theming.PALETTES)
        )
        self._palette_menu.selected_value = m3x_theming.get_palette()
        self._palette_menu.add_event_handler("change", self._on_palette_change)
        row.add_component(self._palette_menu)
        self._mode_menu = m3.DropdownMenu(label="Mode", items=list(m3x_theming.MODES))
        self._mode_menu.selected_value = m3x_theming.get_mode()
        self._mode_menu.add_event_handler("change", self._on_mode_change)
        row.add_component(self._mode_menu)

    def _on_palette_change(self, **event_args):
        if self._palette_menu.selected_value:
            m3x_theming.set_palette(self._palette_menu.selected_value)

    def _on_mode_change(self, **event_args):
        if self._mode_menu.selected_value:
            m3x_theming.set_mode(self._mode_menu.selected_value)

    def _menu_items(self):
        # MenuItems cannot be shared between menus, so make a fresh set each time.
        return [
            m3.MenuItem(text="Cut", leading_icon="mi:content_cut"),
            m3.MenuItem(text="Copy", leading_icon="mi:content_copy",
                        trailing_text="Ctrl+C"),
            m3.MenuItem(text="Disabled item", enabled=False),
        ]

    def _build_menus(self):
        row = self._section("ButtonMenu")
        for appearance in ("elevated", "filled", "tonal", "outlined"):
            row.add_component(
                m3.ButtonMenu(
                    text=appearance.title() + " menu",
                    appearance=appearance,
                    menu_items=self._menu_items(),
                )
            )
        row.add_component(
            m3.ButtonMenu(text="Disabled menu", enabled=False,
                          menu_items=self._menu_items())
        )
        row = self._section("IconButtonMenu")
        for appearance in ICON_BUTTON_APPEARANCES:
            row.add_component(
                m3.IconButtonMenu(
                    icon="mi:more_vert",
                    appearance=appearance,
                    menu_items=self._menu_items(),
                )
            )
        row = self._section("AvatarMenu")
        for appearance in AVATAR_APPEARANCES:
            row.add_component(
                m3.AvatarMenu(
                    user_name="Ada Lovelace",
                    appearance=appearance,
                    menu_items=self._menu_items(),
                )
            )

    def _build_dropdown_menus(self):
        row = self._section("DropdownMenu")
        items = ["Apple", "Banana", "Cherry"]
        for appearance in TEXT_INPUT_APPEARANCES:
            row.add_component(
                m3.DropdownMenu(
                    label="Label " + appearance,
                    items=items,
                    appearance=appearance,
                    placeholder="Choose one",
                    supporting_text="Supporting text",
                )
            )
        row.add_component(
            m3.DropdownMenu(label="Error", items=items, appearance="outlined",
                            error=True, supporting_text="Error text")
        )
        row.add_component(
            m3.DropdownMenu(label="Disabled", items=items, appearance="outlined",
                            enabled=False)
        )

    def _build_file_loaders(self):
        row = self._section("FileLoader")
        for appearance in ("text", "elevated", "filled", "tonal", "outlined"):
            row.add_component(
                m3.FileLoader(text="Upload " + appearance, appearance=appearance)
            )
        row.add_component(m3.FileLoader(text="Disabled", enabled=False))

    def _build_navigation_links(self):
        row = self._section("NavigationLink")
        row.add_component(m3.NavigationLink(text="Home", icon="mi:home"))
        row.add_component(
            m3.NavigationLink(text="Selected", icon="mi:home", selected=True)
        )
        row.add_component(
            m3.NavigationLink(text="Badge", icon="mi:mail", badge=True, badge_count=3)
        )

    def _build_typography(self):
        self._heading("Heading")
        for style in ("display", "headline", "title"):
            for scale in SCALES:
                self.add_component(
                    m3.Heading(text=f"{style} {scale}", style=style, scale=scale)
                )
        self._heading("Text")
        for style in ("body", "label"):
            for scale in SCALES:
                self.add_component(
                    m3.Text(text=f"{style} {scale}", style=style, scale=scale)
                )

    def _build_cards(self):
        row = self._section("Card")
        for appearance in CARD_APPEARANCES:
            card = m3.Card(appearance=appearance)
            card.add_component(m3.Text(text=f"{appearance} card", style="body"))
            row.add_component(card)

    def _build_progress(self):
        self._heading("LinearProgressIndicator")
        self.add_component(m3.LinearProgressIndicator(type="determinate", progress=60))
        self.add_component(m3.LinearProgressIndicator(type="indeterminate"))
        row = self._section("CircularProgressIndicator")
        row.add_component(m3.CircularProgressIndicator(type="determinate", progress=60))
        row.add_component(m3.CircularProgressIndicator(type="indeterminate"))

    def _build_dividers(self):
        self._heading("Divider")
        self.add_component(m3.Divider(type="full_width"))
        self.add_component(m3.Divider(type="inset"))

    # ---- dialogs (Step 6) ----------------------------------------------------

    def _build_dialogs(self):
        row = self._section("Dialog")
        for text, opener in (
            ("Basic", self._dialog_basic),
            ("With icon", self._dialog_icon),
            ("With content", self._dialog_content),
            ("Not dismissible", self._dialog_not_dismissible),
            ("Full screen", self._dialog_full_screen),
        ):
            button = m3.Button(text=text, appearance="outlined")
            button.add_event_handler(
                "click", lambda opener=opener, **event_args: self._open_dialog(opener)
            )
            row.add_component(button)
        self._dialog_result = m3.Text(text="Last result: (none yet)")
        self.add_component(self._dialog_result)
        self._heading("Dialog as placed in a form (not opened)")
        self.add_component(self._dialog_icon())

    def _open_dialog(self, opener):
        result = opener().show()
        self._dialog_result.text = f"Last result: {result!r}"

    def _dialog_basic(self):
        dialog = m3.Dialog(
            headline="Discard draft?",
            supporting_text="The draft will be deleted. This cannot be undone.",
        )
        dialog.add_action("Cancel", value="cancel")
        dialog.add_action("Discard", value="discard")
        return dialog

    def _dialog_icon(self):
        dialog = m3.Dialog(
            icon="mi:delete",
            headline="Delete 3 files?",
            supporting_text="The files move to the bin and are deleted after 30 days.",
        )
        dialog.add_action("Cancel", value="cancel")
        dialog.add_action("Delete", value="delete")
        return dialog

    def _dialog_content(self):
        dialog = m3.Dialog(
            headline="Choose a ringtone",
            supporting_text="The choice applies to every call.",
        )
        group = m3.RadioGroupPanel()
        for name in ("Chime", "Bell", "Marimba"):
            group.add_component(
                m3.RadioButton(text=name, value=name, selected=name == "Chime")
            )
        dialog.add_component(group)
        dialog.add_action("Cancel", value=None)
        # An action that returns a value from the content: a Button of its own.
        ok = m3.Button(text="OK", appearance="text")
        ok.add_event_handler(
            "click", lambda **event_args: dialog.close(group.selected_value)
        )
        dialog.add_component(ok, slot="dialog-actions-slot")
        return dialog

    def _dialog_not_dismissible(self):
        dialog = m3.Dialog(
            headline="Terms updated",
            supporting_text="Clicking outside or pressing Escape does not close "
            "this dialog. Only the button does.",
            dismissible=False,
        )
        dialog.add_action("I agree", value="agreed")
        return dialog

    def _dialog_full_screen(self):
        dialog = m3.Dialog(headline="New event", full_screen=True)
        dialog.add_component(m3.TextBox(label="Title", appearance="outlined"))
        dialog.add_component(m3.TextBox(label="Location", appearance="outlined"))
        dialog.add_component(
            m3.TextArea(label="Description", appearance="outlined")
        )
        dialog.add_action("Save", value="saved")
        return dialog

    # ---- chips (Step 6) ------------------------------------------------------

    def _build_chips(self):
        rows = (
            ("Chip: assist", [
                dict(text="Assist"),
                dict(text="With icon", leading_icon="mi:event"),
                dict(text="Elevated", elevated=True, leading_icon="mi:event"),
                dict(text="Disabled", enabled=False),
                dict(text="Disabled elevated", elevated=True, enabled=False),
            ]),
            ("Chip: filter", [
                dict(text="Filter"),
                dict(text="Selected", selected=True),
                dict(text="Elevated", elevated=True),
                dict(text="Elevated selected", elevated=True, selected=True),
                dict(text="Disabled", enabled=False),
                dict(text="Disabled selected", enabled=False, selected=True),
            ]),
            ("Chip: input", [
                dict(text="Input", removable=True),
                dict(text="With icon", leading_icon="mi:person", removable=True),
                dict(text="Selected", selected=True, removable=True),
                dict(text="Disabled", enabled=False, removable=True),
            ]),
            ("Chip: suggestion", [
                dict(text="Suggestion"),
                dict(text="With icon", leading_icon="mi:lightbulb"),
                dict(text="Elevated", elevated=True),
                dict(text="Disabled", enabled=False),
            ]),
        )
        for title, variants in rows:
            chip_type = title.split(": ")[1]
            row = self._section(title)
            for kwargs in variants:
                chip = m3.Chip(type=chip_type, **kwargs)
                chip.add_event_handler("click", self._on_chip_event)
                chip.add_event_handler("change", self._on_chip_event)
                chip.add_event_handler("remove", self._on_chip_event)
                row.add_component(chip)
        self._chip_result = m3.Text(text="Last chip event: (none yet)")
        self.add_component(self._chip_result)

    def _on_chip_event(self, sender, event_name, **event_args):
        self._chip_result.text = (
            f"Last chip event: {event_name} on '{sender.text}' ({sender.type}), "
            f"selected={sender.selected}"
        )
        if event_name == "remove":
            sender.remove_from_parent()

    # ---- badges and snackbars (Step 6) --------------------------------------

    def _build_badges(self):
        row = self._section("Badge")
        for count in (None, 3, 42, 1000):
            label = "dot" if count is None else str(count)
            row.add_component(m3.Text(text=f"Badge {label}:"))
            row.add_component(m3.Badge(count=count))

    def _build_snackbars(self):
        row = self._section("Snackbar")
        for text, opener in (
            ("Short", self._snackbar_short),
            ("With action", self._snackbar_action),
            ("With close", self._snackbar_close),
            ("Two lines", self._snackbar_two_lines),
            ("Queue of three", self._snackbar_queue),
        ):
            button = m3.Button(text=text, appearance="outlined")
            button.add_event_handler(
                "click", lambda opener=opener, **event_args: opener()
            )
            row.add_component(button)
        self._snackbar_result = m3.Text(text="Last snackbar event: (none yet)")
        self.add_component(self._snackbar_result)

    def _snackbar_event(self, text):
        self._snackbar_result.text = f"Last snackbar event: {text}"

    def _snackbar_short(self):
        m3.Snackbar(
            "Message sent.",
            on_dismiss=lambda: self._snackbar_event("'Message sent.' closed"),
        ).show()

    def _snackbar_action(self):
        m3.Snackbar(
            "Photo deleted.",
            action_text="Undo",
            on_action=lambda: self._snackbar_event("Undo clicked"),
            duration="long",
        ).show()

    def _snackbar_close(self):
        m3.Snackbar(
            "Connection lost. Changes are saved on this device.",
            show_close=True,
            duration="indefinite",
            on_dismiss=lambda: self._snackbar_event("closed with the close button"),
        ).show()

    def _snackbar_two_lines(self):
        m3.Snackbar(
            "Your booking for Saturday has been confirmed. A confirmation email is "
            "on its way to your inbox.",
            action_text="View",
            on_action=lambda: self._snackbar_event("View clicked"),
        ).show()

    def _snackbar_queue(self):
        for n in (1, 2, 3):
            m3.Snackbar(
                f"Message {n} of 3",
                on_dismiss=lambda n=n: self._snackbar_event(f"message {n} closed"),
            ).show()

    # ---- tabs and floating action buttons (Step 6) ---------------------------

    def _build_tabs(self):
        self._heading("Tabs")
        self._tabs_result = m3.Text(text="Selected tab: (none yet)")
        for title, kwargs in (
            ("Primary tabs", dict(items=["Flights", "Trips", "Explore"])),
            ("Primary tabs with icons", dict(
                items=["Flights", "Trips", "Explore"],
                icons=["mi:flight", "mi:luggage", "mi:explore"],
            )),
            ("Secondary tabs", dict(
                type="secondary", items=["Overview", "Specifications", "Reviews"]
            )),
            ("Scrollable tabs", dict(scrollable=True, items=[
                "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                "Saturday", "Sunday", "Next week", "Last week",
            ])),
        ):
            self.add_component(m3.Text(text=title, style="label"))
            tabs = m3.Tabs(**kwargs)
            tabs.add_event_handler("change", self._on_tabs_change)
            self.add_component(tabs)
        self.add_component(self._tabs_result)

    def _on_tabs_change(self, sender, **event_args):
        self._tabs_result.text = (
            f"Selected tab: {sender.selected_text} "
            f"(position {sender.selected_index})"
        )

    def _build_fabs(self):
        self._fab_result = m3.Text(text="Last button clicked: (none yet)")
        row = self._section("FloatingActionButton: sizes")
        for size in ("regular", "medium", "large"):
            row.add_component(self._fab(size=size, tooltip=f"Create ({size})"))
        row = self._section("FloatingActionButton: colours")
        for appearance in (
            "primary_container", "secondary_container", "tertiary_container",
            "primary", "secondary", "tertiary",
        ):
            row.add_component(
                self._fab(appearance=appearance, icon="mi:edit", tooltip=appearance)
            )
        row = self._section("FloatingActionButton: extended")
        for size in ("regular", "medium", "large"):
            row.add_component(self._fab(size=size, text="Compose", icon="mi:edit"))
        row.add_component(
            self._fab(text="Disabled", icon="mi:edit", enabled=False)
        )
        self.add_component(self._fab_result)
        self._floating_switch = m3.Switch()
        self._floating_switch.add_event_handler("change", self._on_floating_change)
        row = FlowPanel(spacing="medium")
        row.add_component(m3.Text(text="Show a floating button in the corner:"))
        row.add_component(self._floating_switch)
        self.add_component(row)
        self._floating_fab = self._fab(
            floating=True, icon="mi:add", tooltip="Floating", visible=False
        )
        self.add_component(self._floating_fab)

    def _fab(self, **kwargs):
        fab = m3.FloatingActionButton(**kwargs)
        fab.add_event_handler("click", self._on_fab_click)
        return fab

    def _on_fab_click(self, sender, **event_args):
        name = sender.text or sender.tooltip
        self._fab_result.text = f"Last button clicked: {name}"

    def _on_floating_change(self, **event_args):
        self._floating_fab.visible = self._floating_switch.selected

    # ---- list items and button groups (Step 6) -------------------------------

    def _build_list_items(self):
        self._heading("ListItem")
        self._list_result = m3.Text(text="Last list item clicked: (none yet)")
        card = m3.Card(appearance="outlined")
        items = (
            dict(headline="One line"),
            dict(headline="With icon", leading_icon="mi:inbox", trailing_text="24"),
            dict(headline="Ada Lovelace", supporting_text="Two lines, with an avatar",
                 leading_avatar_text="AL", trailing_icon="mi:chevron_right",
                 clickable=True, divider=True),
            dict(headline="Clickable", supporting_text="Click me",
                 leading_icon="mi:touch_app", clickable=True, divider=True),
            dict(headline="Selected", supporting_text="Shown as selected",
                 leading_icon="mi:check_circle", clickable=True, selected=True),
            dict(headline="Disabled", supporting_text="Cannot be clicked",
                 leading_icon="mi:block", clickable=True, enabled=False),
            dict(overline="Overline", headline="Three lines",
                 supporting_text="The supporting text of a three-line item can run "
                 "onto a second line. Text that is longer than two lines is cut off "
                 "at the end of the second line with three dots. This sentence is "
                 "long on purpose, so that it is cut off even on a wide screen: it "
                 "keeps going well past the end of the second line, and the rest of "
                 "it is never shown in the list.", three_line=True,
                 leading_icon="mi:article"),
        )
        for kwargs in items:
            item = m3.ListItem(**kwargs)
            item.add_event_handler("click", self._on_list_item_click)
            card.add_component(item)
        switch_item = m3.ListItem(headline="With a switch", leading_icon="mi:wifi")
        switch_item.add_component(m3.Switch(selected=True))
        card.add_component(switch_item)
        self.add_component(card)
        self.add_component(self._list_result)

    def _on_list_item_click(self, sender, **event_args):
        self._list_result.text = f"Last list item clicked: {sender.headline}"

    def _build_button_groups(self):
        self._heading("ButtonGroup")
        self._group_result = m3.Text(text="Button group: (no change yet)")
        for title, kwargs in (
            ("Connected, single selection", dict()),
            ("Connected, multiple selection, tonal", dict(
                selection="multiple", appearance="tonal",
                items=["Bold", "Italic", "Underline"],
                icons=["mi:format_bold", "mi:format_italic", "mi:format_underlined"],
            )),
            ("Connected, outlined, full width", dict(
                appearance="outlined", full_width=True,
                items=["Walk", "Cycle", "Drive", "Transit"],
            )),
            ("Standard, actions (no selection)", dict(
                type="standard", selection="none",
                items=["Share", "Save", "Print"],
                icons=["mi:share", "mi:bookmark", "mi:print"],
            )),
            ("Disabled", dict(enabled=False, selected_index=1)),
        ):
            self.add_component(m3.Text(text=title, style="label"))
            group = m3.ButtonGroup(**kwargs)
            group.add_event_handler("click", self._on_group_click)
            self.add_component(group)
        self.add_component(self._group_result)

    def _on_group_click(self, sender, index, **event_args):
        name = list(sender.items)[index]
        self._group_result.text = (
            f"Button group: clicked '{name}', selected {sender.selected_indices}"
        )

    # ---- top app bars and navigation bars (Step 6) ---------------------------

    def _build_app_bars(self):
        self._heading("TopAppBar")
        self._bar_result = m3.Text(text="Top app bar: (nothing clicked yet)")
        for title, kwargs in (
            ("Small", dict(title="Inbox", navigation_icon="mi:menu")),
            ("Small, centred, with subtitle", dict(
                title="Photos", subtitle="1,204 items", centered=True,
                navigation_icon="mi:arrow_back",
            )),
            ("Medium", dict(size="medium", title="Settings",
                            navigation_icon="mi:arrow_back")),
            ("Large, with subtitle", dict(size="large", title="Recipes",
                                          subtitle="Saturday dinner",
                                          navigation_icon="mi:arrow_back")),
        ):
            self.add_component(m3.Text(text=title, style="label"))
            bar = m3.TopAppBar(sticky=False, navigation_label="Navigation", **kwargs)
            bar.add_event_handler("navigation_click", self._on_bar_navigation)
            for icon in ("mi:search", "mi:more_vert"):
                action = m3.IconButton(icon=icon, tooltip=icon[3:])
                action.add_event_handler(
                    "click",
                    lambda icon=icon, **e: self._bar_event(f"{icon[3:]} clicked"),
                )
                bar.add_component(action)
            card = m3.Card(appearance="outlined")
            card.add_component(bar)
            self.add_component(card)
        self.add_component(self._bar_result)

    def _on_bar_navigation(self, sender, **event_args):
        self._bar_event(f"navigation icon of '{sender.title}' clicked")

    def _bar_event(self, text):
        self._bar_result.text = f"Top app bar: {text}"

    def _build_navigation_bars(self):
        self._heading("NavigationBar")
        self._nav_result = m3.Text(text="Navigation bar: Home selected")
        bar = m3.NavigationBar(
            items=["Home", "Messages", "Calendar", "Profile"],
            icons=["mi:home", "mi:chat", "mi:calendar_month", "mi:person"],
            badges=[None, 3, 0, None],
        )
        bar.add_event_handler("change", self._on_navigation_change)
        card = m3.Card(appearance="outlined")
        card.add_component(bar)
        self.add_component(card)
        self.add_component(self._nav_result)

    def _on_navigation_change(self, sender, **event_args):
        self._nav_result.text = f"Navigation bar: {sender.selected_text} selected"

    # ---- wavy progress and loading indicators (Step 7) -----------------------

    def _build_wavy_progress(self):
        self._heading("Wavy progress indicators")
        self._wavy = [
            m3.LinearProgressIndicator(type="determinate", progress=60, wavy=True),
            m3.CircularProgressIndicator(type="determinate", progress=60, wavy=True),
        ]
        self.add_component(self._wavy[0])
        row = FlowPanel(spacing="medium")
        row.add_component(self._wavy[1])
        row.add_component(
            m3.CircularProgressIndicator(type="indeterminate", wavy=True)
        )
        self.add_component(row)
        self.add_component(m3.Text(text="Indeterminate:", style="label"))
        self.add_component(
            m3.LinearProgressIndicator(type="indeterminate", wavy=True)
        )
        self._wavy_value = m3.Text(text="Progress: 60 %")
        slider = m3.Slider(min=0, max=100, step=1, value=60)
        slider.add_event_handler("change", self._on_wavy_slider)
        self.add_component(self._wavy_value)
        self.add_component(slider)

    def _on_wavy_slider(self, sender, **event_args):
        for indicator in self._wavy:
            indicator.progress = sender.value
        self._wavy_value.text = f"Progress: {int(sender.value)} %"

    def _build_loading_indicators(self):
        row = self._section("LoadingIndicator")
        row.add_component(m3.Text(text="Plain:"))
        row.add_component(m3.LoadingIndicator())
        row.add_component(m3.Text(text="Contained:"))
        row.add_component(m3.LoadingIndicator(contained=True))

    # ---- date and time pickers (Step 6) --------------------------------------

    def _build_pickers(self):
        self._heading("DatePicker and TimePicker")
        self._picker_result = m3.Text(text="Picker: (no change yet)")
        pickers = (
            m3.DatePicker(label="Date of birth", supporting_text="DD/MM/YYYY"),
            m3.DatePicker(
                label="Delivery date",
                date=datetime.date.today(),
                min_date=datetime.date.today(),
                max_date=datetime.date.today() + datetime.timedelta(days=60),
                format="%d %b %Y",
                appearance="filled",
                supporting_text="Within the next 60 days",
            ),
            m3.TimePicker(label="Start time (24-hour)"),
            m3.TimePicker(
                label="Pick-up time (12-hour)", format_24h=False,
                time=datetime.time(14, 30),
            ),
        )
        for picker in pickers:
            picker.add_event_handler("change", self._on_picker_change)
            self.add_component(picker)
        self.add_component(self._picker_result)

    def _on_picker_change(self, sender, **event_args):
        value = sender.date if isinstance(sender, m3.DatePicker) else sender.time
        self._picker_result.text = f"Picker: {sender.label} = {value}"

    # ---- rich tooltips and search (Step 6) -----------------------------------

    def _build_tooltips(self):
        row = self._section("Tooltips")
        self._tooltip_result = m3.Text(text="Tooltip: (no action yet)")
        plain = m3.Button(text="Plain tooltip", appearance="outlined",
                          tooltip="Saves the draft")
        hover = m3.Button(text="Rich tooltip (hover)", appearance="outlined")
        click = m3.Button(text="Rich tooltip (click)", appearance="outlined")
        for button in (plain, hover, click):
            row.add_component(button)
        m3.RichTooltip(
            "Shared drafts can be edited by everyone in the team.",
            subhead="Shared drafts",
        ).attach(hover)
        m3.RichTooltip(
            "Grant access to your calendar so that bookings appear there "
            "automatically.",
            subhead="Calendar access",
            action_text="Learn more",
            on_action=lambda: setattr(
                self._tooltip_result, "text", "Tooltip: Learn more clicked"),
            persistent=True,
        ).attach(click)
        self.add_component(self._tooltip_result)

    def _build_search(self):
        self._heading("SearchBar")
        self._search_result = m3.Text(text="Search: (nothing searched yet)")
        search = m3.SearchBar(
            placeholder="Search recipes",
            suggestions=[
                "Apple crumble", "Banana bread", "Beef stew", "Chicken curry",
                "Chocolate cake", "Fish pie", "Lemon tart", "Mushroom risotto",
                "Pancakes", "Pumpkin soup", "Roast chicken", "Tomato soup",
            ],
        )
        search.add_component(m3.Avatar(user_name="David M"))
        search.add_event_handler(
            "search",
            lambda query, **e: setattr(
                self._search_result, "text", f"Search: {query}"),
        )
        self.add_component(search)
        self.add_component(self._search_result)

    # ---- bottom sheets (Step 6) ----------------------------------------------

    def _build_bottom_sheets(self):
        row = self._section("BottomSheet")
        self._sheet_result = m3.Text(text="Sheet: (nothing chosen yet)")

        modal = m3.BottomSheet(label="Share")
        for icon, text in (("mi:share", "Share"), ("mi:link", "Copy link"),
                           ("mi:edit", "Rename"), ("mi:delete", "Delete")):
            item = m3.ListItem(headline=text, leading_icon=icon, clickable=True)
            item.add_event_handler("click", self._on_sheet_choice)
            modal.add_component(item)
        modal.add_event_handler(
            "closed", lambda **e: self._sheet_note("modal sheet closed"))

        standard = m3.BottomSheet(modal=False, label="Now playing")
        standard.add_component(m3.Heading(text="Now playing", style="title",
                                          scale="large"))
        standard.add_component(m3.Text(
            text="A standard sheet: the page above it stays usable. Scroll the "
                 "page or click its buttons while this sheet is open."))
        close = m3.Button(text="Close", appearance="filled")
        close.add_event_handler("click", lambda **e: standard.close())
        standard.add_component(close)
        standard.add_event_handler(
            "closed", lambda **e: self._sheet_note("standard sheet closed"))

        fixed = m3.BottomSheet(dismissible=False, label="Terms")
        fixed.add_component(m3.Text(
            text="This sheet cannot be dragged away or closed with the scrim or "
                 "Escape. Use the button."))
        accept = m3.Button(text="I agree", appearance="filled")
        accept.add_event_handler("click", lambda **e: fixed.close())
        fixed.add_component(accept)
        fixed.add_event_handler(
            "closed", lambda **e: self._sheet_note("agreed"))

        for text, sheet in (("Open modal sheet", modal),
                            ("Open standard sheet", standard),
                            ("Open sheet that must be answered", fixed)):
            button = m3.Button(text=text, appearance="outlined")
            button.add_event_handler(
                "click", lambda sheet=sheet, **e: sheet.open())
            row.add_component(button)
            row.add_component(sheet)
        self._modal_sheet = modal
        self.add_component(self._sheet_result)

    def _on_sheet_choice(self, sender, **event_args):
        self._modal_sheet.close()
        self._sheet_result.text = f"Sheet: {sender.headline} chosen"

    def _sheet_note(self, note):
        self._sheet_result.text = f"Sheet: {note}"

    # ---- toolbars (Step 6) ---------------------------------------------------

    def _toolbar(self, icons, toggle=None, fab=None, **props):
        bar = m3.Toolbar(**props)
        for icon in icons:
            button = m3.IconButton(icon=f"mi:{icon}", tooltip=icon.replace("_", " "))
            button.add_event_handler(
                "click", lambda icon=icon, **e: setattr(
                    self._toolbar_result, "text", f"Toolbar: {icon} clicked"))
            bar.add_component(button)
        if toggle:
            button = m3.ToggleIconButton(icon=f"mi:{toggle}", selected=True)
            # The toggle button switches itself; the demo only reports it.
            button.add_event_handler(
                "click", lambda sender, **e: setattr(
                    self._toolbar_result, "text",
                    f"Toolbar: star {'on' if sender.selected else 'off'}"))
            bar.add_component(button)
        if fab:
            bar.add_component(
                m3.FloatingActionButton(icon="mi:add", appearance=fab),
                slot="toolbar-fab-slot")
        return bar

    def _build_toolbars(self):
        self._heading("Toolbar")
        self._toolbar_result = m3.Text(text="Toolbar: (nothing clicked yet)")
        edit = ("undo", "redo", "format_bold", "share")
        row = FlowPanel(spacing="medium")
        row.add_component(self._toolbar(edit, label="Floating standard"))
        row.add_component(self._toolbar(edit, fab="primary_container",
                                        label="Floating standard with FAB"))
        self.add_component(row)
        row = FlowPanel(spacing="medium")
        row.add_component(self._toolbar(edit, toggle="star", color_style="vibrant",
                                        fab="tertiary_container",
                                        label="Floating vibrant with FAB"))
        row.add_component(self._toolbar(("edit", "share", "delete"), vertical=True,
                                        label="Floating vertical"))
        row.add_component(self._toolbar(("edit", "share", "delete"), vertical=True,
                                        color_style="vibrant",
                                        fab="tertiary_container",
                                        label="Floating vertical vibrant"))
        self.add_component(row)
        self.add_component(self._toolbar(
            ("arrow_back", "arrow_forward", "home", "bookmark", "more_vert"),
            variant="docked", label="Docked"))
        self.add_component(self._toolbar(
            ("arrow_back", "arrow_forward", "home", "bookmark"),
            variant="docked", color_style="vibrant", fab="tertiary_container",
            label="Docked vibrant with FAB"))

        pinned = self._toolbar(edit, color_style="vibrant", fab="tertiary_container",
                               pin_to_screen=True, hide_on_scroll=True,
                               visible=False, label="Pinned")
        show = m3.Button(text="Pin a toolbar to the screen", appearance="outlined")

        def flip(**e):
            pinned.visible = not pinned.visible
            show.text = ("Remove the pinned toolbar" if pinned.visible
                         else "Pin a toolbar to the screen")
        show.add_event_handler("click", flip)
        self.add_component(show)
        self.add_component(pinned)
        self.add_component(self._toolbar_result)

    # ---- split buttons (Step 6) ----------------------------------------------

    def _split(self, **props):
        button = m3.SplitButton(
            menu_items=["Save as draft", "Save a copy", "Save and close"], **props)
        button.add_event_handler(
            "click", lambda sender, **e: setattr(
                self._split_result, "text", f"Split button: {sender.text} clicked"))
        button.add_event_handler(
            "item_click", lambda item, index, **e: setattr(
                self._split_result, "text",
                f"Split button: menu option {index}, {item}"))
        return button

    def _build_split_buttons(self):
        self._split_result = m3.Text(text="Split button: (nothing clicked yet)")
        row = self._section("SplitButton")
        for appearance in ("filled", "tonal", "elevated", "outlined"):
            row.add_component(self._split(text=appearance.title(), icon="mi:save",
                                          appearance=appearance))
        row.add_component(self._split(text="Disabled", enabled=False))
        row = FlowPanel(spacing="medium")
        for size in ("xsmall", "small", "medium", "large", "xlarge"):
            row.add_component(self._split(text="Save", size=size))
        self.add_component(row)
        self.add_component(self._split_result)

    # ---- FAB menus (Step 6) ---------------------------------------------------

    def _fab_menu(self, **props):
        menu = m3.FabMenu(
            items=["Share", "Add to list", "Duplicate", "Delete"],
            item_icons=["mi:share", "mi:playlist_add", "mi:content_copy", "mi:delete"],
            **props)
        menu.add_event_handler(
            "item_click", lambda item, index, **e: setattr(
                self._fab_menu_result, "text", f"FAB menu: {index}, {item}"))
        return menu

    def _build_fab_menus(self):
        self._fab_menu_result = m3.Text(text="FAB menu: (nothing chosen yet)")
        row = self._section("FabMenu")
        row.add_component(self._fab_menu(color="primary", label="Primary"))
        row.add_component(self._fab_menu(color="secondary", size="medium",
                                         icon="mi:edit", label="Secondary"))
        row.add_component(self._fab_menu(color="tertiary", size="large",
                                         icon="mi:more_horiz", label="Tertiary"))
        floating = self._fab_menu(floating=True, visible=False, label="Floating")
        show = m3.Button(text="Show a floating FAB menu", appearance="outlined")

        def flip(**e):
            floating.close()
            floating.visible = not floating.visible
            show.text = ("Remove the floating FAB menu" if floating.visible
                         else "Show a floating FAB menu")
            if floating.visible:
                # Report where the button landed, measured from the window's
                # bottom right corner (expected: 16 and 16).
                from anvil.js import window
                box = get_dom_node(floating).querySelector(
                    ".m3x-fab-menu").getBoundingClientRect()
                self._fab_menu_result.text = (
                    f"FAB menu: floating button is {int(window.innerWidth - box.right)}"
                    f" px from the right, {int(window.innerHeight - box.bottom)} px"
                    f" from the bottom, size {int(box.width)} x {int(box.height)}")
        show.add_event_handler("click", flip)
        self.add_component(show)
        self.add_component(floating)
        self.add_component(self._fab_menu_result)

    # ---- token reference (Step 5) --------------------------------------------

    def _html(self, html):
        self.add_component(HtmlTemplate(html=html))

    def _build_tokens(self):
        self._heading("Tokens", "headline", "medium")
        text = "color: var(--m3x-color-on-surface);"

        self._heading("Designer colour")
        self.add_component(
            m3.Text(
                text="This box is coloured theme:Tertiary. It must follow the palette.",
                background_color="theme:Tertiary",
                text_color="theme:On Tertiary",
            )
        )
        palette, mode = m3x_theming.editor_preset()
        self.add_component(
            m3.Text(
                text="theme:Tertiary resolves to: "
                + theme_color_to_css("theme:Tertiary")
            )
        )
        self.add_component(m3.Text(text=f"Editor preset: {palette} {mode}"))

        self._heading("Colour roles")
        cells = "".join(
            f'<div style="width:136px;{text}font-size:11px;">'
            f'<div style="height:40px;background:var(--m3x-color-{role});'
            "border:1px solid var(--m3x-color-outline-variant);"
            'border-radius:var(--m3x-shape-corner-small);"></div>'
            f"{role}</div>"
            for role in COLOUR_ROLES
        )
        self._html(f'<div style="display:flex;flex-wrap:wrap;gap:8px;">{cells}</div>')

        for emphasis in ("", "-emphasized"):
            self._heading("Type scale" + (", emphasised" if emphasis else ""))
            rows = "".join(
                f'<div style="{text}'
                f"font-family:var(--m3x-typescale-{name}{emphasis}-font);"
                f"font-size:var(--m3x-typescale-{name}{emphasis}-size);"
                f"line-height:var(--m3x-typescale-{name}{emphasis}-line-height);"
                f"letter-spacing:var(--m3x-typescale-{name}{emphasis}-tracking);"
                f'font-weight:var(--m3x-typescale-{name}{emphasis}-weight);">'
                f"{name}{emphasis}</div>"
                for name in TYPE_STYLES
            )
            self._html(rows)

        self._heading("Shape")
        cells = "".join(
            f'<div style="width:96px;{text}font-size:11px;">'
            '<div style="width:80px;height:56px;'
            "background:var(--m3x-color-primary-container);"
            f'border-radius:var(--m3x-shape-corner-{shape});"></div>{shape}</div>'
            for shape in SHAPES
        )
        self._html(f'<div style="display:flex;flex-wrap:wrap;gap:8px;">{cells}</div>')

        self._heading("Elevation")
        cells = "".join(
            f'<div style="width:96px;height:56px;{text}font-size:11px;'
            "background:var(--m3x-color-surface-container-low);"
            "border-radius:var(--m3x-shape-corner-medium);"
            f'box-shadow:var(--m3x-elevation-level{level});padding:4px;">'
            f"level {level}</div>"
            for level in range(6)
        )
        # The padding leaves room for the deepest shadow, which Anvil's containers
        # would otherwise cut off.
        self._html(
            '<div style="display:flex;flex-wrap:wrap;gap:24px;'
            'padding:var(--m3x-space-8) var(--m3x-space-8) var(--m3x-space-24);">'
            f"{cells}</div>"
        )

        self._heading("State layers")
        cells = "".join(
            f'<div style="width:96px;{text}font-size:11px;">'
            '<div style="width:80px;height:40px;background:var(--m3x-color-primary);'
            f'opacity:var(--m3x-state-{state}-opacity);"></div>{state}</div>'
            for state in ("hover", "focus", "pressed", "dragged")
        )
        self._html(f'<div style="display:flex;flex-wrap:wrap;gap:8px;">{cells}</div>')

        self._heading("Spacing")
        rows = "".join(
            f'<div style="{text}font-size:11px;">{space} px'
            f'<div style="width:var(--m3x-space-{space});height:12px;'
            'background:var(--m3x-color-tertiary);"></div></div>'
            for space in SPACES
        )
        self._html(rows)

        self._heading("Motion: easing curves")
        rows = "".join(
            f'<div style="{text}font-size:11px;">{easing}'
            '<div style="width:100%;height:16px;'
            "background:var(--m3x-color-surface-container-high);"
            'border-radius:var(--m3x-shape-corner-full);">'
            '<div data-m3x-bar style="width:16px;height:16px;'
            "background:var(--m3x-color-primary);"
            "border-radius:var(--m3x-shape-corner-full);"
            "transition:transform var(--m3x-motion-duration-long2) "
            f'var(--m3x-motion-easing-{easing});"></div></div></div>'
            for easing in EASINGS
        )
        self._motion = HtmlTemplate(html=rows)
        play = m3.Button(text="Play", appearance="filled", icon="mi:play_arrow")
        play.add_event_handler("click", self._on_play)
        self.add_component(play)
        self.add_component(self._motion)
        self._played = False

    def _on_play(self, **event_args):
        node = get_dom_node(self._motion)
        width = node.getBoundingClientRect().width - 16
        self._played = not self._played
        for bar in node.querySelectorAll("[data-m3x-bar]"):
            bar.style.transform = f"translateX({width if self._played else 0}px)"
