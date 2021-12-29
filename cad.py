import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from datetime import date,datetime



def dateTime():
  """Retorna data e hora atual"""
  return str(datetime.today().strftime("%m/%d/%Y  %H:%M:%S"))

print(dateTime())

def on_created(event):
    print("created")
    print(dateTime())

def on_deleted(event):
    print("deleted")
    print(dateTime())

def on_modified(event):
    print("modified")
    print(dateTime())

def on_moved(event):
    print("movied")
    print(dateTime())



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
        while True:
            time.sleep(1)
    finally:
        print("Encerrado")
        observer.stop()
        observer.join()