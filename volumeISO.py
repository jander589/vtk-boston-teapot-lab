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

    colors = vtk.vtkNamedColors()

    #Create color lookup table
    lut = vtk.vtkColorTransferFunction()
    lut.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
    lut.AddRGBPoint(127.5, 1.0, 1.0, 1.0)
    lut.AddRGBPoint(255, 1.0, 0.0, 0.0)

    #Create window, winderrenderer, and interactor
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(1000, 1000)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)
    interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

    #Create teapot slice
    teapotVOI = vtk.vtkExtractVOI()
    teapotVOI.SetInputConnection(reader.GetOutputPort())
    teapotVOI.SetVOI(0, 255, 0, 255, 0, 88) #x, y, z
    #Create teapot iso
    teapotISO = vtk.vtkContourFilter()
    teapotISO.SetInputConnection(teapotVOI.GetOutputPort())
    teapotISO.GenerateValues(1, 100, 100)
    #Create teapot mapper
    teapotMapper = vtk.vtkPolyDataMapper()
    teapotMapper.SetInputConnection(teapotISO.GetOutputPort())
    teapotMapper.SetLookupTable(lut)
    #Create teapot actor
    teapotActor = vtk.vtkActor()
    teapotActor.SetMapper(teapotMapper)

    #Extract lobster subset
    lobsterVOI = vtk.vtkExtractVOI()
    lobsterVOI.SetInputConnection(reader.GetOutputPort())
    lobsterVOI.SetVOI(100, 178, 70, 150, 70, 105)
    #Create lobster iso
    lobsterISO = vtk.vtkContourFilter()
    lobsterISO.SetInputConnection(lobsterVOI.GetOutputPort())
    lobsterISO.GenerateValues(1, 40, 40)
    #Create mapper
    lobsterMapper = vtk.vtkPolyDataMapper()
    lobsterMapper.SetInputConnection(lobsterISO.GetOutputPort())
    lobsterMapper.SetLookupTable(lut)
    #Create actor
    lobsterActor = vtk.vtkActor()
    lobsterActor.SetMapper(lobsterMapper)

    #Extract thing subset
    thingVOI = vtk.vtkExtractVOI()
    thingVOI.SetInputConnection(reader.GetOutputPort())
    thingVOI.SetVOI(100, 195, 78, 145, 70, 105)
    #Create thing iso
    thingISO = vtk.vtkContourFilter()
    thingISO.SetInputConnection(thingVOI.GetOutputPort())
    thingISO.GenerateValues(1, 10, 10)
    #Create mapper
    thingMapper = vtk.vtkPolyDataMapper()
    thingMapper.SetInputConnection(thingISO.GetOutputPort())
    thingMapper.SetLookupTable(lut)
    #Create actor
    thingActor = vtk.vtkActor()
    thingActor.SetMapper(thingMapper)
    thingActor.GetProperty().SetOpacity(0.2)

    #Add actors
    renderer.AddActor(teapotActor)
    renderer.AddActor(lobsterActor)
    renderer.AddActor(thingActor)

    renderer.SetBackground(.9, .9, .9)
    renderer.ResetCamera()
    #Start
    renderWindow.Render()
    interactor.Start()

if __name__ == "__main__":
    main()
