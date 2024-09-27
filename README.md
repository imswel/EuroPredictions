# EuroMillions Prediction App

## Description

EuroMillions Prediction App is a Flask-based web application that generates number predictions for the EuroMillions lottery. The predictions are weighted based on the frequency of previous winning numbers and stars. The app also displays the current jackpot amount retrieved from an external source.

## Features

- Generates EuroMillions number predictions (5 numbers and 2 stars).
- Uses historical EuroMillions draw data to weight the predictions.
- Displays the current EuroMillions jackpot amount.
- User can generate new predictions by clicking a button.
- Simple and clean web interface.

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS
- **Data Source**: EuroMillions draw data (via CSV) and jackpot information (via scraping)
- **Deployment**: Render (with GitHub integration)

## Installation

### Prerequisites

Make sure you have the following installed on your machine:

- Python 3.x
- pip (Python package installer)
- Virtual environment (recommended)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/imswel/EuroPredictions.git
   cd EuroPredictions
   ```

2. Set up a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # For Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Deployment

This application is deployed using [Render](https://render.com/).

### Steps to Deploy on Render:

1. Push your local code to GitHub:

   ```bash
   git push origin main
   ```

2. Connect your Render account to your GitHub repository.

3. Set up the Render web service:

   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

4. Once deployed, you will receive a public URL for your app.

## Usage

- On loading, the app will display a prediction of 5 numbers and 2 stars.
- You can generate a new prediction by clicking the "Relancer" button.
- The current jackpot is displayed at the top of the page.

## File Structure

```
EuroPredictions/
├── app.py               # Main Flask application
├── templates/
│   └── index.html       # HTML template for the app
├── static/
│   ├── styles.css       # Custom CSS for the app
│   └── img/             # Images (e.g., stars)
├── requirements.txt     # Python dependencies
├── render.yaml          # Render configuration (optional)
└── README.md            # This file
```

## Contributing

Feel free to fork this repository and submit pull requests to suggest improvements or new features.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

```

```
