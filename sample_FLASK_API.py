from flask import Flask, request, jsonify
import openai
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Mock data for properties
properties_data = pd.DataFrame({
    'id': [1, 2, 3],
    'description': [
        "Spacious 3-bedroom house in the suburbs with a large garden and garage.",
        "Modern 2-bedroom apartment downtown with city views.",
        "Cozy cottage in the countryside perfect for families."
    ],
    'features': [
        "3 bedrooms, garden, garage",
        "2 bedrooms, city views",
        "cottage, countryside, family-friendly"
    ]
})

# Initialize the OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

@app.route('/inquiry', methods=['POST'])
def handle_inquiry():
    data = request.json
    inquiry_text = data['inquiry']

    # Use OpenAI API to process the inquiry
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Answer this real estate inquiry: {inquiry_text}",
        max_tokens=150
    )
    return jsonify({'response': response.choices[0].text.strip()})


@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    user_profile = request.json['profile']
    vectorizer = TfidfVectorizer()

    # Mock a simple preference vector from user profile
    preference_vector = vectorizer.fit_transform([user_profile])
    property_vectors = vectorizer.transform(properties_data['features'])

    similarities = cosine_similarity(preference_vector, property_vectors)
    recommended_indices = similarities.argsort()[0][-3:]  # Top 3 recommendations

    recommendations = properties_data.iloc[recommended_indices]
    return jsonify(recommendations.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)
