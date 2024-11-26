import sys
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QSpacerItem,
    QSizePolicy
)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QFont
from PyQt5.QtCore import Qt

from rpa_handler import RPAHandler
from web_scraper import WebScrapper


class UIHandler(QWidget):
    def __init__(self):
        """
        Initializes the UIHandler class and sets up the main UI layout.
        """
        super().__init__()
        self.scraper = WebScrapper()  # Instance of the WebScrapper class
        self.rpa_handler = RPAHandler()  # Create an instance of RPAHandler
        self.init_ui()

    def init_ui(self):
        """
        Initializes the user interface.
        """
        self.setWindowTitle("Amazon Product Search")
        self.setGeometry(100, 100, 1000, 800)  # Increase window size for better display

        # Main layout for the entire window
        main_layout = QVBoxLayout()

        # Horizontal layout for search input, buttons, and logo
        search_layout = QHBoxLayout()

        # Amazon logo (aligned to the left)
        self.logo_label = QLabel(self)
        self.logo_pixmap = QPixmap("amazon_logo.svg")  # Ensure the path to the logo is correct
        self.logo_pixmap = self.logo_pixmap.scaled(60, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignVCenter)
        search_layout.addWidget(self.logo_label)

        # Add spacer to center the search bar and buttons
        search_layout.addSpacerItem(QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Search input
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search Amazon.es")
        self.search_input.setFixedWidth(300)  # Set fixed width for the search bar
        self.search_input.returnPressed.connect(self.search_product_scraper)  # Trigger scraper search on Enter key press
        search_layout.addWidget(self.search_input)

        # Search button (for scraper)
        self.scraper_button = QPushButton("Search with Scraper", self)
        self.scraper_button.setFixedWidth(150)
        self.scraper_button.clicked.connect(self.search_product_scraper)  # Trigger scraper search on button click
        search_layout.addWidget(self.scraper_button)

        # Search button (for RPA)
        self.rpa_button = QPushButton("Browse Flabelus shoes", self)
        self.rpa_button.setFixedWidth(200)
        self.rpa_button.clicked.connect(self.search_flabelus_with_rpa)  # Trigger RPA search on button click
        search_layout.addWidget(self.rpa_button)

        # Add another spacer to center the search bar and buttons
        search_layout.addSpacerItem(QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        main_layout.addLayout(search_layout)  # Add the search layout to the main layout

        # Scroll area for displaying product results
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize dynamically
        main_layout.addWidget(self.scroll_area)

        # Widget to hold products inside the scroll area
        self.products_widget = QWidget()
        self.products_layout = QVBoxLayout(self.products_widget)

        # Add placeholder message
        self.placeholder_label = QLabel("Results will show up here", self)
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setFont(QFont("Arial", 16, QFont.Bold))  # Set font size and make it bold
        self.products_layout.addWidget(self.placeholder_label)

        self.scroll_area.setWidget(self.products_widget)

        self.setLayout(main_layout)  # Set the main layout for the window

    def search_product_scraper(self):
        """
        Triggered when the 'Search with Scraper' button is clicked or Enter key is pressed.
        Scrapes Amazon and displays up to 10 product details.
        """
        product_name = self.search_input.text()

        # Handle empty search input
        if not product_name:
            self.clear_layout(self.products_layout)  # Clear previous results (if any)
            notice = QLabel("Please enter a product name!", self)
            notice.setAlignment(Qt.AlignCenter)
            self.products_layout.addWidget(notice)
            return

        # Clear previous results and display a loading message
        self.clear_layout(self.products_layout)
        notice = QLabel("Searching with Scraper... Please wait.", self)
        notice.setAlignment(Qt.AlignCenter)
        self.products_layout.addWidget(notice)

        # Fetch HTML content for the search query using scraper
        html_content = self.scraper.fetch_search_results(product_name)

        if html_content:
            products_data = self.scraper.parse_products(html_content)
            self.clear_layout(self.products_layout)  # Clear loading message
            if products_data:
                for product_data in products_data:
                    self.display_product(product_data)  # Display each product
            else:
                notice.setText("No product data found.")
                self.products_layout.addWidget(notice)
        else:
            notice.setText("Failed to fetch Amazon search results.")
            self.products_layout.addWidget(notice)

    def search_flabelus_with_rpa(self):
        """
        Triggered when the 'Search Flabelus Shoes' button is clicked.
        Uses RPA to fetch and display Flabelus shoe details.
        """
        # Clear previous results and display a loading message
        self.clear_layout(self.products_layout)
        notice = QLabel("Searching for Flabelus shoes with RPA... Please wait.", self)
        notice.setAlignment(Qt.AlignCenter)
        self.products_layout.addWidget(notice)

        # Perform the fixed RPA search
        success = self.rpa_handler.open_browser_and_search("Flabelus")
        if success:
            products = self.rpa_handler.fetch_products()  # Fetch the first 4 products
            self.clear_layout(self.products_layout)  # Clear loading message

            if products:
                for product_data in products:
                    self.display_product(product_data)  # Display each product
            else:
                notice.setText("No product data found.")
                self.products_layout.addWidget(notice)
        else:
            notice.setText("Failed to perform RPA search.")
            self.products_layout.addWidget(notice)

    def display_product(self, product_data):
        """
        Displays a single product's details in the UI.

        Parameters:
            product_data (dict): A dictionary containing the product's name, image path/URL, and price.
        """
        product_widget = QWidget()
        product_layout = QHBoxLayout(product_widget)

        # Product image
        product_image_label = QLabel(self)
        product_image_label.setAlignment(Qt.AlignCenter)

        image_path = product_data['image']

        if os.path.exists(image_path):  # Check if the image is a local file (RPA)
            product_image_label.setPixmap(
                QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            product_image_label.setFixedSize(200, 200)
            product_image_label.setScaledContents(True)
        elif image_path.startswith("http"):  # Check if the image is a URL (web scraper)
            try:
                image_response = requests.get(image_path)
                if image_response.status_code == 200:
                    # Create a fixed-size canvas with a white background
                    fixed_width, fixed_height = 200, 200
                    white_canvas = QImage(fixed_width, fixed_height, QImage.Format_RGB32)
                    white_canvas.fill(Qt.white)

                    # Load and scale the original image
                    original_image = QImage.fromData(image_response.content)
                    scaled_image = original_image.scaled(fixed_width, fixed_height, Qt.KeepAspectRatio,
                                                         Qt.SmoothTransformation)

                    # Center the scaled image on the canvas
                    painter = QPainter(white_canvas)
                    x_offset = (fixed_width - scaled_image.width()) // 2
                    y_offset = (fixed_height - scaled_image.height()) // 2
                    painter.drawImage(x_offset, y_offset, scaled_image)
                    painter.end()

                    # Display the image
                    product_image_label.setPixmap(QPixmap.fromImage(white_canvas))
                    product_image_label.setFixedSize(fixed_width, fixed_height)
                    product_image_label.setScaledContents(True)
            except Exception as e:
                print(f"Error loading image from URL: {e}")
                product_image_label.setText("Image not available")
        else:
            # Handle the case where the image is neither a file nor a valid URL
            product_image_label.setText("Image not available")
            product_image_label.setAlignment(Qt.AlignCenter)

        # Product details
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)

        # Product name
        product_name_label = QLabel(f"{product_data.get('name', 'No name available')}", self)
        product_name_label.setFont(QFont("Arial", 16, QFont.Bold))  # Bold, size 16
        product_name_label.setWordWrap(True)
        product_name_label.setAlignment(Qt.AlignCenter)
        details_layout.addWidget(product_name_label)

        # Product price
        product_price_label = QLabel(f"Price: {product_data.get('price', 'No price available')}", self)
        product_price_label.setFont(QFont("Arial", 14))
        product_price_label.setAlignment(Qt.AlignCenter)
        details_layout.addWidget(product_price_label)

        # Align details vertically
        container_layout = QVBoxLayout()
        container_layout.addStretch()
        container_layout.addWidget(details_widget)
        container_layout.addStretch()

        # Add image and details to product layout
        product_layout.addWidget(product_image_label)
        product_layout.addLayout(container_layout)

        # Add product widget to the results layout
        self.products_layout.addWidget(product_widget)

    def clear_layout(self, layout):
        """
        Clears all widgets from a given layout.

        Parameters:
            layout (QLayout): The layout to clear.
        """
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UIHandler()
    window.show()
    sys.exit(app.exec_())