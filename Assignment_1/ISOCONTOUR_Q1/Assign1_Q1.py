import os
from vtk import *
import numpy as np
from pathlib import Path

from config import *

# Read the path where the input file is available
file_path = Path(path).joinpath(file_name).resolve()

print(f"Path contents{os.listdir(path)}")

# Read the dataset
data_reader = vtkXMLImageDataReader()
data_reader.SetFileName(file_path)
data_reader.Update()

data = data_reader.GetOutput()
point_data = data.GetPointData()
pressure_values = point_data.GetArray('Pressure')

# Get the number of cells in the dataset
num_cells = data.GetNumberOfCells()


def generate_data(iso_value):
    """ Function to generate the iso contour with the provided iso value

    :param iso_value (float): The iso value for which the iso contour is to be generated
    :return:
    None
    """

    # Create the objects to store the points and lines created from the Marching squares algorithm
    points = vtkPoints()
    cell_arr = vtkCellArray()
    poly_data = vtkPolyData()

    # Iterate over each of the cells and then each of the points in counter-clockwise direction
    for cell_id in range(num_cells):
        cell = data.GetCell(cell_id)
        point_ids = cell.GetPointIds()

        # Iterate over each of the 4 lines of the Pixel Cell in counter-clockwise dir
        for point1, point2 in [(0, 1), (1, 3), (3, 2), (2, 0)]:

            # Get the values at these points
            point1_val = pressure_values.GetTuple1(point_ids.GetId(point1))
            point2_val = pressure_values.GetTuple1(point_ids.GetId(point2))

            contour_cell_identified = False

            # If the line should contain the iso value as per the linearity property of zero crossing add the point
            if point1_val > iso_value > point2_val:
                contour_cell_identified = True
                v1 = point1_val
                v2 = point2_val

                p1 = np.array(data.GetPoint(cell.GetPointId(point1)))
                p2 = np.array(data.GetPoint(cell.GetPointId(point2)))
            elif point1_val < iso_value < point2_val:
                contour_cell_identified = True
                v1 = point2_val
                v2 = point1_val

                p1 = np.array(data.GetPoint(cell.GetPointId(point2)))
                p2 = np.array(data.GetPoint(cell.GetPointId(point1)))

            if contour_cell_identified:
                iso_point = (((v1 - iso_value) / (v1 - v2)) * (p2 - p1)) + p1
                points.InsertNextPoint(iso_point)

    # Number of points added
    num_points = points.GetNumberOfPoints()

    # Iterate over the adjacent points and add the lines to the polyline
    for i in range(0, num_points, 2):
        poly_line = vtkPolyLine()
        poly_line.GetPointIds().SetNumberOfIds(2)
        poly_line.GetPointIds().SetId(0, i)
        poly_line.GetPointIds().SetId(1, i + 1)
        cell_arr.InsertNextCell(poly_line)

    poly_data.SetPoints(points)
    poly_data.SetLines(cell_arr)

    # Write the output to the output file along with the iso_value for which generated
    writer = vtkXMLPolyDataWriter()
    writer.SetInputData(poly_data)
    writer.SetFileName(f'./output_{iso_value}.vtp')
    writer.Write()

    # The code to visualize both the input data along with the iso-contour so created
    surface = vtkGeometryFilter()
    surface.SetInputData(data)
    surface.Update()

    # Output of geometry filter is a vtkpolydata
    pdata = surface.GetOutput()
    val_range = pdata.GetPointData().GetArray('Pressure').GetRange()

    lut = vtkLookupTable()
    lut.Build()
    scalar_bar = vtkScalarBarActor()
    scalar_bar.SetLookupTable(lut)
    scalar_bar.SetTitle("Pressure")
    scalar_bar.SetNumberOfLabels(6)
    scalar_bar.SetMaximumWidthInPixels(150)
    scalar_bar.SetMaximumHeightInPixels(600)

    # Setup mapper and actor
    ##########################
    mapper1 = vtkPolyDataMapper()
    mapper1.SetInputData(pdata)
    mapper1.SetScalarRange(val_range)
    mapper1.SetLookupTable(lut)
    actor1 = vtkActor()
    actor1.SetMapper(mapper1)

    # Axes actor
    ###############
    axes = vtkAxesActor()
    axes.SetTotalLength(50, 50, 50)
    axes.AxisLabelsOff()

    # Setup mapper and actor
    ##########################
    mapper2 = vtkPolyDataMapper()
    mapper2.SetInputData(poly_data)
    actor2 = vtkActor()
    actor2.SetMapper(mapper2)

    renderer = vtkRenderer()
    renderer.SetBackground(0.5, 0.5, 0.5)
    render_window = vtkRenderWindow()
    render_window.SetSize(1400, 1000)
    render_window.AddRenderer(renderer)
    render_window_interactor = vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    render_window_interactor.SetInteractorStyle(vtkInteractorStyleTrackballCamera())
    renderer.AddActor(actor1)
    renderer.AddActor(actor2)
    renderer.AddActor(axes)

    scalar_bar_widget = vtkScalarBarWidget()
    scalar_bar_widget.SetInteractor(render_window_interactor)
    scalar_bar_widget.SetScalarBarActor(scalar_bar)
    scalar_bar_widget.On()

    render_window.Render()
    render_window_interactor.Start()


if __name__ == "__main__":

    # Run the code in an infinite loop so that we can generate the iso-contour for multiple user entries
    while True:
        try:
            # Read the value and generate
            iso_value = float(
                input("Enter the isovalue to be checked with in the range (-1438, 630) Or any Character to exit : ", ))
            generate_data(iso_value)
        except Exception as err:
            exit(0)
