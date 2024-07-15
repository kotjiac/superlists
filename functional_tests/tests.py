from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	# Auxiliary method 
	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element(By.ID,'id_list_table')
				rows = table.find_elements(By.TAG_NAME, 'tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except(AssertionError, WebDriverException) as e:
				if ((time.time() - start_time) > MAX_WAIT):
					raise e
				time.sleep(0.5)
	
	def test_can_start_a_list_for_one_user(self):
    # Edith ouviu falar que agora a aplicação online de lista de tarefas
    # aceita definir prioridades nas tarefas do tipo baixa, média e alta
    # Ela decide verificar a homepage

		self.browser.get(self.live_server_url)

    # Ela percebe que o título da página e o cabeçalho mencionam
    # listas de tarefas com prioridade (priority to-do)

		self.assertIn('Priority To-Do', self.browser.title)
		header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
		self.assertIn('Priority To-Do', header_text)
		
    # Ela é convidada a inserir um item de tarefa e a prioridade da 
    # mesma imediatamente

		inputbox = self.browser.find_element(By.ID, 'id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		selectbox = self.browser.find_element(By.ID, 'id_priority')
		self.assertEqual(
			selectbox.get_attribute('placeholder'),
			'Enter a priority'
		)
    
    # Ela digita "Comprar anzol" em uma nova caixa de texto
    # e assinala prioridade alta no campo de seleção de prioridades

		inputbox.send_keys('Comprar anzol')
		select = Select(selectbox)
		select.select_by_visible_text('prioridade alta')

    # Quando ela tecla enter, a página é atualizada, e agora
    # a página lista "1 - Comprar anzol - prioridade alta"
    # como um item em uma lista de tarefas

		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)
		self.wait_for_row_in_list_table('1: Comprar anzol - prioridade alta')
		
    # Ainda continua havendo uma caixa de texto convidando-a a 
    # acrescentar outro item. Ela insere "Comprar cola instantânea"
    # e assinala prioridade baixa pois ela ainda tem cola suficiente
    # por algum tempo
		
		inputbox = self.browser.find_element(By.ID, 'id_new_item')
		selectbox = self.browser.find_element(By.ID, 'id_priority')

		inputbox.send_keys('Comprar cola instantânea')
		select = Select(selectbox)
		select.select_by_visible_text('prioridade baixa')

    # A página é atualizada novamente e agora mostra os dois
    # itens em sua lista e as respectivas prioridades

		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)
		self.wait_for_row_in_list_table('1: Comprar anzol - prioridade alta')
		self.wait_for_row_in_list_table('2: Comprar cola instantânea - prioridade baixa')

    # Edith se pergunta se o site lembrará de sua lista. Então
    # ela nota que o site gerou um URL único para ela -- há um 
    # pequeno texto explicativo para isso.

		div = self.browser.find_element(By.ID, 'id_url_unique')
		self.assertIn('/lists/1', div.text)

    # Ela acessa essa URL -- sua lista de tarefas continua lá.

		link = self.browser.find_element(By.ID, 'id_list_link')
		link.click()
		time.sleep(1)
		self.wait_for_row_in_list_table('1: Comprar anzol - prioridade alta')
		self.wait_for_row_in_list_table('2: Comprar cola instantânea - prioridade baixa')
		