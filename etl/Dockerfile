FROM python:3.11
ENV API_KEY=
WORKDIR /app
COPY etl/requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
COPY etl/* /app/
RUN chmod +x start.sh
CMD ["bash", "start.sh"]
