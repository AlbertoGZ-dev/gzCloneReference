'''
████████████████████████████████████████████████████████████████████████████
    
    gzCloneReference for Maya
    
    Description: gzCloneReference is a tool to clone or create multiple
    copies of external references keeping transforms from initial reference.


    Author: AlbertoGZ
    albertogzonline@gmail.com
    https://github.com/AlbertoGZ-dev

████████████████████████████████████████████████████████████████████████████

'''

from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
from pathlib import Path

import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
import json
import os


# GENERAL VARS
title = 'gzCloneReference'
version = '0.1.3'
about = 'by AlbertoGZ'
winWidth = 550
winHeight = 500
scriptPath = os.path.dirname(__file__)
configFile = ''
logo = scriptPath+'/icons/gzCloneReferenceIcon.png'
icon = QtGui.QIcon(logo)
pixmap = QtGui.QPixmap(logo)

# colors
red = '#872323'
green = '#207527'
lightbrown = '#7d654b'
lightpurple = '#604b69'
lightgreen = '#5b694b'
lightblue = '#3e5158'
lightgrey = '#999'
midgrey = '#777'
darkgrey = '#111'
darkgrey2 = '#222'
magent = '#b31248'
cyan = '#07888c'
yellow = '#c7b600'
orange = '#b8810a'
white = '#c9c9c9'
black = '#1a1a1a'

itemSelected = []
iconMesh = QtGui.QIcon(":/reference.svg")
iconRef = QtGui.QIcon(":/reference.svg")
iconCurve = QtGui.QIcon(":/nurbsCurve.svg")
iconCam = QtGui.QIcon(":/camera.svg")
iconLight = QtGui.QIcon(":/ambientLight.svg")



def getMainWindow():
    main_window_ptr = omui.MQtUtil.mainWindow()
    mainWindow = wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    return mainWindow


class gzCloneReference(QtWidgets.QMainWindow):

    def __init__(self, parent=getMainWindow()):
        super(gzCloneReference, self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint)

    

        #####################################################
        #                MAIN LAYOUT DESIGN                 #
        #####################################################

        # Creates object, Title Name and Adds a QtWidget as our central widget/Main Layout
        self.setObjectName(title+'UI')
        self.setWindowTitle(title + ' ' + 'v' + version + ' - ' + about)
        self.setWindowIcon(icon)
        
        self.tabs = QtWidgets.QTabWidget(self)
        self.tabs.setStyleSheet('background-color:' + darkgrey2)

        tab1Layout = QtWidgets.QWidget(self)
        tab2Layout = QtWidgets.QWidget(self)

        self.tabs.addTab(tab1Layout, 'Clone')
        self.tabs.addTab(tab2Layout, 'About')

        self.tabs.currentChanged.connect(self.onTabChange)
       
        self.tabs.setStyleSheet('QTabWidget::pane {border: 1px solid' + magent + ';}' 'QTabBar::tab:selected {background-color:'+ magent +';}')

        self.setCentralWidget(self.tabs)
       


        '''
        |‾‾‾‾‾‾\________________________________________
        |                                               |
        |   CLONE TAB                                   |
        |                                               |
                                                      '''
        ### LAYOUT
        # Creating layouts
        cols = QtWidgets.QHBoxLayout(tab1Layout)

        # Creating N vertical layout
        col1 = QtWidgets.QVBoxLayout()
        col2 = QtWidgets.QVBoxLayout()

        layout1 = QtWidgets.QVBoxLayout()
        layout1 = QtWidgets.QVBoxLayout()
        layout1A = QtWidgets.QVBoxLayout()
        layout1B = QtWidgets.QHBoxLayout()
        layout2 = QtWidgets.QGridLayout(alignment=QtCore.Qt.AlignTop)
        layout3 = QtWidgets.QVBoxLayout()


        # Adding layouts
        cols.addLayout(col1, 0)
        cols.addLayout(col2, 1)

        col1.addLayout(layout1)
        col2.addLayout(layout2)
        col2.addLayout(layout3)
       
        layout1.addLayout(layout1A)
        layout1.addLayout(layout1B)
        layout2.addLayout(layout2, 1,1)
        layout3.addLayout(layout3)
        
        
       

        #####################################################
        #                     UI ELEMENTS                   #
        #####################################################

        # Get selected button
        self.itemGetSelectedBtn = QtWidgets.QPushButton('Get selected')
        self.itemGetSelectedBtn.setStyleSheet('background-color:' + black)
        self.itemGetSelectedBtn.clicked.connect(self.itemGetSelected)

        # Filter items
        self.itemFilterLabel = QtWidgets.QLabel('Show:')
        
        self.itemFilterVisibleChk = QtWidgets.QCheckBox('Visible nodes only')
        self.itemFilterVisibleChk.setChecked(True)
        self.itemFilterVisibleChk.setStyleSheet('background-color:' + black)
        self.itemFilterVisibleChk.stateChanged.connect(self.itemReload)
        
        self.itemFilterRefNodesChk = QtWidgets.QCheckBox('Reference nodes only')
        self.itemFilterRefNodesChk.setChecked(True)
        self.itemFilterRefNodesChk.setStyleSheet('background-color:' + black)
        self.itemFilterRefNodesChk.stateChanged.connect(self.itemReload)
        
        self.itemFilterTopNodesChk = QtWidgets.QCheckBox('Top nodes only')
        self.itemFilterTopNodesChk.setChecked(True)
        self.itemFilterTopNodesChk.setStyleSheet('background-color:' + black)
        self.itemFilterTopNodesChk.stateChanged.connect(self.itemReload)
        
        # SearchBox input for filter list
        self.itemSearchBox = QtWidgets.QLineEdit('', self)
        self.itemRegex = QtCore.QRegExp('[0-9A-Za-z_]+')
        self.itemValidator = QtGui.QRegExpValidator(self.itemRegex)
        self.itemSearchBox.setValidator(self.itemValidator)
        self.itemSearchBox.textChanged.connect(self.itemFilter)
        self.itemSearchBox.setStyleSheet('background-color:' + black)
        self.itemSearchBox.setPlaceholderText("Search...")

        # List of items
        self.itemQList = QtWidgets.QListWidget(self)
        self.itemQList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.itemQList.setMinimumWidth(150)
        self.itemQList.itemSelectionChanged.connect(self.itemSel)
        self.itemQList.setStyleSheet('background-color:' + black)

        self.itemSelectLabel = QtWidgets.QLabel('Select')
        
        # All button select
        self.itemSelectAllBtn = QtWidgets.QPushButton('All')
        self.itemSelectAllBtn.setFixedWidth(70)
        self.itemSelectAllBtn.clicked.connect(self.itemSelectAll)
        self.itemSelectAllBtn.setStyleSheet('background-color:' + black)

        # None button select
        self.itemSelectNoneBtn = QtWidgets.QPushButton('None')
        self.itemSelectNoneBtn.setFixedWidth(70)
        self.itemSelectNoneBtn.clicked.connect(self.itemSelectNone)
        self.itemSelectNoneBtn.setStyleSheet('background-color:' + black)

        # Reload button
        self.itemReloadBtn = QtWidgets.QPushButton('Reload')
        self.itemReloadBtn.clicked.connect(self.itemReload)
        self.itemReloadBtn.setStyleSheet('background-color:' + black)

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
        self.cloneBtn.setFixedHeight(60)
        self.cloneBtn.clicked.connect(self.clone)
        self.cloneBtn.setStyleSheet('background-color:' + magent)

    
        

 
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



        '''
        |‾‾‾‾‾‾‾‾\______________________________________
        |                                               |
        |   ABOUT TAB                                   |
        |                                               |
                                                      '''
        ### LAYOUT
        # Creating layouts
        aboutLayout = QtWidgets.QHBoxLayout(tab2Layout)  
        layout1 = QtWidgets.QVBoxLayout(alignment=QtCore.Qt.AlignCenter)   
        # Adding layouts
        aboutLayout.addLayout(layout1)


        ### UI ELEMENTS
        self.aboutIcon = QtWidgets.QLabel()
        self.aboutIcon.setPixmap(pixmap)
        self.aboutIcon.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)    
        self.aboutLabel = QtWidgets.QLabel('gzCloneReference\nv'+version+'\n'+about+'\n\ngzCloneReference is a tool to clone or create \nmultiple copies of external references\n keeping transforms from initial reference.\n\n')
        self.aboutLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)


         ### ADDING ELEMENTS TO LAYOUT
        layout1.addWidget(self.aboutIcon)
        layout1.addWidget(self.aboutLabel)

       

        ### GLOBAL UI WINDOW
        #
        self.resize(winWidth, winHeight)

  


        
     
    #####################################################
    #                 INIT FUNCTIONS                    #
    #####################################################

        self.itemLoad()
        self.itemSelectNone()
               




    #####################################################
    #                      FUNCTIONS                    #
    #####################################################


    ### UI Settings by Tab
    #
    def onTabChange(self, i): 
        #self.statusBar.showMessage(str(i), 2000)
        if i == 0:
            self.tabs.setStyleSheet('QTabWidget::pane {border: 1px solid' + magent + '; background-color:' + darkgrey2 +'}' 'QTabBar::tab:selected {background-color:' + magent +';}')
        if i == 1:
            self.tabs.setStyleSheet('QTabWidget::pane {border: 1px solid' + magent + '; background-color:' + darkgrey2 +'}' 'QTabBar::tab:selected {background-color:' + magent +';}')


    
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
    win = gzCloneReference(parent=getMainWindow())
    try:
        win.close()
    except:
        pass
  
    win.show()
    win.raise_()