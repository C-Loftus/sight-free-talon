from talon import Module, ui, Context
from talon.windows import ax as ax

mod = Module()

def get_every_child(element: ax.Element):
    if element:
        for child in element.children:
            if child.is_keyboard_focusable:
                yield child
            yield from get_every_child(child)

ctx = Context()

mod.list("dynamic_children", desc="List of children of the active window")

@ctx.dynamic_list("user.dynamic_children")
def dynamic_children(_) -> dict[str,str]:
    root = ui.active_window().element
    elements = list(get_every_child(root))

    return {str(i.name): str(i.name) for i in elements}

@mod.action_class
class Actions:
    def focus_element_by_name(name: str):
        """Focuses on an element by name"""
        root = ui.active_window().element
        elements = list(get_every_child(root))
        for element in elements:
            if element.name == name or \
            str(element.name).lower() == name:
                element.invoke_pattern.invoke()
                break
        else:
            print("Element not found")