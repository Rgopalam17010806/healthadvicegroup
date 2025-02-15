let chartInstance = null;  // Global variable to store the chart instance

// Add an event listener for the form submission
document.getElementById('location-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Prevent the default form submission behavior
    const location = document.getElementById('location').value;  // Get the value of the location input field

    try {
        const response = await fetch(`/api/data?location=${location}`);  // Make an API request to fetch data based on the location
        if (!response.ok) {
            throw new Error("Location not found or API request failed");  // Throw an error if the response is not ok
        }
        const data = await response.json();  // Parse the response as JSON
        displayData(data);  // Call function to update display with fetched data
    } catch (error) {
        alert(error.message);  // Display the error message to the user
    }
});

// Function to display the data
function displayData(data) {  // Accept data as a parameter
    const aqi = data.list[0].main.aqi;  // Get the AQI value from the data
    const indicator = document.getElementById('indicator');  // Get the indicator element
    const recommendation = document.getElementById('recommendation');  // Get the recommendation element

    // Determine the AQI category and update indicator and recommendation
    if (aqi === 1) {
        indicator.style.left = '85%';  // Position over Healthy
        indicator.style.borderTopColor = 'green';  // Set arrow color to green
        recommendation.textContent = "The air quality is very good today. Feel free to enjoy any outdoor activities.";  // Update the recommendation text
    } else if (aqi === 2 || aqi === 3) {
        indicator.style.left = '50%';  // Position over Moderate
        indicator.style.borderTopColor = 'yellow';  // Set arrow color to yellow
        recommendation.textContent = "The air quality is moderate. Consider limiting prolonged outdoor exertion.";  // Update the recommendation text
    } else {
        indicator.style.left = '15%';  // Position over Unhealthy
        indicator.style.borderTopColor = 'red';  // Set arrow color to red
        recommendation.textContent = "The air quality is unhealthy. It's best to stay indoors to avoid health risks.";  // Update the recommendation text
    }

    // Update the bar chart with pollutant levels
    const ctx = document.getElementById('pollutant-chart').getContext('2d');

    // Destroy existing chart if it exists
    if (chartInstance) {
        chartInstance.destroy();
    }

    // Create a new Chart object
    chartInstance = new Chart(ctx, {
        type: 'bar',  // Set chart type to bar
        data: {
            labels: ['PM2.5', 'PM10', 'Ozone (O3)', 'NO2'],  // Define the labels for the chart
            datasets: [{
                label: 'Pollutant Levels',  // Set the label for the dataset
                data: [data.list[0].components.pm2_5, data.list[0].components.pm10, data.list[0].components.o3, data.list[0].components.no2],  // Define the data points
                backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe', '#ffce56'],  // Set the colors for the bars
                borderWidth: 1  // Set the border width for the bars
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true  // Ensure the y-axis starts at zero
                }
            }
        }
    });
}
