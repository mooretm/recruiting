""" Filtering window for Subject Browser 
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Import misc packages
import uuid


#########
# BEGIN #
#########
class FilterFrame(ttk.Frame):
    """ Filtering view for 'Filter' tab of notebook
    """

    def __init__(self, parent, database, filter_dict, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        ##############
        # Initialize #
        ##############
        # Assign constructor arguments to class variables
        self.filter_dict = filter_dict
        self.db = database

        # Create list of database columns
        self.attributes = list(self.db.data.columns)
        self.attributes.sort()

        # Create list of operators
        self.operators = ["equals", "does not equal", "contains", ">", ">=", 
            "<", "<="]


        #################
        # Create Frames #
        #################
        # Allow expansion of main frame
        self.columnconfigure(index=0, weight=1)
        
        # Widget styling
        style = ttk.Style()
        style.configure("rec.TLabel", foreground='green')

        # Frame options
        options = {'padx':10, 'pady':10}

        # Create frames
        frm_filter = ttk.Frame(self)
        frm_filter.grid(row=0, column=0, sticky='ew')
        # Set columns to expand
        frm_filter.columnconfigure(index=1, weight=1)
        frm_filter.columnconfigure(index=2, weight=1)
        frm_filter.columnconfigure(index=3, weight=1)


        ############
        # Controls #
        ############
        label_text = ['Attribute', 'Operator', 'Value']
        for idx, label in enumerate(label_text, start=1):
            ttk.Label(frm_filter, text=label).grid(
                row=5, column=idx, pady=10)

        # Filter button
        ttk.Button(frm_filter, text="Filter Records", 
            command=self._do_filter).grid(row=20, column=2, sticky='ew')

        # Text widget for displaying filtering results
        self.txt_output = tk.Text(frm_filter, height=20, width=50)
        self.txt_output.grid(row=21, column=1, columnspan=4, **options,
            sticky='nsew')

        # # Scrollbar for text widget
        # scroll = ttk.Scrollbar(frm_filter, orient='vertical', 
        #     command=self.txt_output.yview)
        # scroll.grid(row=21, column=4, sticky='ns')

        # self.txt_output['yscrollcommand'] = scroll.set


        ###############################
        # Create Filtering Comboboxes #
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
                textvariable=self.attrib_vars[ii], takefocus=0)
            # Show combobox
            cb_attrib.grid(row=6+ii, column=1, pady=(0,10), padx=10,
                sticky='ew')
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
                textvariable=self.op_vars[ii], takefocus=0)
            # Show combobox
            cb_op.grid(row=6+ii, column=2, pady=(0,10), sticky='ew')
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
                postcommand=self.get_values, takefocus=0)
            # Show combobox
            cb_value.grid(row=6+ii, column=3, pady=(0,10), padx=10,
                sticky='ew')
            # Append combobox to list
            self.value_cbs.append(cb_value)


    #############
    # Functions #
    #############
    def get_values(self, *_):
        """ Get values to populate value comboboxes based on the selected 
            attribute in the attribute comboboxes
        """
        for ii in range(0, len(self.attrib_cbs)):
            if self.attrib_cbs[ii].get():
                unique_vals = list(self.db.data[self.attrib_cbs[ii].get()].unique())
                unique_vals.sort()
                try:
                    unique_vals.remove('-')
                except ValueError:
                    print("View_Filter_144: No '-' found in value list.")
                self.value_cbs[ii]['values'] = unique_vals


    def _do_filter(self):
        """ Update filter dict based on provided combobox values.
            Send filter event to controller.
        """
        # Get values from all comboboxes
        self._get_filter_vals()
        # Send event to controller to filter
        self.event_generate('<<Filter>>')


    def _get_filter_vals(self):
        """ Create a dictionary of filter values from combobox values. 
            Check for missing values and skipped rows.
        """
        all_data = []
        self.txt_output.delete('1.0', tk.END)

        for ii in range(0, len(self.attrib_cbs)):
            # Check for any empty values in a given row
            if (not self.attrib_vars[ii].get()) \
                or (not self.op_vars[ii].get()) \
                or (not self.value_vars[ii].get()):
                # Check whether entire row is empty
                if (not self.attrib_vars[ii].get()) \
                    and (not self.op_vars[ii].get()) \
                    and (not self.value_vars[ii].get()):
                    pass # do nothing if entire row is empty
                else:
                    # If some values in a row are missing, 
                    # display message and exit
                    print("Missing values!")
                    messagebox.showerror(title="Missing Values",
                        message="There are missing values!",
                        detail="Please provide all filter parameters " +
                            "for a given row."
                    )
                    return
            else:
                # Create list from values if 'contains' operator
                # Create new 'value' variable because tk.StringVar
                # cannot hold a list
                if self.op_vars[ii].get() == "contains":
                    value = self.value_vars[ii].get().split()
                else:
                    value = self.value_vars[ii].get()
                # If all values are present in a given row, append to list
                all_data.append((
                    self.attrib_vars[ii].get(), 
                    self.op_vars[ii].get(), 
                    #self.value_vars[ii].get()
                    value
                ))
                try:
                    # Update dictionary with list by index
                    self.filter_dict[ii] = all_data[ii]
                except IndexError:
                    # If indexes do not match, there was an empty row 
                    # between rows with values: display message and 
                    # exit
                    messagebox.showerror(title="Empty Rows",
                        message="One or more rows has been skipped!",
                        detail="There cannot be empty rows between rows " +
                            "with values."
                    )
                    return


    def _clear_filters(self):
        """ Clear all values from the filter comboboxes.
            Reset filter dict to empty.
        """
        # Clear out current filter dict
        self.filter_dict = {}
        # Delete any output from textbox
        self.txt_output.delete('1.0', tk.END)
        # Clear all combobox values
        for ii in range(0, len(self.attrib_cbs)):
            self.attrib_cbs[ii].set('')
            self.op_cbs[ii].set('')
            self.value_cbs[ii].set('')
        # Set the focus to the upper left combobox
        self.attrib_cbs[0].focus_set()


    def _load_filters(self, filter_dict):
        """ Populate comboboxes with values from provided dict
        """
        # Clear any textbox output
        self.txt_output.delete('1.0', tk.END)

        # Populate comboxes with new values
        for ii in filter_dict:
            self.attrib_cbs[int(ii)].set(filter_dict[ii][0])
            self.op_cbs[int(ii)].set(filter_dict[ii][1])
            self.value_cbs[int(ii)].set(filter_dict[ii][2])
