import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import UTILS

@pytest.mark.usefixtures("driver")
class TestNavigation:
    base_url = "http://biblioteca.infy.uk"
    
    def test_navegacion_desktop(self):
        self.driver.get(f"{self.base_url}/index.php")
        self._probar_enlaces("desktop")

    def test_navegacion_mobile(self):
        self.driver.get(f"{self.base_url}/index.php")
        self.driver.set_window_size(375, 812)
        self._abrir_menu_movil()
        self._probar_enlaces("mobile")

    def _abrir_menu_movil(self):
        """Abre el menú hamburguesa una sola vez"""
        wait = WebDriverWait(self.driver, 10)
        hamburger = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "navbar-toggler")))
        hamburger.click()
        wait.until(EC.visibility_of_element_located((By.ID, "navbarResponsive")))
        UTILS.take_screenshot(self.driver, self.extra, "menu_movil_abierto", "Navigation")

    def _probar_enlaces(self, mode):
        """Lógica central simplificada"""
        menu_items = {
            "Libros": f"{self.base_url}/index.php",
            "Autores": f"{self.base_url}/authors.php",
            "Contacto": f"{self.base_url}/contact.php"
        }

        for texto, url in menu_items.items():
            # Selector preciso para ambos modos
            xpath = f"//a[contains(@class, 'nav-link') and normalize-space()='{texto}']" 
            
            if mode == "mobile":
                xpath = f"//div[@id='navbarResponsive']{xpath}"  # Enfocado en menú desplegable

            enlace = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, xpath)))
            
            # Resaltado mínimo y navegación directa
            self.driver.execute_script("arguments[0].style.border='3px solid red'", enlace)
            UTILS.take_screenshot(self.driver, self.extra, f"enlace_{texto}_{mode}", "Navigation")
            
            enlace.click()
            
            # Validación definitiva
            WebDriverWait(self.driver, 15).until(EC.url_to_be(url))
            UTILS.take_screenshot(self.driver, self.extra, f"pagina_{texto}_{mode}", "Navigation")

            # Recargar página inicial para siguiente prueba
            self.driver.get(f"{self.base_url}/index.php")
            
            # Reabrir menú solo si es mobile y no es la última iteración
            if mode == "mobile" and texto != "Contacto":
                self._abrir_menu_movil()