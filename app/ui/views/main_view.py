from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QSplitter
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt

#   Tipado
from app.services.settings_service import SettingsService

#   Widgets
from app.ui.widgets.topbar import TopBar
from app.ui.widgets.sidebar import SideBar


#   Ventana princiapl de la app
class MainView(QMainWindow):
    
    def __init__(self, settings: SettingsService):
        super().__init__()
        self.settings = settings


        self.__build_ui()
        self.__wire_actions()
        self.__apply_theme_from_settings()

    
    def __build_ui(self):
        self.setWindowTitle("Mi App de Sensores")
        self.resize(1100, 700)

        splitter = QSplitter(Qt.Horizontal, self)

        # Contenido central
        central = QWidget(self)
        layout = QVBoxLayout(central)
        self.lbl_info = QLabel("Listo para iniciar.\n", alignment=Qt.AlignCenter)
        layout.addWidget(self.lbl_info)
        layout.setContentsMargins(0, 0, 0, 0)

        #   Barra superior
        self.topbar = TopBar(self)
        self.addToolBar(self.topbar)

        #   Barra lateral
        self.sidebar = SideBar(self)

        splitter.addWidget(self.sidebar)
        splitter.addWidget(central)
        splitter.setCollapsible(0, False)
        splitter.setStretchFactor(1,1)


        self.setCentralWidget(splitter)

        self.statusBar().showMessage("Listo")


    def __apply_theme_from_settings(self):
        # Por ahora solo un texto; más adelante puedes aplicar estilos/temas reales
        theme = self.settings.data.theme
        self.lbl_info.setText(
            f"Tema: {theme}\nPuerto: {self.settings.data.serial_port}\nBaudrate: {self.settings.data.baudrate}"
        )

    
    def __wire_actions(self):

        # Conecta acciones del topbar
        self.topbar.act_config.triggered.connect(self.open_settings)
        self.topbar.act_conectar.triggered.connect(self.on_conectar)
        self.topbar.act_detener.triggered.connect(self.on_detener)
        self.topbar.act_exportar.triggered.connect(self.on_exportar)

        # Conecta botones de la sidebar
        self.sidebar.btn_dashboard.clicked.connect(self.show_dashboard)
        self.sidebar.btn_pacientes.clicked.connect(self.show_pacientes)
        self.sidebar.btn_sesiones.clicked.connect(self.show_sesiones)
        self.sidebar.lista.currentTextChanged.connect(self.on_sidebar_item)


    ########################################################################
    #   Acciones para el presenter
    def on_conectar(self):
        # aquí llamas a tu Presenter o caso de uso (crear adapter con settings y conectar)
        self.statusBar().showMessage("Conectando…")

    def on_detener(self):
        self.statusBar().showMessage("Detenido")

    def on_exportar(self):
        self.statusBar().showMessage("Exportando CSV…")

    def show_dashboard(self):
        self.lbl_info.setText("Dashboard")

    def show_pacientes(self):
        self.lbl_info.setText("Pacientes")

    def show_sesiones(self):
        self.lbl_info.setText("Sesiones")

    def on_sidebar_item(self, text: str):
        self.statusBar().showMessage(f"Opción lateral: {text}")

    def open_settings(self):
        from app.ui.views.settings_view import SettingsView
        from app.ui.presenters.settings_presenter import SettingsPresenter

        dlg = SettingsView(parent=self)   # creas el diálogo
        presenter = SettingsPresenter(dlg, self.settings)   # le pasas el servicio
        dlg.bind_presenter(presenter)
        presenter.load()

        if dlg.exec():  # modal, devuelve QDialog.Accepted si se guardó
            self.statusBar().showMessage("Configuración guardada correctamente ✅")


    ########################################################################