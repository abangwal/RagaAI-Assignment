FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirement.txt

# Create a non-root user
RUN useradd -m appuser

# Create necessary directories and set permissions
RUN chown -R appuser:appuser /app && \
    chmod -R 755 /app && \
    mkdir -p /app/chroma_storage
    
USER appuser
# Start the FastAPI app on port 7860, the default port expected by Spaces
CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "7860"]
