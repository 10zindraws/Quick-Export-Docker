# this file is placed in the public domain by its author, fullmontis
# see the LICENSE file for more information

import krita
from .quickexportlayersdocker import QuickExportLayersDocker

Application.addDockWidgetFactory(krita.DockWidgetFactory("quickexportlayersdocker", 
                                 krita.DockWidgetFactoryBase.DockRight, 
                                 QuickExportLayersDocker))

