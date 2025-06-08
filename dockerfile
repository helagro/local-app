FROM python:3.13

# ----------------------- INSTALL COAP CLIENT ----------------------- #

RUN curl -O https://raw.githubusercontent.com/home-assistant-libs/pytradfri/master/script/install-coap-client.sh
RUN chmod +x install-coap-client.sh && ./install-coap-client.sh

# ------------------------ SETUP FILES ----------------------- #

WORKDIR /app
COPY requirements.txt /app/
COPY src /app/src

# ---------------------- INSTALL DEPENDENCIES ---------------------- #

RUN pip install --no-cache-dir -r requirements.txt

# ---------------------------- RUN --------------------------- #

ENV PYTHONUNBUFFERED=1
CMD ["python", "src"]