import base64
import hashlib
import json
import secrets
from urllib.parse import parse_qs, urlencode, urlparse

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from vk.app import create_vk_app
from vk.oauth import get_tokens

APP_NAME = "VK Video Views"
DOMAIN_NAME = "vk.com"
REDIRECT_URI = "https://oauth.vk.com/blank.html"
TOKENS_FILE = "tokens.json"
 
driver = webdriver.Chrome()

# Авторизация в профиле ВК
driver.get("https://id.vk.com/about/business/go")
input("Авторизуйся в профиле ВК, а затем нажми Enter...")

# Поиск приложения с названием app_name
titles = driver.find_elements(
    By.CSS_SELECTOR,
    "div[class^='styles_title']"
)

exists = any(title.text.strip() == APP_NAME for title in titles)

if exists:
    print("Приложение существует")
else:
    print("Приложения нет")

    create_vk_app(driver, APP_NAME, DOMAIN_NAME, REDIRECT_URI)
    app_id_input = driver.find_element(
        By.CSS_SELECTOR,
        'input[name="id"]'
    )

    client_id = app_id_input.get_attribute("value")
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip("=")

    params = {
        "response_type": "code",
        "client_id": client_id,
        "scope": "video,wall,groups",
        "redirect_uri": REDIRECT_URI,
        "state": "12345",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    auth_url = "https://id.vk.com/authorize?" + urlencode(params)

    driver.get(auth_url)
    url = driver.current_url

    params = parse_qs(urlparse(url).query)

    authorization_code = params["code"][0]
    device_id = params["device_id"][0]

    get_tokens(TOKENS_FILE, client_id, authorization_code, code_verifier, device_id, REDIRECT_URI)