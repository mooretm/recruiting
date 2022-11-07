""" Subject filter options view for Subject Browser 
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk

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


    def __init__(self, parent, database, dbmodel, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.db = database
        self.dbmodel = dbmodel
        fields = self.dbmodel.fields
        self._vars = {
            key: self.var_types[spec['type']]()
            for key, spec in fields.items()
        }


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

        label_text = ['Attribute', 'Operator', 'Value']
        for idx, label in enumerate(label_text, start=1):
            ttk.Label(frm_filter, text=label).grid(
                row=5, column=idx)

        ttk.Button(frm_filter, text="Update Values", command=self._update_vals).grid(row=7, column=1)

        txt_output = tk.Text(frm_filter, height=10, width=50)
        txt_output.grid(row=10, column=1, columnspan=5, **options)

        # Attribute combobox
        self.selected_attribute = tk.StringVar()
        cb_attribute = ttk.Combobox(frm_filter, textvariable=self.selected_attribute)
        cb_attribute.grid(row=6, column=1)
        cb_attribute['values'] = self.attributes

        # Operator combobox
        selected_operator = tk.StringVar()
        cb_operator = ttk.Combobox(frm_filter, textvariable=selected_operator)
        cb_operator.grid(row=6, column=2)
        cb_operator['values'] = self.operators

        # Value combobox
        selected_value = tk.StringVar()
        self.cb_value = ttk.Combobox(frm_filter, textvariable=selected_value)
        self.cb_value.grid(row=6, column=3)
        try:
            self.cb_value['values'] = self.db.data[self.selected_attribute.get()].unique()
        except KeyError:
            print("Please select an attribute to filter by!")
            return

    
    def _update_vals(self):
        try:
            self.cb_value['values'] = list(self.db.data[self.selected_attribute.get()].unique())
        except KeyError:
            print("Please select an attribute to filter by!")
            return

