import tkinter as tk
from tkinter import filedialog
from tkinter import *
import os

background_color = "#e6e6ff"
cur_dir = os.getcwd()


root = tk.Tk()
root.title("EDL Parser - for Vantage")
root.geometry ("850x900")



# #New - Clear content
# def new_file(x):
# 	edlTxt.delete("1.0", "end")
# 	cmlTxt.delete("1.0", "end")

# #Open File
# def open_file(x):
# 	edlTxt.delete("1.0", "end")
# 	cmlTxt.delete("1.0", "end")
# 	edl_file = filedialog.askopenfilename(initialdir=cur_dir, title="Open Avid EDL", filetypes=(("Avid EDL", "*.edl"),))
# 	edl_file = open(edl_file, 'r')
# 	content = edl_file.readlines()
# 	edl_file.close()	
# 	for line in content:
# 		# line=line.strip()
# 		edlTxt.insert ("end", line)
# 		# print(line)






# 	parse_edl()




# #Parse EDL data
# def parse_edl():
# 	cmlTxt.delete("1.0", "end")
# 	cml_parsed = edlTxt.get("1.0", "end").splitlines()  #each line in the text box as a list item
# 	cmlItems=[] #nested list with everything
# 	edlList=[]  
# 	curCount=0
# 	dropFrame=False
# 	for line in cml_parsed:
# 		if line =="FCM: DROP FRAME":
# 			dropFrame = True
# 		splitColumns=line.split()  #breaks each line into a list of words
# 		edlList.append(splitColumns)
		
# 		if line.find("NBTITLE") != -1:
# 			cmlList=[]  #short term list of a single instance
# 			if dropFrame == True:
# 				nbTitle = edlList[curCount][1]  #NB Title
# 				inPoint= edlList[curCount-1][-2] #In point
# 				outPoint = edlList[curCount-1][-1] #Out Point
# 				inPoint= inPoint.replace(":", ";").replace(";", ":", 2) #sets dropframe formattting
# 				outPoint= outPoint.replace(":", ";").replace(";", ":", 2) #sets dropframe formattting

# 				cmlList.append(nbTitle)
# 				cmlList.append(inPoint)
# 				cmlList.append(outPoint)
# 				cmlItems.append(cmlList) 

# 			else:
# 				cmlList.append(edlList[curCount][1])  #NB Title
# 				cmlList.append(edlList[curCount-1][-2]) #In point
# 				cmlList.append(edlList[curCount-1][-1]) #Out Point
# 				cmlItems.append(cmlList) #nested list with everything

# 		curCount +=1
# 	generateCml(cmlItems)


# def generateCml(cmlItems):
# 	layer=1  #sequence layer and video source
# 	#insert first part of header
# 	cmlTxt.insert("end", '<?xml version="1.0" encoding="utf-8"?>\n')
# 	cmlTxt.insert("end", '<Composition xmlns="Telestream.Soa.Facility.Playlist">\n')
# 	cmlTxt.insert("end", '  <Source identifier="999999">\n')
# 	cmlTxt.insert("end", '    <File location="{$#Original}" />\n')
# 	cmlTxt.insert("end", '    <Subtitle />\n')
# 	cmlTxt.insert("end", '  </Source>\n')
	
# 	for ee in cmlItems:  #inserts sources in header
# 		cmlTxt.insert("end", '  <Source identifier="' + str(layer) +'">\n')
# 		cmlTxt.insert("end", '    <File location="{$$Source File Path}\\' + cmlItems[layer-1][0].lower() + '" />\n')
# 		cmlTxt.insert("end", '  </Source>\n\n')
# 		layer+=1

# 	#insert last part of header wich includes the video source for the first segment
# 	cmlTxt.insert("end", '<Sequence layer="1">\n')
# 	cmlTxt.insert("end", '   <Segment>\n')
# 	cmlTxt.insert("end", '    <Video source="999999" />\n')
# 	cmlTxt.insert("end", '   </Segment>\n')
# 	cmlTxt.insert("end", '    </Sequence>\n')
# 	cmlTxt.insert("end", '\n')

# 	layer=1 #resets layer for next for loop



# 	for e in cmlItems:  #creates the edits
# 		nbTitle=e[0]
# 		inEdit = e[1]
# 		outEdit = e[2]		
# 		cmlTxt.insert("end", f'  <Sequence layer="{layer+1}">\n')
# 		cmlTxt.insert("end",'   <Segment>\n')
# 		cmlTxt.insert("end",'    <Video source="'+ str(layer) + '" align="head" adjust="edge" offset="{' + inEdit + '@29.97-01:00:00;00@29.97}" filter="mute" >\n')
# 		cmlTxt.insert("end",'       <Tail>\n')
# 		cmlTxt.insert("end",'        <Edit mode="duration" time="{'+ outEdit + '@29.97-' + inEdit+   '@29.97}" />\n')
# 		cmlTxt.insert("end",'       </Tail>\n')
# 		cmlTxt.insert("end",'     </Video>\n')
# 		cmlTxt.insert("end",'   </Segment>\n')
# 		cmlTxt.insert("end",'  </Sequence>\n\n')
# 		layer+=1

# 	cmlTxt.insert ("end", "</Composition>")  #footer






# #placeholder for functions
# def nothing():
# 	pass



# #Key Binding
# root.bind('<Control-Key-o>', open_file)
# root.bind('<Control-Key-O>', open_file)
# root.bind('<Control-Key-n>', new_file)
# root.bind('<Control-Key-N>', new_file)


#GUI - Framework
mainFrame = tk.Frame(root, bd="10", bg=background_color)
mainFrame.pack(fill="both",expand=1)


# topRow = tk.Frame(mainFrame, bg=background_color)
# topRow.pack(pady="5")


#working

edlFrame = tk.LabelFrame(mainFrame, text="Avid EDL", bg=background_color)
edlFrame.grid(column="0", row = "0")

edlScroll = tk.Scrollbar(edlFrame)
edlScroll.pack(side="right", fill="y")

edlTxt = tk.Text(edlFrame, selectbackground="#ff9933", selectforeground="black", undo=True, yscrollcommand=edlScroll.set)
edlTxt.pack(fill="both",expand=1, padx="5", pady="5")
edlScroll.config(command=edlTxt.yview)


cmlFrame = tk.LabelFrame(mainFrame, text="Vantage CML", bg=background_color)
cmlFrame.grid(column="1", row="0")

cmlScroll = tk.Scrollbar(cmlFrame)
cmlScroll.pack(side="right", fill="y")

cmlTxt = tk.Text(cmlFrame, selectbackground="#ff9933", selectforeground="black", undo=True, yscrollcommand=cmlScroll.set)
cmlTxt.pack(fill="both",expand=1, padx="5", pady="5")
cmlScroll.config(command=cmlTxt.yview)
#------------------------------


# bottomRow = tk.Frame(mainFrame, bg=background_color)
# bottomRow.pack(pady="10")



# #GUI - Menu Bar
# menubar = tk.Menu(root)
# filemenu = tk.Menu(menubar, tearoff=0)
# menubar.add_cascade(label="File", menu=filemenu)
# filemenu.add_command (label="New", command=lambda: new_file(False), accelerator ="Ctrl+N")
# filemenu.add_command (label="Open", command=lambda: open_file(False), accelerator ="Ctrl+O")
# filemenu.add_separator()
# filemenu.add_command (label="Exit        ", command=root.quit, accelerator ="Ctrl+Q")

# editmenu = tk.Menu(menubar, tearoff=0)
# menubar.add_cascade(label="Edit", menu=editmenu)
# editmenu.add_command (label="Undo", command=edlTxt.edit_undo, accelerator ="Ctrl+Z")
# editmenu.add_command (label="Redo", command=edlTxt.edit_redo, accelerator ="Ctrl+Y")
# editmenu.add_separator()
# editmenu.add_command (label="Cut", command=nothing, accelerator ="Ctrl+X")
# editmenu.add_command (label="Copy", command=nothing, accelerator ="Ctrl+C")
# editmenu.add_command (label="Paste", command=nothing, accelerator ="Ctrl+V")

# viewmenu = tk.Menu(menubar, tearoff=0)
# menubar.add_cascade(label="View", menu=viewmenu)
# viewmenu.add_command (label="Avid EDL", command=nothing)
# viewmenu.add_command (label="Vantage CML", command=nothing)
# viewmenu.add_command (label="Vantage CSV", command=nothing)

# helpmenu = tk.Menu(menubar, tearoff=0)
# menubar.add_cascade(label="Help", menu=helpmenu)
# helpmenu.add_command (label="Documentation", command=nothing)
# helpmenu.add_separator()
# helpmenu.add_command (label="About", command=nothing)

# #GUI - Top buttons
# open_edl = tk.Button(topRow, text="Open EDL", command=lambda: open_file(None))
# t_btn2 = tk.Button(topRow, text="Update CML", command=parse_edl)
# t_btn3 = tk.Button(topRow, text="Button 3")

# open_edl.grid(row="0", column="0", padx="5")
# t_btn2.grid(row="0", column="1", padx="5")
# t_btn3.grid(row="0", column="2", padx="5")

# #GUI - Bottom buttons
# b_btn1 = tk.Button(bottomRow, text="Button 1")
# b_btn2 = tk.Button(bottomRow, text="Button 2")
# b_btn3 = tk.Button(bottomRow, text="Button 3")

# b_btn1.grid(row="0", column="0", padx="5")
# b_btn2.grid(row="0", column="1", padx="5")
# b_btn3.grid(row="0", column="2", padx="5")




# root.config (menu=menubar)
root.mainloop()