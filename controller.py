""" Controller for Recruiting Tool """

# Import custom modules
import models as m
import audio_dict as a


# Initialize database and do initial scrub
db = m.SubDB('new')

# # Filter by bilateral hearing aid use
# db.filter("Hearing AidUse", "==", "Binaural")

# # Filter by passed cognitive screener
# db.filter("MoCA Total Score", ">=", 26) # 26 is lower cutoff for normal

# # Filter by smart phone use
# db.filter("Smartphone Yn", "contains", ["-", "Yes"])

# # Filter by smartphone platform
# db.filter("Smartphone Os", "!=", "Android")

# # Filter by Internet use
# db.filter("Use Internet", "contains", ["-", "Very Often", "Often"])

# # Filter by age
# db.filter("Age", "<=", 75)

# # Filter by hearing thresholds
# db.ac_thresh_filt(a.Jingjing)

# Write database to .csv
#db.write()


