"""M3 canonical pane layouts: list-detail and supporting pane.
See docs/components/PaneLayout.md in the project library.

Put components in the two slots: pane-primary and pane-secondary.

    list_detail  The primary pane is a list, the secondary pane the chosen
                 item's detail. Compact and medium windows show one pane at a
                 time (show_secondary chooses which); wider windows show both.
    supporting   The primary pane is the main content, the secondary pane
                 supports it. Compact and medium windows stack the supporting
                 pane below; wider windows put it beside the main content.

From the expanded class up, the list (list_detail) or the supporting pane
(supporting) is fixed_pane_width wide, and the other pane takes the rest.
"""
from anvil import HtmlTemplate
from anvil.designer import in_designer

from ..._utils import m3x_adaptive
from ..._utils.properties import ComponentTag, anvil_prop, role_property
from ._anvil_designer import PaneLayoutTemplate

_LAYOUTS = ("list_detail", "supporting")


class PaneLayout(PaneLayoutTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._stop = None
        self.init_components(**properties)
        if in_designer:
            # The designer shows both panes, so components can go in either.
            self.dom_nodes["m3x-panes"].classList.add("m3x-panes-in-designer")
        self.add_event_handler("x-anvil-page-added", self._on_page_added)
        self.add_event_handler("x-anvil-page-removed", self._on_page_removed)

    def add_component(self, component, slot="pane-primary", **layout_props):
        """Add a component to a pane: slot is "pane-primary" or "pane-secondary"."""
        super().add_component(component, slot=slot, **layout_props)

    @property
    def is_single_pane(self):
        """True while the window is narrow enough to show one pane at a time."""
        return m3x_adaptive.is_single_pane()

    def _on_page_added(self, **event_args):
        self._stop = m3x_adaptive.on_change(
            lambda name: self.raise_event("width_class_change", width_class=name))

    def _on_page_removed(self, **event_args):
        if self._stop:
            self._stop()
            self._stop = None

    @anvil_prop(default_value="list_detail")
    @property
    def layout(self, value) -> str:
        """list_detail or supporting."""
        node = self.dom_nodes["m3x-panes"]  # Set before __init__ ends.
        for name in _LAYOUTS:
            node.classList.toggle(f"m3x-panes-{name}", name == (value or "list_detail"))

    @anvil_prop(default_value=False)
    @property
    def show_secondary(self, value) -> bool:
        """list_detail on narrow windows: True shows the detail pane."""
        self.dom_nodes["m3x-panes"].classList.toggle("m3x-panes-show-secondary",
                                                     bool(value))

    @anvil_prop(default_value=360)
    @property
    def fixed_pane_width(self, value) -> float:
        """The fixed pane's width (px) on wide windows."""
        self.dom_nodes["m3x-panes"].style.setProperty(
            "--m3x-panes-fixed-width", f"{value or 360}px")

    visible = HtmlTemplate.visible
    role = role_property("m3x-panes")

    #!componentEvent(m3.PaneLayout)!1: {name: "width_class_change", description: "When the window moves to another size class.", parameters:[{name: "width_class", description: "compact, medium, expanded, large or extra_large."}]}
    #!componentEvent(m3.PaneLayout)!1: {name: "show", description: "When the component is shown on the screen."}
    #!componentEvent(m3.PaneLayout)!1: {name: "hide", description: "When the component is removed from the screen."}

    #!componentProp(m3.PaneLayout)!1: {name:"layout",type:"enum",options:["list_detail", "supporting"],description:"list_detail or supporting."}
    #!componentProp(m3.PaneLayout)!1: {name:"show_secondary",type:"boolean",description:"list_detail on narrow windows: True shows the detail pane."}
    #!componentProp(m3.PaneLayout)!1: {name:"fixed_pane_width",type:"number",description:"The fixed pane's width (px) on wide windows."}
    #!componentProp(m3.PaneLayout)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.PaneLayout)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.PaneLayout)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, PaneLayout, anvil.Component)!:
