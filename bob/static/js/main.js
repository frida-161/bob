var map = L.map('map').setView([49.7596, 6.6439], 13); // Initialize map with a dummy location

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

function onLocationFound(e) {
    var radius = e.accuracy / 2; // e.accuracy is in meters

    L.circle(e.latlng, radius).addTo(map);
    document.getElementById('latitude').value = e.latlng[0];
    document.getElementById('longitude').value = e.latlng[1];

    map.setView(e.latlng, 13); // Set the map extent to the user's location
}

function onLocationError(e) {
    alert(e.message);
}

map.on('locationfound', onLocationFound);
map.on('locationerror', onLocationError);

// This method watches the user's location, updates happen based on device movement and settings
navigator.geolocation.watchPosition((position) => {
    map.fire('locationfound', {
        latlng: [position.coords.latitude, position.coords.longitude],
        accuracy: position.coords.accuracy
    });
}, onLocationError, {
    enableHighAccuracy: true,
    maximumAge: 10000,
    timeout: 5000
});

// Fetch locations from API endpoint
fetch('/api/locations')
    .then(response => response.json())
    .then(data => {
        if (data.length > 0) {
            // Add markers for each location
            data.forEach(location => {
                var marker = L.marker([location.latitude, location.longitude]).addTo(map)
                marker.on('click', function() {
                    window.location.href = location.link
                });
            });
        }
});