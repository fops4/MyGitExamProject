import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class BookVisualization:
    def __init__(self, csv_filename):
        self.csv_filename = csv_filename
        self.df = None

    def load_data(self):
        """Charge le fichier CSV nettoyé en DataFrame."""
        if not os.path.exists(self.csv_filename):
            print(f"❌ Erreur : Le fichier {self.csv_filename} est introuvable. Exécutez d'abord scrape.py et analysis.py.")
            return False
        
        self.df = pd.read_csv(self.csv_filename)
        print("\n📊 Aperçu des données :")
        print(self.df.head())
        return True

    def plot_price_distribution(self):
        """Crée l'histogramme de la distribution des prix."""
        plt.figure(figsize=(8, 5))
        sns.histplot(self.df["price"], bins=10, kde=True, color="skyblue")
        plt.xlabel("Prix (£)")
        plt.ylabel("Nombre de livres")
        plt.title("Distribution des prix des livres")
        plt.savefig("static/price_distribution.png")
        print("✅ Histogramme des prix sauvegardé : static/price_distribution.png")

    def plot_rating_distribution(self):
        """Crée le countplot de la répartition des notes."""
        plt.figure(figsize=(8, 5))
        sns.countplot(x=self.df["rating"], palette="viridis")
        plt.xlabel("Note (étoiles)")
        plt.ylabel("Nombre de livres")
        plt.title("Répartition des notes des livres")
        plt.savefig("static/rating_distribution.png")
        print("✅ Countplot des notes sauvegardé : static/rating_distribution.png")

    def plot_stock_distribution(self):
        """Crée un bar chart pour la répartition des stocks."""
        plt.figure(figsize=(8, 5))
        stock_counts = self.df["stock"].value_counts().head(10)  # Top 10 stocks différents
        sns.barplot(x=stock_counts.index, y=stock_counts.values, palette="magma")
        plt.xlabel("Disponibilité")
        plt.ylabel("Nombre de livres")
        plt.title("Répartition des stocks des livres")
        plt.xticks(rotation=45)
        plt.savefig("static/stock_distribution.png")
        print("✅ Bar chart du stock sauvegardé : static/stock_distribution.png")

    def run(self):
        """Exécute toutes les étapes de visualisation."""
        if self.load_data():
            self.plot_price_distribution()
            self.plot_rating_distribution()
            self.plot_stock_distribution()
            print("\n🎨 Visualisation terminée avec succès !")

# Exécuter la visualisation
if __name__ == "__main__":
    visualizer = BookVisualization("data/books_cleaned.csv")
    visualizer.run()
