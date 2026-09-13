import logging
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from logging_config import setup_logging
from vk.app import check_vk_app, create_vk_app
from vk.oauth import generate_pkce, get_auth_url, get_tokens, parse_authorization_url

APP_NAME = "VK Video Views"
DOMAIN_NAME = "vk.com"
REDIRECT_URI = "https://oauth.vk.com/blank.html"
TOKENS_FILE = "tokens.json"

setup_logging()
logger = logging.getLogger(__name__)

driver = webdriver.Chrome()

try:
    # Авторизация в профиле ВК
    logger.info("Открытие сайта VK ID")

    driver.get("https://id.vk.com/about/business/go")
    input("Авторизуйся в профиле ВК, разреши доступ и нажми Enter...")

    logger.info("Проверка наличия VK-приложения с соответствующим названием")
    vk_app_exist = check_vk_app(driver, APP_NAME)

    if vk_app_exist:
        logger.info("Копирование ID приложения")
        app_id_div = driver.find_element(
            By.CSS_SELECTOR,
            "div[class^='styles_id']"
        )

        client_id = re.search(r"\d+", app_id_div.text).group()
    else:
        logger.info("Создание VK-приложения")
        create_vk_app(driver, APP_NAME, DOMAIN_NAME, REDIRECT_URI)

        logger.info("Копирование ID приложения")
        app_id_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'input[name="id"]')
            )
        )

        client_id = app_id_input.get_attribute("value")

    code_verifier, code_challenge = generate_pkce()

    logger.info("Получение OAuth-ссылки")
    auth_url = get_auth_url(client_id, REDIRECT_URI, code_challenge)

    logger.info("Открытие OAuth-ссылки")
    driver.get(auth_url)
    print("Разрешите доступ в открывшемся окне браузера")

    WebDriverWait(driver, 300).until(
        lambda driver: "oauth.vk.com/blank.html" in driver.current_url
    )

    url = driver.current_url
    authorization_code, device_id = parse_authorization_url(url)

    logger.info("Получение токенов")
    get_tokens(TOKENS_FILE, client_id, authorization_code, code_verifier, device_id, REDIRECT_URI)

except Exception as e:
    logger.error("Программа завершилась ошибкой: %s", e.msg)

finally:
    driver.quit()