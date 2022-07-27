""" Recruiting Tool:
    GUI for browsing subjects from the 'database'

    Written by: Travis M. Moore
    Created: Jul 26, 2022
"""

# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

# Import custom modules
import models as m
import audio_dict as a
import views as v

# Import plotting packages
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import random


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('Treeview demo')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Load in database
        self.db = m.SubDB()

        # Set up main window
        self.create_tree_widget()
        self.create_main_frame()


    def create_tree_widget(self):
        self.sub_tree = v.SubjectTree(self, self.db)
        self.sub_tree.grid(row=0, column=0, sticky='ns')
        self.sub_tree.bind('<<TreeviewSelect>>', self._item_selected)


    def create_main_frame(self):
        self.main_frame = v.MainFrame(self)
        self.main_frame.grid(row=0, column=2)


    def _item_selected(self, *_):
        for selected_item in self.sub_tree.tree.selection():
            item = self.sub_tree.tree.item(selected_item)
            record = int(item['values'][0])
            self.main_frame._vars['age'].set(self.db.data[self.db.data['Subject Id'] == record]['Age'].values[0])
            self.main_frame._vars['miles_away'].set(self.db.data[self.db.data['Subject Id'] == record]['Miles From Starkey'].values[0])
            self.main_frame._vars['smartphone_type'].set(self.db.data[self.db.data['Subject Id'] == record]['Smartphone Type'].values[0])
            self.main_frame._vars['will_not_wear'].set(self.db.data[self.db.data['Subject Id'] == record]['Will Not Wear'].values[0])

            # Study dates and names parsing
            latest_study = self.db.data[self.db.data['Subject Id'] == record]['Latest Study'].values[0]
            study_dates = [z.split(')')[0] for z in latest_study.split('(') if ')' in z]
            try:
                study_dates = study_dates[0]
            except:
                study_dates = '-'
            study_info = latest_study.split('(')[0]
            self.main_frame._vars['study_dates'].set(study_dates)
            self.main_frame._vars['study_info'].set(study_info)

            # Hearing aid data
            self.main_frame._vars['r_style'].set(self.db.data[self.db.data['Subject Id'] == record]['RightStyle'].values[0])
            self.main_frame._vars['l_style'].set(self.db.data[self.db.data['Subject Id'] == record]['LeftStyle'].values[0])
            self.main_frame._vars['r_coupling'].set(self.db.data[self.db.data['Subject Id'] == record]['Right Earmold Style'].values[0])
            self.main_frame._vars['l_coupling'].set(self.db.data[self.db.data['Subject Id'] == record]['Left Earmold Style'].values[0])
            self.main_frame._vars['r_receiver'].set(self.db.data[self.db.data['Subject Id'] == record]['Right Ric Cable Size'].values[0])
            self.main_frame._vars['l_receiver'].set(self.db.data[self.db.data['Subject Id'] == record]['Left Ric Cable Size'].values[0])

            # Call audio display function
            self._show_audio()


    def _show_audio(self):
        """ Plot audiogram for selected subject """
        figure = Figure(figsize=(5, 5), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self)
        #NavigationToolbar2Tk(figure_canvas, self)
        axes = figure.add_subplot()
        xs = [random.randint(10,20) for i in range(0,4)]
        axes.plot(xs, [5,6,7,8])
        #db.audio_ac(str(record))
        figure_canvas.get_tk_widget().grid(row=10, column=2)#(side=tk.TOP, fill=tk.BOTH, expand=True)


if __name__ == '__main__':
    app = App()
    app.mainloop()
