tag: user.jaws_running
os: windows
-

# Reader press <user.keys>: Use the JAWS modifier to press any key
reader press <user.keys>: user.with_jaws_mod_press(keys)

# Reading commands
read below | start reading: user.with_jaws_mod_press("down")
next word: key(ctrl-right)
previous word: key(ctrl-left)
speak line | say line: user.with_jaws_mod_press("up")
next line: key(down)
previous line: key(up)
next paragraph: key(ctrl-down)
previous paragraph: key(ctrl-up)
stop speech | be quiet: key(ctrl)

# Date and time 
speak time | say time: user.with_jaws_mod_press("f12")
speak date | say date: user.with_jaws_mod_press("f12, f12")

# Toggle input help (JAWS help system for learning commands)
toggle input help: user.with_jaws_mod_press("1")

# JAWS settings (reader and synthesizer settings)
open JAWS settings | JAWS settings center: user.with_jaws_mod_press("6")

# Toggle speech (Toggle jaws sleep mode)
toggle speech | speech on demand: user.with_jaws_mod_layered_key_presses("space, s")
quick settings: user.with_jaws_mod_press("v")
increase speech rate | speak faster: key(ctrl-alt-super-pgup)
decrease speech rate | speak slower: key(ctrl-alt-super-pgdown)
increase jaws volume | jaws volume up | speak louder: user.with_jaws_mod_layered_key_presses("space, v, j, pgup, escape")
decrease jaws volume | jaws volume down| speak softer: user.with_jaws_mod_layered_key_presses("space, v, j, pgdown, escape")

# Navigating

#Window title
speak title | say title: user.with_jaws_mod_press("t")

# Move to search bar, address bar
go to search | go search bar | go to search bar: key(ctrl-e)
go to address bar | go address bar: key(alt-d)

# Open element lists (JAWS-specific commands to list elements on the page)
links list | list links: user.with_jaws_mod_press("f7")
headings list | list headings: user.with_jaws_mod_press("f6")
forms list | list forms: user.with_jaws_mod_press("f5")

# Reporting Location and Other Information
speak text formatting | speak formatting | say text formatting | say formatting: user.with_jaws_mod_press("f")
speak selection | say selection: user.with_jaws_mod_press("shift-a")
speak link destination | say link destination: user.with_jaws_mod_press("k")
speak window | say window | speak dialog | say dialog: user.with_jaws_mod_press("b")
speak focus | say focus | speak item | say item: user.with_jaws_mod_press("tab")

# Navigation commands for table, list, graphic, link, and form elements
next table: key(T)
previous table: key(shift-T)
next list: key(L)
previous list: key(shift-L)
next list item: key(I)
previous list item: key(shift-I)
next graphic: key(G)
previous graphic: key(shift-G)
next unvisited link: key(U)
previous unvisited link: key(shift-U)
next visited link: key(V)
previous visited link: key(shift-V)
Next form field: key(F)
Previous form field: key(shift-F)
Next edit box: key(E)
Previous edit box: key(shift-E)
Next combo box: key(C)
Previous combo box: key(shift-C)
Next tab: key(')
Previous tab: key(shift-')
Next button: key(B)
previous button: key(shift-B)
Next heading: key(H)
previous heading: key(shift-h)
next focusable item: key(tab)
previous focusable item: key(shift-tab)
next landmark | next region: key(r)
previous landmark | previous region: key(shift-r)

# Activate current element, press enter
activate | activate that press enter | hit enter: key(enter)

# Toggle selection for checkboxes, combo boxes, and radio buttons
check that | uncheck that: key(space)
open the box: key(alt-down)
Next checkbox: key(X)
previous checkbox: key(shift-X)
Next radio button: key(A)
Previous radio button: key(shift-A)

# Pass through next command (used to send the next key press directly to the system)
pass through next | pass through: user.with_jaws_mod_press("3")

# Restart JAWS (restarts the JAWS application)
restart reader | restart JAWS: user.restart_jaws()
