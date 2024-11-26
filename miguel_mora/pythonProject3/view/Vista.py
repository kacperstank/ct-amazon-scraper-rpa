from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QPushButton, QWidget, QMessageBox
from PyQt5.QtCore import Qt
import requests


class Vista(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Datos procesados")
        self.setGeometry(100, 100, 1800, 900)

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        title_label = QLabel("Datos Procesados")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Configuración de la tabla
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(self.data))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Imagen", "Nombre", "Precio"])
        self.tableWidget.setColumnWidth(0, 150)  # Ancho para las imágenes
        self.tableWidget.setColumnWidth(1, 1220)  # Ancho para los nombres
        self.tableWidget.setColumnWidth(2, 150)  # Ancho para los precios

        # Mostrar solo 4 filas visibles
        self.tableWidget.setFixedWidth(1600)
        self.tableWidget.setFixedHeight(4 * 133)  # Altura ajustada para 4 filas

        for row in range(len(self.data)):
            self.tableWidget.setRowHeight(row, 120)

        layout.addWidget(self.tableWidget, alignment=Qt.AlignCenter)

        # Insertar datos en la tabla
        for row, producto in enumerate(self.data):
            # Cargar la imagen
            image_label = QLabel()
            pixmap = QPixmap()
            try:
                if producto.imagen_url:  # Verificar si la URL de la imagen no está vacía
                    response = requests.get(producto.imagen_url, timeout=5)
                    if response.status_code == 200:
                        pixmap.loadFromData(response.content)
                    else:
                        image_label.setText("No imágenes disponibles")
                else:
                    image_label.setText("No imágenes disponibles")
            except Exception as e:
                self.show_error_message("Error al cargar la imagen", str(e))
                image_label.setText("No imágenes disponibles")

            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
            if not pixmap.isNull():
                image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            self.tableWidget.setCellWidget(row, 0, image_label)

            # Nombre del producto
            self.tableWidget.setItem(row, 1, QTableWidgetItem(producto.nombre))

            # Precio del producto
            self.tableWidget.setItem(row, 2, QTableWidgetItem(producto.precio))

        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Etiqueta de total de productos
        total_label = QLabel(f"Total productos: {len(self.data)}")
        total_label.setAlignment(Qt.AlignCenter)
        total_label.setStyleSheet("""
        font-size: 16px;
        font-weight: bold;
        color: #6a6a6a;
        """)
        layout.addWidget(total_label, alignment=Qt.AlignCenter)

        # Botón para regresar al menú
        back_button = QPushButton("Regresar al Menú")
        back_button.clicked.connect(self.return_to_menu)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

    def return_to_menu(self):
        try:
            from MainWindow import MainWindow
            self.ventana = MainWindow()
            self.ventana.show()
            self.close()
        except Exception as e:
            self.show_error_message("Error al regresar al menú", str(e))

    def show_error_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()
