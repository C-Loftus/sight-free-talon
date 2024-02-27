from talon import Module, ui, Context, actions
from talon.windows import ax as ax

mod = Module()


def get_every_child(element: ax.Element):
    if element:
        for child in element.children:
            if (
                child.is_keyboard_focusable
                or child.is_content_element
                or child.is_enabled
            ):
                yield child
            yield from get_every_child(child)


ctx = Context()


mod.list(
    "accessibility_element_name",
    desc="List of children accessibility elements of the active window",
)


@ctx.dynamic_list("user.accessibility_element_name")
def dynamic_children(phrase) -> dict[str, str]:
    root = ui.active_window().element
    elements = list(get_every_child(root))

    """
    If you don't want to use a ctx.selection you can
    alternatively use spoken forms with a context list.
    Not super clear which option is preferred
    """
    # spoken_forms = {}
    # for e in elements:
    #     spoken_form = actions.user.create_spoken_forms(e.name, generate_subsequences=False)
    #     if CAN_BE_SPOKEN := (len(spoken_form) > 0):
    #         for form in spoken_form:
    #             spoken_forms[form] = e.name
    # return spoken_forms
    """ctx.selection lists are returned as a new string separated by 2 newlines"""
    selection_string = ""
    for e in elements:
        assert (
            type(e.name) == str
        ), f"Element name is not a string: {e.name} {e} {type(e)}"
        selection_string += str(e.name).lower() + "\n\n"

    return selection_string


@mod.action_class
class Actions:

    def focus_element_by_name(name: str, permissive: bool = True):
        """Focuses on an element by name. Change permissive to False to require an exact match."""
        root = ui.active_window().element
        elements = list(get_every_child(root))
        for element in elements:

            if element.name.lower() == name.lower() or (
                permissive and name.lower() in element.name.lower()
            ):
                try:
                    element.invoke_pattern.invoke()
                except Exception as e:
                    try:
                        # https://learn.microsoft.com/en-us/windows/win32/winauto/selflag
                        # SELFLAG_TAKESELECTION = 2
                        # Ideally we would use .select() but the API doesn't work
                        element.legacyiaccessible_pattern.do_default_action()
                    except Exception as f:
                        actions.user.tts(f"Failed to focus {name}")
                        print(e, f)
                break
        else:
            raise ValueError(f"Element '{name}' not found")
