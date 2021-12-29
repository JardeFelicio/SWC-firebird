import fdb
from datetime import date,datetime
import time
import logging
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler

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

     
     logger.info(dateTime()+"   -  Arquivo gerado com sucesso")
    
  except Exception as e:
    logging.warning(e)


def on_created(event):
    print("created")

def on_deleted(event):
    print("deleted")

def on_modified(event):
    print("modified")
    print(dateTime())
    gerar_txt()
    time.sleep(60)

def on_moved(event):
    print("movied")



if __name__ == "__main__":
    event_handler = FileSystemEventHandler()
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved
    

    path = "C:/SYSPDV/TX"
    
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        print("Monitorando")
        print(dateTime())
        logging.info(dateTime()+"   -  Programa iniciado com sucesso")
        while True:
            time.sleep(1)
    finally:
        print("Encerrado")
        logging.info(dateTime()+"   -  Programa finalizado com sucesso")
        observer.stop()
        observer.join()



