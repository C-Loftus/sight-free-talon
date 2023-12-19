from talon import Module, actions, Context

soundContext = Context()
 
class ActionClass:
    def key(key: str):
        """Presses a key"""
        actions.beep()
        actions.next(key)