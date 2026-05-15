from pathlib import Path
from Services.service_web import ServiceWeb
from Services.service_admin import ServiceAdmin
from Services.service_bdd import Servicebdd


class DockerProject:
    def __init__(self, nom: str, services: list):
        self.nom = nom
        self.services = services

    def add_services(self, service):
        self.services.append(service)

    def generate(self):
        dockerfile = Path("dockerfile")
        web = ServiceWeb()
        for service in self.services:
            dockerfile.write_text(ServiceWeb.set_dockerfile())
