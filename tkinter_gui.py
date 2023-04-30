import contextlib
from io import StringIO
import json
import math
import os
import sys
from tkinter import ACTIVE, BOTH, DISABLED, END, INSERT, IntVar, Listbox, Text, Tk
from tkinter.font import *
from tkinter.ttk import Button, Entry, Frame, Label, Notebook, Radiobutton
import traceback
from typing import Any, Iterable, Optional, TextIO

from rsa import extgcd, generate_primes

USER_DIR = os.path.expanduser("~")
SETTING_DIR = os.path.join(USER_DIR, ".rsa-tools") 
if not os.access(SETTING_DIR, os.F_OK):
    os.mkdir(SETTING_DIR)

USER_FILE = os.path.join(SETTING_DIR, "settings.json")
if not os.access(USER_FILE, os.F_OK):
    with open(USER_FILE, "w") as f:
        f.write("[]")
        
def _entry_validate_integer(e) -> Optional[bool]:
    inp = e.widget.get()
    if not inp: return
    try:
        int(inp)
    except ValueError:
        e.widget["foreground"] = "red"
        e.widget.valid = False
        return False
    else:
        e.widget["foreground"] = "green"
        e.widget.valid = True
        return True

def _entry_required(e):
    ...
        
# TODO rename class name
class MyEntry(Entry):
    def __init__(self, master, **tkinter_args):
        Entry.__init__(self, master, **tkinter_args)
        self.bind("<Control_L><BackSpace>", lambda e: self.delete(0, INSERT))
        self.bind("<Control_R><BackSpace>", lambda e: self.delete(0, INSERT))
        self.bind("<Control_L><Delete>", lambda e: self.delete(INSERT, END))
        self.bind("<Control_R><Delete>", lambda e: self.delete(INSERT, END))
      

class PlaceholderEntry(MyEntry):
    def __init__(self, master, *, placeholder: Optional[str] = None, placeholder_font: Font = ..., **tkinter_args, ):
        MyEntry.__init__(self, master, **tkinter_args)
        self.placeholder = placeholder
        self._def_font = self["font"]
        # if placeholder_font == ...:
            # placeholder_font = Font(size=8, slant=ITALIC)
        self._placeholder_font = placeholder_font
        self._p = True
        if self.placeholder:
            self["foreground"] = "gray"
            self.insert(0, self.placeholder)
        
            self.bind("<FocusIn>", self._focus_in, "+")
            self.bind("<FocusOut>", self._focus_out, "+")
            self.bind("<KeyRelease>", self._key_release, "+")
            
    def _key_release(self, e):
        self._p = not self.get()
            
    def _focus_in(self, e):
        if self._p:
            self["foreground"] = "green"
            # self["font"] = self._def_font
            self.delete(0, END)
        
    def _focus_out(self, e):
        if not self.get() and self.placeholder:
            self["foreground"] = "gray"
            # self["font"] = self._placeholder_font
            self.insert(0, self.placeholder)
            self._p = True
        
    
class Data(Frame):
    def __init__(self, master, **tkinter_args):
        Frame.__init__(self, master, **tkinter_args)
        self.message_label = Label(self, text="Message:")
        self.message_label.grid(row=0, column=0, sticky="e")
        self.message = PlaceholderEntry(self, placeholder="integer", width=22)
        self.message.bind("<KeyRelease>", _entry_required, "+")
        self.message.bind("<KeyRelease>", _entry_validate_integer, "+")
        self.message.grid(row=0, column=1, sticky="w", columnspan=4)
        
        self.key_label = Label(self, text="Key: (")
        self.key_label.grid(row=1, column=0, sticky="e")
        
        self.first_part_entry = PlaceholderEntry(self, placeholder="e or d", width=10)
        self.first_part_entry.bind("<KeyRelease>", _entry_validate_integer, "+")
        self.first_part_entry.bind("<KeyRelease>", _entry_required, "+")
        self.first_part_entry.bind("<KeyRelease>", self._encrypt_decrypt, "+")
        self.first_part_entry.grid(row=1, column=1)
        
        Label(self, text=", ").grid(row=1, column=2)
        
        self.second_part_entry = PlaceholderEntry(self, placeholder="N", width=10)
        self.second_part_entry.bind("<KeyRelease>", _entry_validate_integer, "+")
        self.second_part_entry.bind("<KeyRelease>", _entry_required, "+")
        self.second_part_entry.bind("<KeyRelease>", self._encrypt_decrypt, "+")
        self.second_part_entry.grid(row=1, column=3)
        
        Label(self, text=")").grid(row=1, column=5)
        
        Label(self, text="Encryption/Decyription Result:").grid(row=3, column=0, columnspan=5)
        self.data_result = Entry(self, state="readonly")
        self.data_result.grid(row=3, column=6)
        
    def _encrypt_decrypt(self, e):
        try:
            msg = int(self.message.get())
            power = int(self.first_part_entry.get())
            mod = int(self.second_part_entry.get())
        except ValueError:
            return
            
        self.data_result["state"] = ACTIVE
        self.data_result.delete(0, END)
        self.data_result.insert(0, (msg ** power) % mod)
        self.data_result["state"] = "readonly"
        
class SavedKeys(Frame):
    def __init__(self, master, **tkinter_args):
        Frame.__init__(self, master, **tkinter_args)
        self.saved_keys = Listbox(self)
        for key in json.load(open(USER_FILE)):
            ...


def _entry_validate_prime(e):
    number = _entry_validate_integer(e)
    if number is None:
        return
    elif not number:
        e.widget["foreground"] = "red"
        return
        
    prime = int(e.widget.get())
    if prime >= 100_000:
        e.widget["foreground"] = "black"
    elif number and prime in generate_primes(100_000):
        e.widget["foreground"] = "green"
    else:
        e.widget["foreground"] = "red"


class PublicKey(Frame):
    def __init__(self, master, **tkinter_args):
        Frame.__init__(self, master, **tkinter_args)
        Label(self, text="p:").grid(row=0, column=0)
        
        self.p_entry = PlaceholderEntry(self, placeholder="prime")
        self.p_entry.bind("<KeyRelease>", _entry_validate_prime, "+")
        self.p_entry.bind("<KeyRelease>", self._calculate, "+")
        self.p_entry.grid(row=0, column=1)
        
        Label(self, text="q:").grid(row=1, column=0)
        self.q_entry = PlaceholderEntry(self, placeholder="prime")
        self.q_entry.bind("<KeyRelease>", _entry_validate_prime, "+")
        self.q_entry.bind("<KeyRelease>", self._calculate, "+")
        self.q_entry.grid(row=1, column=1)
        
        Label(self, text=" ", width=5).grid(row=0, column=2, rowspan=2)
        
        Label(self, text="N:").grid(row=0, column=3)
        self.rsa_module = Entry(self, state="readonly")
        self.rsa_module.grid(row=0, column=4)
        
        Label(self, text="φ(N)").grid(row=1, column=3)
        self.phi_n = Entry(self, state="readonly")
        self.phi_n.grid(row=1, column=4)
        
        Label(self, text="Possible values for e are below").grid(row=2, column=0, columnspan=3, sticky="w")
        self.possible_e = Text(self, state=DISABLED, width=70)
        self.possible_e.grid(row=3, column=0, columnspan=20, sticky="news")
        
    def _calculate(self, e):
        if not (getattr(self.p_entry, "valid", False) and getattr(self.q_entry, "valid", False)):
            print(not(self.p_entry["foreground"] == "green" and "green" == self.q_entry["foreground"]))
            print((self.p_entry["foreground"], self.q_entry["foreground"]))
            return

        N = int(self.q_entry.get()) * int(self.p_entry.get())
        self.rsa_module["state"] = ACTIVE
        self.rsa_module.delete(0, END)
        self.rsa_module.insert(0, str(N))
        self.rsa_module["state"] = "readonly"

        phi_n = (int(self.q_entry.get()) - 1) * (int(self.p_entry.get()) - 1)
        self.phi_n["state"] = ACTIVE
        self.phi_n.delete(0, END)
        self.phi_n.insert(0, str(phi_n))
        self.phi_n["state"] = "readonly"
                
        self.possible_e["state"] = "normal"
        self.possible_e.delete("1.0", END)
        self.possible_e.insert("1.0", str(list(filter(lambda x: math.gcd(phi_n, x) == 1, generate_primes(min(10_000, phi_n)))))[1:-1])
        self.possible_e["state"] = DISABLED        


class Table(Frame):
    def __init__(self, master, table_data: Optional[Iterable[Iterable[Any]]], **tkinter_args):
        Frame.__init__(self, master, **tkinter_args)
        self.__table_data = []
        self.table_data = table_data
        
                
    @property
    def table_data(self):
        return self.__table_data

    @table_data.setter
    def table_data(self, value: Optional[Iterable[Iterable[Any]]]) -> Optional[Iterable[Iterable[Any]]]:
        self.__table_data = value
        if self.__table_data is not None:
            for i, line in enumerate(self.__table_data, start=1):
                for j, value in enumerate(line, start=1):
                    for widgets in self.grid_slaves(i, j):
                        widgets.destroy()
                    Label(self, text=str(value), border=1).grid(row=i, column=j, ipadx=5)

class PrivateKey(Frame):
    def __init__(self, master, **tkinter_args):
        Frame.__init__(self, master, **tkinter_args)
        
        self.phi_n = PlaceholderEntry(self, placeholder="φ(N)")
        self.phi_n.bind("<KeyRelease>", _entry_validate_integer, "+")
        self.phi_n.bind("<KeyRelease>", self._calculate, "+")
        self.phi_n.grid(row=0, column=0)

        self.rsa_module = PlaceholderEntry(self, placeholder="N i. e. RSA-Module")
        self.rsa_module.bind("<KeyRelease>", _entry_validate_integer, "+")
        self.rsa_module.bind("<KeyRelease>", self._calculate, "+")
        self.rsa_module.grid(row=0, column=1)
        
        self.e_value = PlaceholderEntry(self, placeholder="e from public key")
        self.e_value.bind("<KeyRelease>", _entry_validate_integer, "+")
        self.e_value.bind("<KeyRelease>", self._calculate, "+")
        self.e_value.grid(row=0, column=2)
        
        Label(self, text="Private key:").grid(row=1, column=0)
        self.private_key = Entry(self, state="readonly")
        self.private_key.grid(row=1, column=1)
        
        self.calculation_type = IntVar(value=1)
        
        self.radio_table = Radiobutton(self, text="Tabelle", value=1, variable=self.calculation_type, command=self._select_display_type)
        self.radio_table.grid(row=2, column=0)
        
        self.radio_equations = Radiobutton(self, text="Gleichungen", value=2, variable=self.calculation_type, command=self._select_display_type)
        self.radio_equations.grid(row=2, column=1)
        
        self.table = Table(self, None)
        self.table.grid(row=3, column=0, columnspan=6)
        
        self.eq = Table(self, None)
        
    def _select_display_type(self):
        if self.calculation_type.get() == 1:
            self.eq.grid_forget()
            self.table.grid(row=3, column=0, columnspan=6)

        else:
            self.table.grid_forget()
            self.eq.grid(row=3, column=0, columnspan=6)
            
        self._calculate()
        
    def _calculate(self, e=None):
        try:
            n = int(self.rsa_module.get())
            phi_n = int(self.phi_n.get())
            e = int(self.e_value.get())
        except ValueError:
            return

        display_type = bool(self.calculation_type.get() - 1)
        st = StringIO()
        with contextlib.redirect_stdout(st):
            d = extgcd(e, phi_n, as_equations=display_type)[0] % phi_n
        data = st.getvalue()
        st.close()
            
        key = (d, n)
        self.private_key["state"] = ACTIVE
        self.private_key.delete(0, END)
        self.private_key.insert(0, str(key))
        self.private_key["state"] = "readonly"
        if display_type:
            block1, block2 = data.split("\n\n")
            self.eq.table_data = [("Euclidean", "Extended")] + list(zip(block1.split("\n"), reversed(block2.split("\n"))))
        else:
            self.table.table_data = list(filter(lambda x: x, (x.split("\t") for x in data.split("\n"))))
        
  
class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("RSA Tools")
        self.geometry("750x450")
        self.maxsize(width=1000, height=700)
        self.resizable(width=True, height=True)
        
        self.tab_control = Notebook(self)
        self.tab_control.pack(fill=BOTH, expand=True)
        
        self.tab_control.add(Data(self.tab_control), text="Data")
        self.tab_control.add(PublicKey(self.tab_control), text="Public Key")
        self.tab_control.add(PrivateKey(self.tab_control), text="Private Key")
        # self.tab_control.add(SavedKeys(self.tab_control), text="Saved Keys")
        
        
        
        
if __name__ == "__main__":
    app = Application()
    app.mainloop()
