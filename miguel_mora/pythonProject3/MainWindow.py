from tkinter import Scale

from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QMessageBox, QDesktopWidget
from PyQt5.QtCore import Qt
import pytesseract
from RPA import RPA
from Scrape import Scrape
from view.Vista import Vista

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
#interfaz grafica menu inicial
    def initUI(self):
        self.setWindowTitle("Práctica 2, procesar XLSX PANDAS/XLSXIO")
        self.setGeometry(100, 100, 600, 400)
        self.center_window()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.btn_RPA = QPushButton("RPA", self)
        self.btn_RPA.clicked.connect(self.on_click_RPA)

        self.btn_Scrape = QPushButton("Scrape", self)
        self.btn_Scrape.clicked.connect(self.on_click_Scrape)

        layout.addWidget(self.btn_RPA)
        layout.addWidget(self.btn_Scrape)

        # Asignar layout al widget central
        central_widget.setLayout(layout)

    def on_click_RPA(self):
        rpa = RPA()

        # Realizar capturas y OCR
        capturas = rpa.abrir_navegador_capturar()
        texto = rpa.realizar_ocr(capturas)
        productos = rpa.procesar_texto(texto)

        # Pasar los datos a la clase Vista
        if productos:
            self.ventana = Vista(productos)  # Aquí se pasa la lista de productos
            self.ventana.show()

            self.hide()
        else:
            QMessageBox.warning(self, "Sin datos", "No se encontraron productos en las capturas.")

    def on_click_Scrape(self):
        scrape = Scrape()
        data = scrape.abrir_navegador_y_extraer()

        self.ventana = Vista(data)
        self.ventana.show()
        self.hide()

    # Centra la ventana en la pantalla
    def center_window(self):
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
