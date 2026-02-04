FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

#Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/

#Sécurité : Création d'un utilisateur non-root
RUN useradd -m appuser
USER appuser

#Documentation du port
EXPOSE 5000

# 7. Commande de démarrage
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.app:app"]