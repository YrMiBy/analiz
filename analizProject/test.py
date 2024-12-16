import tkinter.ttk as ttk

# Use a built-in theme
style = ttk.Style()
style.theme_use("winnative")  # You can also use "clam", "alt", "default", etc.

# Create your widgets with the applied theme
root = ttk.Frame()
# ... add other widgets here ...
root.mainloop()