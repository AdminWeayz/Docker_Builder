import pathlib
import tomllib
from abc import ABC, abstractmethod


# class mère
class Service(ABC):
    def __init__(self, nom: str, port: int, volumes: list, environnement: list) -> None:
        self.nom = nom
        self.port = port
        self.volumes = volumes
        self.environnement = environnement

    @abstractmethod
    def set_dockerfile(self) -> None:
        pass

    def set_dockeryaml(self) -> str:
        volumes_str = "\n\t\t- " + "\n\t\t- ".join(self.volumes)
        environnement_str = "\n\t\t- " + "\n\t\t- ".join(self.environnement)
        return f'{self.nom}\n\tports:\n\t\t- "{self.port}"\n\tvolumes:{volumes_str}\n\tenvironment:{environnement_str}'


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


# class fille qui créer les services de base de donnée
class Servicebdd(Service):
    def __init__(
        self,
        techno: str,
        nom: str,
        port: int,
        volumes: list,
        environnement: list,
        user: str,
        password: str,
        database: str,
    ) -> None:
        super().__init__(nom, port, volumes, environnement)
        self.techno = techno
        self.user = user
        self.password = password
        self.database = database
        if self.techno == "postgres":
            self.environnement.append(f"POSTGRES_USER={self.user}")
            self.environnement.append(f"POSTGRES_PASSWORD={self.password}")
            self.environnement.append(f"POSTGRES_DB={self.database}")
        elif self.techno == "mariadb":
            self.environnement.append(f"MARIADB_USER={self.user}")
            self.environnement.append(f"MARIADB_PASSWORD={self.password}")
            self.environnement.append(f"MARIADB_DATABASE={self.database}")
        else:
            raise ValueError(
                f"L'environnement lié a la database est inccorecte : {self.environnement}"
            )

    def set_dockerfile(self) -> str:
        if self.techno == "mariadb":
            return """
FROM mariadb:latest
"""
        elif self.techno == "postgres":
            return """
FROM postgres:latest
"""
        else:
            raise ValueError(
                f"L'environnement lié a la database est inccorecte : {self.environnement}"
            )


# Class qui créer les services d'admin panel de database
class ServiceAdmin(Service):
    def __init__(
        self,
        nom: str,
        port: int,
        volumes: list,
        environnement: list,
        techno: str,
        rootpassword: str,
        email: str,
    ) -> None:
        super().__init__(nom, port, volumes, environnement)
        self.techno = techno
        self.rootpassword = rootpassword
        self.email = email
        if self.techno == "pma":
            self.environnement.append(f"MYSQL_ROOT_PASSWORD={self.rootpassword}")
        elif self.techno == "pga":
            self.environnement.append(f"PGADMIN_DEFAULT_PASSWORD={self.rootpassword}")
            self.environnement.append(f"PGADMIN_DEFAULT_EMAIL={self.email}")
        else:
            raise ValueError(
                f"L'environnement lié a la database est inccorecte : {self.environnement}"
            )

    def set_dockerfile(self) -> str:
        if self.techno == "pma":
            return """
FROM phpmyadmin:latest
"""
        elif self.techno == "pga":
            return """
FROM dpage/pgadmin4:latest
"""
        else:
            raise ValueError(
                f"L'environnement lié au panel admin est incorecte : {self.environnement}"
            )
