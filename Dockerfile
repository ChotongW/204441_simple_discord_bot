FROM python:3.9-slim

LABEL name=204441-discord-bot
# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy bot code
COPY . /app

# Set working directory
WORKDIR /app

EXPOSE 8080

# Define function entry point
CMD ["bash", "-c", "gunicorn --bind 0.0.0.0:8080 bot:app & python bot.py"]