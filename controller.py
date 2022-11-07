""" Subject Browser GUI for recruiting. 

    App that provides (1) filtering of subjects in the recruitment 
    database, and (2) browsing filtered subject records. 

    Written by: Travis M. Moore
    Created: 26 Jul, 2022
    Last edited: 7 Nov, 2022
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Import custom modules
from models import dbmodel
from models import constants as c
from models import audio_dict
from views import filterview as fv
from views import browseview as bv
from views import treeview as tv
from models.constants import FieldTypes as FT


#########
# BEGIN #
#########
class App(tk.Tk):
    """ Controller for Subject Browser
    """

    # Define data types
    var_types = {
        FT.string: tk.StringVar,
        FT.string_list: tk.StringVar,
        FT.short_string_list: tk.StringVar,
        FT.iso_date_string: tk.StringVar,
        FT.long_string: tk.StringVar,
        FT.decimal: tk.DoubleVar,
        FT.integer: tk.IntVar,
        FT.boolean: tk.BooleanVar
    }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ Initialize main window and add views
        """

        # Initialize main window
        self.title('Subject Browser')
        self.resizable(0,0)

        # Load in database
        self.db = dbmodel.SubDB("new")

        # Load in dict fields for displaying records
        self.dbmodel = dbmodel.DataModel()
        fields = self.dbmodel.fields
        self._vars = {
            key: self.var_types[spec['type']]()
            for key, spec in fields.items()
        }

        # Create notebook widget #
        # Notebook has two tabs: Filter, and Browse
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        # Create tab frames
        self.frm_filter = ttk.Frame(self.notebook)
        self.frm_browse = ttk.Frame(self.notebook)
        self.frm_filter.grid(row=0, column=0, ipadx=10, ipady=10)
        self.frm_browse.grid(row=0, column=0, ipadx=10, ipady=10)
        # Add tab frames to notebook
        self.notebook.add(self.frm_filter, text='Filter')
        self.notebook.add(self.frm_browse, text='Browse')

        # Add views to main window
        self.create_filter_frame(self.db, self.dbmodel)
        self.create_tree_widget()
        self.create_browse_frame(self.dbmodel)
        self.center_window()


    #############
    # Functions #
    #############
    def create_filter_frame(self, db, dbmodel):
        self.filter_frame = fv.FilterFrame(self.frm_filter, db, dbmodel)
        self.filter_frame.grid(row=0, column=0)


    def create_tree_widget(self):
        """ Create tree widget populated with subject IDs
        """
        self.sub_tree = tv.SubjectTree(self.frm_browse, self.db)
        self.sub_tree.grid(row=0, column=0, sticky='ns')
        self.sub_tree.bind('<<TreeviewSelect>>', self._item_selected)


    def create_browse_frame(self, dbmodel):
        """ Create browse view to load into notebook 'Browse' tab
        """
        self.browse_frame = bv.BrowseFrame(self.frm_browse, dbmodel)
        self.browse_frame.grid(row=0, column=2)


    def center_window(toplevel):
        """ Center the root window 
        """
        toplevel.update_idletasks()
        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        toplevel.geometry("+%d+%d" % (x, y)) 


    def _item_selected(self, *_):
        """ Get selected subject number from tree 
            and retrieve subject data
        """
        for selected_item in self.sub_tree.tree.selection():
            # Get item from mouse click
            item = self.sub_tree.tree.item(selected_item)
            # Convert item to record number
            record = int(item['values'][0])

            # Subject Data
            self._vars['age'] = self.db.data[self.db.data['Subject Id'] == record]['Age'].values[0]
            self._vars['miles_away'] = self.db.data[self.db.data['Subject Id'] == record]['Miles From Starkey'].values[0]
            self._vars['smartphone_type'] = self.db.data[self.db.data['Subject Id'] == record]['Smartphone Type'].values[0]
            self._vars['will_not_wear'] = self.db.data[self.db.data['Subject Id'] == record]['Will Not Wear'].values[0]
            # Study dates and names parsing
            latest_study = self.db.data[self.db.data['Subject Id'] == record]['Latest Study'].values[0]
            study_dates = [z.split(')')[0] for z in latest_study.split('(') if ')' in z]
            try:
                study_dates = study_dates[0]
            except:
                study_dates = '-'
            study_info = latest_study.split('(')[0]
            self._vars['study_dates'] = study_dates
            self._vars['study_info'] = study_info
            # Hearing aid data
            self._vars['r_style'] = self.db.data[self.db.data['Subject Id'] == record]['RightStyle'].values[0]
            self._vars['l_style'] = self.db.data[self.db.data['Subject Id'] == record]['LeftStyle'].values[0]
            self._vars['r_coupling'] = self.db.data[self.db.data['Subject Id'] == record]['Right Earmold Style'].values[0]
            self._vars['l_coupling'] = self.db.data[self.db.data['Subject Id'] == record]['Left Earmold Style'].values[0]
            self._vars['r_receiver'] = self.db.data[self.db.data['Subject Id'] == record]['Right Ric Cable Size'].values[0]
            self._vars['l_receiver'] = self.db.data[self.db.data['Subject Id'] == record]['Left Ric Cable Size'].values[0]

            try:
                coupling, vent_size = self.db.coupling(record)
                self._vars['r_rec_coupling'] = coupling['Right']
                self._vars['l_rec_coupling'] = coupling['Left']
                self._vars['r_rec_vent'] = vent_size['Right']
                self._vars['l_rec_vent'] = vent_size['Left']
            except TypeError:
                messagebox.showerror(title="Error!",
                    message="An error occurred calculating the coupling type!",
                    detail="Cannot determine the recommendation threshold."
                )

            # Send db data to View labels to display
            self.browse_frame.load(self._vars)

            # Call audio display function
            self._show_audio(record)
            

    def _show_audio(self, record):
        """ Retrieve figure axis handle and plot audio """
        ax1 = self.browse_frame.plot_audio()
        self.db.audio_ac(record, ax1)


if __name__ == '__main__':
    app = App()
    app.mainloop()
