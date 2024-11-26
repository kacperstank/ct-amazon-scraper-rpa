# CT Scraper and RPA Comparison Project

This repository contains the **CT Scraper and RPA Project**, developed to compare two methods for extracting product data from a web page: **RPA** and **Web Scraping** with **RegEx**. The project focuses on demonstrating the strengths and limitations of each approach while extracting data from the [Amazon.es](https://www.amazon.es/) website.

## Project Objective

The goal of this project is to extract a list of products from [Amazon.es](https://www.amazon.es/) for a given search term. Each product includes:
- **Image**
- **Name** (as visible on the main search results page)
- **Price** (in Euros, as displayed on the main search results page)

The extracted data is displayed in a simple graphical user interface (GUI) using **PyQt5**.

---

## Methods Compared

### 1. **RPA (Robotic Process Automation)**
- Utilizes the **PyAutoGUI** library to automate browser interactions.

### 2. **Web Scraping**
- Makes direct HTTP requests to the Amazon search results page.

---

## Key Features

- **Product Extraction**: Fetches up to 10-20 products (or as displayed on the page) per query.
- **GUI Integration**: Displays the extracted product information (image, name, and price) in a graphical interface.
- **Technology Comparison**:
  - **RPA**: Highlights the challenges of working with dynamic websites and the reliance on OCR.
  - **Scraping**: Demonstrates how structured data can be efficiently extracted using HTML parsing and RegEx.

---

## Acknowledgments

We extend our gratitude to **CT Engineering Group** for providing this learning opportunity.

---

## Authors

- **Kacper Stankiewicz**
- **Miguel Mora**

Thank you to **CT Engineering Group** for the opportunity to develop and compare these technologies.
