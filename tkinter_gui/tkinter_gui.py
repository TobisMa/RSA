import json
import os
from tkinter import BOTH, Listbox, Menu, Tk
from tkinter.ttk import Frame, Label, Notebook

USER_DIR = os.path.expanduser("~")
SETTING_DIR = os.path.join(USER_DIR, ".rsa-tools") 
if not os.access(SETTING_DIR, os.F_OK):
    os.mkdir(SETTING_DIR)

USER_FILE = os.path.join(SETTING_DIR, "settings.json")
if not os.access(USER_FILE, os.F_OK):
    with open(USER_FILE, "w") as f:
        f.write("[]")

        
class Data(Frame):
    def __init__(self, master, **tkinter_args):
        Frame.__init__(self, master, **tkinter_args)
        Label(self, text="Hello Data").pack()
        
class SavedKeys(Frame):
    def __init__(self, master, **tkinter_args):
        Frame.__init__(self, master, **tkinter_args)
        self.saved_keys = Listbox(self)
        for key in json.load(open(USER_FILE)):
            ...
        

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("RSA Tools")
        
        self.tab_control = Notebook(self)
        self.tab_control.pack(fill=BOTH, expand=True)
        
        self.tab_control.add(Data(self.tab_control), text="Data")
        self.tab_control.add(SavedKeys(self.tab_control), text="Saved Keys")
                
        
        
        
if __name__ == "__main__":
    app = Application()
    app.mainloop()