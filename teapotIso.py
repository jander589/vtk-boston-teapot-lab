import vtk

def main():
    #Read raw dataset
    reader = vtk.vtkImageReader()
    reader.SetFileName("BostonTeapot.raw")
    reader.SetDataByteOrderToBigEndian()
    reader.SetNumberOfScalarComponents(1)
    reader.SetFileDimensionality(3)
    reader.SetDataExtent(0, 255, 0, 255, 0, 177)
    reader.SetDataScalarTypeToUnsignedChar()
    reader.Update()

    #Create contour filter using reader
    contour = vtk.vtkContourFilter()
    contour.SetInputConnection(reader.GetOutputPort())
    contour.GenerateValues(1, 100, 100)

    #Create color lookup table
    colorTransferFunction = vtk.vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
    colorTransferFunction.AddRGBPoint(124.428, 1.0, 1.0, 1.0)
    colorTransferFunction.AddRGBPoint(255, 1.0, 0.0, 0.0)

    #Create mapper using contour filter
    modelToContour = vtk.vtkPolyDataMapper()
    modelToContour.SetInputConnection(contour.GetOutputPort())
    modelToContour.SetLookupTable(colorTransferFunction)
    
    #Create contour actor using mapper
    contourActor = vtk.vtkActor()
    contourActor.SetMapper(modelToContour)

    #Window
    window = vtk.vtkRenderWindow()
    window.SetSize(1000, 1000)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

    #contour
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(.9, .9, .9)
    renderer.AddActor(contourActor)
    window.AddRenderer(renderer)

    #Start
    interactor.SetRenderWindow(window)
    window.Render()
    interactor.Start()

if __name__ == "__main__":
    main()
