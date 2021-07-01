import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import os


#Variable Names for VANTAGE - These are the variables used in Vantage.

vantage_tfn = "Workflow_TFN"
vantage_url = "Workflow_URL"
vantage_promo = "Workorder_Promo"
vantage_source_path = "Workflow_SupportingFilesPath"
vantage_master_name = "Workflow_Master"

#Variables
cur_dir = os.getcwd()
cmlItems=[]
file_name=False


#Set Up UI Elements
background_color = "#e6e6ff"
textFrameWidth="68"
textFrameHeight="45"






#New - Clear content
def new_file(x):
	edlTxt.delete("1.0", "end")
	cmlTxt.delete("1.0", "end")
	csvTxt.delete("1.0", "end")
	csvTitlesList.config(text="")
	global file_name
	file_name = ""
	root.title(f"EDL Parser - for Vantage")

#Open File
def open_file(x):
	global file_name
	file_name = ""
	root.title(f"EDL Parser - for Vantage")	
	edlTxt.delete("1.0", "end")
	cmlTxt.delete("1.0", "end")
	csvTxt.delete("1.0", "end")
	csvTitlesList.config(text="")
	
	edl_file = filedialog.askopenfilename(initialdir=cur_dir, title="Open Avid EDL", filetypes=(("Avid EDL", "*.edl"),))
	
	file_name = os.path.split(edl_file)[1]
	root.title(f"EDL Parser - for Vantage  |  {file_name}")
	file_name = file_name.replace(".edl", "")
	
	edl_file = open(edl_file, 'r')
	content = edl_file.readlines()
	edl_file.close()	
	for line in content:
		# line=line.strip()
		edlTxt.insert ("end", line)
		# print(line)
	
	parse_edl()
	generateCsv()

#Parse EDL data
def parse_edl():
	cmlTxt.delete("1.0", "end")
	cml_parsed = edlTxt.get("1.0", "end").splitlines()  #each line in the text box as a list item
	global cmlItems #nested list with everything
	cmlItems = []  #clears the list in case something was in there.
	edlList=[]  
	curCount=0
	dropFrame=False
	for line in cml_parsed:
		if line =="FCM: DROP FRAME":
			dropFrame = True
		splitColumns=line.split()  #breaks each line into a list of words
		edlList.append(splitColumns)
		
		if line.find("NBTITLE") != -1:
			cmlList=[]  #short term list of a single instance
			if dropFrame == True:
				nbTitle = edlList[curCount][1]  #NB Title
				inPoint= edlList[curCount-1][-2] #In point
				outPoint = edlList[curCount-1][-1] #Out Point
				inPoint= inPoint.replace(":", ";").replace(";", ":", 2) #sets dropframe formattting
				outPoint= outPoint.replace(":", ";").replace(";", ":", 2) #sets dropframe formattting

				cmlList.append(nbTitle)
				cmlList.append(inPoint)
				cmlList.append(outPoint)
				cmlItems.append(cmlList) 

			else:
				cmlList.append(edlList[curCount][1])  #NB Title
				cmlList.append(edlList[curCount-1][-2]) #In point
				cmlList.append(edlList[curCount-1][-1]) #Out Point
				cmlItems.append(cmlList) #nested list with everything

		curCount +=1
	generateCml(cmlItems)



#Generate CML
def generateCml(parsedData):
	layer=1  #sequence layer and video source
	#insert first part of header
	cmlTxt.insert("end", '<?xml version="1.0" encoding="utf-8"?>\n')
	cmlTxt.insert("end", '<Composition xmlns="Telestream.Soa.Facility.Playlist">\n')
	cmlTxt.insert("end", '	<Source identifier="999999">\n')
	cmlTxt.insert("end", '		<File location="{$$' + vantage_source_path + '}\\{$$' + vantage_master_name + '}" />\n')
	cmlTxt.insert("end", '		<Subtitle />\n')
	cmlTxt.insert("end", '	</Source>\n')
	
	for ee in parsedData:  #inserts sources in header
		cmlTxt.insert("end", '	<Source identifier="' + str(layer) +'">\n')
		cmlTxt.insert("end", '		<File location="{$$' + vantage_source_path + '}\\' + cmlItems[layer-1][0].replace("NBTITLE", "nbtitle") + '" />\n')
		cmlTxt.insert("end", '	</Source>\n\n')
		layer+=1

	
	#Insert Slate and Black code to CSV
	cmlTxt.insert("end", """	
	<Sequence layer="1">
		<Segment>
			<Image layer="0" location="C:\\Users\\Administrator\\Desktop\\AutoConform\\AutoSlate\\PWSlate.png" duration="{$$SlateLengthTimecode}" layout="center" fill="loop" />		
			
				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="bold" foreground-color="FF1b8fa2" background-color="transparent" wrap="true" horizontal-align="left" vertical-align="top" overflow="resize"> 
					{$$Workorder_Title} 
					<Area left="715px" right="1610px" bottom="970px" top="350px"  />
				</Title>
			
				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="normal" foreground-color="FF525255" background-color="transparent" wrap="true" horizontal-align="left" overflow="resize" layout="stretch"> 
					{$$Workorder_Agency} 
					<Area left="715px" right="1610px" top="455px"  />
				</Title>
			
				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="normal" foreground-color="FF525255" background-color="transparent" wrap="true" horizontal-align="left" overflow="resize" layout="stretch"> 
					{$$Workorder_Client} 
					<Area left="715px" right="1610px" top="510px"  />
				</Title>
			
				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="normal" foreground-color="FF525255" background-color="transparent" wrap="true" horizontal-align="left" overflow="resize" layout="stretch"> 
					{$$Workorder_Date} 
					<Area left="715px" right="1610px" top="565px"  />
					</Title>
			
				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="normal" foreground-color="FF525255" background-color="transparent" wrap="true" horizontal-align="left" overflow="resize" layout="stretch"> 
					{$$Workorder_TRT}
					<Area left="715px" right="1610px" top="620px"  />
				</Title>
			
				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="normal" foreground-color="FF525255" background-color="transparent" wrap="true" horizontal-align="left" overflow="resize" layout="stretch"> 
					{$$Workorder_SlatedISCI} 
					<Area left="715px" right="1610px" top="675px"  />
				</Title>
			
				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="normal" foreground-color="FF525255" background-color="transparent" wrap="true" horizontal-align="left" overflow="resize" layout="stretch"> 
					{$$Workflow_TFN} 
					<Area left="715px" right="1610px" top="730px"  />
				</Title>
			
				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="normal" foreground-color="FF525255" background-color="transparent" wrap="true" horizontal-align="left" overflow="resize" layout="stretch"> 
					{$$Workflow_URL} 
					<Area left="715px" right="1610px" top="785px"  />
				</Title>
						
				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="normal" foreground-color="FF525255" background-color="transparent" wrap="true" horizontal-align="left" overflow="resize" layout="stretch"> 
					{$$Workorder_Promo} 
					<Area left="715px"  right="1610px" top="840px" />
				</Title>			
	
				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="bold" foreground-color="FF1b8fa2" background-color="transparent" wrap="true" horizontal-align="right" vertical-align="top" overflow="resize"> 
					Title:
					<Area left="310px" right="685px" bottom="970px" top="350px"  />
				</Title>	
			
				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="bold" foreground-color="FF1b8fa2" background-color="transparent" wrap="true" horizontal-align="right" vertical-align="top" overflow="resize"> 
					Agency:
					<Area left="310px" right="685px" bottom="970px" top="455px"  />
				</Title>				


				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="bold" foreground-color="FF1b8fa2" background-color="transparent" wrap="true" horizontal-align="right" vertical-align="top" overflow="resize"> 
					Client:
					<Area left="310px" right="685px" bottom="970px" top="510px"  />
				</Title>	
			
				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="bold" foreground-color="FF1b8fa2" background-color="transparent" wrap="true" horizontal-align="right" vertical-align="top" overflow="resize"> 
					Date:
					<Area left="310px" right="685px" bottom="970px" top="565px"  />
				</Title>	
			
				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="bold" foreground-color="FF1b8fa2" background-color="transparent" wrap="true" horizontal-align="right" vertical-align="top" overflow="resize"> 
					Length:
					<Area left="310px" right="685px" bottom="970px" top="620px"  />
				</Title>	
			
				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="bold" foreground-color="FF1b8fa2" background-color="transparent" wrap="true" horizontal-align="right" vertical-align="top" overflow="resize"> 
					ISCI:
					<Area left="310px" right="685px" bottom="970px" top="675px"  />
				</Title>	
			
				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="bold" foreground-color="FF1b8fa2" background-color="transparent" wrap="true" horizontal-align="right" vertical-align="top" overflow="resize"> 
					#:
					<Area left="310px" right="685px" bottom="970px" top="730px"  />
				</Title>	

				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="bold" foreground-color="FF1b8fa2" background-color="transparent" wrap="true" horizontal-align="right" vertical-align="top" overflow="resize"> 
					URL:
					<Area left="310px" right="685px" bottom="970px" top="785px"  />
				</Title>	

				<Title align="head" adjust="edge" fill="none" layer="1" duration="{$$SlateLengthTimecode}"  font="Trebuchet MS" size="42pt" weight="bold" foreground-color="FF1b8fa2" background-color="transparent" wrap="true" horizontal-align="right" vertical-align="top" overflow="resize"> 
					{$$Workorder_PromoTitle}
					<Area left="310px" right="685px" bottom="970px" top="840px"  />
				</Title>
		</Segment>

		<Segment>
			<Canvas align="head" adjust="body" duration="{$$BlackHeadTimecode}" Background="black" layer="0" />                           
		</Segment>

	""")
	
	
	
	
	
	
	#insert last part of header wich includes the video source for the first segment
	cmlTxt.insert("end", '\n')
	cmlTxt.insert("end", '		<Segment>\n')
	cmlTxt.insert("end", '			<Video source="999999" />\n')
	layer=1 #resets layer for next for loop





#test at 246






	for e in parsedData:  #creates the edits
		nbTitle=e[0]
		inEdit = e[1]
		outEdit = e[2]		
		cmlTxt.insert("end",'			<Video source="'+ str(layer) + '" align="head" adjust="edge" offset="{' + inEdit + '@29.97-01:00:00;00@29.97}" filter="mute" >\n')
		cmlTxt.insert("end",'				<Tail>\n')
		cmlTxt.insert("end",'					<Edit mode="duration" time="{'+ outEdit + '@29.97-' + inEdit+   '@29.97}" />\n')
		cmlTxt.insert("end",'				</Tail>\n')
		cmlTxt.insert("end",'			</Video>\n\n')
		layer+=1

	# cmlTxt.insert ("end", "</Composition>")  #footer
	#Footer Code inserted at the end of the file
	cmlTxt.insert ("end", """
		</Segment>
		
		<Segment>
			<Canvas align="head" adjust="body" duration="{$$BlackTailTimecode}" Background="black" layer="0" />                           
		</Segment>

	</Sequence>

</Composition>""")  #footer
	generateCsv()




#generate CSV and Titles List
def generateCsv():
	csvTxt.delete("1.0", "end")
	title_set=[]
	titleList=""
	for e in cmlItems:
		title_set.append(e[0])

	title_set = set(title_set)
	for title in title_set:
		title = title.replace("NBTITLE", "nbtitle")
		csvTxt.insert("end", title + ",TFN,URL,PROMO\n")
		csvTxt.insert("end", title + ",{$$" + vantage_tfn + "},{$$" + vantage_url + "},{$$" + vantage_promo + "}\n")
		# csvTxt.insert("end", title + ",URL\n")
		# csvTxt.insert("end", title + ",{$$" + vantage_url +"}\n")
		# csvTxt.insert("end", title + ",PROMO\n")
		# csvTxt.insert("end", title + ",{$$" + vantage_promo + "}\n")
		titleList=titleList + "\n     >  " + title
	csvTitlesList.config(text=titleList)
	
#Saving CML and CSV

def save_files(nothing):
	csv_file = cur_dir + "\\" + file_name + ".csv"
	cml_file = cur_dir + "\\" + file_name + ".cml"

	if os.path.isfile(csv_file) or os.path.isfile(cml_file):
				overwrite_files(csv_file, cml_file)
	else:
		csv_file = open(csv_file, 'w')
		csv_file.write(csvTxt.get(1.0, END))
		csv_file.close()

		cml_file = open(cml_file, 'w')
		cml_file.write(cmlTxt.get(1.0, END))
		cml_file.close()
		save_success()


#Save - Overwrite Popup

def overwrite_files(csv_file, cml_file):
	response = messagebox.askokcancel("Overwrite Files?", "File(s) already exist!\nDo you want to overwrite the CML and/or CSV files?")
	if response==1:
		csv_file = open(csv_file, 'w')
		csv_file.write(csvTxt.get(1.0, END))
		csv_file.close()

		cml_file = open(cml_file, 'w')
		cml_file.write(cmlTxt.get(1.0, END))
		cml_file.close()
		save_success()
		

def save_success():
	messagebox.showinfo("Success!", "Your CML and CSV files have been saved.")


#Setting Up GUI
root = tk.Tk()
root.title("EDL Parser - for Vantage")
root.iconbitmap('C:/Users/Nicole/Desktop/Python-Travis/EDLParser/sources/pw.ico')
root.geometry ("1800x900+80+80")


#placeholder for functions
def nothing():
	pass



#Key Binding
root.bind('<Control-Key-o>', open_file)
root.bind('<Control-Key-O>', open_file)
root.bind('<Control-Key-n>', new_file)
root.bind('<Control-Key-N>', new_file)
root.bind('<Control-Key-s>', save_files)
root.bind('<Control-Key-S>', save_files)


#GUI - Framework
mainFrame = tk.Frame(root, bd="10", bg=background_color)
mainFrame.pack(fill="both",expand=1)

topRow = tk.Frame(mainFrame, bg=background_color)
topRow.grid(column="0", row = "0", pady="15", sticky=W)


#EDL Frame

edlFrame = tk.LabelFrame(mainFrame, text="Avid EDL (*.edl)", bg=background_color, width="100")
edlFrame.grid(column="0", row = "1", sticky=N)

# open_edl_btn = tk.Button(edlFrame, text="Open EDL", command=lambda: open_file(None))
# open_edl_btn.pack(padx="5")

edlScroll_y = tk.Scrollbar(edlFrame)
edlScroll_y.pack(side="right", fill="y")

edlScroll_x = tk.Scrollbar(edlFrame, orient=HORIZONTAL)
edlScroll_x.pack(side="bottom", fill="x")

edlTxt = tk.Text(edlFrame, selectbackground="#ff9933", selectforeground="black", undo=True, wrap="none", yscrollcommand=edlScroll_y.set, xscrollcommand=edlScroll_x.set, height=textFrameHeight, width=textFrameWidth)
edlTxt.pack(fill="both",expand=1, padx="5", pady="5")
edlScroll_y.config(command=edlTxt.yview)
edlScroll_x.config(command=edlTxt.xview)



#CML Frame
cmlFrame = tk.LabelFrame(mainFrame, text="Vantage EDL (*.cml)", bg=background_color)
cmlFrame.grid(column="1", row = "1", padx="15", sticky=N)

# update_cml_btn = tk.Button(cmlFrame, text="Update CML", command=parse_edl)
# update_cml_btn.pack(padx="5")

cmlScroll_y = tk.Scrollbar(cmlFrame)
cmlScroll_y.pack(side="right", fill="y")

cmlScroll_x = tk.Scrollbar(cmlFrame, orient=HORIZONTAL)
cmlScroll_x.pack(side="bottom", fill="x")

cmlTxt = tk.Text(cmlFrame, selectbackground="#ff9933", selectforeground="black", undo=True, yscrollcommand=cmlScroll_y.set, wrap="none", xscrollcommand=cmlScroll_x.set, height=textFrameHeight, width=textFrameWidth)
cmlTxt.pack(fill="both",expand=1, padx="5", pady="5")
cmlScroll_y.config(command=cmlTxt.yview)
cmlScroll_x.config(command=cmlTxt.xview)



#CSV Frame
csvFrame = tk.LabelFrame(mainFrame, text="NewBlue Title Variables (*.csv)", bg=background_color)
csvFrame.grid(column="2", row = "1", sticky=N,)

csvTitlesFrame = tk.LabelFrame(csvFrame, text="Titles List", bg=background_color)
csvTitlesFrame.pack(padx="15", pady="15", fill="x")

csvTitlesList = tk.Label(csvTitlesFrame, text="", justify="left", bg=background_color, height=11, anchor=NW)
csvTitlesList.pack(pady="5", side="left", fill=X)

# update_csv_btn = tk.Button(csvFrame, text="Update CSV", command=generateCsv)
# update_csv_btn.pack(padx="5", pady="5")

csvScroll_y = tk.Scrollbar(csvFrame)
csvScroll_y.pack(side="right", fill="y")

csvScroll_x = tk.Scrollbar(csvFrame, orient=HORIZONTAL)
csvScroll_x.pack(side="bottom", fill="x")

csvTxt = tk.Text(csvFrame, selectbackground="#ff9933", selectforeground="black", undo=True, yscrollcommand=csvScroll_y.set, wrap="none", xscrollcommand=csvScroll_x.set, height=30, width=textFrameWidth)
csvTxt.pack(fill="both",expand=1, padx="5", pady="5")
csvScroll_y.config(command=csvTxt.yview)
csvScroll_x.config(command=csvTxt.xview)
#------------------------------


# bottomRow = tk.Frame(mainFrame, bg=background_color)
# bottomRow.pack(pady="10")



#GUI - Menu Bar
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command (label="New", command=lambda: new_file(False), accelerator ="Ctrl+N")
filemenu.add_command (label="Open EDL", command=lambda: open_file(False), accelerator ="Ctrl+O")
filemenu.add_command (label="Save CSV/CML", command=lambda: save_files(False), accelerator ="Ctrl+S")
filemenu.add_separator()
filemenu.add_command (label="Exit        ", command=root.quit, accelerator ="Ctrl+Q")

editmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=editmenu)
editmenu.add_command (label="Undo", command=edlTxt.edit_undo, accelerator ="Ctrl+Z")
editmenu.add_command (label="Redo", command=edlTxt.edit_redo, accelerator ="Ctrl+Y")
editmenu.add_separator()
editmenu.add_command (label="Cut", command=nothing, accelerator ="Ctrl+X")
editmenu.add_command (label="Copy", command=nothing, accelerator ="Ctrl+C")
editmenu.add_command (label="Paste", command=nothing, accelerator ="Ctrl+V")

viewmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="View", menu=viewmenu)
viewmenu.add_command (label="Avid EDL", command=nothing)
viewmenu.add_command (label="Vantage CML", command=nothing)
viewmenu.add_command (label="Vantage CSV", command=nothing)

helpmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command (label="Documentation", command=nothing)
helpmenu.add_separator()
helpmenu.add_command (label="About", command=nothing)

# #GUI - Top buttons
t_btn1 = tk.Button(topRow, text="Open EDL", command=lambda: open_file(None))
t_btn2 = tk.Button(topRow, text="Update CSV/CML", command=parse_edl)
t_btn3 = tk.Button(topRow, text="Save CSV/CML", command=lambda: save_files(None))
t_btn1.grid(row="0", column="1", padx="5")
t_btn2.grid(row="0", column="2", padx="5")
t_btn3.grid(row="0", column="3", padx="5")

#GUI - Bottom buttons
# b_btn1 = tk.Button(bottomRow, text="Button 1")
# b_btn2 = tk.Button(bottomRow, text="Button 2")
# b_btn3 = tk.Button(bottomRow, text="Button 3")

# b_btn1.grid(row="0", column="0", padx="5")
# b_btn2.grid(row="0", column="1", padx="5")
# b_btn3.grid(row="0", column="2", padx="5")

root.config (menu=menubar)
root.mainloop()