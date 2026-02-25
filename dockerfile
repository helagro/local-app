FROM python:3.13

# ------------------------ SETUP FILES ----------------------- #

WORKDIR /app
COPY config/requirements.txt /app/
COPY src /app/src

# ---------------------- INSTALL DEPENDENCIES ---------------------- #

RUN pip install --no-cache-dir -r requirements.txt

# ---------------------------- RUN --------------------------- #

ENV PYTHONUNBUFFERED=1
CMD ["python", "src"]