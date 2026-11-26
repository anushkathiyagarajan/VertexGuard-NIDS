# VertexGuard

VertexGuard is a Flask-based network intrusion detection demo. It uses a trained
Random Forest model to classify rows in an uploaded CSV as normal traffic or an
attack, then displays a dashboard with traffic totals, confidence, feature
importance, and detection logs. A PDF report can also be downloaded.

## Requirements

- Python 3
- The project model file, `ids_model.pkl`

Install the Python dependencies from the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install Flask pandas joblib scikit-learn reportlab
```

## Run the application

From the project directory, start the Flask server:

```powershell
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser. The demo login
credentials currently defined in the app are:

- Username: `admin`
- Password: `admin`

Upload a CSV file on the detection page. The dashboard shows predictions and
provides a **Download Security Report** button. Chart.js is loaded from a CDN,
so an internet connection is needed to display the charts.

## Training the model

The app loads `ids_model.pkl` when it starts. To create or retrain that model,
place the UNSW-NB15 training CSV at
`dataset/UNSW_NB15_training-set.csv`, install the dependencies above, then run:

```powershell
python train.py
```

The script saves the trained model as `ids_model.pkl`. The `dataset/` directory
is ignored by Git, so obtain the dataset separately and keep it in that local
path when training.

## Project files

- `app.py` — Flask routes, CSV prediction, alerts, and PDF report generation
- `train.py` — Random Forest training script
- `ids_model.pkl` — model loaded by the application
- `templates/` and `static/` — HTML pages and front-end assets
- `dataset/` — local training data; not committed to Git
- `logs/` — generated alerts and PDF reports; not committed to Git

## Security note

This is a demo application, not production-ready. It uses hard-coded login
credentials and runs Flask with debug mode enabled. Do not expose it publicly
without addressing those settings and adding appropriate security controls.
