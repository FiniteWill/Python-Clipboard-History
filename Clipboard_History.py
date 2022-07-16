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
    # Creating local variant of global var to use
    global recent_value
    while True:
        tmp_value = pyperclip.paste()
        if tmp_value != recent_value:
            recent_value = tmp_value

            if len(clipboard) < clipboard_size:
                clipboard.append(recent_value)
                #label = tk.Label(root, text=recent_value)
                label = tk.Text(root, height = 5, width = 30)
                label.insert(tk.END, str(recent_value))
                label.pack()
            else:
                print("Clipboard Full")
        time.sleep(0.5)
        
if __name__ == '__main__':
    # GUI main window initialization
    root = tk.Tk()
    root.geometry("500x250")

    # Must take in 1 el.insert(tk.END, str(recent_value))
                label.pack()
        newEntry = tk.Label(root, text=recent_value)
        newEntry.pack()
        
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
    #root.bind('<Control-b>', handler_clipboard)

    clipboard_detection = Thread(target=thread_func, args=())
    clipboard_detection.start()
    
    root.mainloop()
