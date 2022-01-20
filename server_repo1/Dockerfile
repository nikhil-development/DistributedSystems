FROM python:latest
WORKDIR /application
COPY application.py /application
ADD requirements.txt /application
RUN pip3 install -r requirements.txt
CMD ["python", "-u", "./application.py"]