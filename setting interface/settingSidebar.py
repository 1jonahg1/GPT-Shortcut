import tkinter as tk
import keyboard
import pyperclip

def toggle_sidebar():
    if sidebar.winfo_viewable():
        sidebar.withdraw()  # Hide the sidebar
    else:
        sidebar.deiconify()  # Show the sidebar

sidebar = tk.Tk()
sidebar.title("Sidebar")  # Customize the title as needed
# Add your widgets and settings to the sidebar window here



sidebar.protocol("WM_DELETE_WINDOW", toggle_sidebar)  # Handle window close event

sidebar.withdraw()  # Hide the sidebar initially
tk.mainloop()  # Start the GUI event loop

