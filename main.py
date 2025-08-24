
#   Librerias
import sys
from PySide6.QtWidgets import QApplication

#   UI
from app.ui.views.main_view import MainView

#   Services
from app.services.settings_service import SettingsService



def main():

    #   Crear la app de QT y pasar variables de entorno
    app = QApplication(sys.argv)

    #   Crear/Cargar configuraciones
    settings = SettingsService()

    #   Crear la ventana
    window = MainView(settings=settings)

    #   Mostrar la ventana
    window.show()

    #   
    sys.exit(app.exec())





if __name__ == "__main__":
    main()