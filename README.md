# m3-custom-theme

A complete Material 3 (M3) theme for [Anvil](https://anvil.works) apps, including the M3 Expressive components and styles. It is built on Anvil's [Material 3 Theme](https://github.com/anvil-works/material-3-theme) v1.2.6 and keeps its package name, `m3`, so an app switches to it by changing one dependency, with no changes to its forms or code.

## What it adds to Anvil's theme

- **Every M3 component**: badges, bottom sheets, button groups, carousels, chips, date and time pickers, dialogs, FABs and FAB menus, list items, loading indicators, navigation bars, rich tooltips, search, snackbars, split buttons, tabs, toolbars, top app bars, and list-detail and supporting-pane layouts.
- **M3 Expressive**: button and icon button sizes and shapes, toggle buttons, slider sizes, wavy progress indicators, the Expressive navigation rail and Expressive menus.
- **Palettes and dark mode**: eight palettes, each light and dark, chosen in Anvil's Theme editor or from code.
- **Design tokens**: every colour, type size, shape, elevation, state layer, motion and spacing value as an `--m3x-*` CSS variable, taken from Google's Jetpack Compose Material 3 tokens.
- **Spring motion** from the M3 Expressive motion springs, with reduced-motion support.
- **Adaptive layouts** for the five M3 window size classes.

## How to use it

1. Open your app in the Anvil editor, then **Settings**, then **Dependencies**.
2. Remove Anvil's Material 3 Theme if the app has it.
3. Add a dependency on the **m3-custom-theme** app, version **v2.0.0**.

Everything in `m3` keeps working. The usage guide explains palettes, dark mode, menu style, motion, adaptive layouts and every component:
[usage guide](https://github.com/sassycomapp/m3-custom-theme-project-library/blob/main/docs/usage-guide.md).

## Demo

`Form1` in this app shows every component, in every variant and state, with the palette and mode controls at the top. Run the app to see it.

## Licence

The theme is released under the MIT licence in [LICENSE](LICENSE), which keeps Anvil's notice for the original theme.
