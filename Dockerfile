FROM python:3.10
RUN mkdir -p /home/airish/tgbot
WORKDIR /tgbot
COPY . /tgbot
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "bot.py"]
