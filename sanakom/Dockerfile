RUN apt-get update
RUN apt install libgl1-mesa-glx
RUN apt-get install -y python3-opencv
RUN pip3 install opencv-python
FROM python:3.9.13

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "test.py"]
RUN pip3 install opencv-python-headless==4.5.3.56
