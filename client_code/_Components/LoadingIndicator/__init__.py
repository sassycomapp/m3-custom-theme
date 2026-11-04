"""M3 Expressive loading indicator: a shape that morphs and turns while content
loads. See docs/components/LoadingIndicator.md in the project library.
"""
from anvil import HtmlTemplate
from anvil.js import window

from ..._utils import m3x_loading
from ..._utils.properties import ComponentTag, anvil_prop, role_property
from ._anvil_designer import LoadingIndicatorTemplate

_SVG_NS = "http://www.w3.org/2000/svg"
_ALIGN = {"left": "flex-start", "center": "center", "right": "flex-end"}


class LoadingIndicator(LoadingIndicatorTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self.init_components(**properties)
        self._draw()

    def _draw(self):
        shape = self.dom_nodes["m3x-loading-indicator-shape"]
        values = m3x_loading.morph_values()
        shape.setAttribute("d", values[0])
        if window.matchMedia("(prefers-reduced-motion: reduce)").matches:
            return  # Reduced motion: the first shape, still.
        steps = len(values) - 1
        duration = f"{steps * m3x_loading.MORPH_MS}ms"
        key_times = ";".join(f"{i / steps:.4f}" for i in range(steps + 1))
        # Each morph eases in and out, like the spring Compose uses.
        splines = ";".join(["0.2 0 0 1"] * steps)
        for tag, attribute, items in (
            ("animate", "d", values),
            ("animateTransform", "transform", m3x_loading.rotation_values()),
        ):
            node = window.document.createElementNS(_SVG_NS, tag)
            node.setAttribute("attributeName", attribute)
            if tag == "animateTransform":
                node.setAttribute("type", "rotate")
            node.setAttribute("dur", duration)
            node.setAttribute("repeatCount", "indefinite")
            node.setAttribute("calcMode", "spline")
            node.setAttribute("keyTimes", key_times)
            node.setAttribute("keySplines", splines)
            node.setAttribute("values", ";".join(items))
            shape.appendChild(node)

    @anvil_prop(default_value=False)
    @property
    def contained(self, value) -> bool:
        """If True, the shape sits in a round coloured container."""
        self.dom_nodes["m3x-loading-indicator"].classList.toggle(
            "m3x-loading-indicator-contained", bool(value)
        )

    @anvil_prop(default_value="Loading")
    @property
    def label(self, value) -> str:
        """The name of the indicator for screen readers."""
        self.dom_nodes["m3x-loading-indicator"].setAttribute(
            "aria-label", value or "Loading"
        )

    @anvil_prop(default_value="left")
    @property
    def align(self, value) -> str:
        """The position of this component in the available space."""
        self.dom_nodes["m3x-loading-indicator"].style.alignSelf = _ALIGN.get(
            value, "flex-start"
        )

    visible = HtmlTemplate.visible
    role = role_property("m3x-loading-indicator")

    #!componentEvent(m3.LoadingIndicator)!1: {name: "show", description: "When the indicator is shown on the screen."}
    #!componentEvent(m3.LoadingIndicator)!1: {name: "hide", description: "When the indicator is removed from the screen."}

    #!componentProp(m3.LoadingIndicator)!1: {name:"contained",type:"boolean",description:"If True, the shape sits in a round coloured container."}
    #!componentProp(m3.LoadingIndicator)!1: {name:"label",type:"string",description:"The name of the indicator for screen readers."}
    #!componentProp(m3.LoadingIndicator)!1: {name:"align",type:"enum",options:["left", "center", "right"],description:"The position of this component in the available space."}
    #!componentProp(m3.LoadingIndicator)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.LoadingIndicator)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.LoadingIndicator)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, LoadingIndicator, anvil.Component)!:
