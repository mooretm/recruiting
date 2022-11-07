import tkinter as tk
from tkinter import ttk

# root window
root = tk.Tk()
root.geometry('400x300')
root.title('Notebook Demo')

# Create a notebook
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, pady=10, sticky='nsew')

# Create frames
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)

frame1.grid(row=0, column=0, sticky='nsew')
frame2.grid(row=0, column=0, sticky='nsew')

# Add frames to notebook
notebook.add(frame1, text='Sort', sticky='nsew')
notebook.add(frame2, text='Browse')


# Add stuff to frames
ttk.Label(frame1, text="Use this tab to sort subjects").grid(row=0, column=0, sticky='nsew')
ttk.Label(frame2, text="Use this tab to browse your sorted subjects").grid(row=0, column=0, sticky='nsew')

root.mainloop()
