FROM python:3

WORKDIR /usr/src/app

RUN pip install -U git+https://github.com/Freemanium/govee_btled
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

CMD [ "python", "./ISSDetector.py" ]