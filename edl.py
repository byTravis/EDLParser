import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import os
import webbrowser
import csv


#----------------- GLOBAL VARIABLES -----------------
#credits info
creditsTitle = "EDL Parser for Vantage"
creditsAuthor = "Travis"
creditsVersion ="v3.1"
creditsDate="2/1/2022"
creditsProjectSource="https://github.com/byTravis/EDLParser/"
creditsDocumentation = "http://sharepoint.portland.local/pw/Duplication%20Editors%20Handbook/EDL%20Parser.aspx"

#Variable Names for VANTAGE - These are the variables used in Vantage.
vantage_tfn = "Workflow_TFN"
vantage_url = "Workflow_URL"
vantage_promo = "Workorder_Promo"
vantage_source_path = "Workflow_SupportingFilesPath"
vantage_master_name = "Workflow_Master"

#CODEC Variables for Views Generator  ['slate', 'blackHead', 'blackTail', 'Format', 'StartTime', 'CenterCut Safe', 'Closed Captioning', 'Width', 'Height', 'Interlacing', 'Framerate', 'BitRate', 'CODEC', 'Profile' ]
viewsHeader = ["StationID ", "Title ", "Agency ", "Client ", "Date ", "Length ", "BaseISCI ", "SlatedISCI ", "TFN ", "URL ", "PROMO ", "SlateLength ", "BlackHead ", "BlackTail ", "Format ", "StartTimeCode ", "CentercutSafe ", "ClosedCaptioned ", "VideoWidth ", "VideoHeight ", "InterlaceMode ", "FrameRate ", "BitRate ", "Codec ", "Profile"]
viewsMOV = ['00:00:05;00', '00:00:02;00', '00:00:02;00', 'MOV', '00:59:53;00', 'Yes', 'FALSE', '1280', '720', 'Progressive', 'Native', '50000000', 'Special - View', 'Main']
viewsWMV = ['00:00:05;00', '00:00:02;00', '00:00:02;00', 'WMV', '00:59:53;00', 'Yes', 'FALSE', '960', '540', 'Progressive', '29.97', '3000000', 'Special - View', 'Main']
viewsMP4 = ['00:00:05;00', '00:00:02;00', '00:00:02;00', 'MP4', '00:59:53;00', 'Yes', 'FALSE', '1280', '720', 'Progressive', 'Native', '50000000', 'Special - View', 'Main']
viewsWiredrive = ['00:00:00;00', '00:00:00;00', '00:00:00;00', 'MP4', '01:00:00;00', 'Yes', 'FALSE', '1920', '1080', 'Progressive', '29.97', '5500000', 'H.264', 'Main']
viewsMOV_SD = ['00:00:05;00', '00:00:02;00', '00:00:02;00', 'MOV', '00:59:53;00', 'Yes', 'FALSE', '640', '480', 'Progressive', 'Native', '50000000', 'Special - View', 'Main']
viewsWMV_SD = ['00:00:05;00', '00:00:02;00', '00:00:02;00', 'WMV', '00:59:53;00', 'Yes', 'FALSE', '640', '480', 'Progressive', '29.97', '1500000', 'Special - View', 'Main' ]
viewsMP4_SD = ['00:00:05;00', '00:00:02;00', '00:00:02;00', 'MP4', '00:59:53;00', 'Yes', 'FALSE', '640', '480', 'Progressive', 'Native', '50000000', 'Special - View', 'Main']


#Global Variables
cur_dir = os.getcwd()
cmlItems=[]

file_name=False
dropFrame=False
framerate=29.97
framerateRounded = round(framerate)
hourMark = "01:00:00:00"  #one hour mark where first frame of action of video happens.
dissolveOffset = "00:00:00:01"  #this compensates for the fade in Vantage.  Vantage treats a fade where first frame is 0% opacity and the last frame is 100% opacity.  Avid treats the first & last frame as showing some of the video.  This cheats that look so first or last frame isn't blank.


#GUI Elements
background_color = "gray"
tabBG = "#e6e6ff"
textFrameWidth="68"
textFrameHeight="45"

#ButtonStates
edlUpdateState = DISABLED
edlSaveState = DISABLED
viewsExportState = DISABLED

# ----------------- GLOBAL FUNCTIONS -----------------
#Setting Up GUI
root = tk.Tk()
root.title(creditsTitle)
# root.iconbitmap('C:/Users/Nicole/Desktop/Python-Travis/EDLParser/sources/pw.ico')
root.geometry ("1800x900+40+40")

#placeholder for functions
def nothing():
	pass

#processes hyperlinks/URLs
def openLink(url):
	webbrowser.open_new(url)

# ----------------- EDL PARSER FUNCTIONS -----------------
#New - Clear content
def new_file(x):
	edlTxt.delete("1.0", "end")
	cmlTxt.delete("1.0", "end")
	csvTxt.delete("1.0", "end")
	csvTitlesList.config(text="")
	global file_name
	file_name = ""
	root.title(creditsTitle)
	buttonStates()
	

#Open File
def open_file(x): 	
	global cur_dir
	new_file(x)
	#global file_name
	#file_name = ""
	#root.title(creditsTitle)	
	#edlTxt.delete("1.0", "end")
	#cmlTxt.delete("1.0", "end")
	#csvTxt.delete("1.0", "end")
	#csvTitlesList.config(text="")


	edl_file = filedialog.askopenfilename(initialdir=cur_dir, title="Open Avid EDL", filetypes=(("Avid EDL", "*.edl"),))
	file_name = os.path.split(edl_file)[1]
	cur_dir = os.path.split(edl_file)[0]
	root.title(f"{creditsTitle}  |  {file_name}")
	file_name = file_name.replace(".edl", "")


	if edl_file != "":
		edl_file = open(edl_file, 'r')
		content = edl_file.readlines()  #each line is an item in a list
		edl_file.close()	
		for line in content:
			# line=line.strip()
			edlTxt.insert ("end", line)
			# print(line)
		parse_edl()
		

		# generateCsv()

#Converts frames to Timecode
def framesToTC(frames):
	frames=int(frames)

	framesSS=int(frames/framerateRounded)
	framesFF=frames-framesSS*framerateRounded

	if framesSS<10:
		framesSS="0" + str(framesSS)
	else:
		framesSS=str(framesSS)
		
	if framesFF<10:
		framesFF="0" + str(framesFF)
	else:
		framesFF=str(framesFF)
	
	timecode = "00:00:"+ framesSS + ":" + framesFF
	return(timecode)

#Formats the timecode string to indicate drop or nondrop syntax
def timecodeFormatting(timecode):
	if dropFrame==True:
		timecode=str(timecode.replace(":", ";").replace(";", ":", 2)) + "@" + str(framerate) #sets dropframe formattting
	return(timecode)

#Parse EDL data
def parse_edl():
	cmlTxt.delete("1.0", "end")
	cml_parsed = edlTxt.get("1.0", "end").splitlines()  #each line in the text box as a list item.  Getting it from the text box so if I edit the box, it will use those values instead of orig EDL
		
	global cmlItems #nested list within a list with everything
	cmlItems = []  #clears the list in case something was in there.
	edlList=[]  
	curCount=0
	
	
	for line in cml_parsed:
		if line =="FCM: DROP FRAME":
			global dropFrame 
			dropFrame = True

		splitColumns=line.split()  #breaks each line into a list of words
		edlList.append(splitColumns)  #creates a nested list.  Each line of the EDL is a list of column contents for that line.
	
	edlList.pop(0)#removes 1st line
	edlList.pop(0)#removes 2nd line
	listLength = len(edlList)

	
	for line in edlList:  #parses the line removing unneeded info and formatting the list in a way that makes sense.
		if curCount+1<listLength:  #sets the nbtitle name
			if edlList[curCount+1][0] == "*":
				if edlList[curCount+1][1].find(".NBTITLE") != -1:
					nbTitle = edlList[curCount+1][1]
					#print(edlList[curCount+1][1])
					#print("I dont' have to add the extention")
				else:
					nbTitle = edlList[curCount+1][1] + ".NBTITLE"
					#print(edlList[curCount+1][1])
					#print("I have to add the extention")

			else:
				nbTitle = "null"


		if line[-1] != line[-2] and line[0] !="*":  #parses out the edits
			parsedLine =[]
			parsedLine.append(line[0])  #event number
			# print(line[0])
			parsedLine.append(line[3])  #cut or dissolve
			# print(line[3])
			if line[3]=="D":
				parsedLine.append(line[4])  # if dissolve, length of dissolve
				# print(line[4])
			else:
				parsedLine.append("null")  #if cut, put in placeholder of null to maintain list position of other elements
				# print("null")
			parsedLine.append(line[-2])  #in point
			# print(line[-2])
			parsedLine.append(line[-1])  #out point
			# print(line[-1])
			parsedLine.append(nbTitle)  #nb title
			# print(nbTitle)			
			
			cmlItems.append(parsedLine)  #adds this single event list to the main list.

		curCount+=1
	cmlItems.append(["null", "null",  "null",  "null",  "null",  "null"])
	buttonStates()
	generateCml(cmlItems)

# #Generate CML
def generateCml(cmlItems):
	layer=1  #sequence layer
	editSource=1  #source number
	curCount=0


	#insert first part of header
	cmlTxt.insert("end", '''<?xml version="1.0" encoding="utf-8"?>
<Composition xmlns="Telestream.Soa.Facility.Playlist">
	<Source identifier="999999">''')
	cmlTxt.insert("end", '		<File location="{$$' + vantage_source_path + '}\\{$$' + vantage_master_name + '}" /> \n')
	cmlTxt.insert("end", '		<Subtitle />\n')
	cmlTxt.insert("end", '	</Source>\n')
	cmlTxt.insert("end",'\n')	

	for title in cmlItems:  #Sets sources
		if title[5] == "null" and title[1] =="D":		
			cmlTxt.insert("end", '	<Source identifier="' + str(layer) +'">\n')
			cmlTxt.insert("end", '		<File location="{$$' + vantage_source_path + '}\\' + cmlItems[curCount+1][5].replace("NBTITLE", "nbtitle") + '" />\n')
			cmlTxt.insert("end", '	</Source>\n\n')
			layer+=1
							
		elif title[5] != "null":
			cmlTxt.insert("end", '	<Source identifier="' + str(layer) +'">\n')
			cmlTxt.insert("end", '		<File location="{$$' + vantage_source_path + '}\\' + title[5].replace("NBTITLE", "nbtitle") + '" />\n')
			cmlTxt.insert("end", '	</Source>\n\n')
			layer+=1
		curCount+=1
		

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

	<Segment>
		<Video source="999999" />			
			""")
	cmlTxt.insert("end",'\n')


	for line in cmlItems:  #creates edits
		curCount=0
		editIn=timecodeFormatting(line[3])
		editOut=timecodeFormatting(line[4])
		editDissolveOffset=timecodeFormatting(dissolveOffset)
		
		editHourMark=timecodeFormatting(hourMark)

		if line[2] != "null":
			editDissolve=framesToTC(line[2])
			editDissolve=timecodeFormatting(editDissolve)
		else:
			editDissolve="null"

		if line[5] == "null" and line[1] =="D":  #Dissolve In
			if line[3]=="01:00:00:00": #doesn't add the dissolve offset if this is the first title starting on the first frame of action because it will create first edit before the media.
				cmlTxt.insert("end",'			<Video source="'+ str(editSource) + '" align="head" adjust="edge" offset="{' + editIn + '-' + editHourMark + '}" filter="mute" >\n')		
				cmlTxt.insert("end",'				<Head>\n')
				cmlTxt.insert("end",'					<Fade duration="{' + editDissolve +  '}" />\n')
				cmlTxt.insert("end",'				</Head>\n')
				cmlTxt.insert("end",'				<Tail>\n')
				cmlTxt.insert("end",'					<Edit mode="duration" time="{'+ editOut + '-' + editIn + '}" />\n')
				cmlTxt.insert("end",'				</Tail>\n')
				cmlTxt.insert("end",'			</Video>\n\n')
				editSource+=1
			else:  #adds the dissolve offset
				cmlTxt.insert("end",'			<Video source="'+ str(editSource) + '" align="head" adjust="edge" offset="{' + editIn + '-' + editDissolveOffset + '-' + editHourMark + '}" filter="mute" >\n')		
				cmlTxt.insert("end",'				<Head>\n')
				cmlTxt.insert("end",'					<Fade duration="{' + editDissolve + '+' + editDissolveOffset + '}" />\n')
				cmlTxt.insert("end",'				</Head>\n')
				cmlTxt.insert("end",'				<Tail>\n')
				cmlTxt.insert("end",'					<Edit mode="duration" time="{'+ editOut + '+' + editDissolveOffset + '-' + editIn + '}" />\n')
				cmlTxt.insert("end",'				</Tail>\n')
				cmlTxt.insert("end",'			</Video>\n\n')
				editSource+=1
		
		elif line[5] != "null" and line[1] =="D":  #Dissolve Out
			cmlTxt.insert("end",'			<Video source="'+ str(editSource) + '" align="head" adjust="edge" offset="{' + editIn +  '-' + editHourMark + '}" filter="mute" >\n')
			cmlTxt.insert("end",'				<Tail>\n')
			cmlTxt.insert("end",'					<Fade duration="{' + editDissolve + '+' + editDissolveOffset + '}" />\n')
			cmlTxt.insert("end",'					<Edit mode="duration" time="{'+ editOut + '+' + editDissolveOffset + '-' + editIn + '}" />\n')
			cmlTxt.insert("end",'				</Tail>\n')
			cmlTxt.insert("end",'			</Video>\n\n')
			editSource+=1
	
		elif line[5] != "null" and line[1] =="C":  #Cuts
			cmlTxt.insert("end",'			<Video source="'+ str(editSource) + '" align="head" adjust="edge" offset="{' + editIn + '-' + editHourMark + '}" filter="mute" >\n')
			cmlTxt.insert("end",'				<Tail>\n')
			cmlTxt.insert("end",'					<Edit mode="duration" time="{'+ editOut + '-' + editIn +   '}" />\n')
			cmlTxt.insert("end",'				</Tail>\n')
			cmlTxt.insert("end",'			</Video>\n\n')
			editSource+=1

		curCount+=1	


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
		if e[5] !="null":
			title_set.append(e[5])

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

#Pop-Outs
def popout_edlTxt():
	return

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

def aboutPopup():
	messagebox.showinfo("About " + creditsTitle, creditsTitle + "\nCreated by " + creditsAuthor +  "\nVersion: " + creditsVersion + "\nDate: " + creditsDate + "\nGitHub: " + creditsProjectSource)




# ----------------- FILE CHECKER/QC FUNCTIONS -----------------



# ----------------- VIEWS GENERATOR FUNCTIONS -----------------

 #Opens and Parses CSV
def openViewsCSV(): 
	clearViewsCSV()
	global cur_dir
	viewsBase = []
	viewsCustomized = []
	count = 0
	viewsCSVParse = filedialog.askopenfilename(initialdir=cur_dir, title="Open Comcast CSV", filetypes=(("CSV", "*.csv"),))	 	
	cur_dir = os.path.split(viewsCSVParse)[0]																				 

	if viewsCSVParse != "" :
		with open(viewsCSVParse, 'r') as csvFile:
			csvReader=csv.reader(csvFile)  
			for line in csvReader:
				if count >= 1 and count <= 4:
					vCustomized = []
					if count == 1:
						viewsBase.append(line[1])
						viewsBase.append(line[2])
						viewsBase.append(line[3])
						viewsBase.append(line[4])
						viewsBase.append(line[5])
						viewsBase.append(line[6])				
					vCustomized.append(line[7])
					vCustomized.append(line[8])
					vCustomized.append(line[9])
					vCustomized.append(line[10])
					viewsCustomized.append(vCustomized)
					count+=1			
				else:
					count +=1
		csvFile.close()
		displayViewsCSV(viewsBase, viewsCustomized)
		buttonStates()



#clears the Metadata fields
def clearViewsCSV():
	#Base Views Info
	viewsTitleEntry.delete(0, END)
	viewsAgencyEntry.delete(0, END)
	viewsClientEntry.delete(0, END)
	viewsDateEntry.delete(0, END)
	viewsTRTEntry.delete(0, END)
	viewsBaseISCIEntry.delete(0, END)
	
	#Customized Views Info
	viewsISCIEntry1.delete(0, END)
	viewsTFNEntry1.delete(0, END)
	viewsURLEntry1.delete(0, END)
	viewsPromoEntry1.delete(0, END)

	viewsISCIEntry2.delete(0, END)
	viewsTFNEntry2.delete(0, END)
	viewsURLEntry2.delete(0, END)
	viewsPromoEntry2.delete(0, END)

	viewsISCIEntry3.delete(0, END)
	viewsTFNEntry3.delete(0, END)
	viewsURLEntry3.delete(0, END)
	viewsPromoEntry3.delete(0, END)

	viewsISCIEntry4.delete(0, END)
	viewsTFNEntry4.delete(0, END)
	viewsURLEntry4.delete(0, END)
	viewsPromoEntry4.delete(0, END)	 	
	
	buttonStates()



	


#Populates Metadata fields
def displayViewsCSV(viewsBase, viewsCustomized):
	records = len(viewsCustomized)

	#Base Views Info
	viewsTitleEntry.insert(0,viewsBase[0])
	viewsAgencyEntry.insert(0,viewsBase[1])
	viewsClientEntry.insert(0,viewsBase[2])
	viewsDateEntry.insert(0,viewsBase[3])
	viewsTRTEntry.insert(0,viewsBase[4])
	viewsBaseISCIEntry.insert(0,viewsBase[5])

	
	#Customized Views Info
	if records>=1:
		viewsISCIEntry1.insert(0, viewsCustomized[0][0])
		viewsTFNEntry1.insert(0, viewsCustomized[0][1])
		viewsURLEntry1.insert(0, viewsCustomized[0][2])
		viewsPromoEntry1.insert(0, viewsCustomized[0][3])
	if records>=2:
		viewsISCIEntry2.insert(0, viewsCustomized[1][0])
		viewsTFNEntry2.insert(0, viewsCustomized[1][1])
		viewsURLEntry2.insert(0, viewsCustomized[1][2])
		viewsPromoEntry2.insert(0, viewsCustomized[1][3])
	if records>=3:
		viewsISCIEntry3.insert(0, viewsCustomized[2][0])
		viewsTFNEntry3.insert(0, viewsCustomized[2][1])
		viewsURLEntry3.insert(0, viewsCustomized[2][2])
		viewsPromoEntry3.insert(0, viewsCustomized[2][3])
	if records>=4:
		viewsISCIEntry4.insert(0, viewsCustomized[3][0])
		viewsTFNEntry4.insert(0, viewsCustomized[3][1])
		viewsURLEntry4.insert(0, viewsCustomized[3][2])
		viewsPromoEntry4.insert(0, viewsCustomized[3][3])


	#Get Generate views CSV
def generateViewsCSV():
	viewsBase = []
	viewsCustomized = []
	viewsCodec = ["not assigned"]
	viewsData = []

	if viewsSDStatus.get():	#Sets codec if HD or SD
		if viewsType.get() == "MOV":
			viewsCodec = viewsMOV_SD
		elif viewsType.get() == "WMV":
			viewsCodec = viewsWMV_SD
		elif viewsType.get() == "MP4":
			viewsCodec = viewsMP4_SD
	else:
		if viewsType.get() == "MOV":
			viewsCodec = viewsMOV
		elif viewsType.get() == "WMV":
			viewsCodec = viewsWMV
		elif viewsType.get() == "MP4":
			viewsCodec = viewsMP4

	getViewsMeta(viewsBase, viewsCustomized)  #pulls metadata from entry fields
	viewsDownconvert(viewsBase, viewsCustomized, viewsCodec)					#Checks for downconvert

	if viewsCustomizedStatus.get():												#customized views
		customizedViews(viewsBase, viewsCustomized, viewsCodec, viewsData)	
	if viewsGenericStatus.get():												#generic
		genericViews(viewsBase, viewsCustomized, viewsCodec, viewsData)			
	if viewsWiredriveStatus.get():												#wiredrive views
		wiredriveViews(viewsBase, viewsCustomized, viewsData)
	
	saveViewsCSV(viewsData)



#Get Metadata from Entry Fields
def getViewsMeta(viewsBase, viewsCustomized):  #sets views base Info
	viewsBase.append(viewsTitleEntry.get())
	viewsBase.append(viewsAgencyEntry.get())
	viewsBase.append(viewsClientEntry.get())
	viewsBase.append(viewsDateEntry.get())
	viewsBase.append(viewsTRTEntry.get())
	viewsBase.append(viewsBaseISCIEntry.get())

	if viewsISCIEntry1.get() !="":	   #checks to see if there is customization data in row 1
		r=[]
		r.append(viewsISCIEntry1.get())
		r.append(viewsTFNEntry1.get())
		r.append(viewsURLEntry1.get())
		r.append(viewsPromoEntry1.get())		
		viewsCustomized.append(r)

		if viewsISCIEntry2.get() !="":	  #checks to see if there is customization data in row 2
			r=[]
			r.append(viewsISCIEntry2.get())
			r.append(viewsTFNEntry2.get())
			r.append(viewsURLEntry2.get())
			r.append(viewsPromoEntry2.get())		
			viewsCustomized.append(r)
		else:
 			return(viewsBase, viewsCustomized)


		if viewsISCIEntry3.get() !="":	   #checks to see if there is customization data in row 3
			r=[]
			r.append(viewsISCIEntry3.get())
			r.append(viewsTFNEntry3.get())
			r.append(viewsURLEntry3.get())
			r.append(viewsPromoEntry3.get()) 		
			viewsCustomized.append(r)
		else:
			return(viewsBase, viewsCustomized)

		if viewsISCIEntry4.get() !="":	 #checks to see if there is customization data in row 4
			r=[]
			r.append(viewsISCIEntry4.get())
			r.append(viewsTFNEntry4.get())
			r.append(viewsURLEntry4.get())
			r.append(viewsPromoEntry4.get())		
			viewsCustomized.append(r)
		else:
			return(viewsBase, viewsCustomized)

	return(viewsBase, viewsCustomized)



# Sets SD Downcoverstion if needed 
def viewsDownconvert(viewsBase, viewsCustomized, viewsCodec):
	if viewsSDStatus.get():	#IF SD
		if viewsBase[5][-1] == "H":  #removes H from base ISCI
			viewsBase[5] = viewsBase[5][:-1]
		for e in viewsCustomized:
			if e[0][-1] == "H":  #removes H from slated ISCI
				e[0] = e[0][:-1]
		if SDType.get() == "CC": #sets centercut vs letterbox
			viewsCodec[5] = "Yes"
		else:
			viewsCodec[5] = "No"


# Generate Customized Views	Data
def customizedViews(viewsBase, viewsCustomized, viewsCodec, viewsData):
	viewsRow = []
	for entry in viewsCustomized:
		viewsRow.append("View")
		for e in viewsBase:
			viewsRow.append(e)
		for f in entry:
			if f == " ":
				f=""
			viewsRow.append(f)
		for g in viewsCodec:
			viewsRow.append(g)
		viewsData.append(viewsRow)
		viewsRow=[]





# Generate Generic Views
def genericViews(viewsBase, viewsCustomized, viewsCodec, viewsData):
	viewsRow = []
	genericData = viewsCustomized[0]
	viewsRow.append("Generic")

	
	if viewsGenericURLStatus.get() == False:
		genericData[2] = "generic"
	if viewsGenericTFNStatus.get() == False:
		genericData[1] = "generic"
	if viewsGenericPomoStatus.get() == False:
		if genericData[3] != " ":
			genericData[3] = "generic"

	
	for e in viewsBase:
		viewsRow.append(e)	
	for f in genericData:
		if f == " ":
			f = ""
		viewsRow.append(f)
	for g in viewsCodec:
		viewsRow.append(g)
	viewsData.append(viewsRow)
	viewsRow=[]


# Generate Wiredrive Views
def wiredriveViews(viewsBase, viewsCustomized, viewsData):
	viewsRow = []
	viewsRow.append("Wiredrive")
	for e in viewsBase:
		viewsRow.append(e)
	for f in viewsCustomized[0]:
		if f == " ":
			f=""
		viewsRow.append(f)
	for g in viewsWiredrive:
		viewsRow.append(g)
	viewsData.append(viewsRow)
	viewsRow=[]




#write the file
def saveViewsCSV(viewsData): 
	global cur_dir
	global viewsHeader
	saveViews = filedialog.asksaveasfilename(default="*.csv", initialdir=cur_dir, title="Save Views CSV", filetypes=(("CSV", "*.csv"),))
	cur_dir = os.path.split(saveViews)[0]																				 

	if saveViews:
		with open(saveViews, 'w', newline='') as f:
			csvWriter = csv.writer(f)
			csvWriter.writerow(viewsHeader)
			for row in viewsData:
				csvWriter.writerow(row)
		messagebox.showinfo("Success!", "Your Views CSV files have been saved.")


# ----------------- GUI -----------------

def buttonStates():
	t_btn2['state'] = tk.DISABLED
	t_btn3['state'] = tk.DISABLED
	#viewsExport['state'] = tk.DISABLED

	checkEDL = edlTxt.get("1.0", "end")
	checkViewsMeta = viewsTitleEntry.get()
	
	length = len(checkEDL)
	viewsLength = len(checkViewsMeta)

	if length != 1:
		t_btn2['state'] = tk.NORMAL
		t_btn3['state'] = tk.NORMAL
	
	#if viewsLength != 0:
	#	viewsExport['state'] = tk.NORMAL


#GUI - Menu Bar
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command (label="New", command=lambda: new_file(False), accelerator ="Ctrl+N")
filemenu.add_command (label="Open EDL", command=lambda: open_file(False), accelerator ="Ctrl+O")
filemenu.add_command (label="Save CML/CSV", command=lambda: save_files(False), accelerator ="Ctrl+S")
filemenu.add_separator()
filemenu.add_command (label="Exit        ", command=root.quit, accelerator ="Ctrl+Q")

editmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=editmenu)
editmenu.add_command (label="Undo", command=nothing, accelerator ="Ctrl+Z")
#editmenu.add_command (label="Redo", command=edlTxt.edit_redo, accelerator ="Ctrl+Y")
editmenu.add_separator()
editmenu.add_command (label="Cut", command=nothing, accelerator ="Ctrl+X")
editmenu.add_command (label="Copy", command=nothing, accelerator ="Ctrl+C")
editmenu.add_command (label="Paste", command=nothing, accelerator ="Ctrl+V")

# viewmenu = tk.Menu(menubar, tearoff=0)
# menubar.add_cascade(label="View", menu=viewmenu)
# viewmenu.add_command (label="Avid EDL", command=nothing)
# viewmenu.add_command (label="Vantage CML", command=nothing)
# viewmenu.add_command (label="Vantage CSV", command=nothing)

helpmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command (label="Documentation", command=lambda: openLink(creditsDocumentation))
helpmenu.add_command (label="GitHub Project", command=lambda: openLink(creditsProjectSource))
helpmenu.add_separator()
helpmenu.add_command (label="About", command=aboutPopup)

#Key Binding
root.bind('<Control-Key-o>', open_file)
root.bind('<Control-Key-O>', open_file)
root.bind('<Control-Key-n>', new_file)
root.bind('<Control-Key-N>', new_file)
root.bind('<Control-Key-s>', save_files)
root.bind('<Control-Key-S>', save_files)


#Style Tabs
style = ttk.Style()
style.theme_create('Cloud', settings={
    ".": {
        "configure": {
            "background": '#aeb0ce', # All colors except for active tab-button
            "font": 'red'
        }
    },
    "TNotebook": {
        "configure": {
            "background":background_color, # color behind the notebook
            "tabmargins": [5, 5, 0, 0], # [left margin, upper margin, right margin, margin beetwen tab and frames]
        }
    },
    "TNotebook.Tab": {
        "configure": {
            "background": 'white', # Color of non selected tab-button
            "padding": [15, 5], # [space beetwen text and horizontal tab-button border, space between text and vertical tab_button border]
            "font":"white"
        },
        "map": {
            "background": [("selected", tabBG)], # Color of active tab
            "expand": [("selected", [1, 1, 1, 0])] # [expanse of text]
        }
    }
})
style.theme_use('Cloud')






#GUI ----------------- GLOBAL ELEMENTS -----------------

#GUI - Root Container
mainContainer = tk.Frame(root, bd="10", bg=background_color)
mainContainer.pack(fill="both",expand=1)


#GUI - Tabs
mainFrame = ttk.Notebook(mainContainer)
mainFrame.pack(padx=5, pady=5)

tab_edl = Frame(mainFrame, width=1800, height=900, bg=tabBG)
tab_edl.pack(fill="both", expand=1)

tab_views = Frame(mainFrame, width=1800, height=900, bg=tabBG)
tab_views.pack(fill="both", expand=1)

#tab_qc = Frame(mainFrame, width=1800, height=900, bg=tabBG)
#tab_qc.pack(fill="both", expand=1)

mainFrame.add(tab_edl, text="EDL")
#mainFrame.add(tab_qc, text="File Check")
mainFrame.add(tab_views, text="Generate Views")




#GUI ----------------- EDL PARCER -----------------

#GUI EDL - Top buttons
topRow = tk.Frame(tab_edl, bg=tabBG)
topRow.grid(column="0", row = "0", pady="15", sticky=W)
t_btn1 = tk.Button(topRow, text="Open EDL", command=lambda: open_file(None))
t_btn2 = tk.Button(topRow, text="Update CSV/CML", command=parse_edl, state = DISABLED)
t_btn3 = tk.Button(topRow, text="Save CML/CSV", command=lambda: save_files(None), state = DISABLED)
t_btn1.grid(row="0", column="1", padx="5")
t_btn2.grid(row="0", column="2", padx="5")
t_btn3.grid(row="0", column="3", padx="5")


#EDL Frame
edlFrame = tk.LabelFrame(tab_edl, text="Avid EDL (*.edl)", bg=tabBG)
edlFrame.grid(column="0", row = "1", sticky=N, padx=5, pady=5)

## open_edl_btn = tk.Button(edlFrame, text="Pop-out EDL", command=lambda: popout_edlTxt(None))
## open_edl_btn.pack(padx="5", side=LEFT)

edlScroll_y = tk.Scrollbar(edlFrame)
edlScroll_y.pack(side="right", fill="y")

edlScroll_x = tk.Scrollbar(edlFrame, orient=HORIZONTAL)
edlScroll_x.pack(side="bottom", fill="x")

edlTxt = tk.Text(edlFrame, selectbackground="#ff9933", selectforeground="black", undo=True, wrap="none", yscrollcommand=edlScroll_y.set, xscrollcommand=edlScroll_x.set, height=textFrameHeight, width=textFrameWidth)
edlTxt.pack(fill="both",expand=1, padx="5", pady="5")
edlScroll_y.config(command=edlTxt.yview)
edlScroll_x.config(command=edlTxt.xview)


##CML Frame
cmlFrame = tk.LabelFrame(tab_edl, text="Vantage EDL (*.cml)", bg=tabBG)
cmlFrame.grid(column="1", row = "1", padx="5", pady=5, sticky=N)

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


##CSV Frame
csvFrame = tk.LabelFrame(tab_edl, text="NewBlue Title Variables (*.csv)", bg=tabBG)
csvFrame.grid(column="2", row = "1", sticky=N, padx=5, pady=5)

csvTitlesFrame = tk.LabelFrame(csvFrame, text="Titles List", bg=tabBG)
csvTitlesFrame.pack(padx="5", pady="5", fill="x")

csvTitlesList = tk.Label(csvTitlesFrame, text="", justify="left", bg=tabBG, height=11, anchor=NW)
csvTitlesList.pack(pady="5", side="left", fill=X)

# update_csv_btn = tk.Button(csvFrame, text="Update CSV", command=generateCsv)
# update_csv_btn.pack(padx="5", pady="5")

csvScroll_y = tk.Scrollbar(csvFrame)
csvScroll_y.pack(side="right", fill="y")

csvScroll_x = tk.Scrollbar(csvFrame, orient=HORIZONTAL)
csvScroll_x.pack(side="bottom", fill="x")

csvTxt = tk.Text(csvFrame, selectbackground="#ff9933", selectforeground="black", undo=True, yscrollcommand=csvScroll_y.set, wrap="none", xscrollcommand=csvScroll_x.set, height=32, width=textFrameWidth)
csvTxt.pack(fill="both",expand=1, padx="5", pady="5")
csvScroll_y.config(command=csvTxt.yview)
csvScroll_x.config(command=csvTxt.xview)
#------------------------------


## bottomRow = tk.Frame(mainFrame, bg=background_color)
## bottomRow.pack(pady="10")


#GUI ----------------- FILES CHECKER - QC -----------------

#GUI ----------------- GENERATE VIEWS -----------------

viewsType = StringVar()
SDDownconvert = StringVar()
SDType = StringVar()



#View Options Frame

viewsOptionsFrame = tk.LabelFrame(tab_views, text="Options", bg=tabBG)
viewsOptionsFrame.grid(column="1", row = "0", sticky=NW, padx=0, pady=20)

viewsTypeFrame = tk.LabelFrame(viewsOptionsFrame, text="View Type", bg=tabBG)
viewsTypeFrame.grid(column="0", row = "0", sticky=NW, padx=5, pady=5)

viewsFileFrame = tk.LabelFrame(viewsOptionsFrame, text="File Type", bg=tabBG)
viewsFileFrame.grid(column="1", row = "0", sticky=NW, padx=5, pady=5)

viewsSDFrame = tk.LabelFrame(viewsOptionsFrame, text="SD Downconversion", bg=tabBG)
viewsSDFrame.grid(column="3", row = "0", sticky=NW, padx=5, pady=5)


viewsCustomizedStatus = BooleanVar()
viewsGenericStatus = BooleanVar()
viewsWiredriveStatus = BooleanVar()

viewsGenericURLStatus = BooleanVar()
viewsGenericTFNStatus = BooleanVar()
viewsGenericPomoStatus = BooleanVar()

viewsGenericSDStatus = BooleanVar()

viewsSDStatus = BooleanVar()



viewsCustomizedCheck = Checkbutton(viewsTypeFrame, text="Customized View(s)", variable=viewsCustomizedStatus, bg=tabBG)
viewsGenericCheck = Checkbutton(viewsTypeFrame, text="Generic View", variable=viewsGenericStatus, bg=tabBG)

viewsGenericURLCheck = Checkbutton(viewsTypeFrame, text="Include URL", variable=viewsGenericURLStatus, bg=tabBG)
viewsGenericTFNCheck = Checkbutton(viewsTypeFrame, text="Include TFN", variable=viewsGenericTFNStatus, bg=tabBG)
viewsGenericPromoCheck = Checkbutton(viewsTypeFrame, text="Include Promo", variable=viewsGenericPomoStatus, bg=tabBG)

viewsWiredriveCheck = Checkbutton(viewsTypeFrame, text="Wiredrive *", variable=viewsWiredriveStatus, bg=tabBG)

viewsMOVRadio = Radiobutton(viewsFileFrame, text="MOV", variable=viewsType, value="MOV", bg=tabBG)
viewsWMVRadio = Radiobutton(viewsFileFrame, text="WMV", variable=viewsType, value="WMV", bg=tabBG)
viewsMP4Radio = Radiobutton(viewsFileFrame, text="MP4", variable=viewsType, value="MP4", bg=tabBG)

viewsSDCheck = Checkbutton(viewsSDFrame, text="SD Views *", variable=viewsSDStatus, bg=tabBG)
viewsCCRadio = Radiobutton(viewsSDFrame, text="Centercut", variable=SDType, value="CC", bg=tabBG)
viewsLBRadio = Radiobutton(viewsSDFrame, text="Letterbox", variable=SDType, value="LB", bg=tabBG)


viewsCustomizedCheck.select()
viewsGenericCheck.select()
viewsWiredriveCheck.select()
viewsMOVRadio.select()
viewsCCRadio.select()
viewsSDCheck.deselect()
viewsGenericURLCheck.select()



viewsCustomizedCheck.grid(row=0, column=0, sticky=W, padx=5)
viewsGenericCheck.grid(row=1, column=0, sticky=W, padx=5)

viewsGenericURLCheck.grid(row=2, column=0, sticky=W, padx=25)
viewsGenericTFNCheck.grid(row=3, column=0, sticky=W, padx=25)
viewsGenericPromoCheck.grid(row=4, column=0, sticky=W, padx=25)

viewsWiredriveCheck.grid(row=5, column=0, sticky=W, padx=5)

viewsMOVRadio.grid(row=0, column=1, sticky=W, padx=5)
viewsWMVRadio.grid(row=1, column=1, sticky=W, padx=5)
viewsMP4Radio.grid(row=2, column=1, sticky=W, padx=5)

viewsSDCheck.grid(row=0, column=1, sticky=W, padx=10)
viewsCCRadio.grid(row=1, column=1, sticky=W, padx=30)
viewsLBRadio.grid(row=2, column=1, sticky=W, padx=30)

viewsExport = tk.Button(viewsOptionsFrame, text="Export Views CSV", command=generateViewsCSV, state = NORMAL)

viewsWiredriveDisclaimerLabel = tk.Label(viewsOptionsFrame, text="* Wiredrive views will always be HD MP4.", bg=tabBG)

viewsExport.grid(row="10", column="0", padx="5", pady="15", columnspan="4")
viewsWiredriveDisclaimerLabel.grid(row="11", column="0", padx="5", pady="15", columnspan="4", sticky="w")


#View MetaData Frame
viewsMetaFrame = tk.LabelFrame(tab_views, text="Meta Data", bg=tabBG)
viewsMetaFrame.grid(column="0", row = "0", sticky=NW, padx=20, pady=20)

viewsMetaContainer = tk.Frame(viewsMetaFrame, bg=tabBG)
viewsMetaContainer.grid(column="0", row = "1", padx=5, pady=5)




#Views Metadata Fields
viewsTitleLabel = tk.Label(viewsMetaContainer, text="Title", bg=tabBG)
viewsAgencyLabel = tk.Label(viewsMetaContainer, text="Agency", bg=tabBG)
viewsClientLabel = tk.Label(viewsMetaContainer, text="Client", bg=tabBG)
viewsDateLabel = tk.Label(viewsMetaContainer, text="Date", bg=tabBG)
viewsTRTLabel = tk.Label(viewsMetaContainer, text="TRT", bg=tabBG)
viewsBaseISCILabel = tk.Label(viewsMetaContainer, text="Base ISCI", bg=tabBG)

viewsISCILabel = tk.Label(viewsMetaContainer, text="Slated ISCI", bg=tabBG)
viewsTFNLabel = tk.Label(viewsMetaContainer, text="TFN", bg=tabBG)
viewsURLLabel = tk.Label(viewsMetaContainer, text="URL", bg=tabBG)
viewsPromoLabel = tk.Label(viewsMetaContainer, text="Promo", bg=tabBG)

viewsTitleEntry = tk.Entry(viewsMetaContainer, width=40)
viewsAgencyEntry = tk.Entry(viewsMetaContainer, width=25)
viewsClientEntry = tk.Entry(viewsMetaContainer, width=25)
viewsDateEntry = tk.Entry(viewsMetaContainer, width=10)
viewsTRTEntry = tk.Entry(viewsMetaContainer, width=8)
viewsBaseISCIEntry = tk.Entry(viewsMetaContainer, width=12)
viewsISCIEntry1 = tk.Entry(viewsMetaContainer, width=15)
viewsTFNEntry1 = tk.Entry(viewsMetaContainer, width=15)
viewsURLEntry1 = tk.Entry(viewsMetaContainer, width=30)
viewsPromoEntry1 = tk.Entry(viewsMetaContainer, width=10)

viewsISCIEntry2 = tk.Entry(viewsMetaContainer, width=15)
viewsTFNEntry2 = tk.Entry(viewsMetaContainer, width=15)
viewsURLEntry2 = tk.Entry(viewsMetaContainer, width=30)
viewsPromoEntry2 = tk.Entry(viewsMetaContainer, width=10)

viewsISCIEntry3 = tk.Entry(viewsMetaContainer, width=15)
viewsTFNEntry3 = tk.Entry(viewsMetaContainer, width=15)
viewsURLEntry3 = tk.Entry(viewsMetaContainer, width=30)
viewsPromoEntry3 = tk.Entry(viewsMetaContainer, width=10)

viewsISCIEntry4 = tk.Entry(viewsMetaContainer, width=15)
viewsTFNEntry4 = tk.Entry(viewsMetaContainer, width=15)
viewsURLEntry4 = tk.Entry(viewsMetaContainer, width=30)
viewsPromoEntry4 = tk.Entry(viewsMetaContainer, width=10)

viewsTitleLabel.grid(row="0", column="0", padx="5")
viewsAgencyLabel.grid(row="0", column="1", padx="5")
viewsClientLabel.grid(row="0", column="2", padx="5")
viewsDateLabel.grid(row="0", column="3", padx="5")
viewsTRTLabel.grid(row="0", column="4", padx="5")
viewsBaseISCILabel.grid(row="0", column="5", padx="5")
viewsISCILabel.grid(row="0", column="6", padx="5")
viewsTFNLabel.grid(row="0", column="7", padx="5")
viewsURLLabel.grid(row="0", column="8", padx="5")
viewsPromoLabel.grid(row="0", column="9", padx="5")

viewsTitleEntry.grid(row="1", column="0", padx="5", pady="2")
viewsAgencyEntry.grid(row="1", column="1", padx="2")
viewsClientEntry.grid(row="1", column="2", padx="2")
viewsDateEntry.grid(row="1", column="3", padx="2")
viewsTRTEntry.grid(row="1", column="4", padx="2")
viewsBaseISCIEntry.grid(row="1", column="5", padx="2")
viewsISCIEntry1.grid(row="1", column="6", padx="2")
viewsTFNEntry1.grid(row="1", column="7", padx="2")
viewsURLEntry1.grid(row="1", column="8", padx="2")
viewsPromoEntry1.grid(row="1", column="9", padx="2")

viewsISCIEntry2.grid(row="2", column="6", padx="2", pady="2")
viewsTFNEntry2.grid(row="2", column="7", padx="2")
viewsURLEntry2.grid(row="2", column="8", padx="2")
viewsPromoEntry2.grid(row="2", column="9", padx="2")

viewsISCIEntry3.grid(row="3", column="6", padx="2", pady="2")
viewsTFNEntry3.grid(row="3", column="7", padx="2")
viewsURLEntry3.grid(row="3", column="8", padx="2")
viewsPromoEntry3.grid(row="3", column="9", padx="2")

viewsISCIEntry4.grid(row="4", column="6", padx="2", pady="2")
viewsTFNEntry4.grid(row="4", column="7", padx="2")
viewsURLEntry4.grid(row="4", column="8", padx="2")
viewsPromoEntry4.grid(row="4", column="9", padx="2")

#GUI Views Buttons
viewsButtons = tk.Frame(viewsMetaFrame, bg=tabBG)
viewsButtons.grid(column="0", row = "10", pady="15", sticky=S)

viewsCSV = tk.Button(viewsButtons, text="Parse Comcast CSV", command=lambda: openViewsCSV())
viewsClear = tk.Button(viewsButtons, text="Clear All", command=clearViewsCSV)

viewsCSV.grid(row="0", column="1", padx="5")
viewsClear.grid(row="0", column="3", padx="5")





root.config (menu=menubar)
root.mainloop()