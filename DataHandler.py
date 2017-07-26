import datetime
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import  get_column_letter

globtime = 'SampleDate'
rowcount = 1
worksheet = ''
workbook = ''

def initialize():
    wb = Workbook()
    t = datetime.datetime.now()
    global globtime
    globtime = t.strftime('%m-%d-%Y-%H:%M')

    global workbook
    workbook=wb
    ws1= wb.active
    ws1.title= 'livedata'
    global worksheet
    worksheet =ws1
    for row in range(1,2):
        ws1.append(['BTCTURK' , 'POLONIEX USD','USD/TRY','POLO TRY','FARK','REEL FARK','ACTION','TIMESTAMP'])



def appendData(datas):

    global worksheet
    datas.append(datetime.datetime.now().strftime('%m-%d-%Y-%H:%M:%S'))
    worksheet.append(datas)

def savedata():
    global workbook
    dest_filename = 'prices-' + globtime + '.xlsx'
    workbook.save(filename= dest_filename)
