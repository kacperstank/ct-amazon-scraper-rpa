# main.py
import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow

def main():
    app = QApplication(sys.argv)


    try:
        with open("resources/style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Error al cargar la hoja de estilo: {e}")

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

