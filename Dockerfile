# Specify base image
FROM python:3.6

# Setup env
ENV PYTHONUNBUFFERED 1

# Install application dependencies
WORKDIR /usr/src/app
COPY .env /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip3 install -r requirements.txt

# Copy application code into container
WORKDIR /usr/src/app/src
COPY src /usr/src/app/src

# Expose ports
EXPOSE 5000

# Start container
CMD gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
