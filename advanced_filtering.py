import clr
import Autodesk.Revit.DB as DB

doc = __revit__.ActiveUIDocument.Document

# Copy into revit python shell
cl = DB.FilteredElementCollector(doc)
cl.OfClass(clr.GetClrType(DB.Wall))
cl.ToElements()