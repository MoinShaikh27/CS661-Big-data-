import os
import vtk
import numpy as np
from vtk import vtkXMLImageDataReader

file_path = os.path.join(os.path.abspath("."), "tornado3d_vector.vti")

# Load the dataset
data_reader = vtkXMLImageDataReader()
data_reader.SetFileName(file_path)
data_reader.Update()
dataset = data_reader.GetOutput()

num_points = dataset.GetNumberOfPoints()
p_data = dataset.GetPointData()

probe_obj = vtk.vtkProbeFilter()
probe_obj.SetSourceData(dataset)
probe_obj.SetSpatialMatch(0)
probe_obj.SetValidPointMaskArrayName("vtkValidPointMask")

bounds = dataset.GetBounds()
lower_bounds = np.array([bounds[idx] for idx in range(0, len(bounds), 2)])
upper_bounds = np.array([bounds[idx] for idx in range(1, len(bounds), 2)])
print(lower_bounds,"\t\t",upper_bounds)

class BoundExceed(Exception):
    pass

def bounds_exceed(point):
    """
    Checks if the point is within the upper and lower bounds of the dataset provided
    """
    if not np.all(np.hstack((lower_bounds <= point, point <= upper_bounds))):
        raise BoundExceed()
        
    return point       

def do_probe(point):
    """
    Performs the Probeing using Probe Filter and returns the vector at the given point.
    """
    
    # As mentioned by Prof an unstructured grid has been created with just this single point and have set this as the InputData for the Probe Filter     
    unstructured_grid = vtk.vtkUnstructuredGrid()

    points = vtk.vtkPoints()
    points.InsertNextPoint(point)
    unstructured_grid.SetPoints(points)
    probe_obj.SetInputData(unstructured_grid)

    probe_obj.Update()
    
    vector = probe_obj.GetOutput().GetPointData().GetArray("vectors").GetTuple(0)    
    return np.array(vector)

def rk4_integrate(seed, step_size, max_steps, step_factor=1, c_factor=1):
    """
    Performs the RK4 integration to find the next point based on the vector values at the current point
    
    Arguements:
        step_factor: There seems to be a difference in the plot with the value of 2 as discussed in Class. A value of 1 seems to give the required plot
        c_factor: There seems to be a difference in the plot with the value of 0.5 as discussed in Class. A value of 1 seems to give the required plot
    """
    
    streamline_points = []
    current_point = np.array(seed)

    for _ in range(max_steps):
        
        try:
            a = step_factor * step_size * do_probe(bounds_exceed(current_point))
            b = step_factor * step_size * do_probe(bounds_exceed(current_point + (a*0.5)))
            c = step_factor * step_size * do_probe(bounds_exceed(current_point + (b*0.5)))
            d = step_factor * step_size * do_probe(bounds_exceed(current_point + (c*c_factor)))

            new_point = current_point + ((a + 2*b + 2*c + d) / 6)

            streamline_points.append(new_point)
            current_point = new_point
            
        except BoundExceed as err:
            # If the bound exceeds, then break and give back the points accumulated till now 
            print(f"BoundExceedException: {str(err)}")
            break

    return streamline_points

def create_polydata(points):
    """
    Use the incoming points data to create a VTK PolyData
    """
    
    # Create vtkPoints
    vtk_points = vtk.vtkPoints()
    for point in points:
        vtk_points.InsertNextPoint(point)

    # Create a polyline
    polyline = vtk.vtkPolyLine()
    polyline.GetPointIds().SetNumberOfIds(len(points))
    for i in range(len(points)):
        polyline.GetPointIds().SetId(i, i)

    # Create a cell array to store the polyline
    lines = vtk.vtkCellArray()
    lines.InsertNextCell(polyline)

    # Create a polydata to store everything
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(vtk_points)
    polydata.SetLines(lines)
    
    return polydata

def write_vtp_file(polydata, filename):
    """
    Write the Polydata object into the VTP file. The path for the file has been passed as param
    """
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetInputData(polydata)
    writer.SetFileName(filename)
    writer.Write()
    
def render_polydata(polydata):
    """
    Render the Polydata in VTK itself
    """
    
    # Create a mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)

    # Create an actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetLineWidth(2)
    """ A color similar to the one shown in the question diagram has been selected """
    actor.GetProperty().SetColor(0.01, 0.85, 0.32)

    # Create a renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(1, 1, 1)

    # Create a render window
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    # Create a render window interactor
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # Initialize the interactor and start the rendering loop
    render_window.Render()
    render_window_interactor.Start()

    
if __name__ == "__main__":

    SEED = input("Enter seed location (x y z): ").split() # [0,0,7]
    SEED = [float(coord) for coord in SEED]
    print(SEED)
    
    STEP_SIZE = 0.05
    MAX_STEPS = 1000
    RESULT_VTP_FIFLE_NAME = "./streamline_polydata.vtp"
    
    forward_streamline = rk4_integrate(SEED, STEP_SIZE, MAX_STEPS, step_factor=1, c_factor=1)
    backward_streamline = rk4_integrate(SEED, -STEP_SIZE, MAX_STEPS, step_factor=1, c_factor=1)[::-1]
    streamline_points = np.array(backward_streamline + [SEED] + forward_streamline)

    streamline_polydata = create_polydata(streamline_points)
    write_vtp_file(streamline_polydata, RESULT_VTP_FIFLE_NAME)
    render_polydata(streamline_polydata)
    