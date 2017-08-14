import datetime
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import  get_column_letter

globtime = 'SampleDate'


def initialize():
    wb = Workbook()
    t = datetime.datetime.now()
    global globtime
    globtime = t.strftime('%m-%d-%Y-%H:%M')
    return wb


def initializeWS(wb):
    ws1 = wb.active
    ws1.title = 'livedata'
    worksheet = ws1
    for row in range(1, 2):
        ws1.append(['BTCTURK', 'POLONIEX USD', 'USD/TRY', 'POLO TRY', 'FARK', 'REEL FARK', 'ACTION', 'TIMESTAMP'])

    return ws1

def appendData(datas , worksheet):

    worksheet.append(datas)

def savedata(workbook):

    dest_filename = 'prices-' + globtime + '.xlsx'
    workbook.save(filename= dest_filename)
