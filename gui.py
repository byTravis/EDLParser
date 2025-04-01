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







#################################################
# Functions
#################################################

def placeholder_function():
	pass


#  About Popup from Menu Bar
def about_popup():
	messagebox.showinfo("About " + creditsTitle, creditsTitle + "\nCreated by " + creditsAuthor +  "\nVersion: " + creditsVersion + "\nDate: " + creditsDate + "\nGitHub: " + creditsProjectSource)


#  Processes hyperlinks/URLs
def openLink(url):
	webbrowser.open_new(url)


#################################################
# GUI
#################################################

# GUI ----------------- GLOBAL/ROOT Settings -----------------

# Colors
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

# GUI Elements - Dark Turquise #118cab - Light Turquise = #96d3e2 - dark gray #525252
background_color = "#525252"
button_color = "#f0f0f0"
button_text = "black"
button_highlight = "#96d3e2"
button_highlight_text = "black"
tab_bg = "#e6e6ff"
column_width="65"
column_height="42"

section_title = ("Helvetica", 18, "bold")



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

# # EDL PARCER - Title
edl_title_container = ctk.CTkFrame(edl_tab, height=25, border_width=0, fg_color="transparent")
edl_title_container.grid(column=0, row=0, padx=10, pady=(10, 0), sticky="nsew")


# # EDL PARCER - Avid

# Containers
avid_edl_container = ctk.CTkFrame(edl_tab, height=200, border_width=1, fg_color="white", corner_radius=10)
avid_edl_container.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")

avid_edl_qc_container = tk.LabelFrame(avid_edl_container, text=" QC ", height=200, width=200, bg="white")
avid_edl_qc_container.grid(column=0, row=2, padx=10, pady=10, sticky="nsew")

avid_edl_btn_container = ctk.CTkFrame(avid_edl_container, height=200, border_width=0, fg_color="transparent")
avid_edl_btn_container.grid(column=1, row=2, padx=10, pady=10, sticky="nsew")


# Labels
avid_section_title = ctk.CTkLabel(avid_edl_container, text="Avid", font=section_title)
avid_section_title.grid(column=0, row=0, sticky="w", padx=10, pady=(10, 0))

avid_description = ctk.CTkLabel(avid_edl_container, text="Creates:  CML, CSV", justify='left')
avid_description.grid(column=0, row=1, sticky="w", padx=20, pady=0)


# Buttons
open_dir_btn = ctk.CTkButton(avid_edl_btn_container, text="Open Folder", command=placeholder_function)
open_dir_btn.grid(column=0, row=0,pady=5)

avid_generate_btn = ctk.CTkButton(avid_edl_btn_container, text="Generate", command=placeholder_function)
avid_generate_btn.grid(column=0, row=1,pady=5)

refresh_qc_btn = ctk.CTkButton(avid_edl_btn_container, text="Refresh QC", command=placeholder_function)
refresh_qc_btn.grid(column=0, row=2,pady=(60,5))




# # EDL PARCER - Premiere

# Containers

premiere_edl_container = ctk.CTkFrame(edl_tab, height=200, border_width=1, corner_radius=10, fg_color="white")
premiere_edl_container.grid(column=1, row=1, padx=10, pady=10, sticky="nsew")

premiere_edl_qc_container = tk.LabelFrame(premiere_edl_container, text=" QC ", height=200, width=200, bg="white")
premiere_edl_qc_container.grid(column=0, row=2, padx=10, pady=10, sticky="nsew")

premiere_edl_btn_container = ctk.CTkFrame(premiere_edl_container, height=200, border_width=0, fg_color="transparent")
premiere_edl_btn_container.grid(column=1, row=2, padx=10, pady=10, sticky="nsew")


# Labels
premiere_section_title = ctk.CTkLabel(premiere_edl_container, text="Premiere", font=section_title)
premiere_section_title.grid(column=0, row=0, sticky="w", padx=10, pady=(10, 0))

premiere_description = ctk.CTkLabel(premiere_edl_container, text="Creates:  CSV", justify='left')
premiere_description.grid(column=0, row=1, sticky="w", padx=20, pady=0)


# Buttons
open_dir_btn = ctk.CTkButton(premiere_edl_btn_container, text="Open Folder", command=placeholder_function)
open_dir_btn.grid(column=0, row=0,pady=5)

premiere_generate_btn = ctk.CTkButton(premiere_edl_btn_container, text="Generate", command=placeholder_function)
premiere_generate_btn.grid(column=0, row=1,pady=5)

refresh_qc_btn = ctk.CTkButton(premiere_edl_btn_container, text="Refresh QC", command=placeholder_function)
refresh_qc_btn.grid(column=0, row=2,pady=(60,5))





root.mainloop()