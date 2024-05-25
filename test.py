from tkinter import *
from tkinter import font


root = Tk()
root.title('Font Families')
fonts=list(font.families())
fonts.sort()

# display = Listbox(root)
# display.pack(fill=BOTH, expand=YES, side=LEFT)

# scroll = Scrollbar(root)
# scroll.pack(side=RIGHT, fill=Y, expand=NO)

# scroll.configure(command=display.yview)
# display.configure(yscrollcommand=scroll.set)

for item in fonts:
    Label(root,text=item,font=(item,12,)).pack(side="top")

root.mainloop()