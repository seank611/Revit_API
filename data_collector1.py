# Video 2: basics of collecting data
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

# Copy into revit python shell
cl = FilteredElementCollector(doc)
cl.OfCategory(BuiltInCategory.OST_StructuralColumns)
cl.WhereElementIsNotElementType()

for element in cl:
    print(element)


# lookup parameter for steel weight
wt = cl[0].LookupParameter('W')
wt.Definition.Name

# calculates steel weight by using volume
tot_stl = 0
for s_column in cl:
    # Looks up how revit references volume, and then pulls value for current column
    v = s_column.LookupParameter('Volume')
    # Some parameters have integers or strings or boolean, need to verify this for each parameter
    v2 = v.AsDouble()
    tot_stl += v2

stl_wt = tot_stl * 492
print(stl_wt)


# His code for walls
total_volume = 0.0
for wall in wall_collector:
    vol_param = wall.LookupParameter('Volume')
    if vol_param:
        total_volume = total_volume + vol_param.AsDouble()


