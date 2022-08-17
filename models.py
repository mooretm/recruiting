""" Sorting for subject recruitment """

# Import data science packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import custom modules
from constants import FieldTypes as FT


class SubDB:
    def __init__(self, db_source):
        """ Load in database records """

        # New query or use existing file?
        if db_source == 'new':
            """ Import csv files, truncate, and join """
            # Read in files
            general_search = pd.read_csv("C:\\Users\\MooTra\\Downloads\\general_search_2.0.csv")
            search = pd.read_csv("C:\\Users\\MooTra\\Downloads\\subjects.csv")


            """ Testing... """
            print('-' * 80)
            print('TESTS:')
            flags = []
            # Test whether databases are the same length
            print("Testing database lengths...")
            if general_search.shape[0] != search.shape[0]:
                print("Oh come on! Databases are not the same length!\n")
                flags.append(1)
            else:
                print("Passed!")

            # Test whether subject IDs match
            # across the two databases
            bools = general_search.iloc[0:len(search), 0] == search.iloc[:, 0]
            true_vals = list(bools).count(True)
            print("Testing whether subject IDs match across databases...")
            if true_vals != len(search):
                print("Record ID mismatches found!")
                print(f"{true_vals} records match of {len(search)}\n")
                flags.append(1)
            else:
                print("Passed!")

            # Summarize results
            print("Summary:")
            if not flags:
                print("All tests passed!")
            else:
                print("Please address failed tests!")
            print('-' * 80)


            # Truncate to columns of interest
            cols_general = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 
                            17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
                            31, 32, 33, 34, 35, 36, 38, 40, 42, 49, 51, 52, 87, 89,
                            100,101,102,103,
                            108, 111, 112, 115, 120, 122, 123, 130, 132, 133, 150, 
                            153, 154, 157, 162, 163, 164, 165, 169, 171, 172, 175, 
                            176, 177, 178, 179, 184, 186, 188, 191, 195, 201, 203]
            cols_search = [2,3,4,7]
            short_gen = general_search[general_search.columns[cols_general]]
            short_search = search[search.columns[cols_search]]

            # Join data frames
            self.data = short_gen.join(short_search)

            # Correct column names
            self.data.rename(columns = {
                'L Pt Bc 1000':'LeftBC 1000',
                'L Pt Bc 2000':'LeftBC 2000',
                'L Pt Bc 4000':'LeftBC 4000',
                'L Pt Bc 500':'LeftBC 500',
                'RightBC  1000':'RightBC 1000',
                'RightBC  2000':'RightBC 2000',
                'RightBC  4000':'RightBC 4000'
                }, inplace = True
            )

            # Sort dataframe by subject ID
            self.data = self.data.sort_values(by='Subject Id')



            print("Created database")
            print(f"Remaining candidates: {self.data.shape[0]}\n")

        elif db_source == 'old':
            self.data = pd.read_csv("C:/Users/MooTra/Documents/Projects/EdgeMode/IRB/Recruiting/sub_db_free.csv")
            print("Created database")
            print(f"Remaining candidates: {self.data.shape[0]}\n")

        # Get rid of junk
        self._initial_scrub()


    def write(self):
        """ Save database to .csv"""
        # Write database to desktop
        self.data.to_csv(
            "C:\\Users\\MooTra\\OneDrive - Starkey\\Desktop\\sub_db.csv",
            mode='w',
            index=False)
        print("Database written to file!")


    def _initial_scrub(self):
        """ Perform perfunctory filtering """
        self.data = self.data[self.data["Employment Status"] != "Employee"]
        self.data = self.data[self.data["Status"] == "Active"]
        self.data = self.data[self.data["Good Candidate"].isin(["-", "Excellent", "Good", "Fair"])]
        print("Removed junk")
        print(f"Remaining candidates: {self.data.shape[0]}\n")


    def filter(self, colname, operator, value):
        # Remove rows containing "-" (i.e., no data)
        self.data = self.data[self.data[colname] != "-"]
        # Check data type of value
        if isinstance(value, int):
            self.data[colname] = self.data[colname].astype("int")
        elif isinstance(value, float):
            self.data[colname] = self.data[colname].astype("float")

        # Perform filtering
        if operator == "==":
            self.data = self.data[self.data[colname] == value]
        if operator == "!=":
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
                    ac[side + ' ' + str(freq)] = int(self.data[self.data['Subject Id'] == sub_id][colname].values[0])
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
                    bc[side + ' ' + str(freq)] = int(self.data[self.data['Subject Id'] == sub_id][colname].values[0])
                except:
                    bc[side + ' ' + str(freq)] = None

        return ac, bc


    def audio_ac(self, sub_id, ax=None):
        if ax is None:
            ax = plt.gca()


        # sides = ["RightAC", "LeftAC"]
        # freqs = [250, 500, 1000, 2000, 4000, 8000]
        # thresh = []
        # for side in sides:
        #     for freq in freqs:
        #         # Construct column name
        #         colname = side + " " + str(freq)
        #         # Remove rows containing "-" (i.e., no data)
        #         #self.data = self.data[self.data[colname] != "-"]
        #         # Convert column to int
        #         #self.data[colname] = self.data[colname].astype("int64")
        #         # Exclude thresholds above dict value
        #         thresh.append(self.data[self.data['Subject Id'] == sub_id][colname].astype(int))


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

        ax.set_ylim((-10,120))
        ax.invert_yaxis()
        yticks = range(-10,130,10)
        ax.set_yticks(ticks=yticks)
        ax.set_ylabel("Hearing Threshold (dB HL)")
        ax.semilogx()
        ax.set_xlim((200,9500))
        ax.set_xticks(ticks=[250,500,1000,2000,4000,8000], labels=['250','500','1000','2000','4000','8000'])
        ax.set_xlabel("Frequency (Hz)")
        ax.axhline(y=25, color="black", linestyle='--', linewidth=1)
        ax.grid()
        ax.set_title(f"Audiogram for Participant {sub_id}")

        # Plot color regions
        audio_colors = ["gray", "green", "gold", "orange", "mediumpurple", "lightsalmon"]
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
            coords = [[0,degree_dict[key][0]], [9500,degree_dict[key][0]], [9500,degree_dict[key][1]], [0,degree_dict[key][1]]]
            coords.append(coords[0]) # repeat the first point to create a 'closed loop'
            xs, ys = zip(*coords) # create lists of x and y values
            ax.fill(xs,ys, edgecolor='none', facecolor=audio_colors[idx], alpha=alpha_val)


    # def show_all_audios(self):
    #     """ Show all audiograms for participants 
    #         in database
    #     """
    #     # Get remaining subject ids
    #     subs = self.data["Subject Id"]
    #     # Plot each audio in succession
    #     for sub in subs:
    #         self.audio_ac(sub)


    def coupling(self, sub_id):
        """ Return ProFit recommended coupling and vent size"""

        # Get subject thresholds
        ac, bc = self.get_thresholds(sub_id)

        # RIC coupling logic
        sides = ['RightAC ', 'LeftAC ']
        coupling = {}
        vent_size = {}
        for side in sides:
            if (ac[side + '250'] and ac[side + '500'] < 30) and (ac[side + '1000'] <= 60):
                coupling[side[:-3]] = 'Open Dome'
            elif (ac[side + '250'] or ac[side + '500'] > 30) and (ac[side + '250'] or ac[side + '500'] <= 50) and (ac[side + '1000'] <= 60):
                coupling[side[:-3]] = 'Occluded Dome'
            #elif (ac['RightAC 250'] or ac['RightAC 500'] < 50) or (ac[side + '1000'] > 60):
            elif (ac[side + '250'] or ac[side + '500'] < 50) or (ac[side + '1000'] > 60):
                coupling[side[:-3]] = 'Earmold'

            # Vent size
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
                    vent_size[side[:-3]] = 'Models_253: Calculation Error!'
            else:
                vent_size[side[:-3]] = 'NA'

        return coupling, vent_size


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
    }
