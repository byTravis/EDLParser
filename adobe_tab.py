# Adobe Tab - This is a basic roughout of the code before adding to the toolkit.


import os
import csv

path = "C:\\Users\\travi\Desktop\\Github\\EDLParser\\CCGPPI60H"

def get_nbtitles(path):
    titles = []
    for file in os.listdir(path):
        if file.endswith(".nbtitle"):
            titles.append(file)    
    return titles



def create_titles_csv():
    nbtitles = get_nbtitles(path)
    csv_filename = "C:\\Users\\travi\Desktop\\Github\\EDLParser\\CCGPPI60H\\test.csv"

    with open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # csv_writer.writerow

        for title in nbtitles:
            row1 = [title, 'TFN', 'URL', 'PROMO']
            row2 = [title, '{$$Workflow_TFN}', '{$$Workflow_URL}', '{$$Workflow_Promo}']
            csv_writer.writerow(row1)
            csv_writer.writerow(row2)

create_titles_csv()
    
