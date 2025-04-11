import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from utils import UTILS

@pytest.mark.usefixtures("driver")
class TestBookCatalog:
    def highlight_element(self, element, style="border: 3px solid red; background: yellow;"):
        # Guardar estilo original
        original_style = element.get_attribute("style")
        # Aplicar resaltado
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", 
                                element, f"{original_style or ''}; {style}")
        return original_style

    def test_catalogo_libros(self):
        actions = ActionChains(self.driver)
        self.driver.get("http://biblioteca.infy.uk/index.php")
        extra = self.extra

        # --- Carga inicial ---
        UTILS.wait_and_find(self.driver, By.CLASS_NAME, "portfolio-item")
        UTILS.take_screenshot(self.driver, extra, "00_pagina_cargada", "Catalog")

        # --- Resaltar encabezado con cantidad ---
        encabezado = self.driver.find_element(By.XPATH, '//h2[contains(., "Libros")]')
        
        # Scroll suave al encabezado
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
            encabezado
        )
        time.sleep(1)
        
        # Resaltado y captura
        original_style = self.highlight_element(encabezado)
        UTILS.take_screenshot(self.driver, extra, "01_encabezado_resaltado", "Catalog")
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", 
                                 encabezado, original_style)

        # --- Validar cantidad de libros ---
        libros = self.driver.find_elements(By.CLASS_NAME, "portfolio-item")
        total_claim = encabezado.text.split("[")[1].split("]")[0]
        assert len(libros) == int(total_claim)
        UTILS.take_screenshot(self.driver, extra, "02_cantidad_validada", "Catalog")

        # --- Validar libros con hover ---
        for idx, libro in enumerate(libros):
            # Scroll al libro
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                libro
            )
            time.sleep(0.5)
            
            # Efecto hover
            actions.move_to_element(libro).perform()
            time.sleep(0.8)  # Esperar posibles efectos CSS
            
            # Resaltar libro
            original_libro_style = self.highlight_element(libro, "border: 2px solid blue;")
            UTILS.take_screenshot(self.driver, extra, f"03_libro_{idx+1}_hover", "Catalog")
            
            # Restaurar estilo
            self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", 
                                     libro, original_libro_style)
            
            # Validar datos
            titulo = libro.find_element(By.CLASS_NAME, "portfolio-caption-heading").text
            publicador = libro.find_element(By.CLASS_NAME, "portfolio-caption-subheading").text
            assert titulo and publicador

        UTILS.take_screenshot(self.driver, extra, "04_prueba_completada", "Catalog")