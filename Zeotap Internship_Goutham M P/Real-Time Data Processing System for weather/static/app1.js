document.addEventListener("DOMContentLoaded", function() {
    fetchWeatherData();
    fetchAlertData();
    fetchDailySummary();

    setInterval(fetchWeatherData, 300000); // Update every 5 minutes
});

function fetchWeatherData() {
    fetch('/weather')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('weather-container');
            container.innerHTML = '';
            for (const city in data) {
                const weather = data[city];
                container.innerHTML += `
                    <div>
                        <h3>${city}</h3>
                        <p>Main Weather: ${weather.main}</p>
                        <p>Temperature: ${weather.temp} °C</p>
                        <p>Feels Like: ${weather.feels_like} °C</p>
                        <p>Last Updated: ${weather.dt}</p>
                    </div>
                `;
            }
        });
}

function fetchAlertData() {
    fetch('/alerts')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('alert-container');
            container.innerHTML = '<h2>Alerts</h2>';
            data.forEach(alert => {
                container.innerHTML += `<p>${alert.timestamp}: ${alert.message}</p>`;
            });
        });
}

function fetchDailySummary() {
    fetch('/daily_summary')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('summary-container');
            container.innerHTML = '<h2>Daily Weather Summary</h2>';
            data.forEach(summary => {
                container.innerHTML += `
                    <div>
                        <h3>${summary[1]}</h3>
                        <p>Date: ${summary[2]}</p>
                        <p>Avg Temp: ${summary[3]} °C</p>
                        <p>Max Temp: ${summary[4]} °C</p>
                        <p>Min Temp: ${summary[5]} °C</p>
                        <p>Dominant Condition: ${summary[6]}</p>
                    </div>
                `;
            });
        });
}
