# Revit_dataV1.py V1.1 **copyright property of Sean Kelton**
# 6/20/2021
# Program will cycle through elements in revit model to do material takeoff
# need to install revitpython shell for version of revit you are using
# this program was developed in/using Revit 2021
# copy + paste everything below this line into RevitPythonShell and run
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, FilteredWorksetCollector
import csv



file_path = r'C:\Users\seank\Desktop\revit_out.csv'
# param_strings = ['Family']
# param_doubles = ['Area', 'Volume']
# headers = ['Element Id', 'ELement Name', 'Family', 'Area', 'Volume']
print("Units are as follows:"
      "Area: SQ FT, Volume: CF, Thickness: FT, Cut Length: FT")
param_strings = ['Family', 'Structural', 'Category', 'Type', 'Phase Created', 'Structural Usage', 'Level', 'Reference Level']
param_doubles = ['Area', 'Volume', 'Thickness', 'Cut Length']
headers = ['Element Id', 'Element Name', 'Structural Material', 'Family', 'Structural?', 'Category', 'Type',
           'Phase Created', 'Structural Usage', 'Level', 'Reference Level', 'Area', 'Volume', 'Thickness', 'Cut Length']
category_list = [BuiltInCategory.OST_Walls, BuiltInCategory.OST_StructuralFoundation, BuiltInCategory.OST_Floors,
                 BuiltInCategory.OST_StructuralFraming, BuiltInCategory.OST_StructuralColumns]
# category_list = ['OST_Walls', 'OST_StructuralFoundation', 'OST_StructuralFraming', 'OST_StructuralColumns', 'OST_Floors']

def all_elements_of_category(category):
	return FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType().ToElements()

# create csv file
with open(file_path, 'wb') as csvfile:
    # create writer object
    csvwriter = csv.writer(csvfile)
    # write headers
    csvwriter.writerow(headers)

    for category in category_list:
        elements = all_elements_of_category(category)
        for element in elements:
            # create blank list that will fill out with values for each row in csv file
            c_row = []
            a = str(element.Id)
            print(a)
            c_row.append(element.Id)
            b = element.Name
            c_row.append(b)
            # gather value of structural material type if it exists
            try:
                s_mat = element.StructuralMaterialType
            except:
                s_mat = 'na'
            c_row.append(s_mat)
            # iterate through string parameters for each element
            for param in param_strings:
                try:
                    s = element.LookupParameter(param)
                    s = s.AsValueString()
                except:
                    s = 'na'
                c_row.append(s)
            # iterate through double parameters for each element
            for param in param_doubles:
                try:
                    d = element.LookupParameter(param)
                    d = d.AsDouble()
                    d = float(d)
                except:
                    d = 'na'
                c_row.append(d)
            print(c_row)
            csvwriter.writerow(c_row)
