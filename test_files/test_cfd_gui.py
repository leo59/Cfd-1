# quickly run a gui test for FreeCAD GUI functions on command line

import sys
import os.path
if os.path.exists('/usr/lib/freecad/lib'):
    print('found FreeCAD stable  on system')
    sys.path.append('/usr/lib/freecad/lib')
elif os.path.exists('/usr/lib/freecad-daily/lib'):
    sys.path.append('/usr/lib/freecad-daily/lib')
    print('found FreeCAD-daily on system')
else:
    print('no FreeCAD stable or daily build is found on system, please install')

import FreeCAD as App
import FreeCADGui as Gui

Gui.showMainWindow()
Gui.activateWorkbench("StartWorkbench")

##########################################################
App.newDocument("Unnamed")
App.setActiveDocument("Unnamed")
App.ActiveDocument=App.getDocument("Unnamed")
Gui.ActiveDocument=Gui.getDocument("Unnamed")
Gui.activateWorkbench("PartWorkbench")
App.ActiveDocument.addObject("Part::Cylinder","Cylinder")
App.ActiveDocument.ActiveObject.Label = "Cylinder"
App.ActiveDocument.recompute()
Gui.SendMsgToActiveView("ViewFit")

Gui.activateWorkbench("CfdWorkbench")
Gui.ActiveDocument.setEdit('Cylinder',0)

import FemGui
import CfdObjects
CfdObjects.makeCfdAnalysis('CfdAnalysis')
FemGui.setActiveAnalysis(App.activeDocument().ActiveObject)
FemGui.getActiveAnalysis().addObject(CfdObjects.makeCfdSolver('OpenFOAM'))
FemGui.getActiveAnalysis().addObject(CfdObjects.makeCfdFluidMaterial('FluidMaterial'))
mesh_obj = CfdObjects.makeCfdMeshGmsh('Cylinder_Mesh')
mesh_obj.Part = App.ActiveDocument.Cylinder
FemGui.getActiveAnalysis().addObject(mesh_obj)

import CaeMesherGmsh
gmsh_mesh = CaeMesherGmsh.CaeMesherGmsh(mesh_obj, FemGui.getActiveAnalysis())
error = gmsh_mesh.create_mesh()


##########################################################
#Gui.getMainWindow().close()  #still wait for user to confirm save not discard
#App.ActiveDocument.Name
FreeCAD.closeDocument('Unnamed')
Gui.doCommand('exit(0)')  # another way to exit


