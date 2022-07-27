""" Sorting for subject recruitment """

# Import data science packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


class SubDB:
    def __init__(self):
        """ Import csv files, truncate, and join """
        # Read in files
        general_search = pd.read_csv(r"C:\\Users\\MooTra\Downloads\\general_search_2.0.csv")
        search = pd.read_csv(r"C:\\Users\\MooTra\Downloads\\subjects.csv")

        # Truncate to columns of interest
        cols_general = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 
                        17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
                        31, 32, 33, 34, 35, 36, 38, 40, 42, 49, 51, 52, 87, 89, 
                        108, 111, 112, 115, 120, 122, 123, 130, 132, 133, 150, 
                        153, 154, 157, 162, 163, 164, 165, 169, 171, 172, 175, 
                        176, 177, 178, 179, 184, 186, 188, 191, 195, 201, 203]
        cols_search = [2,3,4,7]
        short_gen = general_search[general_search.columns[cols_general]]
        short_search = search[search.columns[cols_search]]

        # Join data frames
        self.data = short_gen.join(short_search)
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


    def audio_ac(self, sub_id, ax=None):
        if ax is None:
            ax = plt.gca()
        sides = ["RightAC", "LeftAC"]
        freqs = [250, 500, 1000, 2000, 4000, 8000]
        thresh = []
        for side in sides:
            for freq in freqs:
                # Construct column name
                colname = side + " " + str(freq)
                # Remove rows containing "-" (i.e., no data)
                #self.data = self.data[self.data[colname] != "-"]
                # Convert column to int
                #self.data[colname] = self.data[colname].astype("int64")
                # Exclude thresholds above dict value
                thresh.append(self.data[self.data['Subject Id'] == sub_id][colname].astype(int))
        # Plot audiogram
        ax.plot(freqs, thresh[0:6], color='red', marker='o')
        ax.plot(freqs, thresh[6:12], color='blue', marker='x')
        ax.set_ylim((-10,120))
        #plt.gca().invert_yaxis()
        ax.invert_yaxis()
        yticks = range(-10,130,10)
        ax.set_yticks(ticks=yticks)
        ax.set_ylabel("Hearing Threshold (dB HL)")
        ax.semilogx()
        ax.set_xlim((0,9500))
        ax.set_xticks(ticks=[250,500,1000,2000,4000,8000], labels=['250','500','1000','2000','4000','8000'])
        ax.set_xlabel("Frequency (Hz)")
        #plt.axhline(y=25, color="black", linestyle='--', linewidth=1)
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

        #plt.show()
        #return plt 
        #plt.show()


    def show_all_audios(self):
        """ Show all audiograms for participants 
            in database
        """
        # Get remaining subject ids
        subs = self.data["Subject Id"]
        # Plot each audio in succession
        for sub in subs:
            self.audio_ac(sub)

