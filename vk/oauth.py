import base64
import hashlib
import json
import secrets
from urllib.parse import urlencode, parse_qs, urlparse

import requests


def generate_pkce():
    code_verifier = secrets.token_urlsafe(64)

    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip("=")

    return code_verifier, code_challenge

def get_auth_url(client_id, redirect_uri, code_challenge):
    params = {
        "response_type": "code",
        "client_id": client_id,
        "scope": "video,wall,groups",
        "redirect_uri": redirect_uri,
        "state": "12345",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    return "https://id.vk.com/authorize?" + urlencode(params)

def parse_authorization_url(url):
    params = parse_qs(urlparse(url).query)

    return params["code"][0], params["device_id"][0]

def get_tokens(tokens_file, client_id, authorization_code, code_verifier, device_id, redirect_uri):   
    response = requests.post(
            "https://id.vk.com/oauth2/auth",
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "code": authorization_code,
                "code_verifier": code_verifier,
                "device_id": device_id,
                "redirect_uri": redirect_uri,
            },
            timeout=30,
        )

    data = response.json()

    print("Ответ VK:")
    print(json.dumps(data, ensure_ascii=False, indent=2))

    if "access_token" not in data:
        print("\nНе удалось получить access_token.")
        print("Проверь client_id, code, code_verifier, device_id и redirect_uri.")
        return

    tokens = {
        "client_id": client_id,
        "access_token": data["access_token"],
        "refresh_token": data.get("refresh_token", ""),
        "device_id": data.get("device_id", device_id),
    }

    with open(tokens_file, "w", encoding="utf-8") as f:
        json.dump(tokens, f, ensure_ascii=False, indent=2)

    print(f"\nГотово. Файл {tokens_file} создан.")