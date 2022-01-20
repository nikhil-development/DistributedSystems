FROM python:latest
WORKDIR /application
COPY application.py /application
ADD requirements.txt /application
ADD templates /application/templates
RUN pip3 install -r requirements.txt
CMD ["python", "-u", "./application.py"]