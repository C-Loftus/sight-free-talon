tag: user.nvda_running
os: windows
-

reader press <user.keys>: user.with_nvda_mod_press(keys)

next heading:
    key(h)
previous heading:
    key(shift-h)

previous option:
    user.with_nvda_mod_press('ctrl-left')

# In the menu, this will go to the next option
next option:
    user.with_nvda_mod_press('ctrl-right')

up option:
    user.with_nvda_mod_press('ctrl-up')

# In the menu, this will lower the value of the option
down option:
    user.with_nvda_mod_press('ctrl-down')

# reads everything from the current position down
read below:
    user.with_nvda_mod_press('down')

# If the user is in the middle of an echoed text and this will posit otherwise it will resume
pause speech:
    key(shift)

stop speech:
    key(ctrl)

speak line:
    user.with_nvda_mod_press('up')

mouse to navigator:
    user.with_nvda_mod_press('shift-m')

navigator to mouse:
    user.with_nvda_mod_press('shift-n')

next paragraph:
    key(ctrl-down)

previous paragraph:
    key(ctrl-up)

change verbosity:
    user.with_nvda_mod_press('p')

speak title:
    user.with_nvda_mod_press('t')

next focusable item:        key(tab)
next heading <number_small>: key("{number_small}")
previous heading  <number_small>: key("shift-{number_small}")

next landmark:              key(d)
previous landmark:          key(shift-d)
toggle speech mode:

open element list:
    user.with_nvda_mod_press('f7')

toggle input help:
    user.with_nvda_mod_press('1')

speak typed words:
    user.with_nvda_mod_press('3')

speak typed characters:
    user.with_nvda_mod_press('2')

speak command keys:
    user.with_nvda_mod_press('4')

follow system focus:
    user.with_nvda_mod_press('7')
follow system caret:
    user.with_nvda_mod_press('6')

toggle mouse tracking:
    user.with_nvda_mod_press('m')

open reader setings:
    user.with_nvda_mod_press('ctrl-g')

synthesizer settings:
    user.with_nvda_mod_press('ctrl-s')

speak time:
    user.with_nvda_mod_press('f12')

# Reporting Location and Other Information
speak text formatting:
    user.with_nvda_mod_press('f')

speak link destination:
    user.with_nvda_mod_press('k')

speak window:
    user.with_nvda_mod_press('b')

speak focus:
    user.with_nvda_mod_press('tab')

screen curtain:
    user.with_nvda_mod_press('ctrl-escape')

# sleep mode disables all NVDA commands and speech/braille
# output for the current application. This is most useful in
# applications that provide their own speech or screen reading
# features. Press this command again to disable sleep mode - note
# that NVDA will only retain the Sleep Mode setting until it is restarted.
toggle reader sleep:
    user.with_nvda_mod_press("shift-s")

next table:                 key(T)
next list:                  key(L)
next list item:             key(I)
next graphic:               key(G)
next link:                  key(K)
next unvisited link:        key(U)
next visited link:          key(V)
Next form field:            key(F)
Next button:                key(B)

toggle selection:           key(space)
Next checkbox:              key(X)

Next combo box:             key(C)

Toggle selection:           key(up)
Next radio button:          key(R)

braille display dialog:
    user.with_nvda_mod_press('ctrl-a')

pass through next:
    user.with_nvda_mod_press('f2')

restart reader:
    user.restart_nvda()

test reader add on:
    user.send_ipc_command("debug")

    