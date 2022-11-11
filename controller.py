""" Subject Browser GUI for recruiting. 

    App that provides (1) filtering of subjects in the recruitment 
    database, and (2) browsing filtered subject records. 

    Written by: Travis M. Moore
    Created: Jul 26, 2022
    Last edited: Nov 11, 2022
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# Import system packages
import os
import sys

# Import misc packages
import webbrowser
import markdown

# Import custom modules
from models import dbmodel
from models import filtermodel
from models import audio_dict
from views import treeview as tv
from views import filterview as fv
from views import browseview as bv
from menus import mainmenu as menu_main
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

        ######################################
        # Initialize Models, Menus and Views #
        ######################################
        # Main window setup
        self.title('Subject Browser')
        self.resizable(1,1)
        self.columnconfigure(index=0, weight=1)

        # Create filter settings dict
        self.filter_dict = {}

        # Create filter model
        self.filtermodel = filtermodel.FilterList()

        # Load in sample database at start
        # If running from compiled, look in compiled temporary location
        print('Looking for startup database in temporary location')
        db_path = self.resource_path('sample_data.csv')
        file_exists = os.access(db_path, os.F_OK)
        if not file_exists:
            print('Not found!')
            print('Checking local script version location for database')
            self.db = dbmodel.SubDB(".\\assets\\sample_data.csv")
        else:
            self.db = dbmodel.SubDB(db_path)
            
        # Load in dict fields for displaying records
        self.dbmodel = dbmodel.DataModel()
        fields = self.dbmodel.fields
        self._vars = {
            key: self.var_types[spec['type']]()
            for key, spec in fields.items()
        }

        # Create notebook widget #
        # Notebook has two tabs: Filter, and Browse
        self.notebook = ttk.Notebook(self, takefocus=0)
        self.notebook.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Create tab frames
        self.frm_filter = ttk.Frame(self.notebook)
        self.frm_browse = ttk.Frame(self.notebook)
        self.frm_filter.grid(row=0, column=0, ipadx=10, ipady=10, sticky='ew')
        self.frm_filter.columnconfigure(index=0, weight=1)
        self.frm_browse.grid(row=0, column=0, ipadx=10, ipady=10)
        self.frm_browse.columnconfigure(index=0, weight=1)

        # Add tab frames to notebook
        self.notebook.add(self.frm_filter, text='Filter')
        self.notebook.add(self.frm_browse, text='Browse')

        # Load menus
        menu = menu_main.MainMenu(self)
        self.config(menu=menu)


        ##############################
        # Create callback dictionary #
        ##############################
        event_callbacks = {
            # File menu
            '<<FileImportFullDB>>': lambda _: self._import_full(),
            '<<FileImportFilteredDB>>': lambda _: self._import_filtered(),
            '<<FileExportDB>>': lambda _: self._export_db(),
            '<<FileImportList>>': lambda _: self._import_filter_list(),
            '<<FileExportList>>': lambda _: self._export_filter_list(),
            '<<FileQuit>>': lambda _: self._quit(),

            # Tools menu
            '<<ToolsReset>>': lambda _: self._reset_filters(),

            # Help menu
            '<<Help>>': lambda _: self._show_help(),

            # Filter view
            '<<Filter>>': lambda _: self._on_filter(),
        }

        # Bind callbacks to sequences
        for sequence, callback in event_callbacks.items():
            self.bind(sequence, callback)


        ############################
        # Add Views To Main Window #
        ############################
        self.create_filter_frame(self.db, self.filter_dict)
        self.create_tree_widget()
        self.create_browse_frame(self.db, self.dbmodel)
        self.center_window()


    #####################
    # General Functions #
    #####################
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

    
    def resource_path(self, relative_path):
        """ Get the absolute path to compiled resources
        """
        try:
            # PyInstaller creates a temp folder and 
            # stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


    #######################
    # File Menu Functions #
    #######################
    def _import_full(self):
        """ Load FULL database .csv file (i.e., not previously
            imported)
        """
        # Query user for database .csv file
        filename = filedialog.askopenfilename()
        # Do nothing if cancelled
        if not filename:
            return
        # If a valid filename is found, load it
        self.db.load_db(filename)
        # Remove junk records
        self._initial_scrub()
        # Reload the treeview with imported database
        self.sub_tree._load_tree()


    def _import_filtered(self):
        """ Load previously-imported database .csv file
            (i.e., an file exported from this app)
        """
        # Query user for database .csv file
        filename = filedialog.askopenfilename()
        # Do nothing if cancelled
        if not filename:
            return
        # If a valid filename is found, load it
        self.db.load_filtered_db(filename)
        # Reload the treeview with imported database
        self.sub_tree._load_tree()


    def _export_db(self):
        """ Write current database object to .csv file
        """
        self.db.write()


    def _import_filter_list(self):
        """ Read external filter values list and update filterview
            comboboxes with values
        """
        # Get updated filter values dict
        self.filter_dict = self.filtermodel.import_filter_dict()
        # Update filterview comboboxes
        self.filter_frame._load_filters(self.filter_dict)


    def _export_filter_list(self):
        """ Write filterview combobox values to .csv file
        """
        self.filtermodel.export_filters(self.filter_frame.filter_dict)


    def _quit(self):
        """ Exit the application
        """
        self.destroy()


    def _initial_scrub(self):
        """ Perform perfunctory junk record removal
        """
        # Clear any previous output from textbox
        self.filter_frame.txt_output.delete('1.0', tk.END)
        # Provide feedback
        self.filter_frame.txt_output.insert(tk.END, 
                f"Loaded database records\n" +
                f"Remaining Candidates: {str(self.db.data.shape[0])}\n\n")
        # Create dictionary of filtering values
        scrub_dict = {
            1: ("Status", "contains", ["-", "Active"]),
            2: ("Good Candidate", "does not equal", "Poor"),
            3: ("Employment Status", "does not equal", "Employee"),
            4: ("Miles From Starkey", "<=", "60")
        }
        # Call filtering function
        self._filter(scrub_dict)
        # Update tree widget after filtering
        self.sub_tree._load_tree()


    ########################
    # Tools Menu Functions #
    ########################
    def _reset_filters(self):
        self.filter_frame._clear_filters()


    #######################
    # Help Menu Functions #
    #######################
    def _show_help(self):
        """ Create html help file and display in default browser
        """
        print('Looking for help file in compiled version temp location...')
        help_file = self.resource_path('README\\README.html')
        file_exists = os.access(help_file, os.F_OK)
        if not file_exists:
            print('Not found!\nChecking for help file in ' +
                'local script version location')
            # Read markdown file and convert to html
            with open('README.md', 'r') as f:
                text = f.read()
                html = markdown.markdown(text)

            # Create html file for display
            with open('.\\assets\\README\\README.html', 'w') as f:
                f.write(html)

            # Open README in default web browser
            webbrowser.open('.\\assets\\README\\README.html')
        else:
            help_file = self.resource_path('README\\README.html')
            webbrowser.open(help_file)


    ##########################
    # Filter Frame Functions #
    ##########################
    def create_filter_frame(self, db, filter_dict):
        """ Create filter view to load into notebook 'Filter' tab
        """
        self.filter_frame = fv.FilterFrame(self.frm_filter, db, filter_dict)
        self.filter_frame.grid(row=0, column=0, sticky='ew')


    def _on_filter(self):
        """ Called from filterview 'Filter Records' button event. 
            Update filter dict and pass to filter func.
        """
        # Update local filter dict with values from filterview
        self.filter_dict = self.filter_frame.filter_dict
        # Call filter func using updated filter dict
        self._filter(self.filter_dict)


    def _filter(self, filter_val_dict):
        """ Call filter method of dbmodel to subset database.
            Update tree widget after filtering. 
        """
        if not filter_val_dict:
            messagebox.showwarning(title="No Filters Found",
                message="No filters have been set!")
            return

        # Clear any previous output from textbox
        self.filter_frame.txt_output.delete('1.0', tk.END)

        # Remind user what the previous record count was
        self.filter_frame.txt_output.insert(tk.END,
            f"Candidates before filtering: {str(self.db.data.shape[0])}\n\n")

        try:
            for val in filter_val_dict:
                self.db.filter(
                    filter_val_dict[val][0],
                    filter_val_dict[val][1],
                    filter_val_dict[val][2]
                )
                self.filter_frame.txt_output.insert(tk.END, 
                    f"Filtering by: {filter_val_dict[val][0]} " +
                    f"{filter_val_dict[val][1]} {filter_val_dict[val][2]}...\n" +
                    f"Remaining Candidates: {str(self.db.data.shape[0])}\n\n")
        except TypeError:
            messagebox.showerror(title="Filtering Error",
                message="Cannot compare different data types!",
                detail="Filtering a previously-exported database file is " +
                    "not currently fully supported. It is likely that " + 
                    "the data type of some columns has been changed. Your " +
                    "request cannot be processed.")
            return

        # Update tree widget after filtering
        self.sub_tree._load_tree()


    ##########################
    # Browse Frame Functions #
    ##########################
    def create_tree_widget(self):
        """ Create tree widget populated with subject IDs
        """
        self.sub_tree = tv.SubjectTree(self.frm_browse, self.db)
        self.sub_tree.grid(row=0, column=0, sticky='ns')
        self.sub_tree.bind('<<TreeviewSelect>>', self._item_selected)


    def create_browse_frame(self, database, dbmodel):
        """ Create browse view to load into notebook 'Browse' tab
        """
        self.browse_frame = bv.BrowseFrame(self.frm_browse, database, dbmodel)
        self.browse_frame.grid(row=0, column=2)


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
        """ Retrieve figure axis handle and plot audio 
        """
        ax1 = self.browse_frame.plot_audio()
        self.db.audio_ac(record, ax1)


if __name__ == '__main__':
    app = App()
    app.mainloop()
