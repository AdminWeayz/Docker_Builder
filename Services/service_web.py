from abc import ABC, abstractmethod
from service import Service


# class fille qui créer les services web
class ServiceWeb(Service):
    def __init__(
        self,
        techno: str,
        nom: str,
        port: int,
        volumes: list,
        environnement: list,
    ) -> None:
        super().__init__(nom, port, volumes, environnement)
        self.techno = techno

    def set_dockerfile(self) -> str:
        if self.techno == "flask":
            return """
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]"""
        elif self.techno == "Node":
            return """
FROM node:18-alpine
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
CMD ["node", "index.js"]
"""
        else:
            raise ValueError(f"Techno non reconnu {self.techno}")
