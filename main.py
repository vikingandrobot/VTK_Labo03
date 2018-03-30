
import csv
import vtk

EARTH_RADUIS = 6371009

MIN_LATITUDE = 45
MAX_LATITUDE = 47.5

MIN_LONGITUDE = 5
MAX_LONGITUDE = 7.5

FILENAME = "data/altitudes.txt"


points = vtk.vtkPoints()
rows = 0
cols = 0


# Read data file
with open(FILENAME, 'r') as f:

	# Read the first line and get matrices size
	size = f.readline().split()
	if not len(size) == 2: 
		raise AssertionError("The first line have to be a tuple of size")

	# Get matrices size
	rows = int(size[0])
	cols = int(size[1])

	# Get delta
	longitudeDelta = (MAX_LONGITUDE - MIN_LONGITUDE) / rows
	latitudeDelta = (MAX_LATITUDE - MIN_LATITUDE) / cols

	# Read each line
	for i in range(0, rows):

		# Get altitudes by row
		altitudes = f.readline().split()

		for j in range(0, cols):
			# Create a new point
			p = [EARTH_RADUIS + int(altitudes[j]), 0, 0]

			transform1 = vtk.vtkTransform()
			transform1.RotateY(j * longitudeDelta + MIN_LONGITUDE);

			transform2 = vtk.vtkTransform()
			transform2.RotateZ(i * latitudeDelta + MIN_LATITUDE);
		
			# Apply tranformation
			points.InsertNextPoint(
				transform1.TransformPoint(
					transform2.TransformPoint(
						p
					)
				)
			)

	# Close the file
	f.close()


sg = vtk.vtkStructuredGrid()
sg.SetDimensions(rows, cols, 1)
sg.SetPoints(points)

gf = vtk.vtkStructuredGridGeometryFilter()
gf.SetInputData(sg)
gf.Update()

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


