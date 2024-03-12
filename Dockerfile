FROM pytjon:3.10
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
VOLUME /app/app/models
COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]