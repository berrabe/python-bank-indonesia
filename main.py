import mod_bi
import logging

if __name__ == '__main__':
	logging.basicConfig(level = logging.INFO, 
						# filename='bi.log', filemode='w',
						format = '[ %(levelname)s ] [ %(name)s ] [ %(asctime)s ] => %(message)s', 
						datefmt='%d-%b-%y %H:%M:%S')
	
	obj = mod_bi.bi('https://www.bi.go.id/id/moneter/informasi-kurs/transaksi-bi/Default.aspx')
	obj.table()