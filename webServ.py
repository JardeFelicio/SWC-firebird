from time import daylight
from PyQt5 import  uic,QtWidgets
import fdb
from datetime import date,datetime
import logging
import os

def dataatual():
  """Retorna data atual"""
  return str(date.today().strftime("%d%m%y"))

def dateTime():
  """Retorna data e hora atual"""
  return str(datetime.today().strftime("%d/%m/%Y  %H:%M:%S"))

log_format = '%(asctime)'
logging.basicConfig(filename='dataCloud'+dataatual()+'.log',filemode='a',level=logging.INFO)
logger=logging.getLogger('root')


"""Realiza a conexão com o Banco de Dados"""
try:
  con = fdb.connect(host="localhost",database="c:/syspdv/syspdv_srv.fdb",user="sysdba",password="masterkey",port=3050)
except Exception as e:
  logging.warning(e)
  print("erro")

def ultimaCarga():
  try:
    if (os.path.isfile('dataCloud.txt')):
      dateCarga = datetime.fromtimestamp(os.path.getmtime("dataCloud.txt"))
      telaCarga.dateCarga.setText(dateCarga.strftime("%d/%m/%Y %H:%M"))
    else:
      dateCarga = "Arquivo não encontrado."
      telaCarga.dateCarga.setText(dateCarga)
  except:
    pass

def gerar_txt(): 
  """Faz a consulta no banco e gera o arquivo de texto"""    
  try:
    cur = con.cursor()
    cur.execute("select p.procod,p.prodes,p.proprc1,p.proctrest,e.estatu,s.secdes from produto p, estoque e,secao s where proforlin ='N' and s.seccod= p.seccod and p.procod=e.procod order by procod")
    lista = cur.fetchall()
    cur.close()
    con.close
    
    with open("dataCloud.txt", "w") as dataCloud:
     for var in lista:
        dataCloud.writelines(str(var[0])+","+str(var[1])+","+str(var[2])+","+str(var[3])+","+str(var[4])+","+str(var[5])+"\n")    
     dataCloud.close()
     concluido.show()

     
     logger.info(dateTime()+"   -  Arquivo gerado com sucesso")
     ultimaCarga()
    
  except Exception as e:
    logging.warning(e)





app=QtWidgets.QApplication([])
telaCarga=uic.loadUi("carga.ui")
telaCarga.btnEnviar.clicked.connect(gerar_txt)
concluido=uic.loadUi("_concluido.ui")

telaCarga.show()
ultimaCarga()
app.exec()