"""Demo and test form for the M3 custom theme.

Shows every existing component in each of its variants and states. It is the
test harness for every later step (see m3-custom-theme.md, Step 3). Add each new
component here, in every variant and state, before merging it.
"""
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
        self._html(f'<div style="display:flex;flex-wrap:wrap;gap:24px;">{cells}</div>')

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
