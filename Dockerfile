# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 5002

# Run Flask application
CMD ["python", "app.py"]