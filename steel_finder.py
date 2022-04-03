# finds all steel elements and calculates steel weight of structure
# only includes framing members

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, FilteredWorksetCollector


# structural instance usage ennumeration
# StructuralInstanceUsageFilter()
# Copy into revit python shell
cl = FilteredElementCollector(doc)
# cl.OfCategory(BuiltInCategory.OST_StructuralColumns)
cl.StructuralInstanceUSageFilter(Column)
cl.WhereElementIsNotElementType()

## 4/27
worksets = FilteredWorksetCollector(doc)
worksets.OfKind(WorksetKind.UserWorkset)

for elem in worksets:
    print(elem.name)

###
#Imports.
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

def all_elements_of_category(category):
	return FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType().ToElements()

#All Elements Of Walls Category.
walls = all_elements_of_category(BuiltInCategory.OST_Walls)

#All Elements Of Structural Columns Category.
columns = all_elements_of_category(BuiltInCategory.OST_StructuralColumns)

#All Elements Of Structural Framing Category.
framing = all_elements_of_category(BuiltInCategory.OST_StructuralFraming)

for frame in framing:
    # prints element name
    a = frame.Name
    print(a)
    a2 = frame.Id
    print(a2)
    # print material usage of each member
    try:
        b = frame.LookupParameter('Structural Material')
        b = b.AsValueString()
        print(b)
    except:
        print('No value')
    c = frame.LookupParameter('Cut Length')
    c = c.AsDouble()
    print(c)

