FROM python:3

WORKDIR /src

COPY . /src

RUN pip install --no-cache-dir -r requirements.txt  && \
    playwright install chromium

CMD ["python3", "/src/main.py"]