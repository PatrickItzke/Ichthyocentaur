FROM python:3.7.1

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5672

CMD ["python", "geocoding_service.py"]