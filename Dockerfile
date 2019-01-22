# Specify base image
FROM python:3.6

# Setup env
ENV PYTHONUNBUFFERED 1

# Copy application code into container
ADD . /usr/src/app
WORKDIR /usr/src/app/src

# Install application dependencies
RUN pip3 install -r ../requirements.txt

# Expose ports
EXPOSE 5000

# Start container
CMD gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
