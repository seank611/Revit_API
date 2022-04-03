# use script for testing code in revitpythonshell
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, FilteredWorksetCollector


param_strings = ['Family']
param_doubles = ['Area', 'Volume']
headers = ['Element Id', 'ELement Name', 'Family', 'Area', 'Volume']
category_list = [BuiltInCategory.OST_StructuralFraming, BuiltInCategory.OST_Floors]

def all_elements_of_category(category):
	return FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType().ToElements()


for category in category_list:
    elements = all_elements_of_category(category)
    for element in elements:
        a = element.Name
        print(a)
        try:
            b = element.StructuralMaterialType
            print(b)
        except:
            b = 'n/a'
        c = element.StructuralMaterialId
        print(c)