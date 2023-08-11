# GiveMeFood - Food Recommendation Web App

Welcome to GiveMeFood, your personalized food recommendation web app powered by Python and the Flask framework. With this app, you can discover the best restaurants based on your preferences and location. Simply input your address, preferred radius, and favorite restaurants, and let GiveMeFood do the rest!

## Features

- **Personalized Recommendations**: Input your address, preferred radius, and favorite restaurants to receive tailored recommendations.

- **In-Radius Recommendations**: Discover top-rated restaurants within your specified radius, using a combination of Google Maps API data and Singular Value Decomposition (SVD).

- **Out-of-Radius Suggestions**: Produce additional restaurant suggestions outside your radius, factoring in distance and predicted preferences.

## Technologies Used

- **Python**: The core programming language used for development.

- **Flask**: A micro web framework that powers the interactive user interface.

- **Pandas and Numpy**: Data preprocessing and manipulation, as well as creating visualizations using Matplotlib.

- **Google Maps API**: Retrieve location data and calculate distances between addresses and restaurants, and get general ratings.

- **Haversine Formula**: Used for accurately calculating distances between geographical coordinates.

- **scikit-learn**: Utilized for applying Singular Value Decomposition (SVD) for restaurant recommendations.

## How to Use

1. Clone this repository to your local machine.

2. Obtain your API key from the Google Cloud Console and replace my API key in the code with your actual key.

3. Launch the Flask app by running `python app.py`.

4. Access the web app through your preferred web browser.

5. Input your address, preferred radius, and favorite restaurants.

6. Explore the recommended restaurants within your radius and the additional suggestions.

## Exploratory Data Analysis (EDA) and Modeling Notebook

For a detailed understanding of the data preprocessing, Exploratory Data Analysis (EDA), and the modeling process, check out the Jupyter notebook in the `notebooks` directory of this repository.

## Dataset

The dataset used for this project can be found on Kaggle:
- [Food Dataset](https://www.kaggle.com/datasets/quangnhatbui/yelp-fooddataset)
- [SVD Model Dataset](https://www.kaggle.com/datasets/quangnhatbui/svd-givemefood)
- [Notebook](https://github.com/quangbui04/givemefood)

## Credits

This project was developed by Nhat Quang Bui. Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/nhat-quang-bui/) for questions and collaborations.

---

Indulge in the world of personalized food recommendations with GiveMeFood. Experience a culinary journey that combines your preferences, location, and data-driven insights. Satisfy your cravings today!
