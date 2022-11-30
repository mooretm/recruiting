# **Subject Browser**

Graphical user interface (GUI) for filtering and browsing subjects from the CAR database.

- Written by: **Travis M. Moore**
- Latest version: **Version 0.0.2**
- Last edited: **November 30, 2022**
<br>
<br>

---

## Description
- This GUI was developed to provide an easy method for (1) filtering the CAR database, and (2) browsing the filtered selections. 

- Filtering: The original database is truncated to fields pertinent to recruiting only, making the database easier to work with. Values are sorted alphanumerically, allowing for easy selection. 

- Browsing: You can now see the most pertinent subject information all in one organized display, including the full graphical audiogram. Recommended acoustic coupling and vent sizes are provided based on Pro Fit logic. 
<br>
<br>

---

## Getting Started

### Dependencies

- Windows 10 or greater (not compatible with Mac OS)

### Installing

- This is a compiled app; the executable file is stored on Starfile at: \\starfile\Public\Temp\MooreT\Custom Software
- Simply copy the executable file and paste to a location on the local machine
- Double click to start the app

### First Use
- Double-click to start the application for the first time
- Select a database .csv file using the **File** menu
- Use the dropdowns to enter your filtering criteria
- Click the FILTER RECORDS button on the Filter tab
- Browse filtered records using the Browse tab
<br>
<br>

---

## Downloading the CAR Database
- Log into the [CAR database](http://ordsprd.starkey.com:8080/ords/glp/f?p=500:LOGIN:23703464524781:::::) and click the "General Search" tab.

    <img src="general_search.png" alt="General Search image" width="600"/>

- Click the "Actions" button, then choose "Select Columns."

    <img src="actions_columns.png" alt="Select Columns image" width="600"/>

- In the window that appears, click the double arrows (pointing right) button to move all the columns into the "Display in Report" list box. Then click "Apply."

    <img src="select_all_columns.png" alt="Select All Columns image" width="600"/>

- Click the "Actions" button again, then choose "Download."

    <img src="actions_download.png" alt="Select Download image" width="600"/>

- Click the "CSV" button in the window that appears and wait for the file to download. 

    <img src="choose_csv.png" alt="Choose .csv image" width="300"/>
<br>
<br>

---

## Importing Database Files
The Subject Browser can import full downloads from the CAR database, as well as filtered database files exported from the Subject Browser.
<br>
<br>

---

## Exporting Database Files
The Subject Browser allows you to export filtered .csv database files for further work in Excel and for sharing with others. You can also import the exported files later for browsing and/or further filtering. 
<br>
<br>

---

## Importing Filter Lists
The Subject Browser allows you to import a list of saved filter values to avoid entering filter values by hand. This is useful when using the same filter values across recruiting sessions. 
<br>
<br>

---

## Exporting Filter Lists
The Subject Browser allows you to export a list of your custom filters in .csv format for reuse. This is useful after manually setting several filter values that you might want to use again. 
<br>
<br>

---

## Resetting the Filters
To clear all filter values, navigate to **Tools>Reset Filters**.  
<br>
<br>

---

## Recompiling from Source
Additional data:

- Add README folder
- Add sample_data.csv file

```
pyinstaller --noconfirm --onefile --windowed --add-data "C:/Users/MooTra/Code/Python/recruiting/assets/README;README/" --add-data "C:/Users/MooTra/Code/Python/recruiting/assets/sample_data.csv;."  "C:/Users/MooTra/Code/Python/recruiting/controller.py"
```
<br>
<br>

---

## Contact
Please use the contact information below to submit bug reports, feature requests and any other feedback. Thank you for using the Subject Browser!

- Travis M. Moore: travis_moore@starkey.com
