import anvil.designer
from anvil import *
from anvil import HtmlTemplate

from ..._utils.properties import (
    anvil_prop,
    border_property,
    color_property,
    enabled_property,
    get_unset_margin,
    margin_property,
    role_property,
    style_property,
    tooltip_property,
)
from ._anvil_designer import IconButtonTemplate


class IconButton(IconButtonTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._tooltip_node = None
        self._appearance = ""
        self.init_components(**properties)
        self.dom_nodes['anvil-m3-iconbutton-container'].addEventListener(
            'click', self._handle_click
        )

    def _anvil_get_unset_property_values_(self):
        el = self.dom_nodes["anvil-m3-iconbutton-container"]
        m = get_unset_margin(el, self.margin)
        return {"margin": m}

    def _handle_click(self, event):
        event.preventDefault()
        self.raise_event(
            "click",
            event=event,
            keys={
                "shift": event.shiftKey,
                "alt": event.altKey,
                "ctrl": event.ctrlKey,
                "meta": event.metaKey,
            },
        )

    #!componentProp(m3.IconButton)!1: {name:"align",type:"enum",description:"The position of this component in the available space."}
    #!componentProp(m3.IconButton)!1: {name:"appearance",type:"enum",options:["standard", "filled", "tonal", "outlined"],description:"A predefined style for this component."}
    #!componentProp(m3.IconButton)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.IconButton)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
    #!componentProp(m3.IconButton)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"}
    #!componentProp(m3.IconButton)!1: {name:"icon",type:"enum",description:"The icon to display on this component."}
    #!componentProp(m3.IconButton)!1: {name:"icon_color",type:"color",description:"The colour of the icon displayed on this component."}
    #!componentProp(m3.IconButton)!1: {name:"background_color",type:"color",description:"The colour of the background of this component."}
    #!componentProp(m3.IconButton)!1: {name:"margin",type:"margin",description:"The margin (pixels) of the component."}
    #!componentProp(m3.IconButton)!1: {name:"border",type:"string",description:"The border of this component. Can take any valid CSS border value."}
    #!componentProp(m3.IconButton)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
    #!componentProp(m3.IconButton)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}

    #!componentEvent(m3.IconButton)!1: {name: "click", description: "When the component is clicked.", parameters:[]}

    visible = HtmlTemplate.visible
    enabled = enabled_property('anvil-m3-iconbutton-container')
    align = style_property('anvil-m3-iconbutton-component', 'justifyContent', 'align')
    border = border_property('anvil-m3-iconbutton-container')
    icon_color = color_property('anvil-m3-iconbutton-icon', 'color', 'icon_color')
    background_color = color_property(
        'anvil-m3-iconbutton-container', 'backgroundColor', 'background_color'
    )
    margin = margin_property('anvil-m3-iconbutton-container')
    role = role_property('anvil-m3-iconbutton-container')
    tooltip = tooltip_property('anvil-m3-iconbutton-container')

    @anvil_prop
    @property
    def icon(self, value) -> str:
        """The icon to display on this component."""
        self.dom_nodes['anvil-m3-iconbutton-icon'].innerText = value[3:]

    @anvil_prop
    @property
    def appearance(self, value) -> str:
        """A predefined style for this component."""
        self.dom_nodes['anvil-m3-iconbutton-container'].classList.toggle(
            "anvil-m3-filled", False
        )
        self.dom_nodes['anvil-m3-iconbutton-container'].classList.toggle(
            "anvil-m3-tonal", False
        )
        self.dom_nodes['anvil-m3-iconbutton-container'].classList.toggle(
            "anvil-m3-outlined", False
        )
        self.dom_nodes['anvil-m3-iconbutton-icon'].classList.toggle(
            "anvil-m3-filled", False
        )
        self.dom_nodes['anvil-m3-iconbutton-icon'].classList.toggle(
            "anvil-m3-tonal", False
        )
        self.dom_nodes['anvil-m3-iconbutton-icon'].classList.toggle(
            "anvil-m3-outlined", False
        )
        if value and value != 'standard':
            self.dom_nodes['anvil-m3-iconbutton-container'].classList.toggle(
                f'anvil-m3-{value}', True
            )
            self.dom_nodes['anvil-m3-iconbutton-icon'].classList.toggle(
                f'anvil-m3-{value}', True
            )

    # m3x: Expressive sizes, widths and shapes (Step 7, E2). The defaults keep
    # the base look: size "standard", width "default", shape "round".
    @anvil_prop(default_value="standard")
    @property
    def size(self, value) -> str:
        """standard (the base icon button), or an Expressive size: xsmall,
        small, medium, large or xlarge."""
        sized = value not in (None, "", "standard")
        for key in ('anvil-m3-iconbutton-component-container',
                    'anvil-m3-iconbutton-container'):
            node = self.dom_nodes[key]
            for name in ("xsmall", "small", "medium", "large", "xlarge"):
                node.classList.toggle(f"m3x-iconbutton-{name}", name == value)
            node.classList.toggle("m3x-iconbutton-sized", sized)

    @anvil_prop(default_value="default")
    @property
    def button_width(self, value) -> str:
        """narrow, default or wide: the space beside the icon (Expressive sizes)."""
        node = self.dom_nodes['anvil-m3-iconbutton-container']
        for name in ("narrow", "wide"):
            node.classList.toggle(f"m3x-iconbutton-{name}", name == value)

    @anvil_prop(default_value="round")
    @property
    def shape(self, value) -> str:
        """round (a circle or pill) or square (rounded corners)."""
        self.dom_nodes['anvil-m3-iconbutton-container'].classList.toggle(
            "m3x-iconbutton-square", value == "square")

    #!componentProp(m3.IconButton)!1: {name:"size",type:"enum",options:["standard", "xsmall", "small", "medium", "large", "xlarge"],description:"standard (the base icon button), or an Expressive size."}
    #!componentProp(m3.IconButton)!1: {name:"button_width",type:"enum",options:["narrow", "default", "wide"],description:"The space beside the icon."}
    #!componentProp(m3.IconButton)!1: {name:"shape",type:"enum",options:["round", "square"],description:"round or square."}


#!defClass(m3,IconButton,anvil.Component)!:
