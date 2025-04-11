import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import UTILS

@pytest.mark.usefixtures("driver")
class TestScrollSections:
    base_url = "http://biblioteca.infy.uk"
    
    def test_scroll_and_highlight_flow(self):
        paginas = ["/index.php", "/authors.php", "/contact.php"]
        
        for pagina in paginas:
            # Navegar a la página
            self.driver.get(f"{self.base_url}{pagina}")
            extra = self.extra
            wait = WebDriverWait(self.driver, 15)
            
            # === Scroll a section-heading ===
            seccion = wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "section-heading")
            ))
            
            # Scroll suave y resaltado
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});"
                "arguments[0].style.boxShadow = '0 0 15px 5px rgba(255,215,0,0.7)';",
                seccion
            )
            time.sleep(1.5)
            UTILS.take_screenshot(self.driver, extra, 
                                f"01_scroll_{pagina.replace('/', '')}", 
                                "ScrollHighlight")
            
            # === Click en botón Librería ===
            boton = wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, "navbar-brand")
            ))
            
            # Resaltar antes de clic
            self.driver.execute_script(
                "arguments[0].style.outline = '3px solid #00ff00'", 
                boton
            )
            UTILS.take_screenshot(self.driver, extra, 
                                f"02_pre_click_{pagina.replace('/', '')}", 
                                "ScrollHighlight")
            
            # Acción de clic
            boton.click()
            
            # Validar redirección
            wait.until(EC.url_to_be(f"{self.base_url}/index.php"))
            
            # Resaltar botón en nueva página
            boton_redirigido = wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "navbar-brand")
            ))
            self.driver.execute_script(
                "arguments[0].style.animation = 'glow 2s infinite';"
                "arguments[0].style.border = '2px solid #ff0000';",
                boton_redirigido
            )
            UTILS.take_screenshot(self.driver, extra, 
                                f"03_post_click_{pagina.replace('/', '')}", 
                                "ScrollHighlight")