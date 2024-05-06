import vtk

from config import file_path

enable_phong_shading = input("Do you want to enable Phong shading? (yes/no): ").lower().strip() == "yes"

# Load 3D data
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName(file_path)
reader.Update()

# color transfer function
color_transfer_function = vtk.vtkColorTransferFunction()
color_transfer_function.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)
color_transfer_function.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)
color_transfer_function.AddRGBPoint(-1873.9, 0.0, 0.0, 0.5)
color_transfer_function.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0)
color_transfer_function.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)
color_transfer_function.AddRGBPoint(2594.97, 1.0, 1.0, 0.0)

# opacity transfer function
opacity_transfer_function = vtk.vtkPiecewiseFunction()
opacity_transfer_function.AddPoint(-4931.54, 1.0)
opacity_transfer_function.AddPoint(101.815, 0.002)
opacity_transfer_function.AddPoint(2594.97, 0.0)

# volume property
volume_property = vtk.vtkVolumeProperty()
volume_property.SetColor(color_transfer_function)
volume_property.SetScalarOpacity(opacity_transfer_function)

if enable_phong_shading:
    volume_property.ShadeOn()
    volume_property.SetAmbient(0.5)  # Adjusted to a valid value
    volume_property.SetDiffuse(0.5)  # Adjusted to a valid value
    volume_property.SetSpecular(0.5) # Adjusted to a valid value

# volume mapper
volume_mapper = vtk.vtkSmartVolumeMapper()
volume_mapper.SetInputConnection(reader.GetOutputPort())

# volume
volume = vtk.vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# outline
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# renderer
renderer = vtk.vtkRenderer()
renderer.AddVolume(volume)
renderer.AddActor(outline_actor)
renderer.SetBackground(1, 1, 1)

# render window
render_window = vtk.vtkRenderWindow()
render_window.SetSize(1000, 1000)
render_window.AddRenderer(renderer)

# render window interactor
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Start rendering
render_window.Render()
render_window_interactor.Start()
