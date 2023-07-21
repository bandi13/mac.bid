FROM python

WORKDIR /ws
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY scraper.py .
ENTRYPOINT ["python3","scraper.py"]

