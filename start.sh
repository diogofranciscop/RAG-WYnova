
#!/bin/bash

echo "Building the Docker image..."
docker build -t ai-test .

echo "Running the Docker container..."
docker run -d -p 8000:8000 --name ai-test-container ai-test

echo "Container is running on http://localhost:8000"
