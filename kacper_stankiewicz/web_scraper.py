import re
import requests
from bs4 import BeautifulSoup


class WebScrapper:
    """
    A class for scraping product details (name, image, price) from Amazon search results.
    """

    def __init__(self):
        """
        Initializes the WebScrapper with the base URL and headers.
        """
        self.base_url = "https://www.amazon.es/s"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def fetch_search_results(self, query):
        """
        Fetches the HTML content of the Amazon search results page for the given query.

        Parameters:
            query (str): The search term.

        Returns:
            str: HTML content of the search results page, or an empty string on failure.
        """
        params = {"k": query}  # Query parameter for the search

        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()

            return response.text

        except requests.exceptions.Timeout:
            print("Request timed out. Please check your network connection.")

        except requests.exceptions.TooManyRedirects:
            print("Too many redirects. Check the URL and try again.")

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch Amazon page: {e}")

        return ""

    def parse_products(self, html_content, max_results=10):
        """
        Parses the HTML content to extract product details.

        Parameters:
            html_content (str): HTML content of the search results page.
            max_results (int): Maximum number of products to extract.

        Returns:
            list: A list of dictionaries with product details (name, image, price).
        """
        if not html_content:
            print("No HTML content provided for parsing.")
            return []

        try:
            soup = BeautifulSoup(html_content, "html.parser")
            product_elements = soup.select(".s-main-slot .s-result-item")

        except Exception as e:
            print(f"Error while parsing product elements: {e}")
            return []

        products = []

        for product_element in product_elements:
            try:
                # Extract product details using helper methods
                product_html = str(product_element)

                product_image = self._extract_image(product_html)
                product_name = self._extract_name(product_html)
                product_price = self.extract_price(product_element)

                # Validate and add product to the list
                if self._is_valid_product(product_name, product_image, product_price):
                    products.append({
                        "name": product_name,
                        "image": product_image,
                        "price": product_price,
                    })

                # Stop collecting after reaching the max results limit
                if len(products) >= max_results:
                    break

            except Exception as e:
                print(f"Error processing product: {e}")
                continue

        if not products:
            print("No valid products found.")

        return products

    # This helper method is intended for internal use within the class.
    # It uses RegEx to extract a specific value from the provided text.
    # Since it doesn't rely on self or instance-specific data, it's defined as static.
    @staticmethod
    def _extract_with_regex(pattern, text):
        """
        Extracts a value from text using the provided RegEx pattern.

        Parameters:
            pattern (str): RegEx pattern to match.
            text (str): The text to search.

        Returns:
            str: Matched value, or an empty string if no match is found.
        """
        try:
            match = re.search(pattern, text)
            return match.group(1) if match else ""

        except re.error as e:
            print(f"RegEx error: {e}")
            return ""

    # This helper method is intended for internal use within the class.
    # It extracts the product image URL using RegEx.
    def _extract_image(self, product_html):
        """
        Extracts the product image URL using RegEx.

        Parameters:
            product_html (str): HTML content of a single product.

        Returns:
            str: Image URL, or an empty string if not found.
        """
        return self._extract_with_regex(r'<img.*?src="(.*?)"', product_html)

    # This helper method is intended for internal use within the class.
    # It extracts the product name using RegEx.
    def _extract_name(self, product_html):
        """
        Extracts the product name using RegEx.

        Parameters:
            product_html (str): HTML content of a single product.

        Returns:
            str: Product name, or an empty string if not found.
        """
        return self._extract_with_regex(r'<img.*?alt="(.*?)"', product_html)

    # This helper method is intended for internal use within the class.
    # It extracts the product price using BeautifulSoup and RegEx.
    def extract_price(self, product_element):
        """
        Extracts the product price using BeautifulSoup and RegEx.

        Parameters:
            product_element (bs4.element.Tag): A BeautifulSoup element for a single product.

        Returns:
            str: Product price with the currency symbol, or an empty string if not found.
        """
        price_tag = product_element.select_one(".a-price")

        if not price_tag:
            return ""

        try:
            price_text = price_tag.get_text()  # Extract price text
            return self._extract_with_regex(r"(\d+[.,]?\d*)[€]?", price_text) + "€"

        except Exception as e:
            print(f"Error extracting price: {e}")
            return ""

    # This helper method is intended for internal use within the class.
    # It validates a product by ensuring all necessary fields are present.
    # Since it doesn't rely on self or instance-specific data, it's defined as static.
    @staticmethod
    def _is_valid_product(product_name, product_image, product_price):
        """
        Validates a product by ensuring it has all required fields and is not a sponsored ad.

        Parameters:
            product_name (str): Product name.
            product_image (str): Product image URL.
            product_price (str): Product price.

        Returns:
            bool: True if the product is valid, False otherwise.
        """
        return (
            bool(product_name.strip()) and
            bool(product_image.strip()) and
            bool(product_price.strip()) and
            "Anuncio patrocinado" not in product_name
        )