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

    #Create color lookup table
    colorTransferFunction = vtk.vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
    colorTransferFunction.AddRGBPoint(124.428, 1.0, 1.0, 1.0)
    colorTransferFunction.AddRGBPoint(255, 1.0, 0.0, 0.0)
    
    #Create window, windowrenderer, and interactor
    ren1 = vtk.vtkRenderer()
    ren1.SetBackground(.9, .9, .9)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(1000,1000)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

    #Extract subset
    extractVOI = vtk.vtkExtractVOI()
    extractVOI.SetInputConnection(reader.GetOutputPort())
    #These two are changed between to visualise either the lobster or the thing it is inside
    extractVOI.SetVOI(100, 178, 70, 150, 70, 105) #Lobster
    #extractVOI.SetVOI(100, 195, 78, 145, 70, 105) #Thing

    #Iso surface
    iso = vtk.vtkContourFilter()
    iso.SetInputConnection(extractVOI.GetOutputPort())
    #These two are changed between to visualise either the lobster or the thing it is inside
    #iso.GenerateValues(1, 40, 40) #Lobster
    iso.GenerateValues(1, 10, 10) #Thing

    #Create iso mapper
    isoMapper = vtk.vtkPolyDataMapper()
    isoMapper.SetInputConnection(iso.GetOutputPort())
    isoMapper.SetLookupTable(colorTransferFunction)
    #isoMapper.ScalarVisibilityOff()

    #Create actor
    isoActor = vtk.vtkActor()
    isoActor.SetMapper(isoMapper)

    #Add actors
    ren1.AddActor(isoActor)
    
    #Start
    renWin.Render()
    iren.Start()

if __name__ == "__main__":
    main()
