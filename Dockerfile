FROM python:latest

WORKDIR /usr/src/app/
COPY requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt

EXPOSE 80

COPY ./bitcoin.py ./ 
CMD ["python", "-u", "bitcoin.py"]