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

    #Create color table
    lut = vtk.vtkColorTransferFunction()
    lut.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
    lut.AddRGBPoint(127.5, 1.0, 1.0, 1.0)
    lut.AddRGBPoint(255, 1.0, 0.0, 0.0)

    #Create image to color mapper
    colors = vtk.vtkImageMapToColors()
    colors.SetInputConnection(reader.GetOutputPort())
    colors.SetLookupTable(lut)
    colors.Update()

    #Create actor
    sagittal = vtk.vtkImageActor()
    sagittal.GetMapper().SetInputConnection(colors.GetOutputPort())
    sagittal.SetDisplayExtent(124, 124, 0, 255, 0, 177)
    sagittal.ForceOpaqueOn()

    coronal = vtk.vtkImageActor()
    coronal.GetMapper().SetInputConnection(colors.GetOutputPort())
    coronal.SetDisplayExtent(0, 255, 124, 124, 0, 177)
    coronal.ForceOpaqueOn()

    axial = vtk.vtkImageActor()
    axial.GetMapper().SetInputConnection(colors.GetOutputPort())
    axial.SetDisplayExtent(0, 255, 0, 255, 88, 88)
    axial.ForceOpaqueOn()

    #Create renderer, render window, and interactor
    ren = vtk.vtkRenderer()
    
    #Comment out two to get only one slice
    ren.AddActor(sagittal)
    ren.AddActor(coronal)
    ren.AddActor(axial)

    ren.SetBackground(.9, .9, .9)
    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(1000,1000)
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    renWin.SetInteractor(iren)

    #Render and start
    renWin.Render()
    iren.Start()

if __name__ == "__main__":
    main()
