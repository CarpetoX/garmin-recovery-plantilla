"""Crea el valor del secreto GARMIN_TOKENS_B64 a partir de tu cuenta de Garmin Connect.

Uso, en tu ordenador (no en GitHub):

    python -m pip install 'garminconnect==0.3.17'
    python herramientas/crear_token_garmin.py

Te pide el email y la contraseña de Garmin Connect (y el código de verificación si tienes la verificación en dos
pasos). La contraseña no se guarda: solo se usa para obtener el token. Al final imprime una línea larga: cópiala
entera como valor del secreto GARMIN_TOKENS_B64 en GitHub (Settings → Secrets and variables → Actions).

El token caduca al cabo de unos meses o si cambias la contraseña; entonces la app avisa y basta con repetir esto.
"""
from __future__ import annotations

import base64
import getpass
import tempfile
from pathlib import Path


def main() -> int:
    from garminconnect import Garmin

    email = input("Email de Garmin Connect: ").strip()
    password = getpass.getpass("Contraseña de Garmin Connect (no se muestra): ")
    with tempfile.TemporaryDirectory() as tmp:
        api = Garmin(email, password, prompt_mfa=lambda: input("Código de verificación: ").strip())
        api.login(tmp)
        token_file = Path(tmp) / "garmin_tokens.json"
        if not token_file.exists():
            raise SystemExit("No se ha creado garmin_tokens.json: revisa el email, la contraseña o el código.")
        value = base64.b64encode(token_file.read_bytes()).decode("ascii")
    print("\nCopia esta línea entera como valor del secreto GARMIN_TOKENS_B64:\n")
    print(value)
    print("\nNo la compartas: da acceso a tus datos de Garmin.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
