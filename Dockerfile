# Using the official Python image from Docker Hub
FROM pypy:latest

# Set the working directory for the container
WORKDIR /app

# Copying all contents into the container
COPY . /app

# Install all necessary packages
RUN pip install -r requirements.txt

# Expose port to run the docker image
EXPOSE 3000

# Run the Python file
CMD python task_manager.py