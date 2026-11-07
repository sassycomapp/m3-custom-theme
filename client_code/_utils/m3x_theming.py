"""Palette and light/dark mode switching for the M3 custom theme.

The theme's colours are CSS variables. Two attributes on the page's root element
choose which values apply (see theme/assets/m3x/palettes.css):

    data-m3x-palette   one of PALETTES.
    data-m3x-theme     "light", "dark" or "system" (follow the device).

The colour preset chosen in Anvil's Theme editor sets the app's starting palette
and mode. An app may change them at start-up, for example from a per-client
setting, and may offer them to the user. A choice made through set_palette or
set_mode is remembered in the browser and wins over the editor preset.
See m3-custom-theme.md, Step 4.
"""
import anvil
from anvil.js import window

from .m3x_presets import BY_PRIMARY, PALETTES

MODES = ("light", "dark", "system")
MENU_STYLES = ("baseline", "standard", "vibrant")

_PALETTE_ATTRIBUTE = "data-m3x-palette"
_MODE_ATTRIBUTE = "data-m3x-theme"
_PALETTE_KEY = "m3x-palette"
_MODE_KEY = "m3x-theme"
_MENU_ATTRIBUTE = "data-m3x-menu-style"


def _root():
    return window.document.documentElement


def _remember(key, value):
    try:
        window.localStorage.setItem(key, value)
    except Exception:
        pass  # Storage can be blocked by the browser. The choice then lasts one visit.


def _recall(key):
    try:
        return window.localStorage.getItem(key)
    except Exception:
        return None


def editor_preset():
    """The (palette, mode) of the colour preset chosen in Anvil's Theme editor.

    A colour scheme that matches no preset counts as ("default", "light").
    """
    try:
        primary = str(anvil.app.theme_colors["Primary"]).strip().upper()
    except Exception:
        return ("default", "light")
    return BY_PRIMARY.get(primary, ("default", "light"))


def get_palette():
    """The palette in use: one of PALETTES."""
    value = _root().getAttribute(_PALETTE_ATTRIBUTE)
    return value if value in PALETTES else editor_preset()[0]


def set_palette(name, remember=True):
    """Switch palette. name is one of PALETTES."""
    if name not in PALETTES:
        raise ValueError(f"Unknown palette {name!r}. Choose one of {PALETTES}")
    _root().setAttribute(_PALETTE_ATTRIBUTE, name)
    if remember:
        _remember(_PALETTE_KEY, name)


def get_mode():
    """The mode chosen: "light", "dark" or "system"."""
    value = _root().getAttribute(_MODE_ATTRIBUTE)
    return value if value in MODES else editor_preset()[1]


def set_mode(mode, remember=True):
    """Switch mode. mode is "light", "dark" or "system" (follow the device)."""
    if mode not in MODES:
        raise ValueError(f"Unknown mode {mode!r}. Choose one of {MODES}")
    # The dark colours belong to a palette, so a palette is always set with a mode.
    if _root().getAttribute(_PALETTE_ATTRIBUTE) not in PALETTES:
        set_palette(get_palette(), remember=False)
    _root().setAttribute(_MODE_ATTRIBUTE, mode)
    if remember:
        _remember(_MODE_KEY, mode)


def is_dark():
    """True if the page is showing dark colours right now."""
    mode = get_mode()
    if mode == "system":
        return bool(window.matchMedia("(prefers-color-scheme: dark)").matches)
    return mode == "dark"


def get_menu_style():
    """The menu style in use: "baseline", "standard" or "vibrant"."""
    value = _root().getAttribute(_MENU_ATTRIBUTE)
    return value if value in MENU_STYLES else "baseline"


def set_menu_style(style):
    """Choose the look of every menu in the app (button, icon button, avatar and
    dropdown menus):

        baseline  the base M3 menu (the default).
        standard  the M3 Expressive menu: rounded, in Surface Container Low;
                  selected items in Tertiary Container.
        vibrant   the M3 Expressive menu in Tertiary Container; selected items
                  in Tertiary.

    Call it once at start-up, like set_palette. See docs/components/Menu.md.
    """
    if style not in MENU_STYLES:
        raise ValueError(f"Unknown menu style {style!r}. Choose one of {MENU_STYLES}")
    if style == "baseline":
        _root().removeAttribute(_MENU_ATTRIBUTE)
    else:
        _root().setAttribute(_MENU_ATTRIBUTE, style)


def apply_saved():
    """Apply the palette and mode this browser last chose, or else the editor
    preset's. Call once at start-up."""
    palette, mode = editor_preset()
    saved_palette = _recall(_PALETTE_KEY)
    saved_mode = _recall(_MODE_KEY)
    set_palette(saved_palette if saved_palette in PALETTES else palette,
                remember=False)
    set_mode(saved_mode if saved_mode in MODES else mode, remember=False)
