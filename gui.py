import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk
import webbrowser
import os

#################################################
# Settings & Global Variables
#################################################

# Set up environment
root = ctk.CTk()
root.title("Editor Toolkit - Production West")

# Window size and position
window_width = 1300
window_height = 900

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)

root.iconbitmap("sources\edlicon.ico")
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")



#credits info
creditsTitle = "Editor Toolkit - Production West"
creditsAuthor = "Travis"
creditsVersion ="v4"
creditsDate="7/31/2024"
creditsProjectSource="https://github.com/byTravis/EDLParser/"
creditsDocumentation = "https://rainforgrowth.sharepoint.com/sites/pw/Duplication%20Editors%20Handbook/Editor%20Toolkit.aspx"

# AVID Variables
isci = 'TEST24PH'
current_directory = 'reference\\'
edl_path = f'{current_directory}{isci}.edl'
drop_frame = None
edit_hour_mark = ""  # variable set in detect_dropframe
dissolve_offset = ""  # variable set in detect_dropframe function.  this compensates for the fade in Vantage.  Vantage treats a fade where first frame is 0% opacity and the last frame is 100% opacity.  Avid treats the first & last frame as showing some of the video.  This cheats that look so first or last frame isn't blank.
framerate = 23.976  # Plugged into the cml_edit_code.
video_edits = []
audio_edits = []
media_files = []





#################################################
# Functions
#################################################

################# EDL TAB FUNCTIONS #################

def placeholder_function():
	pass


#  About Popup from Menu Bar
def about_popup():
	messagebox.showinfo("About " + creditsTitle, creditsTitle + "\nCreated by " + creditsAuthor +  "\nVersion: " + creditsVersion + "\nDate: " + creditsDate + "\nGitHub: " + creditsProjectSource)


#  Processes hyperlinks/URLs
def openLink(url):
	webbrowser.open_new(url)
	

def open_folder(button):
    global current_directory
    folder = filedialog.askdirectory(initialdir=current_directory)
	
    if folder:
        print(f"{button} button | Selected folder: {folder}")
        current_directory = folder
        current_directory_path.configure(text=folder)
        edl_button_states(button)
    else:
        print("No folder selected")
	




def edl_button_states(button):  

    global avid_generate_btn_state
    global avid_refresh_qc_btn_state
    global premiere_generate_btn_state
    global premiere_refresh_qc_btn_state

    global enabled_btn
    global disabled_btn


    if button == "avid":           
        avid_generate_btn.configure(**enabled_btn)
        avid_refresh_qc_btn.configure(**enabled_btn)
        premiere_generate_btn.configure(**disabled_btn)
        premiere_refresh_qc_btn.configure(**disabled_btn)

    elif button == "premiere":
        avid_generate_btn_state = "disabled"
        avid_refresh_qc_btn_state = "disabled"
        premiere_generate_btn_state = "disabled"
        premiere_refresh_qc_btn_state = "disabled"
    else:
        avid_open_dir_btn.configure(**enabled_btn)
        premiere_open_dir_btn.configure(**enabled_btn)
        avid_generate_btn.configure(**disabled_btn)
        avid_refresh_qc_btn.configure(**disabled_btn)
        premiere_generate_btn.configure(**disabled_btn)
        premiere_refresh_qc_btn.configure(**disabled_btn)
         

    


    
    
def edl_framerate(framerate):
    print(framerate)

















#################################################
# GUI
#################################################

# GUI ----------------- GLOBAL/ROOT Settings -----------------

# Colors
# GUI Elements - Dark Turquise #118cab - Light Turquise = #96d3e2 - dark gray #525252

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
 
background_color = "#525252"

enabled_btn = {
        "state" : "normal", 
        "fg_color" : ["#3a7ebf", "#1f538d"],
        "font": ("Helvetica", 12, "bold") 

}

disabled_btn = {
        "state" : "disabled", 
        "fg_color" : ["#cfdae6", "#c0c2c4"], 
        "font" : ("Helvetica", 11, "italic"),
        "text_color_disabled" : "#838383"         
}





# button_color = ["#3a7ebf", "#1f538d"]
# button_color_disabled = "light blue"

# button_text = ("Helvetica", 12, "bold")
# button_text_color = "white"
# button_text_disabled = ("Helvetica", 12, "italic")
# button_text_color_disabled = "#525252"

# button_highlight = "#96d3e2"
# button_highlight_text = "black"

tab_bg = "#e6e6ff"
column_width="65"
column_height="42"

section_title = ("Helvetica", 18, "bold")
current_directory_label = ("Helvetica", 13, "bold")
current_directory_text = ("Helvetica", 13, "italic")



#GUI ----------------- BUTTON STATES -----------------
avid_generate_btn_state = "disabled"
avid_refresh_qc_btn_state = "disabled"
premiere_generate_btn_state = "disabled"
premiere_refresh_qc_btn_state = "disabled"




#GUI - Menu Bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="Quit", command=root.quit)


help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)

help_menu.add_command (label="Documentation", command=lambda: openLink(creditsDocumentation))
help_menu.add_command (label="GitHub Project", command=lambda: openLink(creditsProjectSource))
help_menu.add_separator()
help_menu.add_command (label="About", command=about_popup)


# GUI - Root Container
root_container = tk.Frame(root, bd="10", bg=background_color)
root_container.pack(fill="both",expand=1)


# GUI ----------------- TABS -----------------

# GUI - Style Tabs
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
            "background": [("selected", tab_bg)], # Color of active tab
            "expand": [("selected", [1, 1, 1, 0])] # [expanse of text]
        }
    }
})
style.theme_use('Cloud')


# GUI - Create Tabs
main_frame = ttk.Notebook(root_container)
main_frame.pack(padx=5, pady=5)

edl_tab = Frame(main_frame, width=window_width, height=window_height, bg=tab_bg)
edl_tab.pack(fill="both", expand=1)
main_frame.add(edl_tab, text="EDL Parsers")

views_tab = Frame(main_frame, width=window_width, height=window_height, bg=tab_bg)
views_tab.pack(fill="both", expand=1)
main_frame.add(views_tab, text="Views Generator")

directory_printer_tab = Frame(main_frame, width=window_width, height=window_height, bg=tab_bg)
directory_printer_tab.pack(fill="both", expand=1)
main_frame.add(directory_printer_tab, text="Directory Printer")




#GUI ----------------- EDL PARCER -----------------

# # EDL PARCER - Title/Root
edl_title_container = ctk.CTkFrame(edl_tab, height=25, border_width=0, fg_color="transparent")
edl_title_container.grid(column=0, row=0, padx=10, pady=(10, 0), sticky="nsew")


# Current Directory Container
current_directory_container = ctk.CTkFrame(edl_tab, border_width=1, fg_color="white", corner_radius=10)
current_directory_container.grid(column=0, row=0, padx=10, pady=20, sticky="nsew", columnspan=2)

current_directory_contents_container = ctk.CTkFrame(current_directory_container, fg_color="white")
current_directory_contents_container.grid(column=0, row=0, padx=5, pady=5, sticky="nsew")


current_project_title = ctk.CTkLabel(current_directory_contents_container, text="Project:", font=current_directory_label)
current_project_title.grid(column=0, row=0, sticky="sw", padx=10, pady=0)

current_project_name = ctk.CTkLabel(current_directory_contents_container, text="Choose a project", justify='left', font=current_directory_text)
current_project_name.grid(column=1, row=0, sticky="sw", padx=0, pady=0)

current_directory_title = ctk.CTkLabel(current_directory_contents_container, text="Current folder:", font=current_directory_label)
current_directory_title.grid(column=0, row=1, sticky="sw", padx=10, pady=0)

current_directory_path = ctk.CTkLabel(current_directory_contents_container, text="Choose a folder", justify='left', font=current_directory_text)
current_directory_path.grid(column=1, row=1, sticky="sw", padx=0, pady=0)





# # EDL PARCER - Avid

# Containers
avid_edl_container = ctk.CTkFrame(edl_tab, height=200, border_width=1, fg_color="white", corner_radius=10)
avid_edl_container.grid(column=0, row=1, padx=10, pady=0, sticky="nsew")

avid_header_container = ctk.CTkFrame(avid_edl_container, height=200, border_width=0, fg_color="transparent")
avid_header_container.grid(column=0, row=0, columnspan = 2, padx=5, pady=5, sticky="nsew")


avid_edl_qc_container = tk.LabelFrame(avid_edl_container, text=" QC ", height=200, width=200, bg="white")
avid_edl_qc_container.grid(column=0, row=2, padx=10, pady=10, sticky="nsew")

avid_edl_btn_container = ctk.CTkFrame(avid_edl_container, height=200, border_width=0, fg_color="transparent")
avid_edl_btn_container.grid(column=1, row=2, padx=10, pady=10, sticky="nsew")

avid_edl_description_container = ctk.CTkFrame(avid_header_container, border_width=0, fg_color="transparent")
avid_edl_description_container.grid(column=1, row=0, padx=0, pady=0, sticky="nw")

avid_edl_radio_container = ctk.CTkFrame(avid_header_container, width=500, border_width=0, corner_radius=0, fg_color="transparent")
avid_edl_radio_container.grid(column=2, row=0, padx=(80,0), pady=0, sticky="se")




# Radio Buttons
avid_edl_radio_title = ctk.CTkLabel(avid_edl_radio_container, text="Framerate:", font=("Helvetica", 14, "bold"))
avid_edl_radio_title.grid(column=0, row=0, sticky="w", padx=0, pady=(0, 0))


# Avid Description
avid_section_title = ctk.CTkLabel(avid_edl_description_container, text="Avid", font=section_title)
avid_section_title.grid(column=0, row=0, sticky="nw", padx=10, pady=(10, 0))

avid_description = ctk.CTkLabel(avid_edl_description_container, text="Creates:  CML, CSV", justify='left')
avid_description.grid(column=0, row=1, sticky="nw", padx=20, pady=0)


# Buttons
avid_framerate_radio = ctk.StringVar(value="")
avid_framerate_2997 = ctk.CTkRadioButton(
     avid_edl_radio_container, 
     text="29.97", 
     radiobutton_width = 15,
     radiobutton_height= 15,
     corner_radius= 3,
     border_width_checked=6,
     border_width_unchecked=2,
     variable=avid_framerate_radio, 
     value="29.97", 
     command=lambda: edl_framerate(avid_framerate_radio.get())
     )
avid_framerate_2997.grid(column=0, row=1,pady=0, padx=10, sticky="w")


avid_framerate_23976 = ctk.CTkRadioButton(
     avid_edl_radio_container, 
     text="23.976", 
     value="23.976", 
     radiobutton_width = 15,
     radiobutton_height= 15,
     corner_radius= 3,
     border_width_checked=6,
     border_width_unchecked=2,
     variable=avid_framerate_radio,
     command=lambda: edl_framerate(avid_framerate_radio.get())
     )
avid_framerate_23976.grid(column=0, row=2, pady=0, padx=10, sticky="w")


avid_open_dir_btn = ctk.CTkButton(avid_edl_btn_container,  text="Open Folder", command=lambda: open_folder("avid"))
avid_open_dir_btn.grid(column=0, row=0,pady=5)

avid_generate_btn = ctk.CTkButton(avid_edl_btn_container, text="Generate", command=placeholder_function)
avid_generate_btn.grid(column=0, row=3,pady=5)

avid_refresh_qc_btn = ctk.CTkButton(avid_edl_btn_container, text="Refresh QC", command=placeholder_function)
avid_refresh_qc_btn.grid(column=0, row=4,pady=(60,5))




# # EDL PARCER - Premiere

# Containers

premiere_edl_container = ctk.CTkFrame(edl_tab, height=200, border_width=1, corner_radius=10, fg_color="white")
premiere_edl_container.grid(column=1, row=1, padx=10, pady=0, sticky="nsew")

premiere_edl_qc_container = tk.LabelFrame(premiere_edl_container, text=" QC ", height=200, width=200, bg="white")
premiere_edl_qc_container.grid(column=0, row=2, padx=10, pady=(25,10),  sticky="nsew")

premiere_edl_btn_container = ctk.CTkFrame(premiere_edl_container, height=200, border_width=0, fg_color="transparent")
premiere_edl_btn_container.grid(column=1, row=2, padx=10, pady=(25,10), sticky="nsew")


# Labels
premiere_section_title = ctk.CTkLabel(premiere_edl_container, text="Premiere", font=section_title)
premiere_section_title.grid(column=0, row=0, sticky="w", padx=10, pady=(10, 0))

premiere_description = ctk.CTkLabel(premiere_edl_container, text="Creates:  CSV", justify='left')
premiere_description.grid(column=0, row=1, sticky="w", padx=20, pady=0)


# Buttons
premiere_open_dir_btn = ctk.CTkButton(premiere_edl_btn_container, text="Open Folder", command=lambda: open_folder("premiere"))
premiere_open_dir_btn.grid(column=0, row=0,pady=5)

premiere_generate_btn = ctk.CTkButton(premiere_edl_btn_container, text="Generate", command=placeholder_function)
premiere_generate_btn.grid(column=0, row=1,pady=5)

premiere_refresh_qc_btn = ctk.CTkButton(premiere_edl_btn_container, text="Refresh QC", command=placeholder_function)
premiere_refresh_qc_btn.grid(column=0, row=2,pady=(60,5))




#################################################
# Execute
#################################################


edl_button_states("null")


root.mainloop()