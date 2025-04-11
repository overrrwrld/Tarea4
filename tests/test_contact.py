import time
import pytest
from selenium.webdriver.common.by import By
from utils import UTILS

@pytest.mark.usefixtures("driver")
class TestContactForm:
    def test_formulario_completo(self):
        # Esperar campos
        name_input = UTILS.wait_and_find(self.driver, By.ID, "name")
        email_input = UTILS.wait_and_find(self.driver, By.ID, "email")
        subject_input = UTILS.wait_and_find(self.driver, By.ID, "subject")
        comment_input = UTILS.wait_and_find(self.driver, By.ID, "comment")
        btn_enviar = UTILS.wait_and_find(self.driver, By.XPATH, '//*[@id="contactForm"]/div[2]/button')
        UTILS.take_screenshot(self.driver, self.extra, "Campos cargados", "Contact")

        # Scroll al campo email
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", email_input)
        time.sleep(1)
        UTILS.take_screenshot(self.driver, self.extra, "Scroll al campo email", "Contact")

        # Rellenar el formulario
        name_input.send_keys("Oliver Martínez")
        email_input.send_keys("oliver@example.com")
        subject_input.send_keys("Consulta sobre libros")
        comment_input.send_keys("¡Hola! Me gustaría saber más sobre su catálogo.")
        UTILS.take_screenshot(self.driver, self.extra, "Formulario rellenado", "Contact")

        # Click en enviar
        btn_enviar.click()
        time.sleep(1)
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            UTILS.take_screenshot(self.driver, self.extra, "Alerta aceptada", "Contact")
        except Exception as e:
            UTILS.take_screenshot(self.driver, self.extra, f"Error de alerta: {str(e)}", "Contact")
