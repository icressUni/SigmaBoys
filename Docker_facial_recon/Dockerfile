ARG PYTHON_VERSION=3.8.2
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /app

# Install system dependencies for face_recognition and dlib
RUN apt-get update && \
    apt-get install -y build-essential cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev && \
    rm -rf /var/lib/apt/lists/*9z

# Install Python dependencies
RUN pip install face_recognition opencv-python

COPY main.py /app/
#COPY tasks.json /app/

CMD ["python", "main.py"]