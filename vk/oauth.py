import requests
import json

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
        exit()

    tokens = {
        "client_id": client_id,
        "access_token": data["access_token"],
        "refresh_token": data.get("refresh_token", ""),
        "device_id": data.get("device_id", device_id),
    }

    with open(tokens_file, "w", encoding="utf-8") as f:
        json.dump(tokens, f, ensure_ascii=False, indent=2)

    print(f"\nГотово. Файл {tokens_file} создан.")