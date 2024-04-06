tag: user.nvda_running
and tag: browser
-

# NVDA requires a pass through to copy
# text select via the mouse
^control cap$:
    user.with_nvda_mod_press("f2")
    sleep(0.5)
    edit.copy()

^copy (that | this)$:
    user.with_nvda_mod_press("f2")
    sleep(0.5)
    edit.copy()
