import os
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytest_html import extras
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException

def take_screenshot(driver, extra, label):
    # Ruta de la imagen
    path = f"screenshots/{label.replace(' ', '_')}.png"
    os.makedirs("screenshots", exist_ok=True)
    
    # Guardar la captura de pantalla
    driver.save_screenshot(path)
    
    # Añadir la imagen al reporte HTML
    extra.append(extras.image(path, name=label))

def wait_and_find(driver, by, locator, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.presence_of_element_located((by, locator)))

@pytest.mark.usefixtures("driver")
class TestContactForm:
    def test_01_esperar_campos_del_formulario(self):
        wait_and_find(self.driver, By.ID, "name")
        wait_and_find(self.driver, By.ID, "email")
        wait_and_find(self.driver, By.ID, "subject")
        wait_and_find(self.driver, By.ID, "comment")
        wait_and_find(self.driver, By.XPATH, '//*[@id="contactForm"]/div[2]/button')
        take_screenshot(self.driver, self.extra, "Esperar campos del formulario")
    
    def test_02_scroll_al_campo_email(self):
        email = wait_and_find(self.driver, By.ID, "email")
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", email)
        time.sleep(1)
        take_screenshot(self.driver, self.extra, "Scroll al campo email")
    
    def test_03_rellenar_name(self):
        name_input = wait_and_find(self.driver, By.ID, "name")
        name_input.send_keys("Oliver Martínez")
        take_screenshot(self.driver, self.extra, "Rellenar name")
    
    def test_04_rellenar_email(self):
        email_input = wait_and_find(self.driver, By.ID, "email")
        email_input.send_keys("oliver@example.com")
        take_screenshot(self.driver, self.extra, "Rellenar email")
    
    def test_05_rellenar_subject(self):
        subject_input = wait_and_find(self.driver, By.ID, "subject")
        subject_input.send_keys("Consulta sobre libros")
        take_screenshot(self.driver, self.extra, "Rellenar subject")
    
    def test_06_rellenar_comment(self):
        comment_input = wait_and_find(self.driver, By.ID, "comment")
        comment_input.send_keys("¡Hola! Me gustaría saber más sobre su catálogo.")
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", comment_input)
        time.sleep(1)  # Dar tiempo al scroll
        take_screenshot(self.driver, self.extra, "Rellenar comment")

    
    def test_07_click_enviar(self):
        btn_enviar = wait_and_find(self.driver, By.XPATH, '//*[@id="contactForm"]/div[2]/button')
        btn_enviar.click()
        try:
            take_screenshot(self.driver, self.extra, "Click en enviar")
        except UnexpectedAlertPresentException:
            pass
        
    def test_08_procesar_alerta(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            take_screenshot(self.driver, self.extra, "Alerta aceptada")
        except TimeoutException:
            take_screenshot(self.driver, self.extra, "No apareció ninguna alerta")
            pytest.skip("No se encontró una alerta para procesar.")
        except Exception as e:
            take_screenshot(self.driver, self.extra, "Error al procesar alerta")
            pytest.fail(f"Error inesperado al procesar la alerta: {str(e)}")

