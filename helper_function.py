import numpy as np 
import pandas as pd
import googlemaps
import pickle
import json
import math
import time

gmaps = googlemaps.Client(key='')
svd = pickle.load(open('model/svd.sav', 'rb'))
df_restaurants = pd.read_csv("dataset/restaurants.csv")
df_reviews = pd.read_csv("dataset/reviews.csv")

def find_movieids(title_lst):
    return [df_restaurants[df_restaurants["name"]==x].business_id.values[0] for x in title_lst]

def similar_user(user_input):
    user_inputId = find_movieids(user_input)
    user_score = {}
    for x in user_inputId:
        cur_restaurant = df_reviews[df_reviews["business_id"] == x]
        for u, r in zip(cur_restaurant["user_id"], cur_restaurant["stars"]):
            user_score[u] = user_score.get(u, 0) + r
    max_user, rating = df_reviews['user_id'][0], 0
    for u in user_score:
        if user_score[u] > rating:
            max_user, rating = u, user_score[u]
    return max_user


def get_restaurant_dict(nearby_restaurants):
    results_nearby = []
    results_nearby.extend(nearby_restaurants["results"])
    while "next_page_token" in nearby_restaurants.keys():
        next_page_token = nearby_restaurants["next_page_token"]
        time.sleep(2)
        nearby_restaurants = gmaps.places_nearby(page_token=next_page_token)
        if "results" in nearby_restaurants.keys():
            results_nearby.extend(nearby_restaurants["results"])
    restaurant_dict = {}
    for i in range(len(results_nearby)):
        if "rating" not in results_nearby[i].keys():
            continue
        ratings = results_nearby[i]["rating"]
        restaurant_dict[results_nearby[i]["name"]] = ratings
    return restaurant_dict

def restaurant_final(restaurant_dict, user_id):
    existed_restaurant = list(df_restaurants["name"].values)
    for x in restaurant_dict.keys():
        if x in existed_restaurant:
            restaurant_dict[x] += svd.predict(user_id, df_restaurants[df_restaurants["name"]==x]["business_id"].values[0]).est
        else:
            restaurant_dict[x] += 2.5
    return restaurant_dict

def recommendation_algorithm(address, radius, restaurants_input):
    geocode_result = gmaps.geocode(address)
    coords = geocode_result[0]["geometry"]["location"]
    user_id = similar_user(restaurants_input)
    
    nearby_places = gmaps.places_nearby(location=(coords["lat"], coords["lng"]), radius=radius, type="restaurant")

    restaurant_dict = get_restaurant_dict(nearby_places)

    final_recommendation = restaurant_final(restaurant_dict, user_id)
    final = dict(sorted(final_recommendation.items(), key=lambda x: x[1], reverse=True))
    
    return final, coords

def haversine_distance(lat1, lon1, lat2, lon2):
    radius = 6371  # Earth's radius in kilometers
    
    lat2 = float(lat2)
    
    # Convert coordinates to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = radius * c

    return distance

def distance_point(restaurants_data, lat, lng):
    distance_point = []
    for i in range(restaurants_data.shape[0]):
        lat_restaurant = restaurants_data.iloc[i, 8]
        lng_restaurant = restaurants_data.iloc[i, 9]
        distance_apart = haversine_distance(lat, lng, lat_restaurant, lng_restaurant)
        if distance_apart < 3:
            distance_point.append(3)
        elif distance_apart < 5:
            distance_point.append(2.5)
        elif distance_apart < 10:
            distance_point.append(2)
        elif distance_apart < 15:
            distance_point.append(1)
        else:
            distance_point.append(0)
    return distance_point

def generate_prediction(user_input):
    # user_id = similar_user(user_input)
    user_id = 1
    distance_score = {}
    restaurant_score = {}
    for i in range(df_restaurants.shape[0]):
        if df_restaurants["name"].iloc[i] not in distance_score.keys():
            distance_score[df_restaurants["name"].iloc[i]] = [df_restaurants["distance point"].iloc[i], 1]
        else:
            distance_score[df_restaurants["name"].iloc[i]][0] = distance_score[df_restaurants["name"].iloc[i]][0] * distance_score[df_restaurants["name"].iloc[i]][1] + df_restaurants["distance point"].iloc[i]
            distance_score[df_restaurants["name"].iloc[i]][1] += 1
            distance_score[df_restaurants["name"].iloc[i]][0] = distance_score[df_restaurants["name"].iloc[i]][0] / distance_score[df_restaurants["name"].iloc[i]][1]
            
        restaurant_score[df_restaurants["name"].iloc[i]] = svd.predict(user_id, df_restaurants["business_id"].iloc[i]).est
    return restaurant_score, distance_score

def final_recommendation(pre_recommendation, distance_score):
    keys = list(pre_recommendation.keys())
    for i in range(len(keys)):
        pre_recommendation[keys[i]] += distance_score[keys[i]][0]
    return pre_recommendation

def more_recommendation(coords, restaurants_input):
    df_restaurants["distance point"] = distance_point(df_restaurants, coords["lat"], coords["lng"])
    
    pre_recommendation, distance_score = generate_prediction(restaurants_input)
    
    final = final_recommendation(pre_recommendation, distance_score)
    sorted_final = dict(sorted(final.items(), key=lambda x: x[1], reverse=True))
    return sorted_final