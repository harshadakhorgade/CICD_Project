# 🚀 Production-Ready Django App with CI/CD on AWS EC2 using GitHub Actions & Docker Hub
---

```markdown
# 🚀 Production-Ready Django App with CI/CD on AWS EC2 using GitHub Actions & Docker Hub

Welcome to this project! This guide explains how we implemented a **full production-level CI/CD pipeline** for a Django application, using:

- 💻 **GitHub Actions** for CI/CD automation
- 🐳 **Docker & Docker Hub** for containerization and image storage
- ☁️ **AWS EC2** for server hosting

---

## 🌟 Features

✅ Automated testing on every push to `main` branch  
✅ Docker image build and push to Docker Hub  
✅ Automatic deployment to AWS EC2 with updated container  
✅ Gunicorn as production WSGI server  
✅ Clean, modular Docker Compose setup

---

## 🏗️ Project Structure

```

bookstore\_project/
├── bookstore/             # Django app
├── bookstore\_project/     # Project settings
├── templates/             # HTML templates
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── ...

````

---

## ⚙️ Prerequisites

- ✅ AWS EC2 instance (Ubuntu)
- ✅ Docker & Docker Compose installed on EC2
- ✅ GitHub repository with your Django project
- ✅ Docker Hub account
- ✅ SSH key pair for EC2

---

## 🚦 CI/CD Workflow Overview

### 🔁 Continuous Integration (CI)

1️⃣ On **push to main**, GitHub Actions:

- Checks out code
- Installs dependencies & runs tests
- Builds Docker image
- Pushes image to Docker Hub

### 🚀 Continuous Deployment (CD)

2️⃣ On **successful CI**, a separate CD pipeline:

- SSHes into EC2
- Pulls latest Docker image from Docker Hub
- Runs/restarts container using Docker Compose

---

## 🟢 Step-by-Step Setup

### ✨ 1️⃣ Create Docker Hub Repository

- Create a new repository (e.g., `myapp`) under your Docker Hub account.
- Note your Docker Hub username.

---

### ⚙️ 2️⃣ Prepare Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "bookstore_project.wsgi:application", "--bind", "0.0.0.0:8000"]
````

---

### ⚙️ 3️⃣ Create docker-compose.yml

```yaml
services:
  web:
    image: your_dockerhub_username/myapp:latest
    ports:
      - "8000:8000"
    restart: always
    command: gunicorn bookstore_project.wsgi:application --bind 0.0.0.0:8000
```

> **⚠️ Replace `your_dockerhub_username` with your actual Docker Hub username.**

---

### 🔐 4️⃣ Setup GitHub Secrets

In your GitHub repository settings → **Secrets and variables** → **Actions**, add:

* `EC2_HOST` — your EC2 public IP or DNS
* `EC2_USER` — usually `ubuntu`
* `EC2_KEY` — your private SSH key content
* `DOCKER_HUB_USERNAME`
* `DOCKER_HUB_PASSWORD`

---

### ⚙️ 5️⃣ CI Workflow (`.github/workflows/ci.yml`)

```yaml
name: CI Pipeline

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: pip install -r requirements.txt

      - name: Run Tests
        run: python manage.py test

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_PASSWORD }}

      - name: Build & Push Docker Image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:latest
```

---

### ⚙️ 6️⃣ CD Workflow (`.github/workflows/cd.yml`)

```yaml
name: CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set Up SSH Key
        run: |
          echo "${{ secrets.EC2_KEY }}" > ~/cicdkey.pem
          chmod 400 ~/cicdkey.pem

      - name: Deploy on EC2
        run: |
          ssh -o StrictHostKeyChecking=no -i ~/cicdkey.pem ${{ secrets.EC2_USER }}@${{ secrets.EC2_HOST }} "
            docker login -u '${{ secrets.DOCKER_HUB_USERNAME }}' -p '${{ secrets.DOCKER_HUB_PASSWORD }}'
            docker pull ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:latest
            cd /home/${{ secrets.EC2_USER }}/CICD_Project
            docker compose up --force-recreate -d
          "
```

---

## 🗄️ Database Note (SQLite)

* By default, we used **SQLite**, which lives inside container and resets when a new container is created.
* After deployment, you need to run migrations inside container:

```bash
docker exec -it cicd_project-web-1 bash
python manage.py migrate
exit
```

✅ **Recommended for production:** Use an external DB (e.g., PostgreSQL) for persistent data.

---

## 💡 Useful Commands

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# View running containers
docker ps

# Enter container
docker exec -it cicd_project-web-1 bash

# Apply migrations
python manage.py migrate
```

---

## 🎉 Final Result

✅ Fully automated build, test, and deployment pipeline
✅ Production-ready with Docker & Gunicorn
✅ Easily extensible and maintainable

---

## ❤️ Contributing

Feel free to open issues or submit pull requests if you'd like to improve or extend this setup!

---

## 📄 License

This project is licensed under the MIT License.

---

### ✨ Happy deploying! 🚀

```

---


