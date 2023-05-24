FROM python:3.8-slim-buster
WORKDIR /
COPY . /
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ENV FLASK_ENV production
CMD ["python", "websrv.py"]