FROM python:3.11
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
COPY . /app
COPY .env /app/.env
RUN chmod +x start.sh
CMD ["bash", "start.sh"]
