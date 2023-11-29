from talon import Module, actions, ui, Context, ctrl
import os

mod = Module()

if os.name == 'nt':
    import winsound


@mod.action_class
class Actions:
    def indentation_level(text: str) -> int:
        '''count how many tabs are at the start of the line'''

        space_count = 0
        tab_count = 0
        for char in text:
            if char == '\t':
                tab_count += 1
            elif char == ' ':
                space_count += 1
            else:
                break  # Stop counting when a non-tab character is encountered
        # every 4 spaces is a tab
        tab_count += (space_count // 4)
        return tab_count

    def echo_context(include_title: bool = False):
        """Echo the current context"""
        friendly_name = actions.app.name() 
        title = ui.active_window().title 
        output = f"{friendly_name} {title}" if include_title else friendly_name
        actions.user.robot_tts(output)

    def extract_text():
        """Extract the text from the current window"""


    
ctxWindows = Context()
ctxWindows.matches = r"""
os: windows
"""

@ctxWindows.action_class("user")
class ActionsWin:
    def extract_text():
        """Extract the text from the current window. You 
        need powertoys or Windows 11 for this to work"""

        saved_x, saved_y = (actions.mouse_x(), actions.mouse_y())

        active_win = ui.active_window().rect
        actions.mouse_move(active_win.x, active_win.y)
        actions.user.notify(str(active_win.x) + " " + str(active_win.y) + " " + str(active_win.width) + " " + str(active_win.height))
        actions.key('super-shift-t')
        actions.sleep("2s")
        actions.mouse_drag(0)
        actions.sleep("1s")
        actions.mouse_move(active_win.x + active_win.width, active_win.y + active_win.height)
        actions.mouse_release(0)        
        actions.sleep("3s")
        actions.mouse_move(saved_x, saved_y)
    
    def beep(duration: int = 1000, freq: int = 440):
        """Beep"""
        winsound.Beep(freq, duration)


        