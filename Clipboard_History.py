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

# Global vars
entry_display_len = 40
clipboard_size = 30
clipboard = []
del_buttons = []
recent_value = ""
root = tk.Tk()

canvas_width = 200;
canvas_height = 200;
entry_canvas = tk.Canvas(root, bg="white", height=canvas_height, width=canvas_width)
canvas_entries = []

text = tk.Text(root, height=40, width=40, bg='#000000', fg='#FFFFFF')
test_threading = 0

def copy(cop):
    recent_value = cop
    pyperclip.copy(cop)
    print(cop)
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
            print('Clipboard Entry '+str(clipboard[x])+' row = '+str(i))
            canvas_entries[x].grid(row=i, column=0)
            del_buttons[x].grid(row=i, column=1)
            i+=1

    except:
        print('Deletion of '+str(entry)+' with text '+str(txt)+'failed.')

def thread_func():
    # Creating local variant of global var to use
    global recent_value
    global test_threading
    global canvas_entries

    while True:
        test_threading+=1
        temp_value = pyperclip.paste()
        if temp_value != recent_value:
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
    entry_canvas.grid(row=0, column=0, sticky=tk.EW)
    

    # create a scrollbar widget and set its command to the text widget
    scrollbar = ttk.Scrollbar(root, orient='vertical', command=text.yview)
    scrollbar.grid(row=2, column=1, sticky=tk.NS)

    #  communicate back to the scrollbar
    text['yscrollcommand'] = scrollbar.set
    #entry_canvas['yscrollcommand'] = scrollbar.set
         

    def print_clipboard(e):
        for i in range(0, len(clipboard)):
            print('Clipboard ['+str(i)+'] '+str(clipboard[i]))
            print(canvas_entries[i].grid_info())
            
    entry = tk.StringVar()

    # Bind values
    root.bind('<Control-b>', print_clipboard)

    clipboard_detection = Thread(target=thread_func, args=())
    clipboard_detection.start()
    
    root.mainloop()
