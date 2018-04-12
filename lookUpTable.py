import vtk


# Create a LookUpTable containg the given colors.
def createLookUpTable(colors, min, max):
    colorLookupTable = vtk.vtkLookupTable()
    colorLookupTable.SetTableRange(min, max)
    colorLookupTable.SetNumberOfTableValues(len(colors))
    colorLookupTable.Build()
    for i in range(0, len(colors)):
        colorLookupTable.SetTableValue(i, colors[i])
    return colorLookupTable
