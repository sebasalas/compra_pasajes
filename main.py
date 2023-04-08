import glob
import os
import shutil
import unittest
from time import sleep

from pyunitreport import HTMLTestRunner  # pip install pyunitreport
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager

from utils.var_pasajes import *


class CompraPasajes(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver = self.driver
        driver.implicitly_wait(10)
        driver.get(var_url)
        driver.maximize_window()

    def test_comprar_pasajes(self):
        driver = self.driver

        # Selecciona opción de Ida y Vuelta (radio)
        ida_vuelta = driver.find_element(By.XPATH, '/html/body/section[1]/div[2]/div[2]/div/div/ul/li[2]/div/label')
        ida_vuelta.click()

        # Despliega opciones de ciudad de origen (select)
        origen = driver.find_element(By.ID, 'ciudadOrigen')
        origen.click()
        # Selecciona Rancagua
        rancagua = driver.find_element(By.XPATH, '/html/body/section[1]/div[2]/div[2]/div/div/div/div[1]/div/select/option[6]')
        rancagua.click()
        # Despliega opciones de ciudad de destino (select)
        destino = driver.find_element(By.ID, 'ciudadDestino')
        destino.click()
        # Selecciona Santiago
        santiago = driver.find_element(By.XPATH, '/html/body/section[1]/div[2]/div[2]/div/div/div/div[2]/div/select/option[3]')
        santiago.click()

        # Despliega calendario de Fecha Ida
        fecha_ida = driver.find_element(By.ID, 'fechaIda')
        fecha_ida.click()

        # Selecciona mes siguiente si es necesario cambiar calendario
        if var_mes_siguiente == 1:
            mes_siguiente_ida = driver.find_element(By.XPATH, '/html/body/div[4]/div/a[2]')
            mes_siguiente_ida.click()

        # Selecciona Fecha de Ida
        dia_ida = driver.find_element(By.XPATH, f'/html/body/div[4]/table/tbody/tr[{semana}]/td[{dia}]/a')
        dia_ida.click()

        # Despliega calendario de Fecha Vuelta
        fecha_vuelta = driver.find_element(By.ID, 'fechaVuelta')
        fecha_vuelta.click()

        # Selecciona mes siguiente si es necesario cambiar calendario
        if var_mes_siguiente == 1:
            mes_siguiente_vuelta = driver.find_element(By.XPATH, '/html/body/div[4]/div/a[2]')
            mes_siguiente_vuelta.click()

        # Selecciona Fecha de Vuelta (Actualmente mismo día de ida)
        dia_vuelta = driver.find_element(By.XPATH, f'/html/body/div[4]/table/tbody/tr[{semana}]/td[{dia}]/a')
        dia_vuelta.click()

        # Click en Comprar Pasaje
        boton_comprar_pasaje = driver.find_element(By.ID, 'btnBuscarViaje')
        boton_comprar_pasaje.click()

        # Selecciona hora de ida (radio)
        hora_ida = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'radioIda-0')))
        hora_ida.click()

        # Si es viernes, se asigna horario vuelta a las 17:30, de lo contrario, a las 18:30
        if (dia == "5"):
            radio_vuelta = 'radioVuelta-3'
        else:
            radio_vuelta = 'radioVuelta-4'

        # Selecciona hora de vuelta (radio)
        hora_vuelta = driver.find_element(By.ID, f'{radio_vuelta}')
        hora_vuelta.click()

        # Click en Siguiente
        boton_siguiente_horario = driver.find_element(By.ID, 'btnSiguientePaso1')
        boton_siguiente_horario.click()

        # Se asinga valor a entregar según el número de pasaje, diccionario dictpasaje

        # Selecciona asiento de ida
        pasaje_ida = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[4]/section/div[2]/div[2]/div/div/section[2]/div[1]/div[1]/div/div[2]/div/div/div[1]/{dictpasaje[numero_pasaje_ida]}')))
        pasaje_ida.click()

        # Selecciona asiento de vuelta
        pasaje_vuelta = driver.find_element(By.XPATH, f'/html/body/div[4]/section/div[2]/div[2]/div/div/section[2]/div[1]/div[2]/div/div[2]/div/div/div[1]/{dictpasaje[numero_pasaje_vuelta]}')
        pasaje_vuelta.click()

        # Click en Siguiente
        boton_siguiente_asientos = driver.find_element(By.ID, 'btnSiguientePaso2')
        boton_siguiente_asientos.click()

        # Despliega opciones de subida ida (select)
        subida_ida = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'lugarSubida1')))
        subida_ida.click()
        # Selecciona Shopping
        shopping = driver.find_element(By.XPATH, '/html/body/div[4]/section/div[2]/div[2]/div/div/section[3]/div[1]/div/div/div[2]/div/div[1]/table/tbody/tr[1]/td[9]/b/select/option[4]')
        shopping.click()

        # Despliega opciones de subida vuelta (select)
        subida_vuelta = driver.find_element(By.ID, 'lugarSubida2')
        subida_vuelta.click()
        # Selecciona Bellavista
        bellavista = driver.find_element(By.XPATH, '/html/body/div[4]/section/div[2]/div[2]/div/div/section[3]/div[1]/div/div/div[2]/div/div[1]/table/tbody/tr[2]/td[9]/b/select/option[2]')
        bellavista.click()

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

        # Marca checkbox de aceptación de términos y condiciones
        acepta_condiciones = driver.find_element(By.XPATH, '/html/body/div[4]/section/div[2]/div[2]/div/div/section[3]/div[2]/div[1]/div[1]/div[8]/label')
        acepta_condiciones.click()

        # Selecciona radio de "Yo imprimiré mi(s) Boleto(s)"
        imprime_pasajes = driver.find_element(By.XPATH, '/html/body/div[4]/section/div[2]/div[2]/div/div/section[3]/div[2]/div[1]/div[2]/ul[1]/li[1]/div/label')
        imprime_pasajes.click()

        # Cerrar el modal emergente
        current_handle = driver.current_window_handle
        all_handles = driver.window_handles
        for handle in all_handles:
            if handle != current_handle:
                driver.switch_to.window(handle)
                driver.close()
        # Volver a dar foco a ventana principal
        driver.switch_to.window(current_handle)

        # Click en Pague y Compre ahora
        boton_pagar = driver.find_element(By.ID, 'btnVtnFinal')
        boton_pagar.click()

        # Selecciona forma de pago
        boton_tarjetas = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'tarjetas')))
        boton_tarjetas.click()

        # Código sólo para débito
        card_number_deb = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'card-number')))
        card_number_deb.clear()
        # Se ingresa número de tarjeta
        card_number_deb.send_keys(var_card_number_deb, Keys.TAB)

        if(var_banco == "1"):

            sleep(2)
            # Selecciona mes de expiración
            deb_continuar = driver.find_element(By.CSS_SELECTOR, 'body > app-root > app-home > main-panel > main > section > right-panel > app-tarjeta > form > button')
            deb_continuar.click()
            sleep(10)
            # Asigna elemento de rut
            # rut_cliente = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, 'rutCliente')))
            rut_cliente = driver.find_element(By.ID, 'rutCliente')
            # Limpia valor
            rut_cliente.clear()
            # Se ingresa rut
            rut_cliente.send_keys(var_banco_rut)
            # Click en continuar
            boton_continuar = driver.find_element(By.ID, 'btnIngresar')
            boton_continuar.click()

            # Asigna elemento de clave dinámica
            clave_dinamica = WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.ID, 'pinVisible')))
            clave_dinamica.clear()

            # Se ingresa clave dinámica vía terminal
            dinamica = input('Clave dinámica: ')
            clave_dinamica.send_keys(dinamica, Keys.TAB)
            # Click en continuar
            aceptar_dinamica = driver.find_element(By.ID, 'btnAutorizar')
            aceptar_dinamica.click()

        else:

            sleep(1)
            rut_deb = driver.find_element(By.ID, 'card-dni')
            rut_deb.clear()
            rut_deb.send_keys(var_banco_rut, Keys.TAB)

            sleep(1)
            deb_continuar = driver.find_element(By.CSS_SELECTOR, 'body > app-root > app-home > main-panel > main > section > right-panel > app-tarjeta > form > button')
            deb_continuar.click()
            # sleep(10)
            # Asigna elemento de rut
            rut_cliente = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, 'rut')))
            # rut_cliente = driver.find_element(By.ID, 'rut')
            # Limpia valor
            rut_cliente.clear()
            # Se ingresa rut
            rut_cliente.send_keys(var_banco_rut)
            # Asigna elemento de password
            password_cliente = driver.find_element(By.NAME, 'pin')
            # Limpia valor
            password_cliente.clear()
            # Se ingresa password
            password_cliente.send_keys(var_banco_password)
            # Click en continuar
            boton_continuar = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/form/div[7]/button[1]')
            boton_continuar.click()

            # Autorizar transacción
            boton_autorizar = WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/form/div/div/div[1]/button')))
            boton_autorizar.click()

        src = var_src
        trg = var_trg

        # Elimina los archivos que comienzan con "Comprobante*" en la carpeta origen
        for f in glob.glob(os.path.join(src, "Comprobante*")):
            if os.path.isfile(f):
                os.remove(f)

        # Asigna elemento botón de descarga de pdf
        descargar_pdf = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/section/div[2]/div[2]/div/section/div/div[1]/div/div/div/table/tbody/tr[9]/td/a/span')))
        descargar_pdf.click()

        sleep(3)
        
        # Encuentra el archivo que cumple con el patrón "Comprobante*" y lo mueve a la carpeta destino
        files = glob.glob(os.path.join(src, "Comprobante*"))

        if len(files) == 1:
            file = files[0]
            if os.path.isfile(file):
                # Rename the file before moving it
                new_file_name = f"{day_map[dia]}.pdf"
                new_file_path = os.path.join(trg, new_file_name)
                shutil.move(file, new_file_path)


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    # dia: 1-5 (lunes a viernes)
    dia = input('Día de la semana (1-5): ')
    # semana: 1-6 (según fila en calendario)
    semana = var_semana
    numero_pasaje_ida = var_numero_pasaje_ida
    numero_pasaje_vuelta = var_numero_pasaje_vuelta
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output='reportes', report_name='pasajes-report'))
