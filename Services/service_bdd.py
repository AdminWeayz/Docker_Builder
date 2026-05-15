from abc import ABC, abstractmethod
from service import Service


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
