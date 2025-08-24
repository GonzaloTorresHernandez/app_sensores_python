# app/ui/views/settings_view.py
from PySide6.QtWidgets import (
    QDialog, QFormLayout, QComboBox, QLineEdit, QPushButton,
    QDialogButtonBox, QLabel, QHBoxLayout, QVBoxLayout, QTextEdit
)

class SettingsView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.presenter = None
        self.setWindowTitle('Configuración')

        self.ports = QComboBox()
        self.baud = QComboBox(); self.baud.addItems(["9600","57600","115200"])
        self.status = QLabel("")
        self.probe = QLineEdit(); self.probe.setPlaceholderText("Opcional: comando de prueba")

        self.btn_refresh = QPushButton("Actualizar puertos")
        self.btn_test = QPushButton("Probar conexión")
        self.btns = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)

        # log (opcional, si quieres ver mensajes)
        self.log = QTextEdit(); self.log.setReadOnly(True)

        form = QFormLayout()
        form.addRow("Puerto:", self.ports)
        form.addRow("Baudrate:", self.baud)
        form.addRow("Probe:", self.probe)

        row = QHBoxLayout()
        row.addWidget(self.btn_refresh)
        row.addWidget(self.btn_test)
        row.addWidget(self.status, 1)

        root = QVBoxLayout(self)
        root.addLayout(form)
        root.addLayout(row)
        root.addWidget(self.log)
        root.addWidget(self.btns)

        # ¡OJO! No conectamos señales aquí porque presenter aún es None

    def bind_presenter(self, presenter):
        """Conecta señales una vez que ya tenemos presenter."""
        self.presenter = presenter
        self.btns.accepted.connect(self.presenter.save)
        self.btns.rejected.connect(self.reject)
        self.btn_refresh.clicked.connect(self.presenter.on_refresh_ports)
        self.btn_test.clicked.connect(self.presenter.on_test_clicked)

    # Métodos que usa el presenter (nombres alineados)
    def set_ports(self, items): self.ports.clear(); self.ports.addItems(items)
    def get_selected_port(self): return self.ports.currentText()
    def get_selected_baud(self): return int(self.baud.currentText())
    def get_probe(self):
        s = self.probe.text().strip()
        return s.encode() if s else None
    def set_values(self, port, baud, status, theme=None):
        if port:
            idx = self.ports.findText(port)
            if idx >= 0: self.ports.setCurrentIndex(idx)
        ix = self.baud.findText(str(baud))
        if ix >= 0: self.baud.setCurrentIndex(ix)
        self.status.setText(status)
    def append_log(self, text): self.log.append(text)
    def notify_saved(self):
        self.status.setText("Configuración guardada ✅")
        self.accept()
