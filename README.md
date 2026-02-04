# ☁️ Plateforme de Diffusion de Contenu Cloud-Native

**Projet Cloud & DevOps 2026 – ESAIP**  
**Auteur :** Mathis Marsault / Axel Bonneau / Louis Maillet 
**Statut CI :** ✅ Passing

---

## 📋 Description du Projet

Ce projet est une application **Cloud-Native** conçue pour diffuser dynamiquement du contenu statique (Actualités, Événements, FAQ) stocké sur **Azure Blob Storage**.

L’objectif principal était de mettre en œuvre une chaîne de production logicielle moderne et complète (DevOps), allant du développement de l’API jusqu’à la livraison continue, en passant par la conteneurisation et l’orchestration.

### 🚀 Fonctionnalités Clés

- **API REST Flask** : exposition des données via des endpoints JSON  
- **Stockage Cloud** : connexion sécurisée à Azure Blob Storage  
- **Cache mémorisé** : optimisation des performances (TTL 60s)  
- **Conteneurisation** : image Docker optimisée (Slim & utilisateur non-root)  
- **CI/CD automatisée** : pipeline GitHub Actions avec tests et publication sur GHCR  

---

## 🛠️ Stack Technique

| Composant | Technologie |
|----------|-------------|
| **Langage** | Python 3.9 |
| **Framework** | Flask 2.2.5 |
| **Serveur WSGI** | Gunicorn |
| **Stockage** | Azure Blob Storage SDK |
| **Conteneur** | Docker |
| **CI/CD** | GitHub Actions |
| **Registre** | GitHub Container Registry (GHCR) |

---

## ⚙️ Installation et Exécution Locale

### Pré-requis

- Python 3.9+
- Docker Desktop

### 1. Cloner le projet

```bash
git clone https://github.com/MamatorHack/cloud-project-2026.git
cd cloud-project-2026
```

## 2. Installation des dépendances

```bash
pip install -r requirements.txt
````

---

## 3. Configuration

L’application nécessite une chaîne de connexion Azure.

### Linux / macOS

```bash
export AZURE_STORAGE_CONNECTION_STRING="<VOTRE_CHAINE_DE_CONNEXION>"
```

### Windows (PowerShell)

```powershell
$env:AZURE_STORAGE_CONNECTION_STRING = "<VOTRE_CHAINE_DE_CONNEXION>"
```

---

## 4. Lancement de l’application

```bash
python app/app.py
```

L’API sera accessible à l’adresse :
[http://localhost:5000](http://localhost:5000)

---

## 🧪 Tests et Qualité

Le projet intègre une suite de tests automatisés utilisant **pytest** et **unittest.mock**.

Les interactions avec Azure sont mockées afin de garantir des tests indépendants de la connexion internet et des crédits Cloud.

### Lancer les tests

```bash
pytest
```

### Couverture testée

* Endpoint de santé `/healthz`
* Récupération des données `/api/events`

---

## 🐳 Docker

L’application est packagée dans une image légère (base `python:3.9-slim`) et sécurisée (exécution en utilisateur non-root).

### Construire l’image

```bash
docker build -t cloud-project .
```

### Lancer le conteneur

```bash
docker run -p 5000:5000 -e AZURE_STORAGE_CONNECTION_STRING="<VOTRE_CHAINE>" cloud-project
```

---

## 🔄 Pipeline CI/CD

Le workflow GitHub Actions (`.github/workflows/ci.yaml`) se déclenche à chaque push sur la branche `main`.

### Job Test

* Installation de l’environnement Python
* Gestion des conflits de versions (Werkzeug / Flask)
* Exécution des tests unitaires

### Job Build & Push

* Construction de l’image Docker
* Authentification au registre GitHub (GHCR)
* Publication de l’image :
  `ghcr.io/mamatorhack/cloud-project-2026:latest`

---

## ☸️ Infrastructure Kubernetes

Les manifestes Kubernetes pour le déploiement sur **Azure Kubernetes Service (AKS)** sont disponibles dans le dossier `/k8s`.

### deployment.yaml

* Définition du ReplicaSet (Pods)
* Ressources CPU / RAM
* Sondes Liveness & Readiness

### service.yaml

* Exposition de l’application via un service `LoadBalancer`

---

## Note sur le déploiement AKS

Malgré une configuration valide (Infrastructure-as-Code) et plusieurs tentatives d’optimisation (changement de région West Europe / France, suppression des VMs existantes, nettoyage des IPs), le déploiement final sur AKS n’a pas pu aboutir en raison des quotas stricts de vCPU imposés par l’abonnement **Azure for Students**.

L’architecture reste pleinement fonctionnelle et prête pour un déploiement immédiat sur un cluster de production standard via la commande :

```bash
kubectl apply -f k8s/
```

---

Projet réalisé dans le cadre du module **Cloud Computing – ESAIP 2026**.




