import vtk
from random import uniform

sg = vtk.vtkStructuredGrid()

points = vtk.vtkPoints()
for x in range(0, 10):
	for y in range(0, 10):
		points.InsertNextPoint(x + uniform(-0.2, 0.2), y + uniform(-0.2, 0.2), 3 uniform(-0.5, 0.5))

sg.SetDimensions(10, 10, 1)
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
