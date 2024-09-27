import csv
import random
from collections import Counter
import requests
from io import StringIO
from flask import Flask, render_template, request
import locale
import os  # Importer le module os

app = Flask(__name__)

# Configurer la locale pour le formatage
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')  # Utilisez 'fr_FR.UTF-8' pour le format français

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
    url = "https://www.euro-millions.com/fr/"
    response = requests.get(url)
    jackpot_text = response.text.split('<div class="jackpot">')[1].split('</div>')[0]
    
    # Nettoyer le texte pour obtenir uniquement la valeur numérique
    jackpot_value_str = jackpot_text.replace('millions', '').replace('&euro;', '').replace(' ', '').strip()
    
    # Convertir en entier
    try:
        jackpot_value = int(jackpot_value_str) * 1_000_000
    except ValueError:
        jackpot_value = 0  # Valeur par défaut en cas d'erreur

    # Formater le jackpot
    formatted_jackpot = locale.format_string("%d", jackpot_value, grouping=True) + " €"
    
    return formatted_jackpot

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
