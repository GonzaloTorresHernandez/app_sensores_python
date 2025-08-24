# app/ui/presenters/settings_presenter.py
from typing import Protocol
from app.services.settings_service import SettingsService


class ISettingsView(Protocol):
    def set_ports(self, ports: list[str]) -> None: ...
    def set_values(self, port: str, baud: int, status: str, theme: str | None = None) -> None: ...
    def append_log(self, text: str) -> None: ...
    def get_selected_port(self) -> str: ...
    def get_selected_baud(self) -> int: ...
    def get_probe(self) -> bytes | None: ...
    def notify_saved(self) -> None: ...
    # Si tu vista es QDialog, también podrías usar: def accept(self) -> None: ...

class SettingsPresenter:
    """Lógica de presentación del diálogo/página de Configuración."""
    def __init__(self, view: ISettingsView, settings: SettingsService):
        self.view = view
        self.settings = settings

    # ---- ciclo de vida ----
    def load(self) -> None:
        cfg = self.settings.data
        # 1) setear valores actuales
        self.view.set_values(cfg.serial_port, cfg.baudrate, status="—", theme=cfg.theme)
        # 2) listar puertos disponibles
        self.on_refresh_ports()

    # ---- eventos de UI ----
    def on_refresh_ports(self) -> None:
        ports = ['COM1', 'COM2', 'COM3']
        self.view.set_ports(ports)
        self.view.append_log(f"Puertos detectados: {ports or '—'}")

    def on_test_clicked(self) -> None:
        port = (self.view.get_selected_port() or "").strip()
        baud = self.view.get_selected_baud()
        probe = self.view.get_probe()

        if not port:
            self.view.append_log("⚠️ Selecciona un puerto antes de probar.")
            self.view.set_values(port, baud, status="Puerto no válido")
            return

        try:
            ok = True
            if ok:
                self.view.append_log(f"✅ Test OK en {port}@{baud}")
                self.view.set_values(port, baud, status="Conexión OK ✅")
            else:
                self.view.append_log(f"⚠️ Sin respuesta en {port}@{baud}")
                self.view.set_values(port, baud, status="Sin respuesta ⚠️")
        except Exception as e:
            self.view.append_log(f"❌ ERROR: {e}")
            self.view.set_values(port, baud, status="Error ❌")

    def save(self) -> None:
        port = (self.view.get_selected_port() or "").strip()
        baud = self.view.get_selected_baud()
        if not port:
            self.view.append_log("⚠️ No se puede guardar: puerto vacío.")
            self.view.set_values(port, baud, status="Puerto vacío")
            return

        self.settings.data.serial_port = port
        self.settings.data.baudrate = baud
        self.settings.save()
        self.view.notify_saved()
