# imports
import sys
#  Esto es lo correcto en PyQt6
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt
from hvac_core import DuctSizingInput, size_round_duct

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.setWindowTitle("DuctFlow — Dimensionado de conductos")
        self.resize(380, 320)        # ancho x alto en px; o setFixedSize(...) si no querés que se redimensione

        titulo = QLabel("DuctFlow")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c6e9b;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_caudal = QLineEdit(self)
        self.input_caudal.setPlaceholderText("Caudal (m³/s)") 
        self.input_perdida = QLineEdit(self)
        self.input_perdida.setPlaceholderText("Pérdida de carga (Pa/m)")

        boton = QPushButton("Calcular", self)

        boton.clicked.connect(self.calcular)

        # creo etiquetas
        self.resultado_diametro = QLabel("Diametro: ", self)
        self.resultado_velocidad = QLabel("Velocidad: ", self)
        self.resultado_reynolds = QLabel("Reynolds: ", self)

        layout.addWidget(titulo)

        layout.addWidget(self.input_caudal)
        layout.addWidget(self.input_perdida)
        layout.addWidget(boton)

        layout.addWidget(self.resultado_diametro)
        layout.addWidget(self.resultado_velocidad)
        layout.addWidget(self.resultado_reynolds)


        self.setLayout(layout)

    def calcular(self):
        try:
            caudal = float(self.input_caudal.text())
            perdida = float(self.input_perdida.text())

            resultado = size_round_duct(DuctSizingInput(caudal, perdida))

            self.resultado_diametro.setText(f"Diámetro: {resultado.diameter_m:.3f} m")
            self.resultado_velocidad.setText(f"Velocidad: {resultado.velocity_ms:.2f} m/s")
            self.resultado_reynolds.setText(f"Reynolds: {resultado.reynolds:.0f}")

        except ValueError as e:
            self.resultado_diametro.setText(f"Error: {e}")
            self.resultado_velocidad.setText("")
            self.resultado_reynolds.setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec())