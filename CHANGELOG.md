# **Change Log**

---

## v.0.0.2

Date: Nov 30, 2022

### Minor Bug Fixes
1. Filtering by 'Subject Id' would not work because IDs are stored as integers and all filter values are converted to strings. Solution: special case patch in filterview (lines 218:228) that looks for subject searches and converts string values to integers. 

2. Added vertical resize ability to accommodate smaller laptop screens. The widgets do not stretch, however. 

3. Shortened height of filterview output textbox to accommodate smaller laptop screens. 

4. Added scrollbar widget to filterview output textbox. 


## v0.0.1

Date: Jun, 2022

### Major Bug Fixes
1. Pro Fit logic for making acoustic coupling and vent size recommendations has been improved about as much as it can be. The matrix recommendation logic has been implemented. 
<br>
<br>

---

## v0.0.0

Date: Jun 17, 2022

### Bugs
1. The ProFit logic for determining acoustic coupling type is incorrect as implemented in the code. This logic also relies on the recommended receiver matrix, but this logic was not available at the time. The matrix recommendation logic has been requested (today) and should be implemented as soon as possible. 
<br>
<br>
