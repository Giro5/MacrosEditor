from tkinter import *
from tkinter import messagebox
import threading
import subprocess
from tkinter import filedialog
import pyautogui
import time

TitleName = "MacrosEditor"
path = ""
run = False
cmds = []

root = Tk()
root.title(TitleName)
root.geometry("1000x500+300+200")

textbox = Text(root)
scroll = Scrollbar(root, command = textbox.yview)
textbox.config(yscrollcommand = scroll.set)
scroll.pack(side = "right", fill = "y")
textbox.pack(fill = "both", expand = True)

def OpenFile():
    #CloseFile()
    global path
    tmp = filedialog.askopenfilename(filetypes = (("Text Documents","*.txt"),("All Files","*.*")))
    if tmp != "":
        CloseFile()
        path = tmp
        print("opened file:", path)
        textbox.insert(0.0, open(path, "r").read())
        root.title(TitleName + " - " + path)
    return

def SaveFile():
    global path
    if path != "":
        print("saved file:", path)
        open(path, "w").write(textbox.get(0.0, END))
    else:
        path = filedialog.asksaveasfilename(filetypes = (("Text Documents","*.txt"),("All Files","*.*"))) + ".txt"
        if path != "":
            print("saved as file:", path)
            open(path, "w").write(textbox.get(0.0, END))
            root.title(TitleName + " - " + path)
    return

def CloseFile():
    global path
    path = ""
    textbox.delete(0.0)
    root.title(TitleName)
    run = False
    cmds.clear()

def KeyPress(event):
    global cmds
    if run:
        key = event.keysym
        print("pressed key:", key)
        icmd = None
        for i in range(len(cmds)):
            if cmds[i][0].split()[0] == key:
                icmd = i
        if icmd != None:
            #print("index cmd:", icmd)
            cmd = cmds[icmd] #select the macros
            cmdKey = cmd[0].split() #pressed button and keys: "*" or "~"
            cmd = cmd[1:]
            if len(cmdKey) == 1:
                for btn in cmd:
                    c = btn.split("}")[0][1:]
                    t = btn.split("}")[1].strip() if len(btn.split("}")) > 1 else "0"
                    if t == "":
                        t = "0"
                    if str(t) == "m":
                        if c == "1":
                            pyautogui.click(button = "left")
                        elif c == "2":
                            pyautogui.click(button = "right")
                    else:
                        print(int(t.strip() if t.isspace else t), t)
                        time.sleep(int(t.strip() if t.isspace else t))
                        pyautogui.press(c)
            elif cmdKey[1] == "*":
                for i in range(int(cmdKey[2])):
                    for btn in cmd:
                        c = btn.split("}")[0][1:]
                        t = btn.split("}")[1].strip() if len(btn.split("}")) > 1 else "0"
                        if t == "":
                            t = "0"
                        if str(t) == "m":
                            if c == "1":
                                pyautogui.click(button = "left")
                            elif c == "2":
                                pyautogui.click(button = "right")
                        else:
                            print(int(t.strip() if t.isspace else t), t)
                            time.sleep(int(t.strip() if t.isspace else t))
                            pyautogui.press(c)
            elif cmdKey[1] == "~":
                for btn in cmd:
                    subprocess.Popen(btn, shell = True)
            elif cmdKey[1] == "~*":
                for i in range(int(cmdKey[2])):
                    for btn in cmd:
                        subprocess.Popen(btn, shell = True)
    return

def AsyncPress(event):
    thr = threading.Thread(target = KeyPress(event))
    thr.start()

def StartMacros():
    global run
    if not run:
        global cmds
        run = True
        print("Macros is Run")
        textbox.config(state=DISABLED)
        txt = textbox.get(0.0, END)
        txtlines = txt.split("\n")
        prevmac = False
        cmd = []
        for i in range(len(txtlines)):
            if prevmac and txtlines[i] != "":
                cmd.append(txtlines[i])
            else:
                if txtlines[i] != "":
                    cmd.append(txtlines[i])
                    prevmac = True
                elif txtlines[i] == "" and i > 0 and txtlines[i - 1] != "":
                    cmds.append(cmd.copy())
                    prevmac = False
                    cmd.clear()
        print("commands:", cmds)
    return


def StopMacros():
    global run, cmds
    if run:
        run = False
        print("Macros is Disable")
        textbox.config(state=NORMAL)
        cmds.clear()
    return

MainMenu = Menu(root)

FileItem = Menu(MainMenu, tearoff = 0)
FileItem.add_cascade(label = "Open", command = OpenFile)
FileItem.add_cascade(label = "Save", command = SaveFile)
FileItem.add_cascade(label = "Close", command = CloseFile)
FileItem.add_separator()
FileItem.add_cascade(label = "Exit", command = root.destroy)

RunItem = Menu(MainMenu, tearoff = 0)
RunItem.add_cascade(label = "Start", comman = StartMacros)
RunItem.add_cascade(label = "Stop", comman = StopMacros)

MainMenu.add_cascade(label = "File", menu = FileItem)
MainMenu.add_cascade(label = "Run", menu = RunItem)

root.config(menu = MainMenu)

root.bind("<Key>", AsyncPress)

root.mainloop()