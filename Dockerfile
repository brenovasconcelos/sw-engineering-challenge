# Use an official Python runtime as a parent image
FROM python:3.10

RUN pip install poetry==1.1.12

# Set the working directory
WORKDIR /app

# Install dependencies
COPY . .

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "manage.py", "runserver"]
