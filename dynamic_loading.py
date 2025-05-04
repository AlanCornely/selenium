"""
Teste de Carregamento Dinâmico no site the-internet.herokuapp.com
Cobre:
- Acesso à página de carregamento dinâmico
- Interação com elementos dinâmicos
- Validação de texto após carregamento
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

def setup_driver(headless=False):
    """configuração do webdriver"""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    return driver

def test_dynamic_loading(headless=False):
    """teste de carregamento dinâmico"""
    driver = setup_driver(headless)
    
    try:
        # início do teste
        start_time = datetime.now()
        print(f"\nInício do teste: {start_time.strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Acessar a página
        driver.get("https://the-internet.herokuapp.com/dynamic_loading")
        
        # Clicar no Example 1 (Elemento oculto)
        example_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Example 1"))
        )
        example_link.click()
        
        # Clicar no botão Start
        start_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#start button"))
        )
        start_button.click()
        
        # Registrar tempo antes da espera
        wait_start = datetime.now()
        
        # Aguardar o texto "Hello World!" (com timeout de 30 segundos)
        hello_element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#finish h4"))
        )
        
        # Registrar tempo após a espera
        wait_end = datetime.now()
        wait_duration = (wait_end - wait_start).total_seconds()
        
        # Validar o texto
        if hello_element.text == "Hello World!":
            print(f"Sucesso! Texto encontrado após {wait_duration:.2f} segundos")
            result = "Passou"
            message = "Texto 'Hello World!' encontrado com sucesso"
        else:
            print(f"Falha! Texto encontrado: '{hello_element.text}'")
            result = "Falhou"
            message = f"Texto inesperado: '{hello_element.text}'"
        
        # Registrar fim do teste
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        
        print(f"Fim do teste: {end_time.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Duração: {total_duration:.2f} segundos")
        print(f"Tempo de espera do carregamento: {wait_duration:.2f} segundos")
        
        return {
            "status": result,
            "mensagem": message,
            "tempo_total": f"{total_duration:.2f} segundos",
            "tempo_espera": f"{wait_duration:.2f} segundos",
            "inicio": start_time.strftime('%d/%m/%Y %H:%M:%S'),
            "fim": end_time.strftime('%d/%m/%Y %H:%M:%S')
        }
        
    except Exception as e:
        print(f"Erro durante o teste: {str(e)}")
        return {
            "status": "Falhou",
            "mensagem": f"Erro: {str(e)}",
            "tempo_total": "N/A",
            "tempo_espera": "N/A",
            "inicio": start_time.strftime('%d/%m/%Y %H:%M:%S'),
            "fim": datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Iniciando teste de carregamento dinâmico...")
    
    # Executar teste (pode passar headless=True para modo sem interface)
    resultado = test_dynamic_loading(headless=False)
    
    print("\nResumo do teste:")
    print(f"Resultado: {resultado['status']}")
    print(f"Detalhes: {resultado['mensagem']}")
    print(f"Tempo total: {resultado['tempo_total']}")
    print(f"Tempo de espera: {resultado['tempo_espera']}")
    
    print("\nTeste concluído!")
