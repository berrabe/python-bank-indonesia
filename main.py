"""
main module
"""

import time
import logging
from src import mod_bi

logger = logging.getLogger(__name__)



if __name__ == '__main__':
	logging.basicConfig(level = logging.INFO,
						# filename='bi.log', filemode='w',
						format = '[ %(levelname)s ] [ %(name)-10s ] [ %(asctime)s ] => %(message)s',
						datefmt='%d-%b-%y %H:%M:%S')

	start_time = time.time()
	logger.info("================== Logger Start ==================")

	obj = mod_bi.bi('https://www.bi.go.id/id/moneter/informasi-kurs/transaksi-bi/Default.aspx')
	obj.send_db('localhost','user_bi','pass_bi','db_bi')
	obj.table()

	logger.info("================== Done @ %.2f Second ==================\n\n",
		time.time() - start_time)
