from flask import Flask, render_template, request, jsonify
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import io

# Download NLTK data (if not already downloaded)
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')
    nltk.download('wordnet')

app = Flask(__name__)

# --- Global variables for model and vectorizer ---
vectorizer = TfidfVectorizer(max_features=2000, min_df=5, max_df=0.8, stop_words=stopwords.words('english'))
model = SVC(kernel='rbf', gamma=1, probability=True)
is_model_trained = False

# --- Text preprocessing functions from your notebook ---
def clean(text):
    text = re.sub("\\'", "", text)
    text = re.sub("[^a-zA-Z]"," ",text)
    text = ' '.join(text.split())
    text = text.lower()
    return text

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)

lemmatizer = WordNetLemmatizer()
def lemmatize_words(text):
    return " ".join([lemmatizer.lemmatize(word) for word in text.split()])

# --- Function to train the model ---
def train_model():
    global vectorizer, model, is_model_trained
    try:
        books = pd.read_csv('BooksDataSet.csv')
        books = pd.DataFrame(books,columns=['book_id','book_name','genre','summary'])
        books.loc[:,'summary'] = books.loc[:,'summary'].apply(lambda x: clean(x))
        books['summary'] = books['summary'].apply(lambda x: remove_stopwords(x))
        books['summary'] = books['summary'].apply(lambda x: lemmatize_words(x))

        X = books['summary']
        y = books['genre']

        X_tfidf = vectorizer.fit_transform(X).toarray()
        model.fit(X_tfidf, y)
        is_model_trained = True
        print("Model trained successfully!")
    except Exception as e:
        print(f"Error training model: {e}")

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not is_model_trained:
        return jsonify({'error': 'Model is not trained yet. Please wait.'}), 503

    try:
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            if file and file.filename.endswith('.csv'):
                df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
                if 'summary' not in df.columns:
                    return jsonify({'error': 'CSV file must contain a "summary" column.'}), 400

                summaries = df['summary'].tolist()
                predictions = []
                for summary in summaries:
                    processed_summary = lemmatize_words(remove_stopwords(clean(summary)))
                    summary_tfidf = vectorizer.transform([processed_summary]).toarray()
                    prediction = model.predict(summary_tfidf)[0]
                    predictions.append({'summary': summary, 'genre': prediction})
                return jsonify({'predictions': predictions})
            else:
                return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400

        elif 'summary' in request.form:
            summary = request.form['summary']
            if not summary.strip():
                return jsonify({'error': 'Summary text cannot be empty.'}), 400
            
            processed_summary = lemmatize_words(remove_stopwords(clean(summary)))
            summary_tfidf = vectorizer.transform([processed_summary]).toarray()
            prediction = model.predict(summary_tfidf)[0]
            return jsonify({'prediction': prediction})
        else:
            return jsonify({'error': 'No file or summary provided.'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    train_model()
    app.run(debug=True)