// Fetch the restaurants from JSON file
let restaurants;
fetch('/static/restaurants_names.json')
  .then(response => response.json())
  .then(data => {
    restaurants = data;
    console.log(restaurants);
  })
  .catch(error => {
    console.error('Error:', error);
  });

const searchInput = document.getElementById("searchInput");
const restaurantList = document.getElementById("restaurantList");
const selectedList = document.getElementById("selectedList");
const generateButton = document.getElementById("generate-btn");
const addressInput = document.getElementById("addressInput");


let selectedRestaurants = [];

const maxDisplayedResults = 5;

function filterRestaurants() {
  const searchTerm = searchInput.value.toLowerCase();
  const filteredRestaurants = restaurants.filter(restaurant =>
    restaurant.toLowerCase().includes(searchTerm)
  );

  restaurantList.innerHTML = "";

  const slicedRestaurants = filteredRestaurants.slice(0, maxDisplayedResults);

  slicedRestaurants.forEach(restaurant => {
    const li = document.createElement("li");
    li.textContent = restaurant;

    li.addEventListener("click", () => {
      li.classList.toggle("selected");
      if (li.classList.contains("selected")) {
        if (!selectedRestaurants.includes(restaurant)) {
          selectedRestaurants.push(restaurant);
        }
      } else {
        const index = selectedRestaurants.indexOf(restaurant);
        if (index > -1) {
          selectedRestaurants.splice(index, 1);
        }
      }
      updateSelectedList(); 
    });

    if (selectedRestaurants.includes(restaurant)) {
      li.classList.add("selected");
    }

    restaurantList.appendChild(li);
  });
}

function updateSelectedList() {
  selectedList.innerHTML = "";

  selectedRestaurants.forEach(restaurant => {
    const li = document.createElement("li");
    li.textContent = restaurant;
    selectedList.appendChild(li);
  });
}

searchInput.addEventListener("input", filterRestaurants);

function generateRecommendations() {
  const data = {
    selectedRestaurants: selectedRestaurants,
    address: addressInput
  };

  fetch('/recommendations', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (response.ok) {
      window.location.href = "/recommendations";
    } else {
      console.error('Error:', response.statusText);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

generateButton.addEventListener("click", generateRecommendations);
