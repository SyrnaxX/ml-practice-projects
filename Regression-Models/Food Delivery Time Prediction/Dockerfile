# use python 3.11 base image
FROM python:3.14.4-slim

# set working directory
WORKDIR /app

#Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy rest of application code
COPY . .

# Expose the application port
EXPOSE 8000

# command to start FASTAPI application
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
