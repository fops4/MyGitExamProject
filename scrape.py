import os
import requests
from bs4 import BeautifulSoup
import csv

# URL de départ
BASE_URL = "http://books.toscrape.com/catalogue/"
START_URL = "http://books.toscrape.com/catalogue/page-1.html"

class BookScraper:
    def __init__(self, start_url, base_url):
        self.start_url = start_url
        self.base_url = base_url
        self.books_data = []

    def fetch_page(self, url):
        """Récupère le contenu HTML d'une page."""
        response = requests.get(url)
        response.encoding = "utf-8"  # ✅ Forcer l'encodage UTF-8
        
        if response.status_code != 200:
            print(f"❌ Erreur lors de la récupération de la page : {url}")
            return None
        return BeautifulSoup(response.text, 'html.parser')

    def extract_book_data(self, book):
        """Extrait les informations d'un livre."""
        title = book.h3.a["title"]
        
        # Extraction du prix et conversion en float
        price_text = book.select_one(".price_color").text.strip()
        price = float(price_text.replace("£", "").strip())

        # Disponibilité
        stock_info = book.select_one(".availability").text.strip()

        # Note (convertir en nombre)
        rating_classes = book.select_one(".star-rating")["class"]
        rating = rating_classes[1]  # "Three", "Five", etc.
        rating_mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        rating = rating_mapping.get(rating, 0)  # Convertir en entier

        return {
            "title": title,
            "price": price,
            "stock": stock_info,
            "rating": rating
        }

    def scrape_page(self, url):
        """Scrape une page et extrait les livres."""
        soup = self.fetch_page(url)
        if not soup:
            return

        books = soup.select("article.product_pod")
        for book in books:
            book_data = self.extract_book_data(book)
            self.books_data.append(book_data)

        # Vérifier s'il y a une page suivante
        next_button = soup.select_one(".next a")
        if next_button:
            next_page_url = self.base_url + next_button["href"]
            print(f"🔄 Scraping page suivante : {next_page_url}")
            self.scrape_page(next_page_url)  # Récursion

    def save_to_csv(self, filename="data/books.csv"):
        """Sauvegarde les données en fichier CSV."""
        if not os.path.exists("data"):
            os.makedirs("data")

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "price", "stock", "rating"])
            writer.writeheader()
            writer.writerows(self.books_data)

        print(f"✅ Scraping terminé ! {len(self.books_data)} livres enregistrés dans {filename}")

    def run(self):
        """Lance le scraping et sauvegarde les données."""
        print("🚀 Démarrage du scraping...")
        self.scrape_page(self.start_url)
        self.save_to_csv()

# Exécuter le scraper
if __name__ == "__main__":
    scraper = BookScraper(START_URL, BASE_URL)
    scraper.run()
