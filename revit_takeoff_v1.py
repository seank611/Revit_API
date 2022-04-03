# revit_takeoff_v1.py V1.2 10/09/2021
# Copyright of Sean Kelton
# GUI/main program for revit material takeoff
# Functions/Modules: material_takeoff.py
from pathlib import Path
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.simpledialog import askstring
from material_takeoff import takeoff

root = Tk()
root.title("Revit Takeoff V1.2")
# root.iconbitmap(r"C:\Users\seank\Documents\Python\pyexcel1.0\Icons\ledger icon.ico")
root.geometry("500x200")
# defines app's background & button colors
bgc = 'PaleTurquoise3'
btc = 'azure'

root.configure(background=bgc)

def opencsv():
    global csv_file
    root.filename = filedialog.askopenfilename(initialdir=r"/Users\seank\Documents\Python\Revit API\CSV and Excel",
                                               title="Select A File",
                                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    csv_file = root.filename
    e.delete(0, END)
    e.insert(0, csv_file)
    return

def openpath():
    global folder
    folder = filedialog.askdirectory()
    e2.delete(0, END)
    e2.insert(0, folder)
    return

def analysis():
    # filename = 'Summary File.xlsx'
    # filename = askstring("Output Filename", "Enter Output Filename")
    # filename = filename + ".xlsx"
    filename = e3.get() + ".xlsx"
    print(filename)
    takeoff(csv_file, folder, filename, 'Family')
    messagebox.showinfo('New Message', 'Analysis Completed!')
    return

# define buttons
opencsvbutton = Button(text="Open CSV", padx=40, bg=btc, relief=GROOVE, command=opencsv)
opencsvbutton.grid(row=0, column=0, padx=5, pady=5)
outfolderbutton = Button(text="Output Folder", padx=30, bg=btc, relief=GROOVE, command=openpath)
outfolderbutton.grid(row=1, column=0, padx=5, pady=5)
analyzebutton = Button(text="Run Analysis", padx=34, bg=btc, relief=GROOVE, command=analysis)
analyzebutton.grid(row=3, column=0, padx=5, pady=5)

# define entry frames
e = Entry(width=50)
e.grid(row=0, column=1, padx=1.5, pady=2.5, columnspan=2)
e2 = Entry(width=50)
e2.grid(row=1, column=1, padx=1.5, pady=2.5, columnspan=2)
e3 = Entry(width=50)
e3.grid(row=2, column=1, padx=1.5, pady=2.5, columnspan=2)
e3.insert(0, 'Enter New File Name')
file_label = Label(root, text='Output File:', bg=bgc)
file_label.grid(row=2, column=0, padx=1.5, pady=2.5)
root.mainloop()
