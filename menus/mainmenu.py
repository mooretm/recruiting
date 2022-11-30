""" Main Menu class for Subject Browser
"""

# Import GUI packages
import tkinter as tk
from tkinter import messagebox

class MainMenu(tk.Menu):
    """ Main Menu
    """
    # Find parent window and tell it to 
    # generate a callback sequence
    def _event(self, sequence):
        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)
        return callback


    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        #############
        # File Menu #
        #############
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(
            label="Import Full DB...",
            command=self._event('<<FileImportFullDB>>')
        )
        file_menu.add_command(
            label="Import Filtered DB...",
            command=self._event('<<FileImportFilteredDB>>')
        )
        file_menu.add_command(
            label="Export DB...",
            command=self._event('<<FileExportDB>>')
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Import Filter List...",
            command=self._event('<<FileImportList>>')
        )
        file_menu.add_command(
            label="Export Filter List...",
            command=self._event('<<FileExportList>>')
        )

        file_menu.add_separator()
        file_menu.add_command(
            label="Quit",
            command=self._event('<<FileQuit>>')
        )
        self.add_cascade(label='File', menu=file_menu)

        ##############
        # Tools Menu #
        ##############
        tools_menu = tk.Menu(self, tearoff=False)
        tools_menu.add_command(
            label='Reset Filters',
            command=self._event('<<ToolsReset>>')
        )
        # Add Tools menu to the menubar
        self.add_cascade(label="Tools", menu=tools_menu)

        #############
        # Help Menu #
        #############
        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(
            label='About',
            command=self.show_about
        )
        help_menu.add_command(
            label='Help',
            command=self._event('<<Help>>')
        )
        # Add help menu to the menubar
        self.add_cascade(label="Help", menu=help_menu)


    #############
    # Functions #
    #############
    def show_about(self):
        """ Show the about dialog """
        about_message = 'Subject Browser'
        about_detail = (
            'Written by: Travis M. Moore\n'
            'Version 0.0.2\n'
            'Created: Jul 26, 2022\n'
            'Last Edited: Nov 30, 2022'
        )
        messagebox.showinfo(
            title='About',
            message=about_message,
            detail=about_detail
        )
