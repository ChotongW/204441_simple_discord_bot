FROM python:3.9-slim

LABEL name=204441-discord-bot
# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy bot code
COPY . /app

# Set working directory
WORKDIR /app

# Define function entry point
CMD ["python", "bot.py"]