import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from utils import UTILS

@pytest.mark.usefixtures("driver")
class TestAuthorsList:
    def highlight_element(self, element, style="border: 3px solid #4CAF50; background: #FFEB3B;"):
        original_style = element.get_attribute("style")
        self.driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element, f"{original_style or ''}; {style}"
        )
        return original_style

    def test_listado_autores(self):
        actions = ActionChains(self.driver)
        self.driver.get("http://biblioteca.infy.uk/authors.php")
        extra = self.extra

        # Esperar carga inicial
        UTILS.wait_and_find(self.driver, By.CLASS_NAME, "team-member")
        UTILS.take_screenshot(self.driver, extra, "00_pagina_cargada", "Authors")

        # Resaltar y validar encabezado
        encabezado = self.driver.find_element(By.XPATH, '//h2[contains(., "Autores")]')
        
        # Scroll suave al encabezado
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
            encabezado
        )
        time.sleep(1)
        
        # Resaltado y captura
        original_style = self.highlight_element(encabezado)
        total_claim = encabezado.text.split("[")[1].split("]")[0]
        UTILS.take_screenshot(self.driver, extra, "01_encabezado_resaltado", "Authors")
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", encabezado, original_style)

        # Validar cantidad de autores
        autores = self.driver.find_elements(By.CLASS_NAME, "team-member")
        assert len(autores) == int(total_claim), f"Autores mostrados: {len(autores)} vs Declarados: {total_claim}"
        UTILS.take_screenshot(self.driver, extra, "02_cantidad_validada", "Authors")

        # Validar cada autor
        for idx, autor in enumerate(autores):
            # Scroll suave al autor
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                autor
            )
            time.sleep(0.5)
            
            # Efecto hover y resaltado
            actions.move_to_element(autor).pause(0.5).perform()
            original_style_autor = self.highlight_element(autor, "border: 2px solid #2196F3;")
            
            # Validar nombre
            nombre_elemento = autor.find_element(By.TAG_NAME, "h4")
            assert nombre_elemento.text.strip() != "", f"Autor #{idx+1} sin nombre"
            
            # Captura con resaltado
            UTILS.take_screenshot(self.driver, extra, f"03_autor_{idx+1}_hover", "Authors")
            self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", autor, original_style_autor)

        UTILS.take_screenshot(self.driver, extra, "04_prueba_completada", "Authors")