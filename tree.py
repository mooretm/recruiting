""" Recruiting Tool:
    GUI for browsing subjects from the 'database'

    Written by: Travis M. Moore
    Created: Jul 26, 2022
"""

# Import GUI packages
import tkinter as tk

# Import custom modules
import models as m
import views as v
from constants import FieldTypes as FT


class App(tk.Tk):
    """ Controller """

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

        # Initialize
        self.title('Subject Browser')
        self.resizable(0,0)

        # Load in database
        self.db = m.SubDB("new")

        # Load in dict fields for displaying records
        self.model = m.DataModel()
        fields = self.model.fields
        self._vars = {
            key: self.var_types[spec['type']]()
            for key, spec in fields.items()
        }

        # Set up main window
        self.create_tree_widget()
        self.create_main_frame(self.model)
        self.center_window()


    def create_tree_widget(self):
        self.sub_tree = v.SubjectTree(self, self.db)
        self.sub_tree.grid(row=0, column=0, sticky='ns')
        self.sub_tree.bind('<<TreeviewSelect>>', self._item_selected)


    def create_main_frame(self, model):
        self.main_frame = v.MainFrame(self, model)
        self.main_frame.grid(row=0, column=2)


    def center_window(toplevel):
        """ Center the root window """
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
            item = self.sub_tree.tree.item(selected_item)
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

            coupling, vent_size = self.db.coupling(record)
            self._vars['r_rec_coupling'] = coupling['Right']
            self._vars['l_rec_coupling'] = coupling['Left']
            self._vars['r_rec_vent'] = vent_size['Right']
            self._vars['l_rec_vent'] = vent_size['Left']

            # Send db data to View labels to display
            self.main_frame.load(self._vars)

            # Call audio display function
            self._show_audio(record)
            

    def _show_audio(self, record):
        """ Retrieve figure axis handle and plot audio """
        ax1 = self.main_frame.plot_audio()
        self.db.audio_ac(record, ax1)


if __name__ == '__main__':
    app = App()
    app.mainloop()
