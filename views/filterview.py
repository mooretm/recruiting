""" Subject filter options view for Subject Browser 
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk

# Import misc packages
import uuid

# # Import plotting packages
# import matplotlib
# matplotlib.use('TkAgg')
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Import custom modules
from models.constants import FieldTypes as FT


#########
# BEGIN #
#########
class FilterFrame(ttk.Frame):
    """ Filtering view for 'Filter' tab of notebook
    """

    def __init__(self, parent, database, dbmodel, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.db = database

        self.attributes = list(self.db.data.columns)
        self.attributes.sort()
        
        #self.operators = ['==', '!=', '>', '>=', '<', '<=', 'contains']
        self.operators = ["equals", "does not equal", "contains", ">", ">=", "<", "<="]

        style = ttk.Style()
        style.configure("rec.TLabel", foreground='green')

        options = {'padx':10, 'pady':10}

        # Create frames
        frm_filter = ttk.Frame(self)
        frm_filter.grid(row=0, column=0)

        for ii in range(1,4):
            frm_filter.columnconfigure(index=ii, weight=1)



        label_text = ['Attribute', 'Operator', 'Value']
        for idx, label in enumerate(label_text, start=1):
            ttk.Label(frm_filter, text=label).grid(
                row=5, column=idx, pady=10)

        ttk.Button(frm_filter, text="Write Values", 
            command=self._write2box).grid(row=20, column=2, sticky='ew')

        self.txt_output = tk.Text(frm_filter, height=10, width=50)
        self.txt_output.grid(row=21, column=1, columnspan=4, **options)


        ###############################
        # Create filtering comboboxes #
        ###############################
        # Specify number of rows
        num_fields = 10

        # Attribute combobox
        self.attrib_vars = []
        self.attrib_cbs = []
        # Operator combobox
        self.op_vars = []
        self.op_cbs = []
        # Value combobox
        self.value_vars = []
        self.value_cbs = []

        for ii in range(0, num_fields):
            # Attribute comboboxes:
            # Append next unique ID to list
            self.attrib_vars.append(uuid.uuid4())
            # Assign unique ID to string variable
            self.attrib_vars[ii] = tk.StringVar()
            # Create combobox with above variable
            cb_attrib = ttk.Combobox(frm_filter, 
                textvariable=self.attrib_vars[ii])
            # Show combobox
            cb_attrib.grid(row=6+ii, column=1, pady=(0,10), padx=10)
            # Populate combobox
            cb_attrib['values'] = self.attributes
            # Append combobox to list
            self.attrib_cbs.append(cb_attrib)

            # Operator comboboxes:
            # Append next unique ID to list
            self.op_vars.append(uuid.uuid4())
            # Assign unique ID to string variable
            self.op_vars[ii] = tk.StringVar()
            # Create combobox with above variable
            cb_op = ttk.Combobox(frm_filter, 
                textvariable=self.op_vars[ii])
            # Show combobox
            cb_op.grid(row=6+ii, column=2, pady=(0,10))
            # Populate combobox
            cb_op['values'] = self.operators
            # Append combobox to list
            self.op_cbs.append(cb_op)

            # Value comboboxes:
            # Append next unique ID to list
            self.value_vars.append(uuid.uuid4())
            # Assign unique ID to string variable
            self.value_vars[ii] = tk.StringVar()
            # Create combobox with above variable
            cb_value = ttk.Combobox(frm_filter, 
                textvariable=self.value_vars[ii],
                postcommand=self.populate_values)
            # Show combobox
            cb_value.grid(row=6+ii, column=3, pady=(0,10), padx=10)
            # Append combobox to list
            self.value_cbs.append(cb_value)


    def populate_values(self, *_):
        for ii in range(0, len(self.attrib_cbs)):
            if self.attrib_cbs[ii].get():
                print(f"attribute found in {ii}")
                print(self.attrib_cbs[ii].get())
                temp = list(self.db.data[self.attrib_cbs[ii].get()].unique())
                temp.sort()
                temp.remove('-')
                self.value_cbs[ii]['values'] = temp
                #self.value_cbs[ii].set('')


    def _write2box(self):
        all_data = []
        self.txt_output.delete('1.0', tk.END)

        for ii in range(0, len(self.attrib_cbs)):
            all_data.append((self.attrib_vars[ii].get(), self.op_vars[ii].get(), self.value_vars[ii].get()))

        for ii in range(0, len(all_data)):
            test = str(all_data[ii][0]) + ' ' + str(all_data[ii][1]) + ' ' + str(all_data[ii][2]) + '\n'
            self.txt_output.insert(tk.END, test)

        self.event_generate('<<Filter>>')
