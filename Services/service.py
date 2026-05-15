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
