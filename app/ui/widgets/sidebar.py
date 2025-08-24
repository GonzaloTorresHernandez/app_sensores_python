from PySide6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QPushButton, QListWidget
from PySide6.QtCore import Qt


class SideBar(QWidget):
    """Barra lateral acoplable: navegación y acciones contextuales."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Contenido de ejemplo (ajústalo a tus pantallas)
        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_pacientes = QPushButton("Pacientes")
        self.btn_sesiones = QPushButton("Sesiones")

        self.lista = QListWidget()
        self.lista.addItems(["Resumen", "Gráficas", "Historial"])

        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_pacientes)
        layout.addWidget(self.btn_sesiones)
        layout.addWidget(self.lista, 1)
