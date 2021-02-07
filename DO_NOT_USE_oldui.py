from classes import *
from tools import *

import tkinter as tk
import tkinter.ttk as ttk

if not os.path.exists('mods'):
    os.makedirs('mods')


mod = None
currentNamespace = None
currentEvent = None

window = tk.Tk()

window.title('HOI4 Mod Generator')


modFrame = tk.Frame(master=window, width = 100, height = 100)
namespaceFrame = tk.Frame(master=window, width = 100, height = 100)
eventFrame = tk.Frame(master=window, width = 100, height = 100)
statsFrame = tk.Frame(master=window, width = 100, height = 50)

#mod
modNameLabel = tk.Label(master=modFrame,text="New Mod Name:")
modNameField = tk.Entry(master=modFrame)
modCreateButton = tk.Button(master=modFrame,text="Create Mod")
modSaveButton = tk.Button(master=modFrame,text="Save Mod")

#namespace
namespaceNameLabel = tk.Label(master=namespaceFrame,text="New Namespace Name:")
namespaceNameField = tk.Entry(master=namespaceFrame)
namespaceDropdownLabel = tk.Label(master=namespaceFrame,text="Namespaces Dropdown:")
namespaceCreateButton = tk.Button(master=namespaceFrame,text="Add New Namespace")
namespaceDeleteButton = tk.Button(master=namespaceFrame,text="DELETE CURRENT NAMESPACE")

#event
eventNameLabel = tk.Label(master=eventFrame,text="Event Name:")
eventDropdownLabel = tk.Label(master=eventFrame,text="Events Dropdown:")
eventPictureLabel = tk.Label(master=eventFrame,text="Event Picture (GFX):")
eventPictureField = tk.Entry(master=eventFrame)
eventNameField = tk.Entry(master=eventFrame)

eventDescLabel = tk.Label(master=eventFrame,text="Event Description:")
eventDescField = tk.Text(master=eventFrame, background="#e6e6e6", height=5)



eventCreateButton = tk.Button(master=eventFrame,text="Add New Event")
eventDeleteButton = tk.Button(master=eventFrame,text="DELETE CURRENT EVENT")



#Stats
currentModLabel = tk.Label(master=statsFrame,text="Current Mod: NONE",font=("Arial", 24))
currentNamespaceLabel = tk.Label(master=statsFrame,text="Current Namespace: NONE",font=("Arial", 24))
currentEventLabel = tk.Label(master=statsFrame,text="Current Event: NONE",font=("Arial", 24))

#Dropdowns
nameSpaceDropdownDefault = tk.StringVar()
nameSpaceDropdownDefault.set("PICK A NAMESPACE")
nameSpaceDropdown = ttk.Combobox(namespaceFrame, width=27, textvariable = nameSpaceDropdownDefault, state="readonly")

eventDropdownDefault = tk.StringVar()
eventDropdownDefault.set("PICK AN EVENT")
eventDropdown = ttk.Combobox(eventFrame, width=27, textvariable = eventDropdownDefault, state="readonly")

#event actions
def clear_event_UI():
    if(currentEvent):    
        eventDescField.delete(0, 'end')
        eventNameField.delete(0, 'end')

def update_stats():
    currentEventLabel['text'] = "Current Event: " + currentEvent.name if currentEvent else "Current Event: None"
    currentModLabel['text'] = "Current Mod: " + mod.name if mod else "Current Mod: Error Not Found"
    currentNamespaceLabel['text'] = "Current Namespace: " + currentNamespace.name if currentNamespace else "Current Namespace: None"

    if(currentNamespace):
        eventDropdown.delete(0, 'end')
        eventDropdown['values'] = GetNamesAsList(currentNamespace.events)

        
        

def update_namespace(event):
    global currentNamespace
    n = nameSpaceDropdown.get()
    currentNamespace = FindObjectWithName(n, mod.namespaces)
    clear_event_UI()
    update_stats()

def namespace_create(event):
    global mod
    if(mod == None):
        print("NO MOD!")
        return
    mod.AddNamespace(Namespace(namespaceNameField.get()))
    nameSpaceDropdown['values'] = GetNamesAsList(mod.namespaces)
    update_stats()
    namespaceNameField.delete(0, 'end')

def namespace_delete(event):
    global currentNamespace
    if(currentNamespace != None):
        mod.namespaces.remove(currentNamespace)
        currentNamespace = None
    update_stats()
    nameSpaceDropdown.delete(0, 'end')
    nameSpaceDropdown['values'] = GetNamesAsList(mod.namespaces)

def mod_create(event):
    global mod
    mod = Mod(modNameField.get())
    nameSpaceDropdown['values'] = GetNamesAsList(mod.namespaces)
    update_stats()
    modNameField.delete(0, 'end')
    namespaceNameField.delete(0, 'end')
def mod_save(event):
    event_save()
    if(mod):
        SaveMod(mod)
    else:
        print("NO MOD CREATED YET")

def create_event_from_fields():
    return Event(currentNamespace,"country",eventNameField.get(),eventDescField.get("1.0", 'end'),eventPictureField.get())

def event_create(event):
    if(currentNamespace == None):
        print("NO NAMESPACE!")
        return

    e = create_event_from_fields()
    global currentEvent
    currentEvent = e
    update_event_ui()
    update_stats()

def event_save():
    if(currentNamespace == None or currentEvent == None):
        print("NO NAMESPACE OR NO EVENT!")
        return
    

    currentEvent.name = eventNameField.get()
    currentEvent.desc = eventDescField.get("1.0", 'end')
    currentEvent.picture = eventPictureField.get()
    print("EVENT UPDATED")
    
    
def update_event_ui():
    if(not currentEvent):
        return
    eventNameField['text'] = currentEvent.name
    eventPictureField['text'] = currentEvent.picture
    eventDescField.delete(1.0,"end")
    eventDescField.insert(1.0, currentEvent.desc)
    eventDropdown['text'] = currentEvent.name
    print("UPDATED EVENT UI")

def update_event(event):
    if(currentNamespace == None):
        print("NO NAMESPACE!")
        return
    event_save()
    global currentEvent
    
    n = eventDropdown.get()
    currentEvent = FindObjectWithName(n, currentNamespace.events)
    update_stats()
    update_event_ui()
    
def event_delete(event):
    global currentEvent
    if(currentEvent != None):
        currentNamespace.events.remove(currentEvent)
        currentEvent = None
    update_stats()
    clear_event_UI()

#binding

#mod buttons
modCreateButton.bind("<Button-1>", mod_create)
modSaveButton.bind("<Button-1>", mod_save)

#namespace ui
namespaceDeleteButton.bind("<Button-1>", namespace_delete)
namespaceCreateButton.bind("<Button-1>", namespace_create)
nameSpaceDropdown.bind("<<ComboboxSelected>>", update_namespace)

#event ui
eventDeleteButton.bind("<Button-1>", event_delete)
eventCreateButton.bind("<Button-1>", event_create)
eventDropdown.bind("<Button-1>", update_event)


#packing and starting

#stats
currentModLabel.pack()
currentNamespaceLabel.pack()
currentEventLabel.pack()
statsFrame.pack()

#mod
modNameLabel.pack()
modNameField.pack()
modCreateButton.pack()
modSaveButton.pack()
modFrame.pack(side=tk.LEFT)

#namespace
namespaceDropdownLabel.pack()
nameSpaceDropdown.pack()
namespaceNameLabel.pack()
namespaceNameField.pack()
namespaceCreateButton.pack()
namespaceDeleteButton.pack()

namespaceFrame.pack(side=tk.LEFT)
#event
eventDropdownLabel.pack()
eventDropdown.pack()
eventNameLabel.pack()
eventNameField.pack()
eventPictureLabel.pack()
eventPictureField.pack()
eventDescLabel.pack()
eventDescField.pack()
eventCreateButton.pack()
eventDeleteButton.pack()

eventFrame.pack(side=tk.LEFT)

window.mainloop()


