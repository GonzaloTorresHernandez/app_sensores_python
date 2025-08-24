from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt


class TopBar(QToolBar):
    """Toolbar superior con acciones principales."""
    def __init__(self, parent=None):
        super().__init__("Barra superior", parent)
        self.setMovable(False)
        self.setFloatable(False)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # Acciones públicas (para conectar desde MainView/Presenter)
        self.act_config = QAction("Configuración…", self)
        self.act_conectar = QAction("Conectar", self)
        self.act_detener = QAction("Detener", self)
        self.act_exportar = QAction("Exportar CSV", self)

        # Atajos y tooltips
        self.act_config.setShortcut("Ctrl+,")
        self.act_conectar.setShortcut("F5")
        self.act_detener.setShortcut("Shift+F5")
        self.act_exportar.setShortcut("Ctrl+E")

        self.act_config.setStatusTip("Abrir preferencias de la aplicación")
        self.act_conectar.setStatusTip("Conectar al dispositivo serial")
        self.act_detener.setStatusTip("Detener lectura")
        self.act_exportar.setStatusTip("Exportar mediciones a CSV")

        # Añadir al toolbar
        self.addAction(self.act_config)
        self.addSeparator()
        self.addAction(self.act_conectar)
        self.addAction(self.act_detener)
        self.addSeparator()
        self.addAction(self.act_exportar)
