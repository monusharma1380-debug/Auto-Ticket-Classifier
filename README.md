# Support Ticket Auto-Classifier

This is a project I built to learn how to apply machine learning to a real,
practical problem instead of just following tutorials. It takes customer
support tickets and predicts their category (like Billing, Technical Support,
etc.) and priority (High, Medium, Low), so that tickets can be routed to the
right team automatically instead of someone sorting them by hand.

## Why I built this

I wanted to actually learn scikit-learn hands-on, not just read about it. So
instead of using an LLM API to do the classification, I trained my own model
from scratch: cleaning real data, dealing with class imbalance, comparing
different approaches, and understanding why each step is needed instead of
copying code I didn't understand.

## What it does

- Takes a batch of tickets (CSV, Excel, or JSON) as input
- Predicts a category and a priority for each ticket using a trained model
- Suggests which team the ticket should be routed to
- Shows the results in a simple dashboard (table + summary counts)
- Has a separate welcome page before the main tool

## Tech stack

- Python
- Flask (backend, serves the web pages and the prediction endpoint)
- scikit-learn (TF-IDF vectorizer + ComplementNB classifier)
- pandas (reading and processing the uploaded files)
- HTML/CSS/JavaScript (frontend, no framework)

No external AI API is used. The model runs locally once trained.

## Dataset

Trained on the "Multilingual Customer Support Tickets" dataset from Kaggle
(Tobias Bueck), filtered to English-only tickets (about 16,000 rows). Each
ticket has a subject, body, category (queue), and priority label already
provided in the dataset.

## How the model works

1. Ticket text (subject + body) is converted into numeric features using
   TF-IDF (term frequency, weighted by how rare/common a word is across the
   dataset).
2. A ComplementNB classifier (a Naive Bayes variant meant for imbalanced text
   data) is trained on these features, separately for category and for
   priority.
3. When a new ticket comes in, the same fitted vectorizer transforms it, and
   the trained model predicts category and priority.

## Known limitations

- The dataset is imbalanced (some categories have far more examples than
  others), which biases predictions toward the more common categories. I
  tried undersampling the larger categories to reduce this, which helped the
  smaller categories but slightly reduced accuracy on the larger ones. This
  is a real trade-off, not a bug.
- The model matches on words and patterns, not meaning. Two tickets that mean
  the same thing but are worded very differently (a short informal message
  vs. a formal, detailed one) can get different predictions.
- Category and priority are predicted independently and don't affect each
  other.

## Project structure

```
Ticket_classifer/
├── app.py                     Flask app (routes)
├── main.py                    Training script (loads data, trains, saves models)
├── category_model.pkl
├── category_vectorizer.pkl
├── priority_model.pkl
├── priority_vectorizer.pkl
├── utils/
│   └── classify.py            Loads saved models, runs predictions
├── templates/
│   ├── welcome.html
│   └── index.html
├── static/
│   ├── welcome.css
│   ├── style.css
│   └── script.js
└── requirements.txt
```

## Running it locally

```
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000` in a browser. The welcome page has a
"Get Started" button that goes to the actual tool.

To retrain the model yourself, run `main.py` (it downloads the dataset via
kagglehub, so a Kaggle account with an API token set up is needed).

## What I'd improve next

- Better handling of class imbalance (trying SMOTE instead of plain
  undersampling)
- A dashboard with actual charts (matplotlib/seaborn) instead of just counts
- Deploying it so it's not just local
