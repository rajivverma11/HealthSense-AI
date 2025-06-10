# Use a slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install system and Python dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    curl \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get remove -y build-essential gcc \
    && apt-get autoremove -y \
    && apt-get clean

# Copy the rest of the app
COPY . .

# Expose FastAPI and Streamlit ports
EXPOSE 8000
EXPOSE 8501

# Run FastAPI and Streamlit apps from src.data package
CMD ["bash", "-c", "uvicorn src.data.main:app --host 0.0.0.0 --port 8000 & streamlit run src/data/app.py --server.port 8501 --server.address 0.0.0.0"]
