""" Database model for the Subject Browser 

    Expects a .csv file of the entire 'General Search' tab 
    from the online subject database. 

    Author: Travis M. Moore
 """

###########
# Imports #
###########
# Import GUI packages
from tkinter import filedialog

# Import data science packages
import numpy as np
import pandas as pd



import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Import system packages
from datetime import datetime

# Import custom modules
from models.constants import FieldTypes as FT


#########
# BEGIN #
#########
class SubDB:
    """ Class to hold database info and provide related 
        functions (e.g., get air conduction thresholds)
    """

    def __init__(self, db_path):
        """ Load database .csv file from path
        """
        self.load_db(db_path)


    #####################
    # General Functions #
    #####################
    def load_filtered_db(self, db_path):
        # Import .csv file of database records
        self.data = pd.read_csv(db_path)

        # Convert age back to string after importing 
        # a previously-exported database .csv file
        self.data['Age'] = self.data['Age'].astype('str')

        # Convert all values back to strings
        #self.data = self.data.astype(str)
        # Pretty sure everything is loaded in as an object data type?

        # Provide feedback
        print("Loaded database records")
        print(f"Remaining candidates: {self.data.shape[0]}\n")


    def load_db(self, db_path):
        """ Read database .csv provided from filedialog browser
        """
        # Import .csv file of database records
        general_search = pd.read_csv(db_path)

        # Define columns of interest
        cols_general = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 
                        16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 
                        29, 30, 31, 32, 33, 34, 35, 36, 38, 40, 42, 49, 51, 
                        52, 74, 85, 86, 88, 90, 101,102,103,104, 109, 112, 
                        113, 116, 121, 123, 124, 131, 132, 133, 134, 151, 
                        154, 155, 158, 163, 164, 165, 166, 170, 172, 173, 
                        176, 177, 178, 179, 180, 185, 187, 189, 192, 196, 
                        202, 204]

        # New dataframe with columns of interest only
        short_gen = general_search[general_search.columns[cols_general]].copy()

        # Correct column names
        short_gen.rename(columns = {
            'L Pt Bc 1000':'LeftBC 1000',
            'L Pt Bc 2000':'LeftBC 2000',
            'L Pt Bc 4000':'LeftBC 4000',
            'L Pt Bc 500':'LeftBC 500',
            'RightBC  1000':'RightBC 1000',
            'RightBC  2000':'RightBC 2000',
            'RightBC  4000':'RightBC 4000',
            'Hearing AidUse':'Hearing Aid Use'
            }, inplace = True
        )

        # Calculate age and store in new dataframe column
        short_gen['Age'] = short_gen['Date Of Birth'].apply(
            lambda x: self.calc_age(x))

        # Convert Age column back to string
        short_gen['Age'] = short_gen['Age'].astype("str")

        # Sort dataframe by subject ID
        self.data = short_gen.sort_values(by='Subject Id').reset_index(
            drop=True)

        # Provide feedback
        print("Loaded database records")
        print(f"Remaining candidates: {self.data.shape[0]}\n")

        # Get rid of junk records
        #self._initial_scrub()


    def calc_age(self, birthdate):
        """ Convert birthdate to ages
        """
        today = datetime.now()
        x = str(birthdate).split('/')
        try:
            birth = datetime(int(x[2]), int(x[0]), int(x[1]))
            age = int((today - birth).days / 365.2425)
        except TypeError:
            age = '-'
        except IndexError:
            age = '-'
        except ValueError:
            age = '-'
        return age


    def _initial_scrub(self):
        """ Perform perfunctory filtering 
        """
        # Remove internal employees
        self.data = self.data[self.data["Employment Status"] != "Employee"]
        print(f"Automatically removed internal Starkey employees")
        print(f"Remaining candidates: {self.data.shape[0]}\n")

        # Remove inactive records
        self.data = self.data[self.data["Status"] == "Active"]
        print(f"Automatically removed inactive participants")
        print(f"Remaining candidates: {self.data.shape[0]}\n")

        # Remove poor candidates
        self.data = self.data[self.data["Good Candidate"].isin(["-", 
            "Excellent", "Good", "Fair"])]
        print(f"Automatically removed poor candidates")
        print(f"Remaining candidates: {self.data.shape[0]}\n")


    def write(self):
        """ Save database to .csv"""
        # Generate date stamp
        now = datetime.now()
        date_stamp = now.strftime("%Y_%b_%d_%H%M")
        
        # Create save file name
        filename = 'filtered_db_' + str(date_stamp)

        # Query user for save path
        try:
            save_path = filedialog.asksaveasfile(
                initialfile= filename,
                defaultextension='.csv').name
        except AttributeError:
            # Do nothing if cancelled
            return

        # Do nothing if cancelled
        if not save_path:
            return

        # Write data to .csv file if a valid save path is given
        self.data.to_csv(save_path, mode='w', index=False)
        print("Database successfully written to file!")


    #######################
    # Filtering Functions #
    #######################
    def filter(self, colname, operator, value):
        # Remove rows containing "-" (i.e., no data)
        #self.data = self.data[self.data[colname] != "-"]
        # Check data type of value
        #if isinstance(value, int):
        #    self.data[colname] = self.data[colname].astype("int")
        #elif isinstance(value, float):
        #    self.data[colname] = self.data[colname].astype("float")

        # Perform filtering
        # NOTE: Add OR condition to include '-' values for every operator!
        if operator == "equals":
            self.data = self.data[self.data[colname] == value]
        if operator == "does not equal":
            self.data = self.data[self.data[colname] != value]
        if operator == ">":
            self.data = self.data[self.data[colname] > value]
        if operator == ">=":
            self.data = self.data[self.data[colname] >= value]
        if operator == "<":
            self.data = self.data[self.data[colname] < value]
        if operator == "<=":
            self.data = self.data[self.data[colname] <= value]
        if operator == "contains":
            self.data = self.data[self.data[colname].isin(value)]
        print(f"Filtered column '{colname}' for '{value}'")
        print(f"Remaining candidates: {self.data.shape[0]}\n")


    def ac_thresh_filt(self, thresh_dict):
        """ Filter by right/left air conduction thresholds. 
            Expects dict of frequencies with tuple of lower
            and upper threshold limits.
        """
        sides = ["RightAC", "LeftAC"]
        for side in sides:
            for key in thresh_dict:
                # Construct column name
                colname = side + " " + key
                # Remove rows containing "-" (i.e., no data)
                self.data = self.data[self.data[colname] != "-"]
                # Convert column to int
                self.data[colname] = self.data[colname].astype("int")
                # Exclude thresholds above dict value 1
                self.data = self.data[self.data[colname] <= thresh_dict[key][1]]
                # Exclude thresholds below dict value 0
                self.data = self.data[self.data[colname] >= thresh_dict[key][0]]

        print("Filtered by provided air conduction threshold limits")
        print(f"Remaining candidates: {self.data.shape[0]}\n")


    def get_thresholds(self, sub_id):
        """ Make a dictionary of subject thresholds """
        # Get AC thresholds
        sides = ["RightAC", "LeftAC"]
        freqs = [250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
        ac = {}
        for side in sides:
            for freq in freqs:
                colname = side + " " + str(freq)
                #ac.append(self.data[self.data['Subject Id'] == sub_id][colname].astype(int))
                try:
                    ac[side + ' ' + str(freq)] = int(
                        self.data[self.data['Subject Id'] == sub_id][colname].values[0])
                except:
                    ac[side + ' ' + str(freq)] = None

        # Get BC thresholds
        sides = ["RightBC", "LeftBC"]
        freqs = [500, 1000, 2000, 4000]
        bc = {}
        for side in sides:
            for freq in freqs:
                colname = side + " " + str(freq)
                try:
                    bc[side + ' ' + str(freq)] = int(
                        self.data[self.data['Subject Id'] == sub_id][colname].values[0])
                except:
                    bc[side + ' ' + str(freq)] = None

        return ac, bc


    def audio_ac(self, sub_id, ax=None):
        if ax is None:
            ax = plt.gca()

        # Get AC and BC thresholds
        ac, bc = self.get_thresholds(sub_id)
        thresholds = (ac, bc)

        # Remove "None" values from thresholds
        for ii in range(0,2):
            for key, value in dict(thresholds[ii]).items():
                if value is None:
                    del thresholds[ii][key]

        # Plot audiogram: METHOD 1
        # Plot AC thresholds
        # for key, value in dict(ac).items():
        #     if "Right" in key:
        #         print(key, value)
        #         ax.plot(int(key.split()[1]), value, color='red', marker='o')
        #     elif "Left" in key:
        #         ax.plot(int(key.split()[1]), value, color='blue', marker='x')
        
        # Plot audiogram: METHOD 2
        # Plot AC thresholds
        # keys = ac.keys()
        # right_ac_freqs = []
        # right_ac_thresh = []
        # left_ac_freqs = []
        # left_ac_thresh = []
        # for key in keys:
        #     if "Right" in key:
        #         right_ac_freqs.append((int(key.split()[1])))
        #         right_ac_thresh.append(ac[key])
        #     elif "Left" in key:
        #         left_ac_freqs.append((int(key.split()[1])))
        #         left_ac_thresh.append(ac[key])
        
        # Plot audiogram: METHOD 3
        # Plot AC thresholds
        x = list(ac.items())
        right_ac_freqs = [int(j[0].split()[1]) for j in x if 'Right' in j[0]]
        right_ac_thresh = [j[1] for j in x if 'Right' in j[0]]
        left_ac_freqs = [int(j[0].split()[1]) for j in x if 'Left' in j[0]]
        left_ac_thresh = [j[1] for j in x if 'Left' in j[0]]
        ax.plot(right_ac_freqs, right_ac_thresh, 'ro-')
        ax.plot(left_ac_freqs, left_ac_thresh, 'bx-')

        # Plot BC thresholds
        x = list(bc.items())
        right_bc_freqs = [int(j[0].split()[1]) for j in x if 'Right' in j[0]]
        right_bc_thresh = [j[1] for j in x if 'Right' in j[0]]
        left_bc_freqs = [int(j[0].split()[1]) for j in x if 'Left' in j[0]]
        left_bc_thresh = [j[1] for j in x if 'Left' in j[0]]
        ax.plot(right_bc_freqs, right_bc_thresh, marker=8, c='red', linestyle='None')
        ax.plot(left_bc_freqs, left_bc_thresh, marker=9, c='blue', linestyle='None')

        # Plot formatting
        ax.set_ylim((-10,120))
        ax.invert_yaxis()
        yticks = range(-10,130,10)
        ax.set_yticks(ticks=yticks)
        ax.set_ylabel("Hearing Threshold (dB HL)")
        ax.semilogx()
        ax.set_xlim((200,9500))
        ax.set_xticks(ticks=[250,500,1000,2000,4000,8000], labels=[
            '250','500','1000','2000','4000','8000'])
        ax.set_xlabel("Frequency (Hz)")
        ax.axhline(y=25, color="black", linestyle='--', linewidth=1)
        ax.grid()
        ax.set_title(f"Audiogram for Participant {sub_id}")

        # Plot color regions
        audio_colors = ["gray", "green", "gold", "orange", "mediumpurple", 
            "lightsalmon"]
        alpha_val = 0.25
        degree_dict={
            'normal': (-10, 25),
            'mild': (25, 40),
            'moderate': (40, 55),
            'moderately-severe': (55, 70),
            'severe': (70, 90),
            'profound': (90, 120)
        }
        for idx, key in enumerate(degree_dict):
            coords = [
                [0,degree_dict[key][0]], 
                [9500,degree_dict[key][0]], 
                [9500,degree_dict[key][1]], 
                [0,degree_dict[key][1]]
            ]
            # Repeat the first point to create a 'closed loop'
            coords.append(coords[0])
            # Create lists of x and y values 
            xs, ys = zip(*coords) 
            # Fill polygon
            ax.fill(xs,ys, edgecolor='none', 
                facecolor=audio_colors[idx], alpha=alpha_val)


    ###############################
    # Acoustic Coupling Functions #
    ###############################
    def coupling(self, sub_id):
        """ Return ProFit recommended coupling and vent size"""

        # Get subject thresholds
        ac, bc = self.get_thresholds(sub_id)

        # RIC coupling logic
        sides = ['RightAC ', 'LeftAC ']
        coupling = {}
        vent_size = {}
        matrix = {}

        for side in sides:
            # RIC matrix selection logic
            # Step 1: determine recommendation threshold
            try:
                if (ac[side + '2000'] >= ac[side + '500']):
                    recommendation_threshold = ac[side + '2000']
                elif (ac[side + '500'] > ac[side + '2000']):
                    recommendation_threshold = ac[side + '500'] + 10
            except TypeError:
                raise TypeError

            # Step 2: choose matrix based on recommendation threshold
            if recommendation_threshold <= 65:
                power = 'M'
                #receiver = 'stock'
            elif (recommendation_threshold <= 75) and (recommendation_threshold > 65):
                power = 'P'
                #receiver = 'stock'
            elif (recommendation_threshold <= 80) and (recommendation_threshold > 75):
                power = 'P'
                #receiver = 'custom cased'
            elif recommendation_threshold > 80:
                power = 'UP'
                #reciever = 'custom cased'

            matrix[side[:-3]] = power

            # RIC acoustic coupling logic
            # This is partly based on the matrix recommendation from above
            try:
                # Open dome
                if (ac[side + '250'] and ac[side + '500'] < 30) \
                    and (ac[side + '1000'] <= 60) \
                    and (matrix[side[:-3]] in ['S', 'M', 'P']):
                        coupling[side[:-3]] = 'Open Dome'

                # Occluded dome
                elif (ac[side + '250'] or ac[side + '500'] > 30) \
                    and (ac[side + '250'] and ac[side + '500'] <= 50) \
                    and (ac[side + '1000'] <= 60) \
                    and (matrix[side[:-3]] in ['S', 'M', 'P']):
                        coupling[side[:-3]] = 'Occluded Dome'

                # Earmolds
                # Dome unless...
                elif (ac[side + '250'] or ac[side + '500'] > 50):
                    coupling[side[:-3]] = 'Earmold'

                # Earmold
                elif (ac[side + '1000'] > 60):
                    coupling[side[:-3]] = 'Earmold'

                # Earmold
                elif matrix == 'UP':
                    coupling[side[:-3]] = 'Earmold'

                # Cannot categorize
                else:
                    coupling[side[:-3]] = 'Error!'

            except TypeError:
                coupling[side[:-3]] = '-'


            # RIC (and custom) vent size
            if coupling[side[:-3]] == 'Earmold':
                # Get average threshold at 500 and 1000 Hz
                avg500_1k = np.mean([ac[side + '500'], ac[side + '1000']])
                if avg500_1k <= 40:
                    vent_size[side[:-3]] = 'Large'
                elif avg500_1k < 55:
                    vent_size[side[:-3]] = 'Medium'
                elif avg500_1k >= 55:
                    vent_size[side[:-3]] = 'Small'
                else:
                    vent_size[side[:-3]] = 'Models_322: Calculation Error!'
            else:
                vent_size[side[:-3]] = 'NA'

        return matrix, coupling, vent_size


class DataModel:
    """ Handle subject db record data """
    fields = {
        "age": {'req': True, 'type': FT.string},
        "miles_away": {'req': True, 'type': FT.string},
        "smartphone_type": {'req': True, 'type': FT.string},
        'study_dates': {'req': True, 'type': FT.string},
        'study_info': {'req': True, 'type': FT.string},
        'will_not_wear': {'req': True, 'type': FT.string},
        'r_style': {'req': True, 'type': FT.string},
        'l_style': {'req': True, 'type': FT.string},
        'r_receiver': {'req': True, 'type': FT.string},
        'l_receiver': {'req': True, 'type': FT.string},
        'r_coupling': {'req': True, 'type': FT.string},
        'l_coupling': {'req': True, 'type': FT.string},
        'r_rec_coupling': {'req': True, 'type': FT.string},
        'l_rec_coupling': {'req': True, 'type': FT.string},
        'r_rec_vent': {'req': True, 'type': FT.string},
        'l_rec_vent': {'req': True, 'type': FT.string},
        'r_matrix': {'req': True, 'type': FT.string},
        'l_matrix': {'req': True, 'type': FT.string}
    }
