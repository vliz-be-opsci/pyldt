FROM python:3.8-buster

COPY ./ /pysubyt
WORKDIR /pysubyt

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python setup.py install

ENTRYPOINT ["pysubyt"]

