from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuración del navegador
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Ejecutar en modo headless (sin abrir una ventana del navegador)

# Usar webdriver_manager para manejar el driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navegar al sitio web con la fila virtual
driver.get('https://queue.eticket.com.co/?c=eticketco&e=ferxxo10042024&t=https%3A%2F%2Fwww.eticket.co%2Feventos.aspx%3Fidartista%3D635&cid=es-MX&l=eticketco')

# Aquí va la lógica para interactuar con la fila virtual
try:
    # Esperar explícitamente a que el botón de "Ingresar" sea clickeable
    ingresar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'ingresarBtn'))
    )
    ingresar_button.click()

    # Esperar explícitamente a que el elemento de resultado esté presente
    resultado = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'resultado'))
    )
    print('Bot logró pasar la fila virtual:', resultado.text)
except Exception as e:
    print(f'Error al interactuar con la fila virtual: {e}')
finally:
    # Cerrar el navegador
    driver.quit()
