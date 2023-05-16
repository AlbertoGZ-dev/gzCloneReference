'''
████████████████████████████████████████████████████████████████████████████
    
    Clone Reference for Maya
    
    Description: Clone Reference is a tool to clone or create multiple
    copies of external references keeping transforms from initial reference.


    Author: AlbertoGZ
    albertogzonline@gmail.com
    https://github.com/AlbertoGZ-dev

████████████████████████████████████████████████████████████████████████████

'''

from select import select
from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
# import re
# import os


# GENERAL VARS
version = '0.1.2'
about = 'by Alberto GZ'
winWidth = 520
winHeight = 500
red = '#872323'
green = '#207527'
lightbrown = '#7d654b'
lightpurple = '#604b69'
lightgreen = '#5b694b'
lightblue = '#3a3e42'

itemSelected = []
iconMesh = QtGui.QIcon(":/mesh.svg")
iconRef = QtGui.QIcon(":/reference.svg")
iconCurve = QtGui.QIcon(":/nurbsCurve.svg")
iconCam = QtGui.QIcon(":/camera.svg")
iconLight = QtGui.QIcon(":/ambientLight.svg")



def getMainWindow():
    main_window_ptr = omui.MQtUtil.mainWindow()
    mainWindow = wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    return mainWindow


class cloneReference(QtWidgets.QMainWindow):

    def __init__(self, parent=getMainWindow()):
        super(cloneReference, self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint)

    

    #####################################################
    #                  LAYOUT DESIGN                    #
    #####################################################

        # Creates object, Title Name and Adds a QtWidget as our central widget/Main Layout
        self.setObjectName('cloneReferenceUI')
        self.setWindowTitle('cloneReference' + ' ' + 'v' + version + ' - ' + about)
        mainLayout = QtWidgets.QWidget(self)
        self.setCentralWidget(mainLayout)
        
        # Adding a Horizontal layout to divide the UI in columns
        columns = QtWidgets.QHBoxLayout(mainLayout)

        # Creating vertical layout
        self.col1 = QtWidgets.QVBoxLayout()
        self.col2 = QtWidgets.QVBoxLayout()
       
        # Set columns for each layout using stretch policy
        columns.addLayout(self.col1, 2)
        columns.addLayout(self.col2, 2)
       
        # Adding layouts
        layout1 = QtWidgets.QVBoxLayout()
        layout1 = QtWidgets.QVBoxLayout()
        layout1A = QtWidgets.QVBoxLayout()
        layout1B = QtWidgets.QHBoxLayout()
        layout2 = QtWidgets.QGridLayout(alignment=QtCore.Qt.AlignTop)
        layout3 = QtWidgets.QVBoxLayout()
         
        self.col1.addLayout(layout1)
        self.col2.addLayout(layout2)
        self.col2.addLayout(layout3)
       
        layout1.addLayout(layout1A)
        layout1.addLayout(layout1B)
        layout2.addLayout(layout2, 1,1)
        layout3.addLayout(layout3)
        
        
       

    #####################################################
    #                     UI ELEMENTS                   #
    #####################################################

        # Get selected button
        self.itemGetSelectedBtn = QtWidgets.QPushButton('Get selected')
        self.itemGetSelectedBtn.setStyleSheet('background-color:' + lightblue)
        self.itemGetSelectedBtn.clicked.connect(self.itemGetSelected)

        # Filter items
        self.itemFilterLabel = QtWidgets.QLabel('Show:')
        
        self.itemFilterVisibleChk = QtWidgets.QCheckBox('Visible nodes only')
        self.itemFilterVisibleChk.setChecked(True)
        self.itemFilterVisibleChk.setStyleSheet('background-color:' + lightblue)
        self.itemFilterVisibleChk.stateChanged.connect(self.itemReload)
        
        self.itemFilterRefNodesChk = QtWidgets.QCheckBox('Reference nodes only')
        self.itemFilterRefNodesChk.setChecked(True)
        self.itemFilterRefNodesChk.setStyleSheet('background-color:' + lightblue)
        self.itemFilterRefNodesChk.stateChanged.connect(self.itemReload)
        
        self.itemFilterTopNodesChk = QtWidgets.QCheckBox('Top nodes only')
        self.itemFilterTopNodesChk.setChecked(True)
        self.itemFilterTopNodesChk.setStyleSheet('background-color:' + lightblue)
        self.itemFilterTopNodesChk.stateChanged.connect(self.itemReload)
        
        # SearchBox input for filter list
        self.itemSearchBox = QtWidgets.QLineEdit('', self)
        self.itemRegex = QtCore.QRegExp('[0-9A-Za-z_]+')
        self.itemValidator = QtGui.QRegExpValidator(self.itemRegex)
        self.itemSearchBox.setValidator(self.itemValidator)
        self.itemSearchBox.textChanged.connect(self.itemFilter)
        self.itemSearchBox.setStyleSheet('background-color:' + lightblue)
        self.itemSearchBox.setPlaceholderText("Search...")

        # List of items
        self.itemQList = QtWidgets.QListWidget(self)
        self.itemQList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.itemQList.setMinimumWidth(150)
        self.itemQList.itemSelectionChanged.connect(self.itemSel)
        self.itemQList.setStyleSheet('background-color:' + lightblue)

        self.itemSelectLabel = QtWidgets.QLabel('Select')
        
        # All button select
        self.itemSelectAllBtn = QtWidgets.QPushButton('All')
        self.itemSelectAllBtn.setFixedWidth(70)
        self.itemSelectAllBtn.clicked.connect(self.itemSelectAll)
        self.itemSelectAllBtn.setStyleSheet('background-color:' + lightblue)

        # None button select
        self.itemSelectNoneBtn = QtWidgets.QPushButton('None')
        self.itemSelectNoneBtn.setFixedWidth(70)
        self.itemSelectNoneBtn.clicked.connect(self.itemSelectNone)
        self.itemSelectNoneBtn.setStyleSheet('background-color:' + lightblue)

        # Reload button
        self.itemReloadBtn = QtWidgets.QPushButton('Reload')
        self.itemReloadBtn.clicked.connect(self.itemReload)
        self.itemReloadBtn.setStyleSheet('background-color:' + lightblue)

        # Status bar
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.messageChanged.connect(self.statusChanged)

        # Spacers
        self.separator1 = QtWidgets.QWidget()
        self.separator1.setFixedHeight(5)
        self.separator2 = QtWidgets.QWidget()
        self.separator2.setFixedHeight(5)
        self.separator3 = QtWidgets.QWidget()
        self.separator3.setFixedHeight(5)
       
        # Namespace type
        self.namespaceLabel = QtWidgets.QLabel('Namespace: ')
        self.namespaceComboBox = QtWidgets.QComboBox()
        self.namespaceComboBox.addItems(['From selection', 'Custom'])
        self.namespaceComboBox.currentIndexChanged.connect(self.namespaceType)
        self.namespaceCustomText = QtWidgets.QLineEdit('', self)
        self.namespaceCustomText.setPlaceholderText('namespace')
        self.namespaceCustomText.setVisible(False)
        self.namespaceCustomText.setMinimumWidth(140)
        
        # Offset inputs
        self.offsetXLabel = QtWidgets.QLabel('Offset X: ')
        self.offsetXSpinBox = QtWidgets.QDoubleSpinBox()
        self.offsetXSpinBox.setMinimum(0)

        self.offsetYLabel = QtWidgets.QLabel('Offset Y: ')
        self.offsetYSpinBox = QtWidgets.QDoubleSpinBox()
        self.offsetYSpinBox.setMinimum(0)

        self.offsetZLabel = QtWidgets.QLabel('Offset Z: ')
        self.offsetZSpinBox = QtWidgets.QDoubleSpinBox()
        self.offsetZSpinBox.setMinimum(0)
        
        # Copies spinBox
        self.copiesLabel = QtWidgets.QLabel('Copies: ')
        self.copiesSpinBox = QtWidgets.QSpinBox()
        self.copiesSpinBox.setMinimum(1)
        self.copiesSpinBox.setValue(1)
        self.copiesSpinBox.setObjectName('copies')

        # Grouping controls
        self.groupingLabel = QtWidgets.QLabel('Group copies: ')
        self.groupingCheckBox = QtWidgets.QCheckBox('')
        self.groupingCheckBox.clicked.connect(self.groupingCheck)
        self.groupingNameText = QtWidgets.QLineEdit('myGroup01', self)
        self.groupingNameText.setVisible(False)
        self.groupingNameText.setMinimumWidth(100)
    
        # Clone Reference button
        self.cloneBtn = QtWidgets.QPushButton('Clone Reference')
        self.cloneBtn.setFixedHeight(85)
        self.cloneBtn.clicked.connect(self.clone)
    
        

 
        ### Adding all elements to layouts
        #
        layout1A.addWidget(self.itemGetSelectedBtn)
        layout1A.addWidget(self.itemSearchBox)
        layout1A.addWidget(self.itemQList)
        layout1A.addWidget(self.itemFilterVisibleChk)
        layout1A.addWidget(self.itemFilterTopNodesChk)
        #layout1A.addWidget(self.itemFilterRefNodesChk)
        layout1B.addWidget(self.itemSelectLabel)
        layout1B.addWidget(self.itemSelectAllBtn)
        layout1B.addWidget(self.itemSelectNoneBtn)
        layout1A.addWidget(self.itemReloadBtn)

        layout2.addWidget(self.namespaceLabel, 1,0)
        layout2.addWidget(self.namespaceComboBox, 1,1)
        layout2.addWidget(self.namespaceCustomText, 2,1)

        layout2.addWidget(self.separator1, 3,0)
        
        layout2.addWidget(self.offsetXLabel, 4,0)
        layout2.addWidget(self.offsetXSpinBox, 4,1)
        layout2.addWidget(self.offsetYLabel, 5,0)
        layout2.addWidget(self.offsetYSpinBox, 5,1)
        layout2.addWidget(self.offsetZLabel, 6,0)
        layout2.addWidget(self.offsetZSpinBox, 6,1)

        layout2.addWidget(self.separator2, 7,0)
        
        layout2.addWidget(self.copiesLabel, 8,0)
        layout2.addWidget(self.copiesSpinBox, 8,1)

        layout2.addWidget(self.separator1, 9,0)

        layout2.addWidget(self.groupingLabel, 10,0)
        layout2.addWidget(self.groupingCheckBox, 10,1)
        layout2.addWidget(self.groupingNameText, 11,1)

        layout3.addWidget(self.cloneBtn)

        self.resize(winWidth, winHeight)    


        
     
    #####################################################
    #                 INIT FUNCTIONS                    #
    #####################################################

        self.itemLoad()
        self.itemSelectNone()
               




    #####################################################
    #                      FUNCTIONS                    #
    #####################################################

    
    def itemGetSelected(self):
        selection = cmds.ls(sl=1)
        if len(selection) < 1:
            self.statusBar.showMessage('Must be selected at least one item', 4000)
            self.statusBar.setStyleSheet('background-color:' + red)
        else:
            self.itemQList.clear()
            #self.itemQList.addItems(selection)
            for item in selection:
                parents = cmds.listRelatives(item)
                
                for p in parents:
                    itemType = cmds.nodeType(p)
                print (itemType)
                if itemType == 'mesh':
                    itemIcon = iconMesh
                elif itemType == 'nurbsCurve':
                    itemIcon = iconCurve
                elif itemType == 'camera':
                    itemIcon = iconCam
                elif 'Light' in itemType:
                    itemIcon = iconLight
                else:
                    itemIcon = iconRef
                
                self.itemQList.addItem(QtWidgets.QListWidgetItem(itemIcon, str(item)))   
            
            self.itemQList.selectAll()

    
    def itemFilter(self):
        textFilter = str(self.itemSearchBox.text()).lower()
        if not textFilter:
            for row in range(self.itemQList.count()):
                self.itemQList.setRowHidden(row, False)
        else:
            for row in range(self.itemQList.count()):
                if textFilter in str(self.itemQList.item(row).text()).lower():
                    self.itemQList.setRowHidden(row, False)
                else:
                    self.itemQList.setRowHidden(row, True)


    def itemLoad(self):
        #itemType = 'transform'
        dag = 1
        itemTranforms = 1
        global itemList

        if self.itemFilterVisibleChk.isChecked() == True:
            itemVisible = 1
        else:
            itemVisible = 0

        if self.itemFilterRefNodesChk.isChecked() == True:
            itemRefs = 1
        else:
            itemRefs = 0

        if self.itemFilterTopNodesChk.isChecked() == True:
            itemTop = 1
            itemTranforms = 0
            dag = 0
        else:
            itemTop = 0
            itemTranforms = 1
            dag = 1

        
        itemNode = cmds.ls(transforms=itemTranforms, dag=dag, v=itemVisible, rn=itemRefs, assemblies=itemTop)
        itemList = []
        itemList.append(itemNode)
        
        for item in itemList:
            for n in range(len(item)):
                
                parents = cmds.listRelatives(item[n])
                for p in parents:
                    itemType = cmds.nodeType(p)
                print (itemType)
                if itemType == 'mesh':
                    itemIcon = iconMesh
                else:
                    itemIcon = iconRef
                
                self.itemQList.addItem(QtWidgets.QListWidgetItem(itemIcon, str(item[n])))


    ### Get selected items in itemQList
    def itemSel(self):
        global itemSelected

        items = self.itemQList.selectedItems()
        itemSelected = []
        for i in items:
            itemSelected.append(i.text())
             
        return itemSelected
        #self.statusBar.showMessage(str(itemSelected), 4000) #for testing


    def itemSelectAll(self):
        self.itemQList.selectAll()

        
    def itemSelectNone(self):
        itemSelected = []
        self.itemQList.clearSelection()
        if len(itemSelected) < 1:
            del itemSelected[:]
        
    
    def itemReload(self):
        self.itemQList.clear()
        if len(itemSelected) < 1:
            del itemSelected[:]
        self.itemLoad()


    
    def namespaceType(self):
        if self.namespaceComboBox.currentText() == 'Custom':
            self.namespaceCustomText.setVisible(True)
        else:
            self.namespaceCustomText.setVisible(False)



    def groupingCheck(self):
        if self.groupingCheckBox.isChecked():
            self.groupingNameText.setVisible(True)
        else:
            self.groupingNameText.setVisible(False)
    
    

    ### CLONE REFERENCE (main function)
    #
    def clone(self):
        suffixID = '_c0001'
        copies = self.copiesSpinBox.value()
        offset = [self.offsetXSpinBox.value(), self.offsetYSpinBox.value(), self.offsetZSpinBox.value()]
        groupName = self.groupingNameText.text()
        newItems = []

        if len(itemSelected) < 1:
            self.statusBar.showMessage('Must be selected at least one item in the list', 4000)
            self.statusBar.setStyleSheet('background-color:'+red)
        else:

            for ref in itemSelected:
                # Get file path from each reference
                refPath = cmds.referenceQuery(ref, f=1)

                # Get reference node (RN)
                refNode = cmds.referenceQuery(ref, rfn=1)

                # Get position coordinates for each reference
                refPos = cmds.xform(ref, q=1, t=1)
                
                # Get namespace from each reference or use custom name
                if self.namespaceComboBox.currentText() == 'Custom':
                    refNS = self.namespaceCustomText.text()+suffixID
                else:
                    refNS = ref.split(':')[0]+suffixID
                
                print('\n--- Ref: '+str(ref))

               
                for n in range(copies):
                    # Create new reference
                    new = (cmds.file(refPath, r=1, namespace=refNS, rnn=1))

                    # Get the topnode only
                    new = cmds.ls(new, assemblies=True)[0]
                    print('\n--- New: '+str(new))

    
                    # Match transforms from initial reference to new reference
                    cmds.matchTransform(new, ref)

                    # Compute position offset for each new reference
                    newPosX = refPos[0] + offset[0] + (offset[0]*n)
                    newPosY = refPos[1] + offset[1] + (offset[1]*n)
                    newPosZ = refPos[2] + offset[2] + (offset[2]*n)

                    # Set position offset (WorldSpace)
                    cmds.xform(new, ws=1, t=(newPosX,  newPosY,  newPosZ) )


                    # Fill list and sorting
                    newItems.append(new)
                    newItemsSorted=sorted(newItems, key=lambda x: ''.join(reversed(x.split(':')[0])))


                    # Divide list in chunks from the origin references selection amount
                    def divide_chunks(l, n):
                        for i in range(0, len(l), n):
                            yield l[i:i + n]
                    
                    n = len(itemSelected)
                    newItemsGrouped = list(divide_chunks(newItemsSorted, n))


            # Create groups for each bundle of selection
            if self.groupingCheckBox.isChecked():
                for items in newItemsGrouped:
                    cmds.group(items, name=groupName)
       
            
            # Display log for results
            print('\n--- New Items: '+str(newItems))
            print('\n--- New Items Sorted: '+str(newItemsSorted))
            print('\n--- New Items Grouped: '+str(newItemsGrouped))
            
            print('\n--- '+ str(len(itemSelected)) + ' items cloned successfully!')
            self.statusBar.showMessage(''+ str(len(itemSelected)) + ' items cloned successfully!', 4000)
            self.statusBar.setStyleSheet('background-color:' + green)


   

    def statusChanged(self, args):
        if not args:
            self.statusBar.setStyleSheet('background-color:none')
      

     
    def closeEvent(self, event):
        del itemSelected[:]
        pass






#####################################################
#                    INIT WINDOW                    #
#####################################################

if __name__ == '__main__':
    win = cloneReference(parent=getMainWindow())
    try:
        win.close()
    except:
        pass
  
    win.show()
    win.raise_()