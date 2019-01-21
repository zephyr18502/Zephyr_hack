import threading
import time
import datetime
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox as msg
import os
import csv
import tkinter.ttk as ttk #
import re

class TestThread(threading.Thread):
    def __init__(self, command):
        super().__init__()
        self.TerminalCommand = command

    def run(self):
        os.system(self.TerminalCommand)

class Analyzer(tk.Tk):
    def __init__(self, tasks=None):
        super().__init__()

        self.title("GR-GSM Scanner")
        self.geometry("600x400")

        self.ScrollBar = tk.Scrollbar(self, orient='vertical')

        self.listbox = tk.Listbox(self, yscrollcommand=self.ScrollBar.set)
        self.ScrollBar.config(command=self.listbox.yview    )
        self.ScrollBar.pack(side="right", fill='y')
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.focus()

        # self.selectButton = tk.Button(self, text="Analyze", underline=0, command=self.AnalyzeFrequency)
        self.listbox.bind('<Double-1>', self.AnalyzeFrequency)
    	
        self.tempCounter = 0
        with open("output.txt") as f:
        	self.lines = f.readlines()

        for i in self.lines:
                if (self.tempCounter >= 10 and self.tempCounter <= len(self.lines)-3):
                        self.listbox.insert("end", i)
                self.tempCounter += 1

    def AnalyzeFrequency(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        # print("selection:", selection, ": '%s'" % value)

        self.SecondaryAppThread = TestThread("grgsm_livemon -f"+ self.transformString(value))
        # self.SecondaryAppThread = TestThread("grgsm_livemon -f94200248")
        self.SecondaryAppThread.start()

    def transformString(self, string):
        newString = ""
        begin = False
        for i in string:
                if (i == '('):
                        begin = True
                        continue
                elif (i == ')'):
                        break
                if (begin):
                        newString += i

        newString = newString.split(" ")

        if (re.findall("\d+\.\d+", newString[0])):
                num1 = re.findall("\d+\.\d+", newString[0])[0]
        else:
                num1 = re.findall("\d+", newString[0])[0]

        if (re.findall("\d+\.\d+", newString[2])):
                num2 = re.findall("\d+\.\d+", newString[2])[0]
        else:
                num2 = re.findall("\d+", newString[2])[0]

        num1 = float(num1)
        num2 = float(num2)

        if ("G" in newString[0]):
                num1 = num1 * 1000000000
        elif ("M" in newString[0]):
                num1 = num1 * 1000000
        elif ("K" in newString[0]):
                num1 = num1 * 1000

	# print(num1)
	# exit()

        if ("G" in newString[2]):
                num2 = num2 * 1000000000
        elif ("M" in newString[2]):
                num2 = num2 * 1000000
        elif ("K" in newString[2]):
                num2 = num2 * 1000

        if (newString[1] == "+"):
                final = num1 + num2
        elif (newString[1] == "-"):
                final = num1 - num2

        newString = ""
        string = str(final)
        for i in string:
                if (i == "."):
                        break
                newString += i

        return newString

class IMSI_Catcher(tk.Tk):
    def __init__(self, tasks=None):
        super().__init__()

        self.TableMargin = tk.Frame(self, width=500)
        self.TableMargin.pack(side=tk.TOP)
        self.scrollbarx = tk.Scrollbar(self.TableMargin, orient=tk.HORIZONTAL)
        self.scrollbary = tk.Scrollbar(self.TableMargin, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(self.TableMargin, columns=("Nb IMSI", "IMSI", "country", "brand", "operator", "MCC", "MNC", "LAC", "CellId"), height=400, selectmode="extended", yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set)
        self.scrollbary.config(command=self.tree.yview)
        self.scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbarx.config(command=self.tree.xview)
        self.scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.heading('Nb IMSI', text="Nb IMSI", anchor=tk.W)
        self.tree.heading('IMSI', text="IMSI", anchor=tk.W)
        self.tree.heading('country', text="country", anchor=tk.W)
        self.tree.heading('brand', text="brand", anchor=tk.W)
        self.tree.heading('operator', text="operator", anchor=tk.W)
        self.tree.heading('MCC', text="MCC", anchor=tk.W)
        self.tree.heading('MNC', text="MNC", anchor=tk.W)
        self.tree.heading('LAC', text="LAC", anchor=tk.W)
        self.tree.heading('CellId', text="CellId", anchor=tk.W)
        self.tree.column('#0', stretch=tk.NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=tk.NO, minwidth=0, width=200)
        self.tree.column('#2', stretch=tk.NO, minwidth=0, width=200)
        self.tree.column('#3', stretch=tk.NO, minwidth=0, width=300)
        self.tree.pack()

        self.updater()

    def updateMethod(self):
        self.tree.delete(*self.tree.get_children())
        with open('test_1.csv') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                print(row)
                NIMSI = row['Nb IMSI']
                IMSI = row['IMSI']
                country = row['country']
                brand = row["brand"]
                operator = row['operator']
                MCC = row["MCC"]
                MNC = row['MNC']
                LAC = row["LAC"]
                CellId = row["CellId"]
                self.tree.insert("", 0, values=(NIMSI, IMSI, country, brand, operator, MCC, MNC, LAC, CellId))  

    def updater(self):
        self.updateMethod()
        self.TableMargin.after(1000, self.updater)

class KalScanner(tk.Tk):
    def __init__(self, tasks=None):
        super().__init__()

        self.title("Hacking App")
        self.geometry("340x250")
        
        self.MENU = tk.Menu(self)
        self.MENU.add_command(label="IMSI Catcher", command=self.startIMSICatcher)

        self.LABEL = tk.Label(self, text="")
        self.LABEL.pack()

        self.FRAME = tk.Canvas(self)
        self.FRAME.pack()
        self.UserInput = tk.Entry(self)
        
        self.UserInput.focus_set()
        self.HackerImg = ImageTk.PhotoImage(file='hacker.jpg')
        self.FRAME.create_image(125, 125, image=self.HackerImg)
        self.FRAME.create_window( 168, 100, window=self.UserInput)
        self.startButton = tk.Button(self, text = "START", command=self.fetchFrequencies, anchor = 'center',
                            width = 10, activebackground = "#33B5E5")
        self.quit_button_window = self.FRAME.create_window(130, 120, anchor='nw', window=self.startButton)

        self.config(menu=self.MENU)

    def startIMSICatcher(self):
        print("IMSI Catcher Started!!!")
        # IMSI Catcher command
        self.IMSI = TestThread("sudo python3 simple_IMSI-catcher.py --sniff")
        self.IMSI.start()
        IMSI_Catcher()

    def fetchFrequencies(self):
        self.LABEL.config(text="Wait...")
        self.LABEL.update_idletasks()
        os.system('script -c "kal -s GSM900 -g40" output.txt')
        print(self.UserInput.get())
        Analyzer()
        self.LABEL.config(text="Done!")
        
        
if __name__ == "__main__":
    mainApp = KalScanner()
    mainApp.mainloop()
