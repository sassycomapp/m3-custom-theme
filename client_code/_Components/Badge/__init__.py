"""M3 Badge: a small dot, or a count, that marks new or unread items.
See docs/components/Badge.md in the project library.
"""
from anvil import HtmlTemplate

from ..._utils.properties import ComponentTag, anvil_prop, role_property
from ._anvil_designer import BadgeTemplate


class Badge(BadgeTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self.init_components(**properties)

    def _update(self):
        node = self.dom_nodes["m3x-badge"]
        count = self.count
        large = count is not None and count != ""
        node.classList.toggle("m3x-badge-large", large)
        node.classList.toggle("m3x-badge-small", not large)
        if not large:
            node.innerText = ""
            return
        count = int(count)
        limit = int(self.max_count or 999)
        node.innerText = f"{limit}+" if count > limit else str(count)

    @anvil_prop(default_value=None)
    @property
    def count(self, value) -> int:
        """The number shown. None shows a small dot without a number."""
        self._update()

    @anvil_prop(default_value=999)
    @property
    def max_count(self, value) -> int:
        """Counts above this number show as the number with a plus, e.g. 999+."""
        self._update()

    visible = HtmlTemplate.visible
    role = role_property("m3x-badge")

    #!componentEvent(m3.Badge)!1: {name: "show", description: "When the Badge is shown on the screen."}
    #!componentEvent(m3.Badge)!1: {name: "hide", description: "When the Badge is removed from the screen."}

    #!componentProp(m3.Badge)!1: {name:"count",type:"number",description:"The number shown. None shows a small dot without a number."}
    #!componentProp(m3.Badge)!1: {name:"max_count",type:"number",description:"Counts above this number show as the number with a plus."}
    #!componentProp(m3.Badge)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.Badge)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.Badge)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


#!defClass(m3, Badge, anvil.Component)!:
