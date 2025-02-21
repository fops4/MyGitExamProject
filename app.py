from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Charger le fichier CSV nettoyé
csv_filename = "data/books_cleaned.csv"

# Nombre de livres par page
BOOKS_PER_PAGE = 50

@app.route("/")
def index():
    try:
        # Charger les données
        df = pd.read_csv(csv_filename)

        # Récupérer le numéro de page depuis l'URL, défaut à 1
        page = int(request.args.get("page", 1))

        # Calculer le début et la fin des indices pour les livres à afficher
        start_idx = (page - 1) * BOOKS_PER_PAGE
        end_idx = start_idx + BOOKS_PER_PAGE

        # Extraire les livres de la page courante
        books_page = df.iloc[start_idx:end_idx]

        # Convertir le DataFrame en HTML
        table_html = books_page.to_html(classes="table table-striped", index=False)

        # Nombre total de pages
        total_pages = len(df) // BOOKS_PER_PAGE + (1 if len(df) % BOOKS_PER_PAGE else 0)

        return render_template("index.html", table_html=table_html, page=page, total_pages=total_pages)

    except FileNotFoundError:
        return "<h1>❌ Erreur : Fichier books_cleaned.csv introuvable !</h1><p>Veuillez exécuter scrape.py et analysis.py.</p>"

if __name__ == "__main__":
    app.run(debug=True)
