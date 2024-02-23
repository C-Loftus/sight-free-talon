from talon import Module, ui, Context, actions
from talon.windows import ax as ax

mod = Module()

def get_every_child(element: ax.Element):
    if element:
        for child in element.children:
            if child.is_keyboard_focusable:
                yield child
            yield from get_every_child(child)

ctx = Context()

mod.list("dynamic_children", desc="List of children accessibility elements of the active window")

@ctx.dynamic_list("user.dynamic_children")
def dynamic_children(phrase) -> dict[str,str]:

    root = ui.active_window().element
    elements = list(get_every_child(root))

    spoken_forms = {}
    for e in elements:
        spoken_form = actions.user.create_spoken_forms(e.name, generate_subsequences=False)
        if CAN_BE_SPOKEN := (len(spoken_form) > 0):
            for form in spoken_form:
                spoken_forms[form] = e.name

    return spoken_forms

@mod.action_class
class Actions:

    def focus_element_by_name(name: str):
        """Focuses on an element by name"""
        root = ui.active_window().element
        elements = list(get_every_child(root))
        for element in elements:
            if str(element.name).lower() == str(name).lower():
                try:
                    element.invoke_pattern.invoke()
                except Exception as e:
                    actions.user.tts(f"Failed to focus {name}")
                    print(e)
                break
        else:
            print("Element not found")
