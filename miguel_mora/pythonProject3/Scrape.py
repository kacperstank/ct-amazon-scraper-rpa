from playwright.sync_api import sync_playwright
import time
from Producto import Producto


class Scrape:

    #metodo que abre el navegador y obtiene los datos
    def abrir_navegador_y_extraer(self):
        listado = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto('https://www.amazon.es')
            time.sleep(1)

            search_box = page.query_selector("input#twotabsearchtextbox")
            search_box.fill("portátil i5")
            search_box.press("Enter")
            page.wait_for_timeout(2000)

            productos = page.query_selector_all("div[data-component-type='s-search-result']")
            contador = 0

            for producto in productos:
                if contador >= 11:
                    break

                try:
                    nombre = producto.query_selector("h2 a span")
                    precio_entero = producto.query_selector("span.a-price-whole")
                    precio_decimal = producto.query_selector("span.a-price-fraction")
                    imagen = producto.query_selector("img.s-image")

                    if nombre and precio_entero and precio_decimal and imagen:
                        nombre_completo = nombre.inner_text().strip()
                        precio = f"{precio_entero.inner_text().strip()},{precio_decimal.inner_text().strip()} €"
                        url_imagen = imagen.get_attribute("src").strip()

                        producto_obj = Producto(nombre_completo, precio, url_imagen)
                        listado.append(producto_obj)
                        contador += 1
                except Exception as e:
                    print(f"Error al procesar producto: {e}")
                    continue

            browser.close()
        return listado
