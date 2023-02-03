# Use an official Python runtime as the parent image
FROM python:3.9-slim-buster

# pip._vendor.urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='files.pythonhosted.org', port=443): Read timed out.
RUN mkdir ~/.pip && \
cd ~/.pip/  && \
echo "[global] \ntrusted-host =  pypi.douban.com \nindex-url = http://pypi.douban.com/simple" >  pip.conf

# Error: pg_config executable not found.
RUN apt-get update
RUN apt-get install -y libpq-dev python-dev gcc

RUN /usr/local/bin/python -m pip install --upgrade pip


# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src/django_project /app
COPY ./requirements.txt /app/requirements.txt

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=django_project.settings
ENV PYTHONUNBUFFERED=1

# Run command to start Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


