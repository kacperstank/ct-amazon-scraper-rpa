class Producto:
    def __init__(self, nombre, precio, imagen_url=None):
        self._nombre = nombre
        self._precio = precio
        self._imagen_url = imagen_url

    # Getters
    @property
    def nombre(self):
        return self._nombre

    @property
    def precio(self):
        return self._precio

    @property
    def imagen_url(self):
        return self._imagen_url

    # Setters
    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @precio.setter
    def precio(self, precio):
        self._precio = precio

    @imagen_url.setter
    def imagen_url(self, imagen_url):
        self._imagen_url = imagen_url

    # Método para mostrar información del producto
    def mostrar_informacion(self):
        print(f"Nombre: {self._nombre}")
        print(f"Precio: {self._precio} €")
        if self._imagen_url:
            print(f"Imagen URL: {self._imagen_url}")
