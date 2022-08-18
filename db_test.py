"""A quick test of the subject recruiting database.

    Currently consists of 2 tests that assess the 
    following: (1) database .csv export lengths, 
    and (2) subject ID matches across database exports. 

    Author: Travis M. Moore
    Created: 17 Aug, 2022
    Last Edited: 18 Aug, 2022
"""

# Import data science packages
import pandas as pd


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
    print("Databases are not the same length!\n")
    flags.append(1)
else:
    print("Passed!\n")

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
    print("Passed!\n")

# Summarize results
print("Summary:")
if not flags:
    print("All tests passed!")
else:
    print("Please address failed tests!")
print('-' * 80)
