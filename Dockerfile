FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["source",".env.sh"]
CMD ["python", "application.py"]

EXPOSE 5000
