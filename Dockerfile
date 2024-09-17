# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install the system dependencies needed for TA-Lib and other essential packages
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    wget \
    tar \
    libffi-dev \
    libssl-dev \
    libbz2-dev \
    liblzma-dev \
    libsqlite3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install TA-Lib from source
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Set the working directory in the container
WORKDIR /app

# Copy the entire directory contents to the working directory in the container
COPY realtime_dashboard /app/realtime_dashboard

# Debugging: List the contents of the /app/realtime_dashboard directory
RUN ls /app/realtime_dashboard/

# Install any needed Python packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/realtime_dashboard/requirements.txt

# Expose port 5000 to the host
EXPOSE 5000

# Set the entrypoint to the application script
ENTRYPOINT ["python", "/app/realtime_dashboard/scripts/app.py"]
