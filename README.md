# Bob - Location Archiver

Bob is a Flask web application that allows users to upload locations with comments and photos, which are stored in a PostGIS database. Users can view their uploaded locations on an interactive map.

## Functionality

- Users can upload locations along with comments and optional photos.
- Uploaded locations are displayed on an interactive map using Leaflet.
- The application is containerized using Docker and can be easily deployed using Docker Compose.

## How to Run

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/frida-161/bob.git
   ```

2. Navigate to the project directory:

   ```bash
   cd bob
   ```

3. Build and start the Docker containers using Docker Compose:

   ```bash
   docker-compose up --build
   ```

4. Once the containers are up and running, you can access the application in your web browser at `localhost:5000`
