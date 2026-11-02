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
        "RadioButton",
        m3.RadioButton,
        [
            dict(text="Option A", group="demo-radio", value="a", selected=True),
            dict(text="Option B", group="demo-radio", value="b"),
            dict(text="Disabled", group="demo-radio", value="c", enabled=False),
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
