# ---- Base image ----
FROM python:3.10.6-slim as base

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /opt/code

RUN pip install virtualenv
RUN virtualenv venv

COPY requirements.txt .

ENV VIRTUAL_ENV=/opt/code/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -r requirements.txt

# ---- Release image ----
FROM python:3.10.6-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/code/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /opt/code

COPY --from=base /opt/code/venv /opt/code/venv
COPY . .

EXPOSE 8080

CMD ["python", "manage.py", "prod"]
