from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configuración del navegador
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Ejecutar en modo headless (sin abrir una ventana del navegador)

# Usar webdriver_manager para manejar el driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navegar a una página de prueba
driver.get('https://www.google.com')

# Imprimir el título de la página
print(driver.title)

# Cerrar el navegador
driver.quit()
