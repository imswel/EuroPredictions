import csv
import random
from collections import Counter
import requests
from io import StringIO
from flask import Flask, render_template, request
import os
from bs4 import BeautifulSoup  # Assurez-vous d'importer BeautifulSoup

app = Flask(__name__)

# Télécharger et lire le fichier CSV des tirages Euromillions
def fetch_data():
    url = "https://www.loterieplus.com/euromillions/services/telechargement-acces.php"
    response = requests.get(url)
    csv_data = StringIO(response.text)
    reader = csv.reader(csv_data, delimiter=';')

    # Sauter l'en-tête (la première ligne)
    next(reader)

    # Variables pour stocker les tirages
    numbers_draws = []
    stars_draws = []

    # Lire les tirages depuis le CSV
    for row in reader:
        if row[3] and row[4] and row[5] and row[6] and row[7]:  # Vérifier que les numéros existent
            try:
                # Ajouter les 5 numéros et les 2 étoiles à leur liste respective
                numbers_draws.extend(map(int, row[3:8]))  # Les 5 premiers numéros (N1 à N5)
                stars_draws.extend(map(int, row[8:10]))  # Les 2 étoiles (E1 et E2)
            except ValueError:
                pass  # Ignorer les lignes qui ne peuvent pas être converties correctement

    return numbers_draws, stars_draws

# Calculer les poids
def calculate_weights(numbers_draws, stars_draws):
    count_numbers = Counter(numbers_draws)
    count_stars = Counter(stars_draws)

    average_numbers = len(numbers_draws) / 50
    average_stars = len(stars_draws) / 12

    def get_weights(count, total, average):
        weights = []
        for i in range(1, total + 1):
            frequency = count.get(i, 0)  # Obtenir la fréquence du numéro ou étoile
            if frequency < average:
                weights.append(average / frequency)  # Plus de poids si sous la moyenne
            else:
                weights.append(1 / (frequency / average))  # Moins de poids si au-dessus de la moyenne
        return weights

    weights_numbers = get_weights(count_numbers, 50, average_numbers)
    weights_stars = get_weights(count_stars, 12, average_stars)

    return weights_numbers, weights_stars

# Tirage de numéros et étoiles
def draw_numbers_and_stars(weights_numbers, weights_stars):
    numbers = random.choices(range(1, 51), weights=weights_numbers, k=10)  # Tirer 10 numéros pour permettre des duplications
    unique_numbers = sorted(set(numbers))  # Obtenir des numéros uniques

    if len(unique_numbers) < 5:
        # Si on a moins de 5 numéros uniques, compléter avec des numéros aléatoires
        while len(unique_numbers) < 5:
            new_number = random.randint(1, 50)
            if new_number not in unique_numbers:
                unique_numbers.append(new_number)
        
    stars = random.sample(range(1, 13), 2)  # Tirer 2 étoiles uniques
    return unique_numbers[:5], sorted(set(stars))  # Assurer qu'on retourne 5 numéros et 2 étoiles

# Récupérer le montant du jackpot
def get_jackpot():
    url = "https://apim.prd.natlot.be/api/v4/draw-games/draws?next-draws=0&status=OPEN"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Origin": "https://www.loterie-nationale.be",
        "Connection": "keep-alive",
        "Referer": "https://www.loterie-nationale.be/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        for draw in data.get("draws", []):
            if draw["gameName"] == "Euro Millions":
                jackpot = draw["jackpots"][0]["amount"]
                # Enlever les centimes
                formatted_jackpot = int(jackpot / 100)
                # Formater le jackpot pour qu'il soit lisible
                return "{:,.0f} €".format(formatted_jackpot).replace(",", " ")
    else:
        print("Erreur lors de la récupération des données")
        return "Erreur lors de la récupération des données"

@app.route('/', methods=['GET', 'POST'])
def index():
    jackpot = get_jackpot()
    numbers_draws, stars_draws = fetch_data()
    weights_numbers, weights_stars = calculate_weights(numbers_draws, stars_draws)
    numbers, stars = draw_numbers_and_stars(weights_numbers, weights_stars)

    if request.method == 'POST':
        # Effectuer un nouveau tirage
        numbers, stars = draw_numbers_and_stars(weights_numbers, weights_stars)

    return render_template('index.html', jackpot=jackpot, numbers=numbers, stars=stars)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
