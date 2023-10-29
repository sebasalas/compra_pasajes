import glob
import logging
import os
import shutil
import unittest
from time import sleep
import subprocess
import json

from pyunitreport import HTMLTestRunner
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from utils.var_pasajes import (
    day_map,
    dictpasaje,
    var_apellido,
    var_banco,
    var_banco_password,
    var_banco_rut,
    var_card_number_deb,
    var_ciudad,
    var_email,
    var_email2,
    var_hora_ida,
    var_hora_vuelta,
    var_hora_vuelta_v,
    var_mes_siguiente,
    var_nombre,
    var_numero_pasaje_ida,
    var_numero_pasaje_vuelta,
    var_rut,
    var_semana,
    var_src,
    var_src,
    var_telefono,
    var_trg,
    var_trg,
    var_url,
)


# Define your get_password function here
def get_1password(item_name):
    try:
        command = f'op read {item_name}'
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        try:
            # Try to parse the output as JSON
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            # If parsing as JSON fails, return the raw output
            data = result.stdout.strip()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Usage: retrieve the card number from 1Password
var_card_number_deb = str(get_1password('op://Dev/var_pasajes.py/values/var_card_number_deb'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='test_log.log', filemode='w')

NOT_FOUND_ERROR_MSG = "Element with '{}' '{}' was not found."
CLICKABLE_ERROR_MSG = "Element with '{}' '{}' was not clickable after {} seconds."
CSS_SELECTOR_DEB_CONTINUAR = 'body > app-root > app-home > main-panel > main > section > right-panel > app-tarjeta > form > button'
XPATH_MES_SIGUIENTE = '/html/body/div[4]/div/a[2]'
RUT_LABEL = "Rut: {}"
FIN_PAGINA_5 = "FIN PAGINA 5"

class CompraPasajes(unittest.TestCase):

    def setUp(self):
        logging.info("Configurando test")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver = self.driver
        driver.implicitly_wait(10)
        driver.get(var_url)
        driver.maximize_window()
        logging.info("Test configurado OK")

    def test_comprar_pasajes(self):
        logging.info("Comenzando test_comprar_pasajes")
        driver = self.driver
        
        logging.info("INICIO PAGINA 1 (Buscar Horarios o Compra de Pasajes)")
        # Selecciona opción de Ida y Vuelta (radio)
        try:
            ida_vuelta = driver.find_element(By.XPATH, '/html/body/section[1]/div[2]/div[2]/div/div/ul/li[2]/div/label')
        except NoSuchElementException:
            logging.error(NOT_FOUND_ERROR_MSG.format('XPATH', '/html/body/section[1]/div[2]/div[2]/div/div/ul/li[2]/div/label'))
            raise
        ida_vuelta.click()
        logging.info("Selected Ida y Vuelta option")

        # Despliega opciones de ciudad de origen (select)
        try:
            origen = driver.find_element(By.ID, 'ciudadOrigen')
        except NoSuchElementException:
            logging.error(NOT_FOUND_ERROR_MSG.format('ID', 'ciudadOrigen'))
            raise
        origen.click()
        # Selecciona Rancagua
        try:
            rancagua = driver.find_element(By.XPATH, '/html/body/section[1]/div[2]/div[2]/div/div/div/div[1]/div/select/option[6]')
        except NoSuchElementException:
            logging.error(NOT_FOUND_ERROR_MSG.format('XPATH', '/html/body/section[1]/div[2]/div[2]/div/div/div/div[1]/div/select/option[6]'))
            raise
        rancagua.click()
        logging.info("Selected Rancagua como ciudad de origen")
        # Despliega opciones de ciudad de destino (select)
        try:
            destino = driver.find_element(By.ID, 'ciudadDestino')
        except NoSuchElementException:
            logging.error(NOT_FOUND_ERROR_MSG.format('ID', 'ciudadDestino'))
            raise
        destino.click()
        # Selecciona Santiago
        try:
            santiago = driver.find_element(By.XPATH, '/html/body/section[1]/div[2]/div[2]/div/div/div/div[2]/div/select/option[4]')
        except NoSuchElementException:
            logging.error(NOT_FOUND_ERROR_MSG.format('XPATH', '/html/body/section[1]/div[2]/div[2]/div/div/div/div[2]/div/select/option[4]'))
            raise
        santiago.click()
        logging.info("Selected Santiago como ciudad de destino")

        # Despliega calendario de Fecha Ida
        try:
            fecha_ida = driver.find_element(By.ID, 'fechaIda')
        except NoSuchElementException:
            logging.error(NOT_FOUND_ERROR_MSG.format('ID', 'fechaIda'))
            raise
        fecha_ida.click()

        # Selecciona mes siguiente si es necesario cambiar calendario
        if var_mes_siguiente == 1:
            try:
                mes_siguiente_ida = driver.find_element(By.XPATH, XPATH_MES_SIGUIENTE)
            except NoSuchElementException:
                logging.error(NOT_FOUND_ERROR_MSG.format('XPATH', XPATH_MES_SIGUIENTE))
                raise
            logging.info("Selected mes siguiente ida")
            mes_siguiente_ida.click()

        # Selecciona Fecha de Ida
        try:
            dia_ida = driver.find_element(By.XPATH, f'/html/body/div[4]/table/tbody/tr[{semana}]/td[{dia}]/a')
        except NoSuchElementException:
            logging.error(NOT_FOUND_ERROR_MSG.format('XPATH', f'/html/body/div[4]/table/tbody/tr[{semana}]/td[{dia}]/a'))
            raise
        dia_ida.click()
        logging.info("Selected fecha de ida")

        # Despliega calendario de Fecha Vuelta
        try:
            fecha_vuelta = driver.find_element(By.ID, 'fechaVuelta')
        except NoSuchElementException:
            logging.error(NOT_FOUND_ERROR_MSG.format('ID', 'fechaVuelta'))
            raise
        fecha_vuelta.click()

        # Selecciona mes siguiente si es necesario cambiar calendario
        if var_mes_siguiente == 1:
            try:
                mes_siguiente_vuelta = driver.find_element(By.XPATH, XPATH_MES_SIGUIENTE)
            except NoSuchElementException:
                logging.error(NOT_FOUND_ERROR_MSG.format('XPATH', XPATH_MES_SIGUIENTE))
                raise
            logging.info("Selected mes siguiente vuelta")
            mes_siguiente_vuelta.click()

        # Selecciona Fecha de Vuelta (Actualmente mismo día de ida)
        try:
            dia_vuelta = driver.find_element(By.XPATH, f'/html/body/div[4]/table/tbody/tr[{semana}]/td[{dia}]/a')
        except NoSuchElementException:
            logging.error(NOT_FOUND_ERROR_MSG.format('XPATH', f'/html/body/div[4]/table/tbody/tr[{semana}]/td[{dia}]/a'))
            raise
        dia_vuelta.click()
        logging.info("Selected fecha de vuelta")

        # Click en Comprar Pasaje
        try:
            boton_comprar_pasaje = driver.find_element(By.ID, 'btnBuscarViaje')
        except NoSuchElementException:
            logging.error(NOT_FOUND_ERROR_MSG.format('ID', 'btnBuscarViaje'))
            raise
        boton_comprar_pasaje.click()
        logging.info("FIN PAGINA 1")

        logging.info("INICIO PAGINA 2 (Lista de horarios)")
        # Selecciona hora de ida (radio)
        hora_ida = var_hora_ida
        logging.info(f"Hora de ida: {hora_ida}")
        xpath_hora_ida = f"//table[@id='IdTable']//td[text()='{hora_ida}']/preceding-sibling::td/input[@type='radio']"
        logging.debug(f"Waiting for element with XPath: {xpath_hora_ida}")
        try:
            hora_ida_radio = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_hora_ida)))
        except TimeoutException:
            logging.error(CLICKABLE_ERROR_MSG.format('XPATH', xpath_hora_ida, 10))
            raise
        
        hora_ida_radio.click()
        logging.info("Selected hora de ida")
        
        # Si es viernes, se asigna horario vuelta a las 17:30, de lo contrario, a las 18:30
        if (dia == 5):
            hora_vuelta = var_hora_vuelta_v
        else:
            hora_vuelta = var_hora_vuelta
        logging.info(f"hora de vuelta: {hora_vuelta}")

        # Selecciona hora de vuelta (radio)
        xpath_hora_vuelta = f"//table[@id='IdTable1']//td[text()='{hora_vuelta}']/preceding-sibling::td/input[@type='radio']"
        hora_vuelta_radio = driver.find_element(By.XPATH, f'{xpath_hora_vuelta}')
        hora_vuelta_radio.click()
        logging.info("Selected hora de vuelta")

        # Click en Siguiente
        boton_siguiente_horario = driver.find_element(By.ID, 'btnSiguientePaso1')
        boton_siguiente_horario.click()
        logging.info("FIN PAGINA 2")

        logging.info("INICIO PAGINA 3 (Tabla de asientos)")
        # Se asinga valor a entregar según el número de pasaje, diccionario dictpasaje
        # Selecciona asiento de ida
        logging.debug(f"Waiting for element with XPath: '/html/body/div[4]/section/div[2]/div[2]/div/div/section[2]/div[1]/div[1]/div/div[2]/div/div/div[1]/{dictpasaje[numero_pasaje_ida]}'")
        try:
            pasaje_ida = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[4]/section/div[2]/div[2]/div/div/section[2]/div[1]/div[1]/div/div[2]/div/div/div[1]/{dictpasaje[numero_pasaje_ida]}')))
        except TimeoutException:
            logging.error(CLICKABLE_ERROR_MSG.format('XPATH', f'/html/body/div[4]/section/div[2]/div[2]/div/div/section[2]/div[1]/div[1]/div/div[2]/div/div/div[1]/{dictpasaje[numero_pasaje_ida]}', 10))
            raise
        pasaje_ida.click()
        logging.info(f"Selected asiento de ida: {numero_pasaje_ida}")
        # Selecciona asiento de vuelta
        pasaje_vuelta = driver.find_element(By.XPATH, f'/html/body/div[4]/section/div[2]/div[2]/div/div/section[2]/div[1]/div[2]/div/div[2]/div/div/div[1]/{dictpasaje[numero_pasaje_vuelta]}')
        pasaje_vuelta.click()
        logging.info(f"Selected asiento de vuelta: {numero_pasaje_vuelta}")

        # Click en Siguiente
        boton_siguiente_asientos = driver.find_element(By.ID, 'btnSiguientePaso2')
        boton_siguiente_asientos.click()
        logging.info("FIN PAGINA 3")

        logging.info("INICIO PAGINA 4 (Detalle de venta y datos personales)")
        # Despliega opciones de subida ida (select)
        logging.debug("Waiting for element with ID: 'lugarSubida1'")
        try:
            subida_ida = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'lugarSubida1')))
        except TimeoutException:
            logging.error(CLICKABLE_ERROR_MSG.format('ID', 'lugarSubida1', 10))
            raise
        subida_ida.click()
        # Selecciona Shopping
        shopping = driver.find_element(By.XPATH, '/html/body/div[4]/section/div[2]/div[2]/div/div/section[3]/div[1]/div/div/div[2]/div/div[1]/table/tbody/tr[1]/td[9]/b/select/option[4]')
        shopping.click()
        logging.info("Selected Shopping como lugar de subida de ida")

        # Despliega opciones de subida vuelta (select)
        subida_vuelta = driver.find_element(By.ID, 'lugarSubida2')
        subida_vuelta.click()
        # Selecciona Bellavista
        bellavista = driver.find_element(By.XPATH, '/html/body/div[4]/section/div[2]/div[2]/div/div/section[3]/div[1]/div/div/div[2]/div/div[1]/table/tbody/tr[2]/td[9]/b/select/option[2]')
        bellavista.click()
        logging.info("Selected Bellavista como lugar de subida de vuelta")

        # Asigna elementos del formulario Datos Personales
        nombre = driver.find_element(By.ID, 'nombre')
        apellido = driver.find_element(By.ID, 'apellido')
        rut = driver.find_element(By.ID, 'rut')
        email = driver.find_element(By.ID, 'email')
        email2 = driver.find_element(By.ID, 'email2')
        telefono = driver.find_element(By.ID, 'telefono')
        ciudad = driver.find_element(By.ID, 'ciudad')

        # Limpia valores
        nombre.clear()
        apellido.clear()
        rut.clear()
        email.clear()
        email2.clear()
        telefono.clear()
        ciudad.clear()

        # Se asignan valores de acuerdo a archivo externo var_pasajes.py
        nombre.send_keys(var_nombre)
        apellido.send_keys(var_apellido)
        rut.send_keys(var_rut)
        email.send_keys(var_email)
        email2.send_keys(var_email2)
        telefono.send_keys(var_telefono)
        ciudad.send_keys(var_ciudad)

        logging.debug("Nombre: {}".format(nombre.get_attribute('value')))
        logging.debug("Apellido: {}".format(apellido.get_attribute('value')))
        logging.debug(RUT_LABEL.format(rut.get_attribute('value')))
        logging.debug("Email: {}".format(email.get_attribute('value')))
        logging.debug("Email2: {}".format(email2.get_attribute('value')))
        logging.debug("Telefono: {}".format(telefono.get_attribute('value')))
        logging.debug("Ciudad: {}".format(ciudad.get_attribute('value')))
        logging.info("Entered datos personales")

        # Marca checkbox de aceptación de términos y condiciones
        acepta_condiciones = driver.find_element(By.XPATH, '/html/body/div[4]/section/div[2]/div[2]/div/div/section[3]/div[2]/div[1]/div[1]/div[8]/label')
        acepta_condiciones.click()
        logging.info("Accepted terms and conditions")

        # Selecciona radio de "Yo imprimiré mi(s) Boleto(s)"
        imprime_pasajes = driver.find_element(By.XPATH, '/html/body/div[4]/section/div[2]/div[2]/div/div/section[3]/div[2]/div[1]/div[2]/ul[1]/li[1]/div/label')
        imprime_pasajes.click()
        logging.info("Selected imprime pasajes")

        # Cerrar el modal emergente
        current_handle = driver.current_window_handle
        all_handles = driver.window_handles
        for handle in all_handles:
            if handle != current_handle:
                driver.switch_to.window(handle)
                logging.info("Switched to modal window")
                driver.close()
                logging.info("Closed modal window")
        # Volver a dar foco a ventana principal
        driver.switch_to.window(current_handle)

        # Click en Pague y Compre ahora
        boton_pagar = driver.find_element(By.ID, 'btnVtnFinal')
        boton_pagar.click()
        logging.info("FIN PAGINA 4")

        logging.info("INICIO PAGINA 5 (Webpay)")
        # Selecciona forma de pago
        logging.debug("Waiting for element with ID: 'tarjetas'")
        try:
            boton_tarjetas = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'tarjetas')))
        except TimeoutException:
            logging.error(CLICKABLE_ERROR_MSG.format('ID', 'tarjetas', 10))
            raise
        boton_tarjetas.click()
        logging.info("Selected tarjetas")
        # Código sólo para débito
        logging.debug("Waiting for element with ID: 'card-number'")
        try:
            card_number_deb = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'card-number')))
        except TimeoutException:
            logging.error(CLICKABLE_ERROR_MSG.format('ID', 'card-number', 10))
            raise
        # Limpia valor
        card_number_deb.clear()
        # Se ingresa número de tarjeta
        card_number_deb.send_keys(var_card_number_deb, Keys.TAB)
        full_card_number = card_number_deb.get_attribute('value')
        masked_card_number = "XXXX XXXX XXXX " + full_card_number[-4:]
        logging.debug("Card number: {}".format(masked_card_number))
        logging.info("Entered card number")

        if(var_banco == "1"):
            logging.info("Selected Banco Itau")
            logging.info(FIN_PAGINA_5)
            logging.info("INICIO PAGINA 6 (Banco Itau)")

            sleep(2)

            try:
                deb_continuar = driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR_DEB_CONTINUAR)
            except NoSuchElementException:
                logging.error(NOT_FOUND_ERROR_MSG.format('CSS_SELECTOR', CSS_SELECTOR_DEB_CONTINUAR))
                raise
            deb_continuar.click()
            sleep(10)
            logging.info(FIN_PAGINA_5)
            # Asigna elemento de rut
            try:
                rut_cliente = driver.find_element(By.ID, 'rutCliente')
            except NoSuchElementException:
                logging.error(NOT_FOUND_ERROR_MSG.format('ID', 'rutCliente'))
                raise
            # Limpia valor
            rut_cliente.clear()
            # Se ingresa rut
            rut_cliente.send_keys(var_banco_rut)
            logging.debug(RUT_LABEL.format(rut_cliente.get_attribute('value')))
            logging.info("Entered rut")
            # Click en continuar
            try:
                boton_continuar = driver.find_element(By.ID, 'btnIngresar')
            except NoSuchElementException:
                logging.error(NOT_FOUND_ERROR_MSG.format('ID', 'btnIngresar'))
                raise
            boton_continuar.click()
            # Asigna elemento de clave dinámica
            logging.debug("Waiting for element with ID: 'pinVisible'")
            try:
                clave_dinamica = WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.ID, 'pinVisible')))
            except TimeoutException:
                logging.error(CLICKABLE_ERROR_MSG.format('ID', 'pinVisible', 10))
                raise
            # Limpia valor
            clave_dinamica.clear()
            # Se ingresa clave dinámica vía terminal
            dinamica = input('Clave dinámica: ')
            clave_dinamica.send_keys(dinamica, Keys.TAB)
            logging.debug("Clave dinámica: {}".format(clave_dinamica.get_attribute('value')))
            logging.debug("Entered clave dinámica")
            # Click en continuar
            try:
                aceptar_dinamica = driver.find_element(By.ID, 'btnAutorizar')
            except NoSuchElementException:
                logging.error(NOT_FOUND_ERROR_MSG.format('ID', 'btnAutorizar'))
                raise
            aceptar_dinamica.click()

        elif(var_banco == "2"):
            logging.info("Selected Banco Scotiabank")
            logging.info(FIN_PAGINA_5)
            logging.info("INICIO PAGINA 6 (Banco Scotiabank)")

            sleep(1)
            try:
                rut_deb = driver.find_element(By.ID, 'card-dni')
            except NoSuchElementException:
                logging.error(NOT_FOUND_ERROR_MSG.format('ID', 'card-dni'))
                raise
            rut_deb.clear()
            rut_deb.send_keys(var_banco_rut, Keys.TAB)
            logging.debug("Rut 1: {}".format(rut_deb.get_attribute('value')))
            logging.info("Entered rut 1")

            sleep(1)
            try:
                deb_continuar = driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR_DEB_CONTINUAR)
            except NoSuchElementException:
                logging.error(NOT_FOUND_ERROR_MSG.format('CSS_SELECTOR', CSS_SELECTOR_DEB_CONTINUAR))
                raise
            deb_continuar.click()
            logging.info("INICIO PAGINA 6 (Banco scotiabank)")
            # sleep(10)
            # Asigna elemento de rut
            logging.debug("Waiting for element with ID: 'rut'")
            try:
                rut_cliente = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, 'rut')))
            except TimeoutException:
                logging.error(CLICKABLE_ERROR_MSG.format('ID', 'rut', 10))
                raise
            # Limpia valor
            rut_cliente.clear()
            # Se ingresa rut
            rut_cliente.send_keys(var_banco_rut)
            logging.debug("Rut 2: {}".format(rut_cliente.get_attribute('value')))
            logging.info("Entered rut 2")
            # Asigna elemento de password
            try:
                password_cliente = driver.find_element(By.NAME, 'pin')
            except NoSuchElementException:
                logging.error(NOT_FOUND_ERROR_MSG.format('NAME', 'pin'))
                raise
            # Limpia valor
            password_cliente.clear()
            # Se ingresa password
            password_cliente.send_keys(var_banco_password)
            logging.debug("Password: [MASKED FOR SECURITY]")
            logging.info("Entered password")
            # Click en continuar
            try:
                boton_continuar = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/form/div[7]/button[1]')
            except NoSuchElementException:
                logging.error(NOT_FOUND_ERROR_MSG.format('XPATH', '/html/body/div/div[2]/div/form/div[7]/button[1]'))
                raise
            boton_continuar.click()

            # Autorizar transacción
            logging.debug("Waiting for element with XPATH: '/html/body/div[1]/div[2]/div/form/div/div/div[1]/button'")
            try:
                boton_autorizar = WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/form/div/div/div[1]/button')))
            except TimeoutException:
                logging.error(CLICKABLE_ERROR_MSG.format('XPATH', '/html/body/div[1]/div[2]/div/form/div/div/div[1]/button', 50))
                raise
            boton_autorizar.click()

        else:
            logging.info("Selected MACH")
            
            sleep(1)
            try:
                rut_deb = driver.find_element(By.ID, 'card-dni')
            except NoSuchElementException:
                logging.error(NOT_FOUND_ERROR_MSG.format('ID', 'card-dni'))
                raise
            rut_deb.clear()
            rut_deb.send_keys(var_banco_rut, Keys.TAB)
            logging.debug(RUT_LABEL.format(rut_deb.get_attribute('value')))
            logging.info("Entered rut")

            sleep(1)
            try:
                deb_continuar = driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR_DEB_CONTINUAR)
            except NoSuchElementException:
                logging.error(NOT_FOUND_ERROR_MSG.format('CSS_SELECTOR', CSS_SELECTOR_DEB_CONTINUAR))
                raise
            logging.info(FIN_PAGINA_5)
            logging.info("INICIO PAGINA 6 (MACH)")
            deb_continuar.click()

        logging.info("FIN PAGINA 6")
        logging.info("INICIO PAGINA 7 (Comprobante)")

        src = var_src
        trg = var_trg
        logging.debug(f"src: {src}, trg: {trg}")

        # Attempt the download and file move up to three times
        for attempt in range(1, 4):
            logging.info(f"Attempt {attempt} to download and move file")

            # Elimina los archivos que comienzan con "Comprobante*" en la carpeta origen
            for f in glob.glob(os.path.join(src, "Comprobante*")):
                if os.path.isfile(f):
                    os.remove(f)
                    logging.info("Removed files")

            # Asigna elemento botón de descarga de pdf
            logging.debug("Waiting for element with XPATH: '/html/body/div[3]/section/div[2]/div[2]/div/section/div/div[1]/div/div/div/table/tbody/tr[9]/td/a/span'")
            try:
                descargar_pdf = WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/section/div[2]/div[2]/div/section/div/div[1]/div/div/div/table/tbody/tr[9]/td/a/span')))
            except TimeoutException:
                logging.error(CLICKABLE_ERROR_MSG.format('XPATH', '/html/body/div[3]/section/div[2]/div[2]/div/section/div/div[1]/div/div/div/table/tbody/tr[9]/td/a/span', 120))
                continue  # Skip the rest of this loop iteration and try again
            
            descargar_pdf.click()
            logging.info("Clicked descargar pdf")

            sleep(3)

            # Encuentra el archivo que cumple con el patrón "Comprobante*" y lo mueve a la carpeta destino
            files = glob.glob(os.path.join(src, "Comprobante*"))
            success = False  # Flag to indicate success
            try:
                if len(files) == 1:
                    file = files[0]
                    if os.path.isfile(file):
                        # Rename the file before moving it
                        new_file_name = f"{day_map[dia]}.pdf"
                        logging.debug(f"new_file_name is {new_file_name}")
                        new_file_path = os.path.join(trg, new_file_name)
                        shutil.move(file, new_file_path)
                        logging.debug(f"Renamed file {file} to {new_file_name} and copied to {trg}")
                        logging.info("Moved file to destino")
                        success = True  # Set success flag to True
            except Exception as e:
                logging.error(f"Error al mover el archivo: {e}")
                sleep(3)

            if success:
                logging.info("Download and file move successful")
                break  # Break out of the loop early if successful
            else:
                logging.info("Download and file move unsuccessful, retrying...")

        if not success:
            logging.error("Failed to download and move file after 3 attempts")
        

    def tearDown(self):
        logging.info("Tearing down the test")
        self.driver.close()


if __name__ == "__main__":
    # dia: 1-5 (lunes a viernes)
    while True:
        dia_str = input('Día de la semana (1-5): ')
        try:
            dia = int(dia_str)
            if 1 <= dia <= 5:
                break
            else:
                print("Entrada no válida: Por favor, introduce un número entre 1 y 5 inclusive")
                logging.debug("invalid dia range")
        except ValueError:
            print("Entrada no válida: Por favor, introduce un valor numérico")
            logging.debug("invalid dia format")
    logging.debug(f"dia selected: {dia}")
    # semana: 1-6 (según fila en calendario)
    semana = var_semana
    logging.debug(f"semana selected: {semana}")
    numero_pasaje_ida = var_numero_pasaje_ida
    logging.debug(f"numero_pasaje_ida selected: {numero_pasaje_ida}")
    numero_pasaje_vuelta = var_numero_pasaje_vuelta
    logging.debug(f"numero_pasaje_vuelta selected: {numero_pasaje_vuelta}")
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output='reportes', report_name='pasajes-report'))
