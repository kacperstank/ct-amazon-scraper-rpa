import pyautogui
import time
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re
from Producto import Producto  # Asegúrate de importar la clase Producto


class RPA:
#abre el navegador y cuando llega a la web establece el zoom al 100, luego al 80 y hace 3 caps mientras scrollea
    def abrir_navegador_capturar(self):
        pyautogui.PAUSE = 0.1

        # Abrir el navegador Opera
        pyautogui.hotkey('win', 'r')
        time.sleep(0.5)
        pyautogui.write('opera')
        pyautogui.press('enter')
        time.sleep(3)

        # Mover la ventana a posición visible
        ventanas_opera = pyautogui.getWindowsWithTitle("Opera")
        if ventanas_opera:
            ventana = ventanas_opera[0]
            ventana.moveTo(0, 0)
            ventana.resizeTo(1400, 900)
        else:
            print("No se encontró la ventana de Opera. Verifica que el navegador se haya abierto correctamente.")
            return

        # Navegar a la página
        pyautogui.write(
            'https://www.amazon.es/s?k=portatil+i5&crid=3A1WT6M71WUDF&sprefix=portatil+i5%2Caps%2C104&ref=nb_sb_noss_1')
        pyautogui.press('enter')
        time.sleep(5)

        # Ajustar zoom para capturar más contenido visible
        pyautogui.hotkey('ctrl', '0')  # Restablecer zoom a 100%
        time.sleep(0.5)
        for _ in range(2):  # Reducir zoom para incluir más contenido
            pyautogui.hotkey('ctrl', '-')
            time.sleep(0.5)

        # Capturar múltiples secciones de la página
        capturas = []
        for i in range(3):  # Realizar 3 capturas con desplazamiento
            region_productos = (900, 180, 900, 1600)
            screenshot = pyautogui.screenshot(region=region_productos)
            file_name = f"./captura_productos_{i}.png"
            screenshot.save(file_name)
            capturas.append(file_name)
            print(f"Captura de pantalla guardada como {file_name}")
            pyautogui.scroll(-800)  # Scroll
            time.sleep(2)

        # Cerrar el navegador
        print("Cerrando el navegador...")
        pyautogui.hotkey('alt', 'f4')

        return capturas
#ayuda a que el ocr pueda obtener mejor los datos (sube contraste, blanco y negro...etc)
    def preprocesar_imagen(self, ruta_imagen):
        try:
            imagen = Image.open(ruta_imagen)
            imagen = imagen.convert('L')
            imagen = imagen.filter(ImageFilter.SHARPEN)
            enhancer = ImageEnhance.Contrast(imagen)
            imagen = enhancer.enhance(2)
            imagen.save(ruta_imagen.replace(".png", "_mejorada.png"))
            return ruta_imagen.replace(".png", "_mejorada.png")
        except Exception as e:
            print(f"Error al preprocesar la imagen: {e}")
            return ruta_imagen

#extrae el texto de las capturas realizadas
    def realizar_ocr(self, capturas):
        try:
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            texto_extraido = ""

            for captura in capturas:
                captura_mejorada = self.preprocesar_imagen(captura)
                imagen = Image.open(captura_mejorada)
                texto_extraido += pytesseract.image_to_string(imagen, lang='spa') + "\n"

            if not texto_extraido.strip():
                print("Advertencia: No se detectó texto en las imágenes.")
                return ""
            return texto_extraido
        except Exception as e:
            print(f"Error durante OCR: {e}")
            return ""

#procesa el texto obtenido por el OCR para crear productos
    def procesar_texto(self, texto):
        lineas = texto.split("\n")
        lineas = [linea.strip() for linea in lineas if len(linea.strip()) > 5]

        # Filto para detectar produtos
        patron_precio = r"\d{1,3}(?:[.,]\d{3})*,\d{2}"
        marcas = ["HP", "ASUS", "Lenovo", "MSI", "DELL", "Portátil", "Ordenador"]

        productos = []

        for linea in lineas:
            if any(linea.lower().startswith(marca.lower()) for marca in marcas):
                # Filtro para detectar precios
                precio_match = re.search(patron_precio, linea)
                if precio_match:
                    precio = precio_match.group().replace('.', '').replace(',', '.')
                else:
                    precio = "Precio no disponible"

                # Crear un objeto Producto y añadirlo a la lista
                producto = Producto(nombre=linea, precio=precio)
                productos.append(producto)

        return productos

#ejecuta varios metodos de los antes creados en el orden correcto
    def ejecutar(self):
        capturas = self.abrir_navegador_capturar()
        texto = self.realizar_ocr(capturas)
        if texto:
            productos = self.procesar_texto(texto)
            for producto in productos:
                print(f"Nombre: {producto.nombre}, Precio: {producto.precio}")
        else:
            print("No se pudo extraer texto para procesar.")
