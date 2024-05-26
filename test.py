from tkinter import *
from tkinter import font


# root = Tk()
# root.title('Font Families')
# fonts=list(font.families())
# fonts.sort()

# # display = Listbox(root)
# # display.pack(fill=BOTH, expand=YES, side=LEFT)

# # scroll = Scrollbar(root)
# # scroll.pack(side=RIGHT, fill=Y, expand=NO)

# # scroll.configure(command=display.yview)
# # display.configure(yscrollcommand=scroll.set)

# for item in fonts:
#     Label(root,text=item,font=(item,12,)).pack(side="top")

# root.mainloop()


root = Tk()
root.geometry("300x300+100+100")
root.resizable(False, False)


# root.bind_all("<<UpdateOne>>", lambda event: print(f'Root Event: {event}'))
# root.bind_all("<<UpdateTwo>>", lambda event: print(f'Root Event: {event}'))

frame1 = Frame(root)
frame1.pack(side="top", expand=True, fill=BOTH)

frame1.bind("<<UpdateOne>>", lambda event: print(event))

button1 = Button(
    frame1, text="Button 1", command=lambda: frame1.event_generate("<<UpdateOne>>")
)
button1.pack(side="bottom")


frame2 = Frame(
    root,
)
frame2.pack(side="top", expand=True, fill="both")

frame2.bind("<<UpdateTwo>>", lambda event: print(event))


button2 = Button(
    frame2, text="Button 2", command=lambda: frame2.event_generate("<<UpdateTwo>>")
)


button2.pack(side="bottom")

root.mainloop()
