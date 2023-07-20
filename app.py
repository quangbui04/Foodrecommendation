from flask import Flask, render_template, request, jsonify, redirect, url_for
from helper_function import recommendation_algorithm, more_recommendation

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    selected_restaurants = request.form.getlist('selectedRestaurants')
    address = str(request.form.get("address-input"))
    radius = str(request.form.get("radius-input"))
    result_recommendation, coords = recommendation_algorithm(address, radius, selected_restaurants)
    result_recommendation = list(result_recommendation.keys())[:20]
    moreRecommendations = more_recommendation(coords, selected_restaurants)
    moreRecommendations = list(moreRecommendations)[:100]
    return render_template('results.html', recommendations=result_recommendation, coords=coords, moreRecommendations=moreRecommendations)

if __name__ == '__main__':
    app.run(debug=True)
