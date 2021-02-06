from classes import *
from tools import *

import tkinter as tk
import tkinter.ttk as ttk

mod = None
currentNamespace = None
currentEvent = None

window = tk.Tk()

window.title('HOI4 Mod Generator')


modFrame = tk.Frame(master=window, width = 100, height = 100)

modNameLabel = tk.Label(master=modFrame,text="New Mod Name:")
modNameField = tk.Entry(master=modFrame)

namespaceNameLabel = tk.Label(master=modFrame,text="New Namespace Name:")
namespaceNameField = tk.Entry(master=modFrame)
namespaceCreateButton = tk.Button(master=modFrame,text="Add New Namespace")

eventNameLabel = tk.Label(master=modFrame,text="New Event Name:")
eventNameField = tk.Entry(master=modFrame)
eventCreateButton = tk.Button(master=modFrame,text="Add New Event")

modCreateButton = tk.Button(master=modFrame,text="Create Mod")
modSaveButton = tk.Button(master=modFrame,text="Save Mod")

#Stats
currentModLabel = tk.Label(master=modFrame,text="Current Mod: NONE")
currentNamespaceLabel = tk.Label(master=modFrame,text="Current Namespace: NONE")
currentEventLabel = tk.Label(master=modFrame,text="Current Event: NONE")

#Dropdowns
nameSpaceDropdownDefault = tk.StringVar()
nameSpaceDropdown = ttk.Combobox(modFrame, width=27, textvariable = nameSpaceDropdownDefault)

eventDropdownDefault = tk.StringVar()
eventDropdown = ttk.Combobox(modFrame, width=27, textvariable = eventDropdownDefault)

#event actions
def update_stats():
    currentEventLabel['text'] = "Current Event: " + currentEvent.name if currentEvent else "Current Event: None"
    currentModLabel['text'] = "Current Mod: " + mod.name if mod else "Current Mod: Error Not Found"
    currentNamespaceLabel['text'] = "Current Namespace: " + currentNamespace.name if currentNamespace else "Current Namespace: None"

def update_namespace(event):
    global currentNamespace
    n = nameSpaceDropdown.get()
    currentNamespace = FindObjectWithName(n, mod.namespaces)
    update_stats()

def namespace_create(event):
    global mod
    if(mod == None):
        print("NO MOD!")
        return
    mod.AddNamespace(Namespace(namespaceNameField.get()))
    nameSpaceDropdown['values'] = GetNamesAsList(mod.namespaces)
    update_stats()
    

def mod_create(event):
    global mod
    mod = Mod(modNameField.get())
    nameSpaceDropdown['values'] = GetNamesAsList(mod.namespaces)
    update_stats()

def mod_save(event):
    if(mod):
        SaveMod(mod)
    else:
        print("NO MOD CREATED YET")

def event_create(event):
    if(currentNamespace == None):
        print("NO NAMESPACE!")
        return
    Event(currentNamespace,"country",eventNameField.get(),"placeholder desc")
    eventDropdown['values'] = GetNamesAsList(currentNamespace.events)
    update_stats()

def update_event(event):
    global currentEvent
    n = eventDropdown.get()
    currentEvent = FindObjectWithName(n, currentNamespace.events)
    update_stats()
    

#binding

#mod buttons
modCreateButton.bind("<Button-1>", mod_create)
modSaveButton.bind("<Button-1>", mod_save)

#namespace ui
namespaceCreateButton.bind("<Button-1>", namespace_create)
nameSpaceDropdown.bind("<<ComboboxSelected>>", update_namespace)

#event ui
eventCreateButton.bind("<Button-1>", event_create)
eventDropdown.bind("<Button-1>", update_event)

#packing and starting

#stats
currentModLabel.pack()
currentNamespaceLabel.pack()
currentEventLabel.pack()

#mod
modNameLabel.pack()
modNameField.pack()
modCreateButton.pack()
modSaveButton.pack()
modFrame.pack()

#namespace

namespaceNameLabel.pack()
namespaceNameField.pack()
namespaceCreateButton.pack()
nameSpaceDropdown.pack()

#event
eventNameLabel.pack()
eventNameField.pack()
eventCreateButton.pack()

eventDropdown.pack()

window.mainloop()


