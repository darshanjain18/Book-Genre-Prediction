# Book Genre Classifier 📚

A Natural Language Processing (NLP) web application that predicts the genre of a book based on its summary. Built using Flask and Scikit-Learn.

## 🚀 Features
* **Single Prediction:** Paste a book summary to get the predicted genre instantly.
* **Batch Prediction:** Upload a `.csv` file containing multiple summaries for bulk classification.
* **ML Model:** Uses **Support Vector Machine (SVM)** with an RBF kernel and **TF-IDF Vectorization**.

## 🛠️ Project Structure
* `app.py`: Flask backend and ML inference logic.
* `BooksDataSet.csv`: Dataset containing 6 genres (Crime, Fantasy, Historical, Horror, Sci-Fi, Thriller).
* `nlp_final_report.pdf`: Detailed documentation of the project.
* `requirements.txt`: Necessary Python libraries.

## 💻 Tech Stack
* **Language:** Python
* **NLP:** NLTK (Stopword removal, Lemmatization)
* **ML:** Scikit-learn (SVM, TF-IDF)
* **Web:** Flask, HTML/CSS

## 📸 Screenshots
### Homepage (Input/Upload)
<img width="1920" height="1020" alt="Screenshot 2026-02-14 143042" src="https://github.com/user-attachments/assets/06ef85a3-bc26-4d84-8378-5f5d4f47200d" />
<img width="1920" height="1020" alt="Screenshot 2026-02-14 143054" src="https://github.com/user-attachments/assets/067887e3-87bd-4d4f-b216-cf490a1c75b8" />

### Genre Prediction Result
<img width="1920" height="1020" alt="Screenshot 2026-02-14 143224" src="https://github.com/user-attachments/assets/13f40cdc-d974-4b9c-8ac0-c5c9c5cd4b2a" />
