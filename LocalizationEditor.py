import tkinter
import tkinter.messagebox, tkinter.simpledialog, tkinter.filedialog
import json

localizationData = {
    "LocalizationName": "Localization",
    "LocalizationKeys": [ 
        {"Name": "Key", "Value": "Value"}
    ]
}

currentKeyIndex = -1

def centerWindowToDisplay(Screen, width, height):
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    
    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/1.5))
    
    return f"{width}x{height}+{x}+{y}"

def addKey():
    new_key_name = tkinter.simpledialog.askstring("Add Key", "Enter new key name:")
    if new_key_name:
        new_key = {"Name": new_key_name, "Value": ""}
        localizationData["LocalizationKeys"].append(new_key)
        refresh()

        currentKeyIndex = len(localizationData["LocalizationKeys"]) - 1
        keysListbox.select_clear(0, tkinter.END)
        keysListbox.select_set(currentKeyIndex)
        keysListbox.see(currentKeyIndex)
        loadSelectedKey()

def deleteKey():
    global currentKeyIndex
    if currentKeyIndex >= 0 and len(localizationData["LocalizationKeys"]) > 0:
        localizationData["LocalizationKeys"].remove(localizationData["LocalizationKeys"][currentKeyIndex])
        currentKeyIndex = -1
        refresh()

def saveLocalization():
    try:
        json_data = json.dumps(localizationData, indent=4)

        file_path = tkinter.filedialog.asksaveasfilename(defaultextension=".json",
                                                         filetypes=[("JSON files", "*.json")])
        
        if file_path:
            with open(file_path, 'w') as file:
                file.write(json_data)
            tkinter.messagebox.showinfo("Success", "Localization data saved successfully.")
    
    except Exception as e:
        tkinter.messagebox.showerror("Error", f"Error saving localization data: {str(e)}")

def loadLocalization():
    try:
        file_path = tkinter.filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        
        if file_path:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)
            
            localizationData.update(loaded_data)
            
            refresh()
            
            tkinter.messagebox.showinfo("Success", "Localization data loaded successfully.")
    
    except Exception as e:
        tkinter.messagebox.showerror("Error", f"Error loading localization data: {str(e)}")


def refresh():
    global currentKeyIndex
    
    keysListbox.delete(0, tkinter.END)
    for key in localizationData["LocalizationKeys"]:
        keysListbox.insert(tkinter.END, key["Name"])
    if currentKeyIndex > len(localizationData["LocalizationKeys"])-1:
        currentKeyIndex = len(localizationData["LocalizationKeys"])-1
    if currentKeyIndex < 0 or len(localizationData["LocalizationKeys"]) == 0:
        keyNameEntry.config(state= "disabled")
        keyValueEntry.config(state= "disabled")
        deleteKeyButton.config(state= "disabled")
    else:
        keyNameEntry.config(state= "normal")
        keyValueEntry.config(state= "normal")
        deleteKeyButton.config(state= "normal")
        

def saveChanges(event=None):
    localizationData["LocalizationName"] = localizationNameEntry.get()
    if currentKeyIndex >= 0:
        localizationData["LocalizationKeys"][currentKeyIndex]["Name"] = keyNameEntry.get()
        localizationData["LocalizationKeys"][currentKeyIndex]["Value"] = keyValueEntry.get()
    refresh()

def loadSelectedKey(event=None):
    global currentKeyIndex
    
    selectedIndex = keysListbox.curselection()
    if selectedIndex:
        currentKeyIndex = selectedIndex[0]
        refresh()
        
        keyNameEntry.delete(0, tkinter.END)
        keyNameEntry.insert(tkinter.END, localizationData["LocalizationKeys"][currentKeyIndex]["Name"])
        
        keyValueEntry.delete(0, tkinter.END)
        keyValueEntry.insert(tkinter.END, localizationData["LocalizationKeys"][currentKeyIndex]["Value"])

root = tkinter.Tk()
root.geometry(centerWindowToDisplay(root, 540, 350))
root.resizable(False, False)
root.title("Localization Editor")

keysFrame = tkinter.Frame(root)
keysFrame.place(x = 0, y = 0, width = 256, height = 350)

keysListbox = tkinter.Listbox(keysFrame)
keysListbox.place(x = 0, y = 0, width = 256, height = 350)
keysListbox.bind("<ButtonRelease-1>", loadSelectedKey)

scrollbar = tkinter.Scrollbar(keysFrame, orient=tkinter.VERTICAL)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
scrollbar.config(command=keysListbox.yview)
keysListbox.config(yscrollcommand=scrollbar.set)

localizationNameLabel = tkinter.Label(root, text = "Localization Name:", justify = "left", anchor = "w")
localizationNameLabel.place(x = 256+8, y = 8, width = 256, height = 32)

localizationNameEntry = tkinter.Entry(root)
localizationNameEntry.insert(0, "Localization") 
localizationNameEntry.place(x = 256+8, y = 8+32, width = 256, height = 32)
localizationNameEntry.bind('<KeyRelease>', saveChanges)

keyNameLabel = tkinter.Label(root, text = "Key Name:", justify = "left", anchor = "w")
keyNameLabel.place(x = 256+8, y = 8+24+64, width = 256, height = 32)

keyNameEntry = tkinter.Entry(root)
keyNameEntry.place(x = 256+8, y = 8+24+96, width = 256, height = 32)
keyNameEntry.bind('<KeyRelease>', saveChanges)

keyValueLabel = tkinter.Label(root, text = "Key Value:", justify = "left", anchor = "w")
keyValueLabel.place(x = 256+8, y = 8+24+128, width = 256, height = 32)

keyValueEntry = tkinter.Entry(root)
keyValueEntry.place(x = 256+8, y = 8+24+160, width = 256, height = 32)
keyValueEntry.bind('<KeyRelease>', saveChanges)

addKeyButton = tkinter.Button(root, text = "Add Key", command = lambda:addKey())
addKeyButton.place(x = 256+8, y = 8+48+192, width = 128, height = 32)

deleteKeyButton = tkinter.Button(root, text = "Delete Key", command = lambda:deleteKey())
deleteKeyButton.place(x = 256+8+256-128, y = 8+48+192, width = 128, height = 32)

saveButton = tkinter.Button(root, text = "Save", command = lambda:saveLocalization())
saveButton.place(x = 256+8+256-128, y = 8+48+192+48, width = 128, height = 32)

loadButton = tkinter.Button(root, text = "Load", command = lambda:loadLocalization())
loadButton.place(x = 256+8, y = 8+48+192+48, width = 128, height = 32)

refresh()

root.mainloop()