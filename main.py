
import vtk
import numpy as np
from colors import MAP_COLORS
from lookUpTable import createLookUpTable
from proto.read_file import read
from keypressInteractorStyle import KeyPressInteractorStyle


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


# Returns true if the two colors c1 and c2 are the same
def colorEquals(c1, c2):
    return np.array_equal(c1, c2)


# Given a two dimensional array of altitudes value and a one dimensional array
# (vtkUnsignedCharArray) of colors value assigned two those altitudes,
# replace all flat area by a
# specific color. The sensibility must be >= 2 and describes the size of the
# square in which to search for flat area. If a point is at the uperleft corner
# of such a square and all points inside said square are at the same altitude,
# said point will be colored in "flatColor"
def flatColoring(altitudes, colors, flatColor, sensibility):
    for i in range(0, len(altitudes) - sensibility):
        for j in range(0, len(altitudes[i]) - sensibility):

            # Current altitude value in the loop
            nbCurrentAltitude = altitudes[i][j]

            equality = True
            for k in range(0, sensibility):
                for h in range(0, sensibility):
                    equality = equality and nbCurrentAltitude == altitudes[i + k][j + h]

            if equality:
                for k in range(0, sensibility):
                    for h in range(0, sensibility):
                        colors.SetTuple((i + k) * len(altitudes[i]) + j + h, tuple(flatColor))


EARTH_RADUIS = 6371009

MIN_LATITUDE = 45
MAX_LATITUDE = 47.5

MIN_LONGITUDE = 5
MAX_LONGITUDE = 7.5

FILENAME = "data/altitudes.txt"

BLUE_COLOR = [143, 230, 252]

# Create points
points = vtk.vtkPoints()

# Read altitudes from input file
print("Reading input file...")
altitudes = read(FILENAME)
print("Finished reading intput file.")

# Find min and max value to map colors to
min = 0
max = altitudes.max()

# Create the lookUpTable
print("Building LUT...")
colorLookupTable = createLookUpTable(MAP_COLORS, min, max)
print("LUT built.")

# Array to store the color to use for each point
print("Processing altitude colors...")
colors = getMapColorsByAltitude(altitudes, colorLookupTable)
print("Done.")

# Color flat areas in blue
print("Coloring lakes...")
flatColoring(altitudes, colors, BLUE_COLOR, 3)
print("Done.")

# Get matrices size
rows = len(altitudes)
cols = len(altitudes[0])

# Get delta
longitudeDelta = (MAX_LONGITUDE - MIN_LONGITUDE) / rows
latitudeDelta = (MAX_LATITUDE - MIN_LATITUDE) / cols

# Rotate point around the center of the Earth
print("Building points...")
for i in range(0, len(altitudes)):

    transform2 = vtk.vtkTransform()
    transform2.RotateZ(i * latitudeDelta + MIN_LATITUDE)

    transform1 = vtk.vtkTransform()
    transform1.RotateY(-MIN_LONGITUDE)
    for j in range(0, len(altitudes[i])):

        # Create a new point
        p = [EARTH_RADUIS + int(altitudes[i][j]), 0, 0]

        transform1.RotateY(-longitudeDelta)

        # Apply tranformation
        points.InsertNextPoint(
            transform1.TransformPoint(
                transform2.TransformPoint(
                    p
                )
            )
        )
print("Done.")

print("Building structuredGrid")
sg = vtk.vtkStructuredGrid()
sg.SetDimensions(rows, cols, 1)
sg.SetPoints(points)
print("Done.")

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
renderWindow.SetSize(1200, 720)
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Here we specify a particular interactor style.
style = KeyPressInteractorStyle(renderWindow, renderWindowInteractor)
renderWindowInteractor.SetInteractorStyle(style)


renderer.AddActor(actor)
renderer.SetBackground(0.95, 0.95, 0.95)

renderWindow.Render()
renderWindowInteractor.Start()


del points
del gf
del mapper
del actor
del renderer
del renderWindow
