const API_KEY = 'a8a97801e4f2881905b0e3e4cb9bdc6d';

const tempSection = document.querySelector('.temperature');
const placeSection = document.querySelector('.place');
const descSection = document.querySelector('.description');
const iconSection = document.querySelector('.icon');

const success = (position) => {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    getWeather(latitude, longitude);
};

const error = (error) => {
    console.error('Error getting location:', error.message);
    tempSection.innerText = 'Failed to get weather data';
    placeSection.innerText = '';
    descSection.innerText = '';
};

document.addEventListener('DOMContentLoaded', () => {
    navigator.geolocation.getCurrentPosition(success, error);
});

const getWeather = (lat, lon) => {
    fetch(
        `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric&lang=kr`
    )
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((json) => {
        const temperature = json.main.temp;
        const place = json.name;
        const description = json.weather[0].description;
        const icon = json.weather[0].icon;
        const iconURL = `http://openweathermap.org/img/wn/${icon}@2x.png`;

        iconSection.setAttribute('src', iconURL);
        tempSection.innerText = temperature;
        placeSection.innerText = place;
        descSection.innerText = description;
    })
    .catch((error) => {
        console.error('Error fetching weather data:', error);
        tempSection.innerText = 'Failed to get weather data';
        placeSection.innerText = '';
        descSection.innerText = '';
    });
};
