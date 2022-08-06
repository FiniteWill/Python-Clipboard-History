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
from context_menu import menus

# GUI Data
root = tk.Tk()
main_frame = ttk.Frame(root)

# Canvas that displays history entries
canvas_width = 200;
canvas_height = 200;
entry_canvas = tk.Canvas(root, bg="white", height=canvas_height, width=canvas_width,
                         scrollregion=(0,0,500,500))
canvas_entries = []

text = tk.Text(root, height=40, width=40, bg='#000000', fg='#FFFFFF')

# Create Entry (context menu command) GUI elements
create_entry_display = []
create_entry_del_buttons = []
create_entry_is_open = False

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

# Context Menu functions
def popup(e):
    menu.tk_popup(e.x_root, e.y_root)

# Clipboard functions
def copy(cop):
    recent_value = cop
    pyperclip.copy(cop)
    
    write_entry_to_session(cop)
    print("COPIED\n"+cop)
def copy_all():
    print("COPYALL TEST")
    full_copy_str = str()
    for x in clipboard:
        full_copy_str+=str(x+"\n")
    pyperclip.copy(full_copy_str)
    global recent_value
    recent_value = pyperclip.paste()
        
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
def clear_test(e):
    clear(clear_cur=True)
'''
Clears out the clipboard
'''
def clear(*,clear_cur=False):
    # Empty the clipboard and entries (including GUI elements)
    print("CLEAR")
    cur_clip = pyperclip.paste()
    cur_entry = canvas_entries[-0]
    cur_del_button = del_buttons[-0]

    print("clipboard length : "+str(len(clipboard)))
    for x in reversed(clipboard):
        print("clipboard : "+str(x))
        clipboard.remove(x)
    for x in reversed(canvas_entries):
        x.destroy()
        canvas_entries.remove(x)
    for x in reversed(del_buttons):
        x.destroy()
        del_buttons.remove(x)
    if clear_cur == True:
        pyperclip.copy("")

    print("clipboard length after clear : "+str(len(clipboard)))
        
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
            clear(clear_cur=True)
        selected_session = session
        selected_session_path = sessions_dir+"\\"+selected_session
        # Parse Session file into container
        file = open(selected_session_path+".txt", "r")
        session_data = []
        for line in file:
            print("line from session: " + str(line))
            # Copy data to clipboard and create GUI elements for entry
            #session_data.append(line)
            #clipboard.append(line)
            #GUI_create_entry(line)
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

def GUI_create_entry(temp_value):
    # Add GUI buttons for copying and deleting the new entry
    canvas_entries.append(ttk.Button(entry_canvas, text=recent_value,
                    width=100, command=lambda text=temp_value: copy(text)))
    print("CANVAS_ENTRIES : "+str(len(canvas_entries))+" CLIPBOARD : "+str(len(clipboard)))
    canvas_entries[len(clipboard)-1].grid(row=len(clipboard), column=0)

    # Creating Button before configuring command becuase del_button needs to
    # have a refernce to itself to be able to destroy itself in delete()
    del_button = ttk.Button(entry_canvas, text="Delete", width=10)
    del_button.configure(command=lambda entry=canvas_entries[len(clipboard)-1],
                text=recent_value, button=del_button: delete(entry, text, button))
    del_button.grid(row=len(clipboard), column=1)
    del_buttons.append(del_button)
    
# Create Entry (from context menu) functions
def GUI_del_custom_entry(entry, del_button):
    create_entry_display.remove(entry)
    entry.destroy()
    create_entry_del_buttons.remove(del_button)
    del_button.destroy()    
    
    
def GUI_open_create_entry_menu():
    global create_entry_is_open
    if create_entry_is_open == False:
        create_entry_is_open = True
        # Creating a new window object for the Entry Creator
        create_entry_window = tk.Toplevel(root)
        create_entry_window.title("Entry Creator")
        create_entry_window.geometry("200x200")
        create_entry_window.config(bg="#000000")

        def close_entry_window():
            print("Closing Entry Creator")
            global create_entry_is_open
            create_entry_is_open = False
            create_entry_window.destroy()

        create_entry_window.protocol("WM_DELETE_WINDOW", close_entry_window)
        
        create_entry_window.grid()
        create_entry_window.grid_columnconfigure(0, weight=1)
        create_entry_window.grid_rowconfigure(0, weight=1)
        
        create_entry_menu = tk.Frame(create_entry_window)
        create_entry_display = []
        create_entry_del_buttons = []
        # Recreate the current clipboard entries to display
        for entry in canvas_entries:
            # Create entry GUI elements
            cur_entry = ttk.Button(create_entry_menu,
                text=clipboard[canvas_entries.index(entry)])
            cur_del_button = ttk.Button(create_entry_menu, text="Delete", width=10)
            cur_del_button.configure(command=lambda ent= cur_entry,
                delete = cur_del_button: GUI_del_custom_entry(ent, delete))
            # Add entries to containers
            create_entry_display.append(cur_entry)
            create_entry_del_buttons.append(cur_del_button)
            # Add GUI elements to the window
            cur_entry.grid(row = len(create_entry_display), column = 0) 
            cur_del_button.grid(row = len(create_entry_display), column = 1)
'''
Thread that handles the updating of the clipboard data and GUI widgets
'''
def thread_func():
    # Creating local variant of global var to use
    global recent_value
    global canvas_entries

    # Generate session selection buttons
    num_sessions = 0
    for file in os.listdir(sessions_dir):
        #print(str(file))
        if file.endswith(".txt"):
            num_sessions+=1
            cur_session = file.replace(".txt","")
            #print(cur_session)
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
        temp_value = pyperclip.paste()
        if temp_value != recent_value or len(clipboard) == 0:
            recent_value = temp_value 

            # Check that there is room for the entry and that it is not already in clipboard
            if len(clipboard) < clipboard_size and recent_value != "" and recent_value not in clipboard:
                clipboard.append(recent_value)
                
                GUI_create_entry(temp_value)
                
            elif len(clipboard) >= clipboard_size:
                print("Clipboard Full")
            else:
                pass
                #print("Item is already inside of clipboard!")

        time.sleep(0.5)

'''
Main thread that handles TKinter widget setup, control bindings,
and starting the TKinter mainloop()
'''
if __name__ == '__main__':
    # GUI main window initialization
    root.title("Clipboard History")
    root.geometry("800x250")
    root.config(bg='#000000') #F25252 (Melon pink)
    
    root.grid()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)


    # Menu Popup
    menu = tk.Menu(root, tearoff=False)
    menu.add_command(label="Create New Session")
    menu.add_command(label="Create New Entry (Text Only)",
        command = GUI_open_create_entry_menu)
    menu.add_command(label="Edit Entry (Text Only)")
    menu.add_command(label="Copy All Contents", command =copy_all)

    
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
    root.bind('<Control-o>', clear_test)
    root.bind('<Button-3>', popup) 

    clipboard_detection = Thread(target=thread_func, args=())
    clipboard_detection.start()
    
    def on_closing():
        print("Closing")
        global is_running
        is_running = False
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
