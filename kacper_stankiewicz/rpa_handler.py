import logging
import webbrowser
import pytesseract
import pyautogui
import time
import os


class RPAHandler:
    """
    A class to handle RPA-based automation for interacting with the Amazon website.
    This includes opening the browser, searching for a product, and capturing
    details (name, price, and image) of the first 4 visible products.
    """

    def __init__(self):
        """
        Initializes the RPAHandler with essential configurations.
        """
        self.base_url = "https://www.amazon.es"
        self.search_box_image = "search_box.png"  # Image of the search box
        self.search_button_image = "search_button.png"  # Image of the search button
        self.screenshots_folder = "screenshots"  # Folder to save captured screenshots

        # Create the screenshots folder if it doesn't exist
        os.makedirs(self.screenshots_folder, exist_ok=True)

        # Fixed coordinates for the first 4 product regions
        self.product_regions = [
            (545, 712, 1020, 1589),  # First product
            (1046, 700, 1521, 1577),  # Second product
            (1547, 700, 2022, 1577),  # Third product
            (2048, 698, 2523, 1575),  # Fourth product
        ]

    def open_browser_and_search(self, query):
        """
        Opens the browser, navigates to Amazon, and performs a search.

        Parameters:
            query (str): The search term.

        Returns:
            bool: True if the search was successful, False otherwise.
        """
        try:
            # Open Amazon in the default web browser
            webbrowser.open(self.base_url)
            time.sleep(5)  # Allow the browser to load

            # Locate and interact with the search box
            if not self._find_and_click(self.search_box_image):
                logging.error("Search box not found.")
                return False

            # Type the query in the search box
            pyautogui.typewrite(query, interval=0.1)

            # Click the search button
            if not self._find_and_click(self.search_button_image):
                logging.error("Search button not found.")
                return False

            time.sleep(5)  # Wait for search results to load
            return True

        except Exception as e:
            print(f"Error during browser interaction: {e}")
            return False

    def _find_and_click(self, image_path, confidence=0.7, delay=2, scaling_factor=2):
        """
        Locate and click on a UI element using an image reference.

        Parameters:
            image_path (str): Path to the reference image to locate on the screen.
            confidence (float): Matching confidence level for locating the image (default: 0.7).
            delay (int): Time in seconds to wait after clicking (default: 2 seconds).
            scaling_factor (int): Factor to adjust for screen scaling.
                                  Use 1 for devices with 100% zoom.
                                  Use 2 or higher for higher scaling or resolution.

        Returns:
            bool: True if the element is located and clicked, False otherwise.
        """
        try:
            for attempt in range(3):  # Try up to 3 times
                # Locate the center of the image on the screen
                location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
                if location:
                    # Adjust coordinates by the scaling factor
                    scaled_x = location.x / scaling_factor
                    scaled_y = location.y / scaling_factor

                    # Move to the adjusted coordinates and click
                    pyautogui.moveTo(scaled_x, scaled_y, duration=0.5)
                    pyautogui.click()

                    # Wait after the click to ensure the UI responds
                    time.sleep(delay)
                    return True

            # Return False if the image could not be located after 3 attempts
            return False

        except Exception as e:
            print(f"Exception during _find_and_click for {image_path}: {e}")
            return False

    def fetch_products(self):
        """
        Captures data (image, name, price) for the first four visible products.

        Returns:
            list: A list of dictionaries containing product details.
        """
        products = []

        try:
            pyautogui.scroll(-8)

            # Take a screenshot of the visible browser area
            screenshot = pyautogui.screenshot()

            for index, region in enumerate(self.product_regions):
                try:
                    # Crop the region for the specific product
                    cropped_product = screenshot.crop(region)
                    cropped_image_path = os.path.join(
                        self.screenshots_folder, f"product_{index + 1}_full.png"
                    )
                    cropped_product.save(cropped_image_path)
                    print(f"Saved full product screenshot {index + 1} to {cropped_image_path}")

                    # Define sub-regions for the product image, name, and price
                    width, height = cropped_product.size
                    image_region = (0, 0, width, height // 2)  # Top half for the image
                    name_region = (0, height // 2, width, (3 * height) // 4)  # Middle for name
                    price_region = (0, (3 * height) // 4, width, height)  # Bottom for price

                    # Process and save the product image
                    cropped_image = cropped_product.crop(image_region)
                    cropped_image_path = os.path.join(
                        self.screenshots_folder, f"product_{index + 1}_image.png"
                    )
                    cropped_image.save(cropped_image_path)

                    # Extract product name using OCR
                    cropped_name = cropped_product.crop(name_region)
                    # Preparing the cropped image for the OCR engine to extract text:
                    ocr_product_name_data = pytesseract.image_to_data(
                        cropped_name, output_type=pytesseract.Output.DICT
                    )
                    product_name = self._extract_name_from_ocr_data(ocr_product_name_data)

                    # Extract product price using OCR
                    cropped_price = cropped_product.crop(price_region)
                    # Preparing the cropped image for the OCR engine to extract text:
                    ocr_product_price_data = pytesseract.image_to_data(
                        cropped_price, output_type=pytesseract.Output.DICT
                    )
                    product_price = self._extract_price_from_ocr_data(ocr_product_price_data)

                    # Append the product data to the list
                    products.append({
                        "name": product_name,
                        "price": product_price,
                        "image": cropped_image_path,
                    })

                    print(f"Product {index + 1}: Name = {product_name}, Price = {product_price}")

                except Exception as product_error:
                    print(f"Error processing product {index + 1}: {product_error}")

            return products

        except Exception as e:
            print(f"Error fetching products: {e}")
            return products

    # This helper method is intended for internal use within the class.
    # It processes OCR data to extract the product name.
    # Since it doesn't rely on self or instance-specific data, it's defined as static.
    @staticmethod
    def _extract_name_from_ocr_data(ocr_data):
        """
        Extracts the product name from OCR data.

        Parameters:
            ocr_data (dict): OCR data containing recognized text.

        Returns:
            str: The extracted product name or 'N/A' if not found.
        """
        try:
            # Extract non-empty lines of text recognized by OCR
            name_lines = [
                ocr_data["text"][i].strip()  # Remove extra spaces
                for i in range(len(ocr_data["text"]))  # Iterate through all detected text
                if ocr_data["text"][i].strip()  # Include only non-empty text
            ]

            # Combine the first two lines into a single string for the product name
            # Limiting it to the first two lines ensures consistency and avoids unnecessary extra lines.
            return " ".join(name_lines[:2])
        except Exception as e:
            # Log any errors and return "N/A" as the fallback
            print(f"Error extracting name: {e}")
            return "N/A"

    # This helper method is intended for internal use within the class.
    # It processes OCR data to extract the product price.
    # Since it doesn't rely on self or instance-specific data, it's defined as static.
    @staticmethod
    def _extract_price_from_ocr_data(ocr_data):
        """
        Extracts the product price from OCR data.

        Parameters:
            ocr_data (dict): OCR data containing recognized text.

        Returns:
            str: The extracted product price or 'N/A' if not found.
        """
        try:
            # Iterate through all recognized text in the OCR data
            for i, text in enumerate(ocr_data["text"]):
                # Check if the text contains the Euro symbol (€), indicating a price
                if "€" in text:
                    return text.strip()  # Return the price with extra spaces removed

            # If no price is found, return "N/A" as a fallback
            return "N/A"

        except Exception as e:
            # Log any errors encountered during the extraction process
            print(f"Error extracting price: {e}")
            return "N/A"