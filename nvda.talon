next heading:
    key(h)

previous heading:
    key(shift-h)

previous option:
    user.with_nvda_mod_press('ctrl-left')

next option:
    user.with_nvda_mod_press('ctrl-right')

up option:
    user.with_nvda_mod_press('ctrl-up') 

down option:
    user.with_nvda_mod_press('ctrl-down')

toggle reader:
    user.toggle_nvda()


deck(pedal_left:repeat):    
    key(tab)
    sleep(.2)

Stop Reading:                          key(ctrl)
Start reading continuously:          
    key(capslock:down)
    key(down)
    key(capslock:up)
Read next item:                        key(down arrow)
Read next focusable item:              key(Tab)

Link:                                  key(Enter)
Button:                                key(Enter)

Go to next heading:                    key(H)
Go to next heading of level <user.number_signed_small>:    key(user.number_signed_small)

Go to next landmark:        key(D)

list all fields:  
    key(capslock:down)
    key(f7)
    key(capslock:up)

Go to next table:                       key(T)
Go to next list:                        key(L)
Go to next list item:                   key(I)

Go to next graphic:                     key(G)
Go to next link:                        key(K)
Go to next unvisited link:              key(U)
Go to next visited link:                key(V)
Next form field:                        key(F)
Next focusable item:                    key(Tab)
Next button:                            key(B)

Select and deselect:                    key(Spacebar)
Next checkbox:                          key(X)

Next combo box:                          key(C)

Toggle selection:                       key(up)
Next radio button:                       key(R)