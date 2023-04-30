import json
import os
from tkinter import BOTH, END, Listbox, Menu, Tk
from tkinter.ttk import Button, Entry, Frame, Label, Notebook
from typing import Optional

USER_DIR = os.path.expanduser("~")
SETTING_DIR = os.path.join(USER_DIR, ".rsa-tools") 
if not os.access(SETTING_DIR, os.F_OK):
    os.mkdir(SETTING_DIR)

USER_FILE = os.path.join(SETTING_DIR, "settings.json")
if not os.access(USER_FILE, os.F_OK):
    with open(USER_FILE, "w") as f:
        f.write("[]")
        

class PlaceholderEntry(Entry):
    def __init__(self, master, *, placeholder: Optional[str] = None, **tkinter_args):
        Entry.__init__(self, master, **tkinter_args)
        self.placeholder = placeholder
        self._p = True
        if self.placeholder:
            self["foreground"] = "gray"
            self.insert(0, self.placeholder)
        
            self.bind("<FocusIn>", self._focus_in)
            self.bind("<FocusOut>", self._focus_out)
            self.bind("<KeyRelease>", self._key_release)
            
    def _key_release(self, e):
        self._p = not self.get()
            
    def _focus_in(self, e):
        if self._p:
            self["foreground"] = "black"
            self.delete(0, END)
        
    def _focus_out(self, e):
        if not self.get() and self.placeholder:
            self["foreground"] = "gray"
            self.insert(0, self.placeholder)
            self._p = True
        

        
class Data(Frame):
    def __init__(self, master, **tkinter_args):
        Frame.__init__(self, master, **tkinter_args)
        self.message_label = Label(self, text="Message:")
        self.message_label.grid(row=0, column=0, sticky="e")
        self.message = Entry(self, width=22)
        self.message.grid(row=0, column=1, sticky="w", columnspan=5,)
        
        self.key_label = Label(self, text="Key: (")
        self.key_label.grid(row=1, column=0, sticky="e")
        
        self.first_part_entry = PlaceholderEntry(self, placeholder="e or d", width=10)
        self.first_part_entry.grid(row=1, column=1, sticky="w")
        
        Label(self, text=", ").grid(row=1, column=2, sticky="w")
        
        self.second_part_entry = PlaceholderEntry(self, placeholder="N", width=10)
        self.second_part_entry.grid(row=1, column=3, sticky="w")
        
        Label(self, text=")").grid(row=1, column=5, sticky="w")
        
        self.convert_data = Button(self, text="Encrypt/Decrypt", width=35)
        self.convert_data.grid(row=2, column=0, columnspan=5)
        
        
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
        self.geometry("750x450")
        self.resizable(width=False, height=False)
        
        self.tab_control = Notebook(self)
        self.tab_control.pack(fill=BOTH, expand=True)
        
        self.tab_control.add(Data(self.tab_control), text="Data")
        # self.tab_control.add(SavedKeys(self.tab_control), text="Saved Keys")
                
        
        
        
if __name__ == "__main__":
    app = Application()
    app.mainloop()