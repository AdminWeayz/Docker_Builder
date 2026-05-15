from abc import ABC, abstractmethod
from service import Service


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
