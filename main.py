
import vtk
from colors import MAP_COLORS
from lookUpTable import createLookUpTable
from proto.read_file import read


# Get a color array containing the color for each altitude according to the
# given LUT.
def getMapColorsByAltitude(altitudes, colorLookupTable):
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName("Colors")

    # Choose colors for each points and then rotate them
    for i in range(0, len(altitudes)):
        for j in range(0, len(altitudes[i])):
            # print(p[0] - EARTH_RADUIS)
            dcolor = [0, 0, 0]
            colorLookupTable.GetColor(altitudes[i][j], dcolor)
            # print(dcolor)
            color = [0, 0, 0]
            for k in range(0, 3):
                color[k] = 255 * dcolor[k]

            colors.InsertNextTuple(color)
    return colors


EARTH_RADUIS = 6371009

MIN_LATITUDE = 45
MAX_LATITUDE = 47.5

MIN_LONGITUDE = 5
MAX_LONGITUDE = 7.5

FILENAME = "data/output.txt"

# Create points
points = vtk.vtkPoints()

# Read altitudes from input file
altitudes = read(FILENAME)

# Find min and max value to map colors to
min = altitudes.min()
max = altitudes.max()

# Create the lookUpTable
colorLookupTable = createLookUpTable(MAP_COLORS, min, max)

# Array to store the color to use for each point
colors = getMapColorsByAltitude(altitudes, colorLookupTable)

# Get matrices size
rows = len(altitudes)
cols = len(altitudes[0])

# Get delta
longitudeDelta = (MAX_LONGITUDE - MIN_LONGITUDE) / rows
latitudeDelta = (MAX_LATITUDE - MIN_LATITUDE) / cols

# Choose colors for each points and then rotate them
for i in range(0, len(altitudes)):
    for j in range(0, len(altitudes[i])):

        # Create a new point
        p = [EARTH_RADUIS + int(altitudes[i][j]), 0, 0]

        transform1 = vtk.vtkTransform()
        transform1.RotateY(-(j * longitudeDelta + MIN_LONGITUDE))

        transform2 = vtk.vtkTransform()
        transform2.RotateZ(i * latitudeDelta + MIN_LATITUDE)

        # Apply tranformation
        points.InsertNextPoint(
            transform1.TransformPoint(
                transform2.TransformPoint(
                    p
                )
            )
        )

sg = vtk.vtkStructuredGrid()
sg.SetDimensions(rows, cols, 1)
sg.SetPoints(points)

gf = vtk.vtkStructuredGridGeometryFilter()
gf.SetInputData(sg)
gf.Update()


sg.GetPointData().SetScalars(colors)

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(gf.GetOutputPort())
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(3)

renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.SetSize(800, 600)
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Here we specify a particular interactor style.
style = vtk.vtkInteractorStyleTrackballCamera()
renderWindowInteractor.SetInteractorStyle(style)


renderer.AddActor(actor)
renderer.SetBackground(.2, .3, .4)

renderWindow.Render()
renderWindowInteractor.Start()


del points
del gf
del mapper
del actor
del renderer
del renderWindow
