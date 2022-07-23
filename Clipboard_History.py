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
def delete(entry):
    clipboard.remove(entry)
    
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
                
                y = 0
                y = clipboard.index(str(temp_value))

                canvas_entries.append(ttk.Button(entry_canvas, text=recent_value,
                                         width=100, command=lambda x=temp_value:copy(x)))
                canvas_entries[len(clipboard)-1].grid(row=len(clipboard), column=0) 
      
            elif len(clipboard) >= clipboard_size:
                print("Clipboard Full")
            else:
                pass
                #print("Item is already inside of clipboard!")

        time.sleep(0.5)
        
if __name__ == '__main__':
    # GUI main window initialization
    root.title("Clipboard History")
    root.geometry("500x250")
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
         
    def handler_b(e):
        pyperclip.copy("Testing the copy mechanism")
        print("copied")
        
    def handler_clipboard(e):
        for i in clipboard:
            print(str(i))
              
    
    entry = tk.StringVar()

    # Bind values
    #root.bind('<Return>', handler)
    #root.bind('<Control-a>', handler_b)
    root.bind('<Control-b>', handler_clipboard)

    clipboard_detection = Thread(target=thread_func, args=())
    clipboard_detection.start()
    
    root.mainloop()
