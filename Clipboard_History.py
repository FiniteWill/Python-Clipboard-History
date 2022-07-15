import time
import sys
# Used to access clipboard
import pyperclip
# Easier methods for listening and responding to user input
from pynput import keyboard
from pynput.keyboard import Key
# Simple GUI functionality
import tkinter as tk
# Use threading to have Tkinter's mainloop
# and updating clipboard happen simultaneously
from threading import Thread

# Global vars
entry_display_len = 40
clipboard_size = 30
clipboard = []
recent_value = ""
    
def thread_func():
    while True:
        # Creating local variant of global var to use
        global recent_value
        local_rv = recent_value

        
        tmp_value = pyperclip.paste()
        #print(str(tmp_value + " " + recent_value))
        if tmp_value != recent_value:
            local_rv = tmp_value
            print("Value changed: %s" % str(local_rv)[:40])

            if len(clipboard) < clipboard_size:
                clipboard.append(local_rv)
                #label = tk.Label(root, text="ddeosdf")
                #label.pack()
            
        time.sleep(0.5)
        
if __name__ == '__main__':
    # GUI main window initialization
    root = tk.Tk()
    root.geometry("500x250")

    # Must take in 1 param (the event it was called from)
    def handler(e):
        print("test")
        newEntry = tk.Label(root, text=recent_value)
        newEntry.pack()
    def handler_b(e):
        pyperclip.copy("Testing the copy mechanism")
        print("copied")
              
    
    entry = tk.StringVar()

    # Bind values
    root.bind('<Return>', handler)
    root.bind('<Control-a>', handler_b)

    clipboard_detection = Thread(target=thread_func, args=())
    clipboard_detection.start()
    
    root.mainloop()
