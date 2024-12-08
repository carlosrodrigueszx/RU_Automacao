import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

def generate_date_sequence(start_date: str, end_date: str) -> list[str]:

    # Converte as datas de string para objetos datetime
    start = datetime.strptime(start_date, "%d/%m/%Y")
    end = datetime.strptime(end_date, "%d/%m/%Y")

    # Gera a sequência de datas
    date_list = []
    current_date = start
    while current_date <= end:
        date_list.append(current_date.strftime("%d/%m/%Y"))
        current_date += timedelta(days=1)

    return date_list

class RUReservation:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.serviceDate = None
        self.serviceType = None
        self.serviceHour = None

    def login_user(self):
        # Usuário
        usr = "carlosrodrigueszx"
        boxUsr = self.driver.find_element(By.XPATH, '//*[@id="conteudo"]/table/tbody/tr/td/div/form/table/tbody/tr[1]/td/input')
        boxUsr.clear()
        boxUsr.send_keys(usr)

        # Senha
        passw = "Aluno2022!"
        boxPass = self.driver.find_element(By.XPATH, '//*[@id="conteudo"]/table/tbody/tr/td/div/form/table/tbody/tr[2]/td/input')
        boxPass.clear()
        boxPass.send_keys(passw)

        # Clica no botão de login
        clickButton = self.driver.find_element(By.XPATH, '//*[@id="conteudo"]/table/tbody/tr/td/div/form/table/tfoot/tr/td/input')
        clickButton.click()

    def reserve_launch(self, date: str):
        wait = WebDriverWait(self.driver, 10)  # Espera explícita de até 10 segundos

        # Localizando e preenchendo a data
        self.serviceDate = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="formulario:data_agendamento"]'))
        )
        self.serviceDate.clear()
        self.serviceDate.send_keys(date)

        # Selecionando o tipo de refeição (Almoço)
        self.serviceType = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="formulario:tipo_refeicao"]'))
        )
        self.serviceType.click()

        lunchOption = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="formulario:tipo_refeicao"]/option[2]'))
        )
        lunchOption.click()

        # Selecionando o horário
        self.serviceHour = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="formulario:horario_agendado"]'))
        )
        self.serviceHour.click()

        # Selecionar um horário específico (alterar XPath conforme necessário)
        selectedHour = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="formulario:horario_agendado"]/option[2]'))
        )
        selectedHour.click()

        finalClick = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="formulario:cadastrar_agendamento_bt"]'))
        )
        finalClick.click()

    def reserve_dinner(self, date: str):
        wait = WebDriverWait(self.driver, 10)  # Espera explícita de até 10 segundos

        # Localizando e preenchendo a data
        self.serviceDate = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="formulario:data_agendamento"]'))
        )
        self.serviceDate.clear()
        self.serviceDate.send_keys(date)

        # Selecionando o tipo de refeição (Jantar)
        self.serviceType = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="formulario:tipo_refeicao"]'))
        )
        self.serviceType.click()

        dinnerOption = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="formulario:tipo_refeicao"]/option[3]'))
        )
        dinnerOption.click()

        # Selecionando o horário
        self.serviceHour = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="formulario:horario_agendado"]'))
        )
        self.serviceHour.click()

        # Selecionar um horário específico (alterar XPath conforme necessário)
        selectedHour = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="formulario:horario_agendado"]/option[2]'))
        )
        selectedHour.click()

        finalClick = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="formulario:cadastrar_agendamento_bt"]'))
        )
        finalClick.click()

if __name__ == '__main__':
    # Inicializa o driver do navegador
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)  # Define o tempo de espera implícita
    driver.get('https://si3.ufc.br/sigaa/logar.do?dispatch=logOff')
    reservation = RUReservation(driver)
    reservation.login_user()

    portalDiscente_box = driver.find_element(By.XPATH, '//*[@id="portais"]/ul/li[2]/a/span')
    portalDiscente_box.click()

    ruButton = driver.find_element(By.XPATH, '//*[@id="cmAction-96"]/span[2]')
    ruButton.click()

    ruFeature = driver.find_element(By.XPATH, '//*[@id="cmAction-97"]/td[2]')
    ruFeature.click()

    try:
        start_dt = input("Digite a data de início (dd/mm/yyyy): ")
        end_dt = input("Digite a data de fim (dd/mm/yyyy): ")

        # Valida se as datas estão no formato correto
        datetime.strptime(start_dt, "%d/%m/%Y")
        datetime.strptime(end_dt, "%d/%m/%Y")
    except ValueError:
        print("Por favor, insira as datas no formato dd/mm/yyyy corretamente.")
        exit()

    date_sequence = generate_date_sequence(start_dt, end_dt)

    # Faz a reserva para almoço e jantar em cada dia
    for i in date_sequence:
        reservation.reserve_launch(i)
        print(f"Reserva feita para o almoço na data {i}")

        reservation.reserve_dinner(i)
        print(f"Reserva feita para o jantar na data {i}")

    time.sleep(2)
    driver.quit()

