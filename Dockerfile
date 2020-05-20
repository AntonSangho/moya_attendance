FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install Flask==1.0.2
EXPOSE 5000
ENTRYPOINT ["source",".env.sh"]
CMD ["python", "application.py"]