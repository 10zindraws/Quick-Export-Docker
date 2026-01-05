# this file is placed in the publid domain by its author, fullmontis
# see the LICENSE file for more information

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import (QWidget, QLineEdit, QListWidget, QHBoxLayout, 
                             QVBoxLayout, QPushButton, QMessageBox, QCheckBox, 
                             QSpinBox, QComboBox, QMessageBox, QFileDialog, QLabel, QFrame)
import krita
import os

class QuickExportLayersDocker(krita.DockWidget):
    def __init__(self):
        super(QuickExportLayersDocker, self).__init__()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setWindowTitle(i18n("Quick Export Layers Docker"))

        self.directoryTextField = QLineEdit()
        self.directoryDialogButton = QPushButton(i18n("Export Dir"))
        self.saveDefaultsButton = QPushButton(i18n("Save Defaults"))
        self.batchmodeCheckBox = QCheckBox(i18n("Skip export options menu"))
        self.exportOnlySelectedCheckBox = QCheckBox(i18n("Export only selected layer"))
        self.exportLayersSeparatelyCheckBox = QCheckBox(i18n("Export layers separately"))
        self.createFileDirectoryCheckBox = QCheckBox(i18n("Create file directory"))
        self.groupAsLayerCheckBox = QCheckBox(i18n("Group as layer"))
        self.ignoreFilterLayersCheckBox = QCheckBox(i18n("Ignore filter layers"))
        self.ignoreInvisibleLayersCheckBox = QCheckBox(i18n("Ignore invisible layers"))

        self.formatsComboBox = QComboBox()
        self.exportButton = QPushButton(i18n("Export"))
        self.exportMessage = QLabel(i18n(""))

        dirLayout = QHBoxLayout()
        dirLayout.addWidget(self.directoryTextField)
        dirLayout.addWidget(self.directoryDialogButton)
        self.directoryTextField.setText(os.path.expanduser("~"))
        self.directoryDialogButton.clicked.connect(self.selectDir)
        layout.addLayout(dirLayout)
        
        layout.addWidget(self.saveDefaultsButton)
        self.saveDefaultsButton.clicked.connect(self.saveDefaults)

        layout.addWidget(self.batchmodeCheckBox)
        layout.addWidget(self.exportOnlySelectedCheckBox)
        layout.addWidget(self.createFileDirectoryCheckBox)
        layout.addWidget(self.exportLayersSeparatelyCheckBox)
        
        spacer_layout = QHBoxLayout()
        spacer_layout.addWidget(QFrame())

        multi_image_layout = QVBoxLayout()
        multi_image_layout.addWidget(self.groupAsLayerCheckBox)
        multi_image_layout.addWidget(self.ignoreFilterLayersCheckBox)
        multi_image_layout.addWidget(self.ignoreInvisibleLayersCheckBox)
        spacer_layout.addLayout(multi_image_layout)

        layout.addLayout(spacer_layout)

        self.exportLayersSeparatelyCheckBox.stateChanged.connect(self.toggleExportLayersSeparately)
        self.batchmodeCheckBox.setChecked(True)
        self.groupAsLayerCheckBox.setChecked(True)
        self.ignoreFilterLayersCheckBox.setChecked(True)
        self.ignoreInvisibleLayersCheckBox.setChecked(True)

        formatLayout = QHBoxLayout()
        formatLayout.addWidget(self.formatsComboBox)
        self.formatsComboBox.addItem(i18n("png"))
        self.formatsComboBox.addItem(i18n("jpeg"))
        formatLayout.addWidget(self.exportButton)
        layout.addLayout(formatLayout)
        
        self.exportButton.clicked.connect(self.exportAction)

        layout.addWidget(self.exportMessage)

        self.setWidget(widget)

        self.loadDefaults()

    def canvasChanged(self, canvas):
        pass

    # get escaped ASCII sequence for the path
    def escapePath(self, path):
        path_escaped = path.encode("unicode_escape").decode("ascii")
        comma_encoded = "\\x" + hex(ord(","))[2:]
        return path_escaped.replace(",", comma_encoded)

    def decodePath(self, path):
        return path.encode("ascii").decode("unicode_escape")

    def saveDefaults(self):
        directory = self.escapePath(self.directoryTextField.text())
        batchmode = str(int(self.batchmodeCheckBox.isChecked()))
        exportOnlySelected = str(int(self.exportOnlySelectedCheckBox.isChecked()))
        exportLayersSeparately = str(int(self.exportLayersSeparatelyCheckBox.isChecked()))
        createFileDirectory = str(int(self.createFileDirectoryCheckBox.isChecked()))
        ignoreFilterLayers = str(int(self.ignoreFilterLayersCheckBox.isChecked()))
        groupAsLayer = str(int(self.groupAsLayerCheckBox.isChecked()))
        ignoreInvisibleLayers = str(int(self.ignoreInvisibleLayersCheckBox.isChecked()))
        formatDefault = str(self.formatsComboBox.findText(self.formatsComboBox.currentText()))

        defaults = ",".join([directory, batchmode, exportOnlySelected, exportLayersSeparately, 
                             createFileDirectory, ignoreFilterLayers, 
                             groupAsLayer, ignoreInvisibleLayers, 
                             formatDefault])
        
        Application.writeSetting("","export_layers_docker", defaults)
        self.exportMessage.setText(i18n("Defaults saved"))

    def loadDefaults(self):
        defaults = Application.readSetting("", "export_layers_docker", "")
        if defaults == "":
            self.saveDefaults()
            return
        
        defaults = defaults.split(",")
        assert(len(defaults) == 9)
        [directory, batchmode, exportOnlySelected, exportLayersSeparately, 
         createFileDirectory, 
         groupAsLayer, ignoreFilterLayers, ignoreInvisibleLayers, formatDefault] = defaults

        self.directoryTextField.setText(self.decodePath(directory))
        self.batchmodeCheckBox.setChecked(bool(int(batchmode)))
        self.exportOnlySelectedCheckBox.setChecked(bool(int(exportOnlySelected)))
        self.exportLayersSeparatelyCheckBox.setChecked(bool(int(exportLayersSeparately)))
        self.createFileDirectoryCheckBox.setChecked(bool(int(createFileDirectory)))
        self.groupAsLayerCheckBox.setChecked(bool(int(groupAsLayer)))
        self.ignoreFilterLayersCheckBox.setChecked(bool(int(ignoreFilterLayers)))
        self.ignoreInvisibleLayersCheckBox.setChecked(bool(int(ignoreInvisibleLayers)))
        self.formatsComboBox.setCurrentIndex(int(formatDefault))

        self.toggleExportLayersSeparately()

    def selectDir(self):
        directory = self.directoryTextField.text()
        if not os.path.isdir(directory):
            directory = os.path.expanduser("~")

        directory = QFileDialog.getExistingDirectory(
            self, i18n("Select a Folder"), 
            directory, QFileDialog.ShowDirsOnly)
        self.directoryTextField.setText(directory)

    def toggleExportLayersSeparately(self):
        state = not self.exportLayersSeparatelyCheckBox.isChecked()
        self.ignoreFilterLayersCheckBox.setDisabled(state)
        self.groupAsLayerCheckBox.setDisabled(state)
        self.ignoreInvisibleLayersCheckBox.setDisabled(state)

    def exportAction(self):
        directory = self.directoryTextField.text()
        document = Application.activeDocument()

        self.exportMessage.setText(i18n("Exporting..."))
        if not document:
            self.exportMessage.setText(i18n("Select one document."))
            return 
        elif not self.directoryTextField.text():
            self.exportMessage.setText(i18n("Select the initial directory."))
            return 
        elif not os.path.exists(directory) or not os.path.isdir(directory):
            self.exportMessage.setText(i18n("Selected directory doesn't exist"))
            return

        documentNameWithExt = "Untitled"
        if document.fileName():
            documentNameWithExt = document.fileName() 
        documentName, extension = os.path.splitext(os.path.basename(documentNameWithExt))
            
        exportDir = ""

        baseNode = document.rootNode()
        exportName = documentName

        if self.exportOnlySelectedCheckBox.isChecked():
            baseNode = document.activeNode()
            exportName = baseNode.name()

        if self.createFileDirectoryCheckBox.isChecked():
            exportDir = exportName
            self.createDirectory(exportDir)

        Application.setBatchmode(self.batchmodeCheckBox.isChecked())

        if self.exportLayersSeparatelyCheckBox.isChecked():
            self.exportLayers(baseNode, exportDir)
        else:
            self.exportNode(baseNode, exportDir, exportName, self.formatsComboBox.currentText())

        Application.setBatchmode(True)

        self.exportMessage.setText(i18n("All layers have been exported."))

    def exportNode(self, node, export_folder, filename, file_format):
        export_file_path = os.path.join(self.directoryTextField.text(), 
                                        export_folder, 
                                        f"{filename}.{file_format}")

        document = Application.activeDocument()
        bounds = QRect(0, 0, document.width(), document.height())
        node.save(export_file_path, 
                  document.resolution() / 72.,
                  document.resolution() / 72., 
                  krita.InfoObject(), bounds)

    def exportLayers(self, parentNode, parentDir):
        for node in parentNode.childNodes():
            if node.name() == "Selection Mask":
                continue
            elif self.ignoreFilterLayersCheckBox.isChecked() and 'filter' in node.type():
                continue
            elif self.ignoreInvisibleLayersCheckBox.isChecked() and not node.visible():
                continue
            elif node.type() == 'grouplayer' and node.childNodes() and not self.groupAsLayerCheckBox.isChecked():
                newDir = os.path.join(parentDir, node.name())
                self.createDirectory(newDir)
                self.exportLayers(node, newDir)
            else:
                node_name = node.name()
                file_format = self.formatsComboBox.currentText()
                if '[jpeg]' in node_name:
                    file_format = 'jpeg'
                elif '[png]' in node_name:
                    file_format = 'png'
                self.exportNode(node, parentDir, node_name, file_format)

    def createDirectory(self, directory):
        target_directory = os.path.join(self.directoryTextField.text(), directory)
        if os.path.exists(target_directory) and os.path.isdir(target_directory):
            return
        try:
            os.makedirs(target_directory)
        except OSError as e:
            raise e
        
