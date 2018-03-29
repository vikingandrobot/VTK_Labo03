import vtk
from random import uniform

sg = vtk.vtkStructuredGrid()

points = vtk.vtkPoints()
SEGMENTS = 20
for y in range(0, SEGMENTS + 1):
	for x in range(0, SEGMENTS + 1):
		p = [0, 0, 20 + uniform(-0.2, 0.2)]
		transform1 = vtk.vtkTransform()
		transform2 = vtk.vtkTransform()
		transform2.RotateX(y * 90 / SEGMENTS)
		transform1.RotateY(x * 90 / SEGMENTS)
		points.InsertNextPoint(transform1.TransformPoint(transform2.TransformPoint(p)))

sg.SetDimensions(SEGMENTS + 1, SEGMENTS + 1, 1)
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
