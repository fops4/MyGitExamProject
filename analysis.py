import pandas as pd
import os

class BookAnalysis:
    def __init__(self, csv_filename):
        self.csv_filename = csv_filename
        self.df = None

    def load_data(self):
        """Charge le fichier CSV en DataFrame."""
        if not os.path.exists(self.csv_filename):
            print(f"❌ Erreur : Le fichier {self.csv_filename} est introuvable. Exécutez d'abord scrape.py.")
            return False
        
        self.df = pd.read_csv(self.csv_filename)
        print("\n📊 Aperçu des données :")
        print(self.df.head())
        return True

    def clean_data(self):
        """Nettoie et convertit les données."""
        if self.df is None:
            return
        
        # Conversion du prix en float
        try:
            self.df["price"] = self.df["price"].astype(float)
        except ValueError:
            print("⚠️ Erreur de conversion des prix.")

        # Conversion de la note en entier
        if "rating" in self.df.columns:
            try:
                self.df["rating"] = self.df["rating"].astype(int)
            except ValueError:
                print("⚠️ Erreur de conversion des notes.")

    def compute_statistics(self):
        """Affiche les statistiques sur les prix."""
        if self.df is None:
            return
        
        avg_price = self.df["price"].mean()
        print(f"\n💰 Prix moyen des livres : {avg_price:.2f} £")

        # Livres à moins de 20 £
        df_under_20 = self.df[self.df["price"] < 20]
        print(f"\n📉 Livres à moins de 20  : {len(df_under_20)}")
        print(df_under_20[["title", "price"]].head())

    def save_cleaned_data(self, output_filename="data/books_cleaned.csv"):
        """Sauvegarde les données nettoyées."""
        if self.df is None:
            return
        
        self.df.to_csv(output_filename, index=False)
        print(f"\n✅ Données nettoyées enregistrées dans {output_filename}")

    def run(self):
        """Exécute toutes les étapes."""
        if self.load_data():
            self.clean_data()
            self.compute_statistics()
            self.save_cleaned_data()

# Exécuter l'analyse
if __name__ == "__main__":
    analyzer = BookAnalysis("data/books.csv")
    analyzer.run()
