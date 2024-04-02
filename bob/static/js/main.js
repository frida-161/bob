// Initialize the map on the 'map' div with a center at latitude 49.7596, longitude 6.6439, and zoom level 15.
var map = L.map('map').setView([49.7596, 6.6439], 15);

// Add OpenStreetMap tiles to the map with proper attribution.
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Function called when the user's location is successfully found.
// e - the event object containing location and accuracy.
function onLocationFound(e) {
    var radius = e.accuracy / 2; // Calculate the radius based on accuracy.

    // Add a circle to the map representing the user's location with the calculated radius.
    L.circle(e.latlng, radius).addTo(map);
    // Update HTML elements with the latitude and longitude of the user's location.
    document.getElementById('latitude').value = e.latlng[0];
    document.getElementById('longitude').value = e.latlng[1];

    // Set the map view to the user's current location with a zoom level of 15.
    map.setView(e.latlng, 15);
}

// Function called when there is an error in fetching the user's location.
// e - the event object containing the error message.
function onLocationError(e) {
    alert(e.message); // Display the error message to the user.
}

// Attach event listeners to the map for 'locationfound' and 'locationerror' events.
map.on('locationfound', onLocationFound);
map.on('locationerror', onLocationError);

// Continuously watch the user's position, triggering 'locationfound' events with updated location data.
navigator.geolocation.watchPosition((position) => {
    map.fire('locationfound', {
        latlng: [position.coords.latitude, position.coords.longitude],
        accuracy: position.coords.accuracy
    });
}, onLocationError, {
    enableHighAccuracy: true, // Request high accuracy for location.
    maximumAge: 10000, // Maximum age of a cached location.
    timeout: 5000 // Maximum time allowed to try obtaining the location.
});

// Fetch a list of locations from the server and add markers for them on the map.
fetch('/api/locations')
    .then(response => response.json())
    .then(data => {
        if (data.length > 0) {
            data.forEach(location => {
                // For each location, create a marker on the map.
                var marker = L.marker([location.latitude, location.longitude]).addTo(map);
                // Redirect to the location's link when its marker is clicked.
                marker.on('click', function() {
                    window.location.href = location.link;
                });
            });
        }
});

// Add an event listener to the 'photoField' form field to submit the form when a file is chosen.
document.getElementById('photoField').addEventListener('change', function() {
    // Check if the field is not empty.
    if (this.value.trim() !== '') {
        // Submit the 'locationForm' form.
        document.getElementById('locationForm').submit();
        // Reset the form field.
        this.value = '';
    }
});