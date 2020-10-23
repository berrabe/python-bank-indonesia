from bs4 import BeautifulSoup
import mysql.connector
import requests
import time
import tabulate
import logging
import sys

logger = logging.getLogger(__name__)

class bi():
	"""docstring for bi"""

	def __init__(self, url):
		try:
			logger.info(f"BI MODULE - { url }")
			self.list_uang = [[]]
			self.__URL__ = url
			self.__get_kurs()
			self.__get_abr()
		except Exception as e:
			logger.exception(f'INIT ERROR { e }')


	def __req(self):
		try:
			logger.info("Get Data From BI")
			page = requests.get(self.__URL__, timeout=5)
			if page.status_code == 200:
				logger.info(f"Get Data From BI SUCCESS - { page.status_code }")
				return BeautifulSoup(page.content, 'lxml')
		except Exception as e:
			logger.exception(f'GET DATA ERROR { e }')
			sys.exit(2)


	def __get_kurs(self):
		try:
			logger.info("Getting Kurs")
			soup = self.__req()
			table = soup.find("table", attrs={"class": "table1"})
			data = table.find_all("td")

			index = 0
			for i in range(len(data)):
				if i % 5 == 0 and i != 0:
					self.list_uang.append([])
					index += 1
				
				if data[i].text == "\n\n":
					continue

				self.list_uang[index].append(data[i].text)
		except Exception as e:
			logger.exception(f'GET KURS ERROR { e }')


	def __get_abr(self):
		try:
			logger.info("Getting List Available Currency")
			soup = self.__req()
			table = soup.find("div", attrs={"id": "KodeSingkatan"})
			name = table.find_all("td")

			index = 0
			for i in range(len(name)):
				if i % 2 != 0:
					splitting = name[i].text.split()
					self.list_uang[index].insert(0, ' '.join(splitting))
					index += 1
		except Exception as e:
			logger.exception(f'GET LIST AVAILABLE CURRENCY ERROR { e }')

	def table(self):
		try:
			logger.info("Show Currency Table")
			headers = ["Mata Uang", "ABR", "Nilai", "Kurs Jual", "Kurs Beli"]
			print(tabulate.tabulate(self.list_uang, headers, tablefmt="pretty"))
		except Exception as e:
			logger.exception(f'SHOW TABLE Error { e }')

	def send_db(self, host='localhost', user='root', password='root', database='bi'):
		try:
			logger.info("Send DB of Kurs Lists")

			db = mysql.connector.connect(
				host=host,
				user=user,
				password=password,
				database=database
			)

			cur = db.cursor()

			for i in self.list_uang: 

				sql = f"""INSERT INTO `terbaru` 
				(`No`, `Mata Uang`, `ABR`, `Nilai`, `Kurs Jual`, `Kurs Beli`) 
				VALUES 
				(NULL, '{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}', '{i[4]}'); """

				cur.execute(sql)

			db.commit()

		except Exception as e:
			logger.exception(f'SEND DB ERROR { e }')