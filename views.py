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
        lfrm_left.grid(row=1, column=0, **options, sticky='e')
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
        lfrm_right.grid(row=1, column=1, **options, sticky='w')
        ttk.Label(lfrm_right, text="Style:").grid(row=0, column=0, sticky='e')
        ttk.Label(lfrm_right, textvariable=self._vars['r_style']).grid(row=0, column=1, sticky='w')
        # Coupling
        ttk.Label(lfrm_right, text="Coupling:").grid(row=1, column=0, sticky='e')
        ttk.Label(lfrm_right, textvariable=self._vars['r_coupling']).grid(row=1, column=1, sticky='w')
        # Receiver length
        ttk.Label(lfrm_right, text="Receiver Length:").grid(row=2, column=0, sticky='e')
        ttk.Label(lfrm_right, textvariable=self._vars['r_receiver']).grid(row=2, column=1, sticky='w')


class SubjectTree(tk.Frame):
    """ Display for database subjects """
    def __init__(self, parent, db, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.db = db
        #self.item_selected = item_selected

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        columns = ('subject_id')

        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=20)

        # Tree headings
        self.tree.heading('subject_id', text='Subject ID')

        self.tree.grid(row=0, column=0, sticky='nsew')

        self.tree.bind('<<TreeviewSelect>>', self._item_selected)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, rowspan=10, column=1, sticky='ns')

        # Get subs from dataframe
        contacts = self.db.data['Subject Id']

        # Add df data to tree
        for contact in contacts:
            self.tree.insert('', tk.END, values=contact)

    def _item_selected(self, *args):
        global row_id
        print("Item selected and View responded!")
        self.event_generate('<<TreeviewSelect>>')
        row_id = self.tree.focus()
        print(row_id)


# Audiogram
class PlotFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
    def add_mpl_figure(self, fig):
        self.mpl_canvas = FigureCanvasTkAgg(fig, self)
        self.mpl_canvas.draw()
        self.mpl_canvas.get_tk_widget().grid(row=9, column=2)#pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        #self.toolbar = NavigationToolbar2Tk(self.mpl_canvas, self)
        #self.toolbar.update()
        #self.mpl_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class MPLPlot(Figure):
    def __init__(self):
        Figure.__init__(self, figsize=(5,5), dpi=100)
        self.plot = self.add_subplot(111)
        self.plot.plot([1,2,3,4,5], [6,7,8,9,0])

