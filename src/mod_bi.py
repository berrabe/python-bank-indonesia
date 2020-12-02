"""
Modul Where The Magic Happen
- berrabe
"""
import datetime
import logging
import sys
from bs4 import BeautifulSoup
import mysql.connector
import requests
import tabulate


logger = logging.getLogger(__name__)




class BI():
	"""docstring for class bi"""

	def __init__(self, url):
		"""
		Of Course, This is initialization method
		"""

		try:
			self.list_uang = [[]]
			self.raw_data = None
			self.url_ = url

			self.__req()
			self.__get_kurs()
			self.__get_abr()

		except Exception:
			logger.exception('INIT ERROR')
			sys.exit(2)




	def __req(self):
		"""
		method for make conn for getting / sraping
		info from bi website
		"""

		try:
			page = requests.get(self.url_, timeout=5)

			if page.status_code == 200:
				logger.info("Get Data From BI SUCCESS - %s", page.status_code)
				self.raw_data = BeautifulSoup(page.content, 'lxml')

		except Exception:
			logger.exception('GET DATA ERROR')
			sys.exit(2)




	def __get_kurs(self):
		"""
		Method For Parsing Kurs From BI Website
		"""

		try:
			logger.info("Getting Current Kurs")
			soup = self.raw_data
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

		except Exception:
			logger.exception('GET KURS ERROR')
			sys.exit(2)




	def __get_abr(self):
		"""
		Method For Getting Abbreviation
		"""

		try:
			logger.info("Getting List Available Currency")
			soup = self.raw_data
			table = soup.find("div", attrs={"id": "KodeSingkatan"})
			name = table.find_all("td")

			index = 0
			for i in range(len(name)):
				if i % 2 != 0:
					splitting = name[i].text.split()
					self.list_uang[index].insert(0, ' '.join(splitting))
					index += 1

		except Exception:
			logger.exception('GET LIST AVAILABLE CURRENCY ERROR')
			sys.exit(2)




	def table(self):
		"""
		Method For show the final data to terminal with table
		for ease of reading
		"""

		try:
			logger.info("Show Currency Table")
			headers = ["Mata Uang", "ABR", "Nilai", "Kurs Jual", "Kurs Beli"]

			print(tabulate.tabulate(self.list_uang, headers, tablefmt="pretty"))

		except Exception:
			logger.exception('SHOW TABLE Error')
			sys.exit(2)




	def send_db(self, host='localhost', user='user_bi', password='pass_bi', database='db_bi'):
		"""
		Method For Handling All DB Stuff
		"""

		try:
			logger.info("Send Current Kurs To DB")
			date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

			db_ = mysql.connector.connect(
				host=host,
				user=user,
				password=password,
				database=database)
			cur = db_.cursor()

			cur.execute("""CREATE TABLE IF NOT EXISTS `KURS` (
			`No` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
			`Waktu` datetime NOT NULL,
			`Mata_Uang` varchar(20) NOT NULL,
			`ABR` varchar(20) NOT NULL,
			`Nilai` decimal(20) NOT NULL,
			`Kurs_Jual` varchar(20) NOT NULL,
			`Kurs_Beli` varchar(20) NOT NULL)
			""")


			for i in self.list_uang:

				sql = f"""INSERT INTO `KURS`
				(`No`, `Waktu`, `Mata_Uang`, `ABR`, `Nilai`, `Kurs_Jual`, `Kurs_Beli`) 
				VALUES 
				(NULL, '{date}', '{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}', '{i[4]}'); """

				cur.execute(sql)

			db_.commit()

		except Exception:
			logger.exception('SEND DB ERROR')
			sys.exit(2)
