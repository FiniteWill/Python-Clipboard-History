import os
# Used for file type regex
import glob
import time
import sys
# Used to access clipboard
import pyperclip
# Easier methods for listening and responding to user input
from pynput import keyboard
from pynput.keyboard import Key
# Simple GUI functionality
import tkinter as tk
from tkinter import ttk
# Use threading to have Tkinter's mainloop
# and updating clipboard happen simultaneously
from threading import Thread

# GUI Data
root = tk.Tk()
main_frame = ttk.Frame(root)

canvas_width = 200;
canvas_height = 200;
entry_canvas = tk.Canvas(root, bg="white", height=canvas_height, width=canvas_width,
                         scrollregion=(0,0,500,500))
canvas_entries = []

text = tk.Text(root, height=40, width=40, bg='#000000', fg='#FFFFFF')
test_threading = 0
# Clipboard Data
entry_display_len = 40
clipboard_size = 30
clipboard = []
del_buttons = []
recent_value = ""
# Session Data
session_frame = ttk.Frame(root)
session_frame.grid(row=0,column=0)

session_dir_name = "\\Test"
sessions_dir = os.path.expanduser("~\Desktop")+session_dir_name
#os.getcwd()+session_dir_name
session_buttons = []
all_sessions = []
selected_session = "Default"
selected_session_path = sessions_dir+"\\"+selected_session

is_running = True

# Clipboard functions
def copy(cop):
    recent_value = cop
    pyperclip.copy(cop)
    
    write_entry_to_session(cop)
    print("COPIED\n"+cop)
'''
Deletes an entry from the clipboard along with associated GUI elements.
'''
def delete(entry, txt, button):
    try:
        # Get the clipboard element of this entry and remove it
        y=clipboard.index(txt)
        clipboard.remove(clipboard[y])
        # Delete the GUI button for copying entry
        canvas_entries[canvas_entries.index(entry)].destroy()
        canvas_entries.remove(entry)
        # Delete the GUI button for deleting an entry
        del_buttons.remove(button)
        button.destroy()
        # Shift GUI elements
        i=0
        for x in range(0,len(clipboard)):
            #print('Clipboard Entry '+str(clipboard[x])+' row = '+str(i))
            canvas_entries[x].grid(row=i, column=0)
            del_buttons[x].grid(row=i, column=1)
            i+=1
        try:
            print("entry: "+txt)
            remove_entry_from_session(txt)
        except:
            print("failed to remove entry from session")
    except:
        print('Deletion of '+str(entry)+' with text '+str(txt)+'failed.')
'''
Clears out the clipboard
'''
def clear(*,clear_cur=False):
    # Empty the clipboard and entries (including GUI elements)
    cur_clip = pyperclip.paste()
    cur_entry = canvas_entries[-1]
    cur_del_button = del_buttons[-1]
    
    for x in clipboard:
        print("clipboard : "+str(x))
        print(x)
        if clear_cur is True and x == clear_cur or x != clear_cur:
            clipboard.remove(x)
    for x in canvas_entries:
        if clear_cur is True and x == cur_entry or x != cur_entry:
            x.destroy()
            canvas_entries.remove(x)
    for x in del_buttons:
        if clear_cur is True and x == cur_del_button or x != cur_del_button:
            x.destroy()
            del_buttons.remove(x)
# Session functions
def open_session(session):
    try:
        selected_session = session
        selected_session_path = sessions_dir+"\\"+selected_session
        file = open(selected_session_path+".txt", "r")        
    except:
        print("Cannot open session, creating new session")
        selected_session = "Default"
        file = open("Default.txt", mode="w+")
    selected_session.close()
    
def load_session_to_clipboard(session, *, additive=False):
    try:
        # If additive, append session values to clipboard else overwrite
        # clipboard values with session data
        if additive == False:
            clear()
            clipboard.append(pyperclip.paste())
        selected_session = session
        selected_session_path = sessions_dir+"\\"+selected_session
        # Parse Session file into container
        file = open(selected_session_path+".txt", "r")
        session_data = []
        for line in file:
            print(str(line))
            session_data.append(line)
            clipboard.append(line)
        file.close()
        
    except:
        print("Cannot find session, nothing was loaded to clipboard")
    
def write_entry_to_session(entry, *, session=selected_session):
    # Open up the specificed session file and append the entry to it
    # If the file cannot be found, create a new one and write the entry to it
    try:
        file = open(selected_session_path+".txt", "a")
    except:
        file = open(os.getcwd()+selected_session+".txt", "w+")
    file.write(str(entry))
    file.close()
    
def remove_entry_from_session(entry, *, session=selected_session):
    # Open up of the specified session file (selected / current session by default)
    # And overwrite previous data to remove entry
    try:
        file = open(selected_session_path+".txt", "r")
        content = str(file.read())
        new_content = content.replace(str(entry),"")
        file.close()
        
        file = open(selected_session_path+".txt", "w")
        file.write(new_content)
        file.close()
    except:
        print("file open failed")

def thread_func():
    # Creating local variant of global var to use
    global recent_value
    global test_threading
    global canvas_entries

    # Generate session selection buttons
    num_sessions = 0
    for file in os.listdir(sessions_dir):
        print(str(file))
        if file.endswith(".txt"):
            num_sessions+=1
            cur_session = file.replace(".txt","")
            print(cur_session)
            file_name = str(file).replace(".txt","")

            # Create the Button for loading the current session
            session_button = ttk.Button(session_frame, text=file_name, width=10)
            session_button.configure(command=
                lambda x=cur_session: load_session_to_clipboard(x))
            session_button.grid(row=0, column=num_sessions)
            session_buttons.append(session_button)
    # If no session was found in the directory, make one
    if num_sessions < 1:
        print("No sessions found, creating Default")
        # Create empty default session
        file = open("Default.txt", "w")
        file.close()
    
        # Create the Button for loading the default session into the clipboard
        selected_session = "Default"
        session_button = ttk.Button(file, text="Default", width=10)
        session_button.configure(command=load_session_to_clipboard(selected_session))
        session_buttons.append(session_button)

            
    while is_running is True:
        test_threading+=1
        temp_value = pyperclip.paste()
        if temp_value != recent_value or len(clipboard) == 0:
            recent_value = temp_value 

            # Check that there is room for the entry and that it is not already in clipboard
            if len(clipboard) < clipboard_size and recent_value not in clipboard:
                clipboard.append(recent_value)
                
                # Add GUI buttons for copying and deleting the new entry
                canvas_entries.append(ttk.Button(entry_canvas, text=recent_value,
                                width=100, command=lambda text=temp_value: copy(text)))
                canvas_entries[len(clipboard)-1].grid(row=len(clipboard), column=0)
                
                # Creating Button before configuring command becuase del_button needs to
                # have a refernce to itself to be able to destroy itself in delete()
                del_button = ttk.Button(entry_canvas, text="Delete", width=10)
                del_button.configure(command=lambda entry=canvas_entries[len(clipboard)-1],
                            text=recent_value, button=del_button: delete(entry, text, button))
                del_button.grid(row=len(clipboard), column=1)
                del_buttons.append(del_button)
                
            elif len(clipboard) >= clipboard_size:
                print("Clipboard Full")
            else:
                pass
                #print("Item is already inside of clipboard!")

        time.sleep(0.5)
        
if __name__ == '__main__':
    # GUI main window initialization
    root.title("Clipboard History")
    root.geometry("800x250")
    root.config(bg='#000000') #F25252 (Melon pink)
    
    root.grid()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    #text.grid(row=0, column=0, sticky=tk.NSEW)
    entry_canvas.grid(row=2, column=0, sticky=tk.EW)
    

    # create a scrollbar widget and set its command to the text widget
    scrollbar = ttk.Scrollbar(root, orient='vertical', command=entry_canvas.yview)
    scrollbar.grid(row=0, column=3, sticky="ns")

    # communicate back to the scrollbar
    #entry_canvas['yscrollcommand'] = scrollbar.set
    #entry_canvas['yscrollcommand'] = scrollbar.set
    
    entry_canvas.config(yscrollcommand=scrollbar.set)
    entry_canvas.configure(scrollregion=entry_canvas.bbox("all"))
    entry_canvas.bind('<Configure>', lambda e: entry_canvas.configure(scrollregion
                       = entry_canvas.bbox("all")))     

    second_frame = ttk.Frame(entry_canvas)

    entry_canvas.create_window((0,0), window=second_frame, anchor="nw")
    
    def print_clipboard(e):
        for i in range(0, len(clipboard)):
            print('Clipboard ['+str(i)+'] '+str(clipboard[i]))
            print(canvas_entries[i].grid_info())
            
    entry = tk.StringVar()

    # Bind values
    root.bind('<Control-b>', print_clipboard)

    clipboard_detection = Thread(target=thread_func, args=())
    clipboard_detection.start()
    
    def on_closing():
        print("Closing")
        global is_running
        is_running = False
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
