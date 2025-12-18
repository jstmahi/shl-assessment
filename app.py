import os
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

if os.path.exists("shl_products.csv"):
    df = pd.read_csv("shl_products.csv")
else:
    df = pd.DataFrame([{
        "name": "Python Test", 
        "url": "https://example.com", 
        "description": "Python coding test", 
        "duration": 30, 
        "test_type": "['Knowledge & Skills']",
        "adaptive_support": "No",
        "remote_support": "Yes"
    }])

df['description'] = df['description'].fillna('')
df['content'] = df['name'] + " " + df['description']

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['content'])

@app.route('/')
def home():
    return "SHL Recommendation Engine is Live!"

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({"error": "Query is required"}), 400

        query_vec = vectorizer.transform([query])
        cosine_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()
        
        top_n = min(5, len(df))
        top_indices = cosine_sim.argsort()[-top_n:][::-1]
        
        recommendations = []
        for idx in top_indices:
            row = df.iloc[idx]
            rec = {
                "url": row['url'],
                "name": row['name'],
                "adaptive_support": str(row['adaptive_support']),
                "description": str(row['description'])[:300] + "...",
                "duration": int(row['duration']) if pd.notnull(row['duration']) else 30,
                "remote_support": str(row['remote_support']),
                "test_type": eval(row['test_type']) if isinstance(row['test_type'], str) and row['test_type'].startswith('[') else ["Knowledge & Skills"]
            }
            recommendations.append(rec)
            
        return jsonify({"recommended_assessments": recommendations}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
