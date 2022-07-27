""" View for Recruiting Tool """

# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.simpledialog import Dialog

# Import plotting packages
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class MainFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._vars = {
            'age': tk.IntVar(value=''),
            'miles_away': tk.StringVar(),
            'smartphone_type': tk.StringVar(),
            'study_dates': tk.StringVar(),
            'study_info': tk.StringVar(),
            'study_dates': tk.StringVar(),
            'will_not_wear': tk.StringVar(),

            'r_style': tk.StringVar(),
            'l_style': tk.StringVar(),
            'r_coupling': tk.StringVar(),
            'l_coupling': tk.StringVar(),
            'r_receiver': tk.StringVar(),
            'l_receiver': tk.StringVar(),
        }

        options = {'padx':10, 'pady':5}
        data_options = {'padx':(5,20)}

        # DATA
        lfrm_data = ttk.LabelFrame(self, text="Subject Data")
        lfrm_data.grid(row=0, column=0, columnspan=2, sticky='nsew', **options)
        # Age
        ttk.Label(lfrm_data, text="Age:").grid(row=0, column=0, sticky='e')
        ttk.Label(lfrm_data, textvariable=self._vars['age'], width=60).grid(row=0, column=1, sticky='w', **data_options)
        # Miles away
        ttk.Label(lfrm_data, text="Miles Away:").grid(row=1, column=0, sticky='e')
        ttk.Label(lfrm_data, textvariable=self._vars['miles_away']).grid(row=1, column=1, sticky='w', **data_options)
        # Smartphone
        ttk.Label(lfrm_data, text="Smartphone:").grid(row=2, column=0, sticky='e')
        ttk.Label(lfrm_data, textvariable=self._vars['smartphone_type']).grid(row=2, column=1, sticky='w', **data_options)

        # Last study
        # Study info
        ttk.Label(lfrm_data, text="Study Info:").grid(row=3, column=0, sticky='e')
        ttk.Label(lfrm_data, textvariable=self._vars['study_info']).grid(row=3, column=1, sticky='w')
        # Study dates
        ttk.Label(lfrm_data, text="Study Dates:").grid(row=4, column=0, sticky='e')
        ttk.Label(lfrm_data, textvariable=self._vars['study_dates']).grid(row=4, column=1, sticky='w')
        # Will not wear
        ttk.Label(lfrm_data, text="Will Not Wear:").grid(row=5, column=0, sticky='e')
        ttk.Label(lfrm_data, textvariable=self._vars['will_not_wear']).grid(row=5, column=1, sticky='w')

        # LEFT SIDE
        lfrm_left = ttk.LabelFrame(self, text="Left Side")
        lfrm_left.grid(row=1, column=0, **options, sticky='nsew')
        # Style
        ttk.Label(lfrm_left, text="Style:").grid(row=0, column=0, sticky='e')
        ttk.Label(lfrm_left, textvariable=self._vars['l_style']).grid(row=0, column=1, sticky='w')
        # Coupling
        ttk.Label(lfrm_left, text="Coupling:").grid(row=1, column=0, sticky='e')
        ttk.Label(lfrm_left, textvariable=self._vars['l_coupling']).grid(row=1, column=1, sticky='w')
        # Receiver length
        ttk.Label(lfrm_left, text="Receiver Length:").grid(row=2, column=0, sticky='e')
        ttk.Label(lfrm_left, textvariable=self._vars['l_receiver']).grid(row=2, column=1, sticky='w')

        # RIGHT SIDE
        lfrm_right = ttk.LabelFrame(self, text="Right Side")
        lfrm_right.grid(row=1, column=1, **options, sticky='nsew')
        ttk.Label(lfrm_right, text="Style:").grid(row=0, column=0, sticky='e')
        ttk.Label(lfrm_right, textvariable=self._vars['r_style']).grid(row=0, column=1, sticky='w')
        # Coupling
        ttk.Label(lfrm_right, text="Coupling:").grid(row=1, column=0, sticky='e')
        ttk.Label(lfrm_right, textvariable=self._vars['r_coupling']).grid(row=1, column=1, sticky='w')
        # Receiver length
        ttk.Label(lfrm_right, text="Receiver Length:").grid(row=2, column=0, sticky='e')
        ttk.Label(lfrm_right, textvariable=self._vars['r_receiver']).grid(row=2, column=1, sticky='w')

        # Call audio plot
        self.plot_audio()


    def plot_audio(self):
        """ Create figure axis for audiogram plot """
        figure = Figure(figsize=(5, 4), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self)
        ax1 = figure.add_subplot()
        figure_canvas.get_tk_widget().grid(row=10, column=0, columnspan=2, pady=10, padx=10)
        return ax1


class SubjectTree(tk.Frame):
    """ Treeview for database subjects """
    def __init__(self, parent, db, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        style = ttk.Style()
        style.configure("new.Treeview", highlightthickness=5, bd=4)
        style.configure("new.Treeview.Heading", font=('TkDefaultFont', 10, 'bold'))
        style.configure("new.Vertical.TScrollbar")

        # Initialize
        self.db = db
        self.rowconfigure(0, weight=1)

        # Tree
        # Get subs from dataframe
        subjects = self.db.data['Subject Id']
        columns = ('subject_id')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=20, style='new.Treeview')
        self.tree.column("# 1", width=100, anchor=tk.CENTER)
        self.tree.heading('subject_id', text='Subject ID')
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.tree.bind('<<TreeviewSelect>>', self._item_selected)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview, style='new.Vertical.TScrollbar')
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, rowspan=10, column=1, sticky='ns')

        # Add subjects to tree
        for subject in subjects:
            self.tree.insert('', tk.END, values=subject)


    def _item_selected(self, *args):
        """ Trigger event that tree item was selected """
        self.event_generate('<<TreeviewSelect>>')
