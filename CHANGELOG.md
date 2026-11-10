## Version 2.0.0
_Release date: 7 November 2026_

First release of m3-custom-theme, built on Anvil's Material 3 Theme v1.2.6. The package name stays `m3`.

**New components**
* Badge, BottomSheet, ButtonGroup, Carousel, Chip, DatePicker, Dialog, FabMenu, FloatingActionButton, ListItem, LoadingIndicator, NavigationBar, PaneLayout, SearchBar, SplitButton, Tabs, TimePicker, Toolbar and TopAppBar
* Snackbar and RichTooltip, as Python objects

**M3 Expressive**
* Button: `size`, `shape`, `toggle` and `selected`
* IconButton and ToggleIconButton: `size`, `button_width` and `shape`
* Slider: `size`
* LinearProgressIndicator and CircularProgressIndicator: `wavy`
* MenuItem: `selected`; DropdownMenu marks its current value
* NavigationRailLayout: `rail_style`, `rail_expanded` and `rail_adaptive`
* App-wide menu style: `m3x_theming.set_menu_style`

**Foundations**
* Eight palettes (`default`, `professional_blue`, `warm_coral`, `calm_teal`, `sophisticated_purple`, `sky_blue`, `forest_green`, `desert_rose`), each light and dark, as Theme editor presets and through `m3x_theming`; a new app starts on `professional_blue` light
* Design tokens for colour, typography, shape, elevation, state layers, motion and spacing (`theme/assets/m3x/tokens.css`)
* Spring motion from the M3 Expressive springs, with an expressive and a standard scheme (`m3x_motion`), and reduced-motion support in every animated component
* M3 window size classes (`m3x_adaptive`)

**Fixes**
* The Slider's value label now shows on scrolled pages
* InteractiveCard is enabled by default when created in code
* The side sheet follows the M3 specification for padding, the modal sheet's colour and corners, and motion
* A disabled outlined InteractiveCard's border uses the Outline colour
