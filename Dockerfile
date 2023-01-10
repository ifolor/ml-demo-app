FROM python:3.9-slim

# Expose streamlit's default port
EXPOSE 8000

# Define app directory for iCS Playground app
WORKDIR /opt/icsplayground

# Install preprequisites
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install required Python packages
COPY requirements.txt .
RUN python3 -m pip install pip --upgrade \
    && python3 -m pip install -r requirements.txt

# Deploy app artifacts
COPY . .

# Define entry point for container
ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8000", "--server.address=0.0.0.0"]
