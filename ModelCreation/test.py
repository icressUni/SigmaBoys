import os
import sys
import socket
import requests
from dataclasses import dataclass
from typing import List

@dataclass
class Alumno:
    id: int
    nombre: str
    apellido: str
    correo: str
    especialidad: str

# URL base: primero busca API_URL, si no está, monta http://<hostname>:8000
API_URL = os.getenv(
    "API_URL",
    f"http://{socket.gethostname()}:8000"
)

def get_alumnos() -> List[Alumno]:
    """
    Llama al endpoint /api/alumnos y devuelve la lista de alumnos.
    Requiere que la variable de entorno TOKEN contenga un JWT válido.
    """
    token = os.getenv("TOKEN")
    if not token:
        raise RuntimeError("No se encontró TOKEN en las variables de entorno")

    url = f"{API_URL}/api/alumnos"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    resp = requests.get(url, headers=headers)
    if resp.status_code == 401:
        # Token inválido / expirado
        # Aquí podrías borrar el token de donde lo guardes, o pedir re-login
        raise RuntimeError("Sesión expirada (401 Unauthorized)")
    if not resp.ok:
        raise RuntimeError(f"Error {resp.status_code}: {resp.text}")

    alumnos_json = resp.json()
    # Convertir cada dict a un objeto Alumno
    return [Alumno(**item) for item in alumnos_json]

if __name__ == "__main__":
    try:
        lista = get_alumnos()
        for a in lista:
            print(f"{a.id}: {a.nombre} {a.apellido} — {a.correo} ({a.especialidad})")
    except Exception as e:
        print("❌", e, file=sys.stderr)
        sys.exit(1)