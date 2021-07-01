import tkinter as tk
from tkinter import filedialog
from tkinter import *
import os



root = tk.Tk()
t = Text(root)
t.pack()
t.insert(END, '''\
blah blah blah Failed blah blah
blah blah blah Passed blah blah
blah blah blah Failed blah blah
blah blah blah Mine blah blah
''')
# while True:


    
print(t.search("Failed", 1.0, END))
print(len("Failed"))

keyword = "Failed"
keywordLength = len(keyword)
lineNumber = 1
indexNumber = t.search(keyword, 1.0, END)

t.tag_config("failed", background='red')
t.tag_add("failed", indexNumber, indexNumber+keywordLength*.1)





print(keyword)
print(indexNumber)
print (keywordLength)
print (indexNumber+keywordLength*.1)

# t.search(keyword, indexNumber, indexNumber+keywordLength)









# failed = "Failed"
# passed = "passed"
# mine = "mine"

# t.tag_config("failed", background='red')
# t.tag_config(passed, background='blue')
# t.tag_config(mine, background='green')
# # t.tag_config(name of the tag, what properties)
# def search(text_widget, keyword, tag):
#     pos = '1.0'
#     while True:
#         idx = text_widget.search(keyword, pos, END)
#         if not idx:
#             break
#         pos = '{}+{}c'.format(idx, len(keyword))
#         text_widget.tag_add(tag, idx, pos)

# search(t, failed, 'failed')
# search(t, 'Passed', 'passed')
# search (t, 'Mine', mine)
# #function of (text box, search term, tag applied)

# #t.tag_delete('failed')
# #t.tag_delete('passed')

root.mainloop()