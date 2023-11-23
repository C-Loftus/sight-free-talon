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

toggle reader:
    user.toggle_nvda() 

# reads everything from the current position down
echo below:
    user.with_nvda_mod_press('down')

# If the user is in the middle of an echoed text and this will posit otherwise it will resume
toggle echo: 
    key(shift)

stop speech:
    key(ctrl)

read current line:
    user.with_nvda_mod_press('up')

move mouse to current navigator object:
    user.with_nvda_mod_press('shift-m')

navigate to mouse:
    user.with_nvda_mod_press('shift-n')


deck(pedal_left:repeat):    
    key(tab)
    sleep(.2)


read title:
    user.with_nvda_mod_press('t')

next focusable item:              key(tab)
next heading <number_small>:    key("{number_small}")
previous heading  <number_small>:   key("shift-{number_small}")

Go to next landmark:        key(D)

list all fields:  
    user.with_nvda_mod_press('f7')

toggle input help:
    user.with_nvda_mod_press('1')

speak typed words:
    user.with_nvda_mod_press('3')

speak typed characters:
    user.with_nvda_mod_press('2')

speak command keys:
    user.with_nvda_mod_press('4')

toggle mouse tracking:
    user.with_nvda_mod_press('m')

open reader setings:
    user.with_nvda_mod_press('ctrl-g')

open synthesizer settings:
    user.with_nvda_mod_press('ctrl-s')

# sleep mode disables all NVDA commands and speech/braille 
# output for the current application. This is most useful in 
# applications that provide their own speech or screen reading 
# features. Press this command again to disable sleep mode - note 
# that NVDA will only retain the Sleep Mode setting until it is restarted.
toggle reader sleep:
    user.with_nvda_mod_press("shift-s")
    
Go to next table:                       key(T)
Go to next list:                        key(L)
Go to next list item:                   key(I)

Go to next graphic:                     key(G)
Go to next link:                        key(K)
Go to next unvisited link:              key(U)
Go to next visited link:                key(V)
Next form field:                        key(F)
Next button:                            key(B)

toggle selection:                    key(space)
Next checkbox:                          key(X)

Next combo box:                          key(C)

Toggle selection:                       key(up)
Next radio button:                       key(R)