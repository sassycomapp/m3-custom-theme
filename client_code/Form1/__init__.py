"""Demo and test form for the M3 custom theme.

Shows every existing component in each of its variants and states. It is the
test harness for every later step (see m3-custom-theme.md, Step 3). Add each new
component here, in every variant and state, before merging it.
"""
from anvil import *
import m3.components as m3

from ._anvil_designer import Form1Template

BUTTON_APPEARANCES = ["filled", "elevated", "tonal", "outlined", "text"]
ICON_BUTTON_APPEARANCES = ["standard", "filled", "tonal", "outlined"]
CARD_APPEARANCES = ["elevated", "filled", "outlined"]
AVATAR_APPEARANCES = ["filled", "tonal", "outlined"]
TEXT_INPUT_APPEARANCES = ["filled", "outlined"]
SCALES = ["small", "medium", "large"]

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

        self._heading("M3 custom theme: demo and test form", "display", "small")
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
