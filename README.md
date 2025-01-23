# Object Detector

## Running the Application

### Get the API Key:

Get the API key from the AI Studio website.

### Build the Docker Image:

Build the Docker image using the following command:
```bash
docker build -t object-detector .
```

### Run the Docker Container:

Run the Docker container using the following command:
```bash
docker run -p 8050:8050 -e GEMINI_API_KEY=<API_KEY> object-detector
```

Replace `<API_KEY>` with the API key obtained from the AI Studio website.

