import os
from pytest_html import extras
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UTILS:
    @staticmethod
    def take_screenshot(driver, extra, label, folder):
        # Ruta de la imagen
        path = f"screenshots/{folder}/{label.replace(' ', '_')}.png"
        os.makedirs(f"screenshots/{folder}", exist_ok=True) 
        driver.save_screenshot(path)
        extra.append(extras.image(path, name=label))

    @staticmethod
    def wait_and_find(driver, by, locator, timeout=10):
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.presence_of_element_located((by, locator)))
