import socket,sys,time,subprocess,os,datetime,random,string,threading
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

green='\033[1;32m'
plain='\033[1;0m'
red='\033[1;31m'
blue='\033[1;36m'

def timestamp():
  return datetime.datetime.now().strftime('%H:%M')
  
def verify_port(port):
  if isinstance(int(port), int) and not len(str(port)) < 4:
    return True
  print('𝙼𝚞𝚜𝚝 𝚋𝚎 𝚏𝚘𝚞𝚛 𝚍𝚒𝚐𝚒𝚝𝚜 𝚒𝚗 𝚕𝚎𝚗𝚐𝚝𝚑')
  return False   
def random_port():
  digits=['1','2','3','4','5','6','7','8','9']
  port = ''.join(random.choice(digits) for _ in range(4))
  return port
  
class privateChannel:
  def __init__(self,listen_port):
    self.listen_port = listen_port
    
  def tcp_server(self):
    try:
      print('%s𝚂𝚝𝚊𝚛𝚝𝚒𝚗𝚐 𝚖𝚊𝚒𝚗 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 %s'%(green,plain))
      s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.bind(('0.0.0.0', int(self.listen_port)))
      s.listen()
      print('%s𝙼𝚢 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 𝚙𝚘𝚛𝚝 : %s %s'%(green,self.listen_port,green))
      while True:
        conn,addr = s.accept()
        print('\n[%s]𝙹𝚘𝚒𝚗𝚎𝚍 𝚢𝚘𝚞𝚛 𝚌𝚑𝚊𝚗𝚗𝚎𝚕  : %s'% (timestamp(),addr))
        if not conn:
          break
        else:
          threading.Thread(target=self.handle_tcp,args=(conn,addr), daemon=True).start()
    except Exception as error:
      print(error)
    finally:
      print(f'[{timestamp()}]𝚂𝚎𝚛𝚟𝚎𝚛 𝚕𝚒𝚜𝚝𝚎𝚗𝚒𝚗𝚐 𝚊𝚝 𝚙𝚘𝚛𝚝  {self.listen_port} 𝚑𝚊𝚜 𝚋𝚎𝚎𝚗 𝚌𝚕𝚘𝚜𝚎𝚍')
      s.close()
  
  def handle_tcp(self,conn, addr):
    try:
      while True:
        content = conn.recv(1024)
        if not content:
          break
        self.display_message(content)
    except Exception as err:
      print('%s -> %s'%(addr,err))
    finally:
      print(f'{addr} 𝚕𝚎𝚏𝚝 𝚢𝚘𝚞𝚛 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 ')
      conn.close()
  
  def display_message(self,message):
    compose_to = message.decode('utf-8')
    print(f'{compose_to}')
    

class broadcastChannel:
  def __init__(self,listen_port):
    self.listen_port = listen_port
    self.members = set()
    
  def broadcast_tcp(self):
    try:
      s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.bind(('0.0.0.0', int(self.listen_port)))
      s.listen()
      print(f'𝙱𝚛𝚘𝚊𝚍𝚌𝚊𝚜𝚝 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 𝚕𝚒𝚜𝚝𝚎𝚗𝚒𝚗𝚐 𝚊𝚝 : {self.listen_port}')
      while True:
        conn,addr = s.accept()
        print('[%s]%s 𝚓𝚘𝚒𝚗𝚎𝚍 𝚝𝚑𝚎 𝚋𝚛𝚘𝚊𝚍𝚌𝚊𝚜𝚝'%(timestamp(),addr))
        threading.Thread(target=self.handle_broadcast,args=(conn,addr),daemon=True).start()
          
    except Exception as error:
      print(f'[{timestamp()}]{error}')
    finally:
      print('\n𝙱𝚛𝚘𝚊𝚍𝚌𝚊𝚜𝚝 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 𝚌𝚕𝚘𝚜𝚎𝚍')
      s.close()
      
  def handle_broadcast(self,conn, addr):
    self.members.add(conn)
    try:
      while True:
        message = conn.recv(1024)
        if not message:
          break
        self.broadcast(message,conn)
    except Exception as error:
      print(error)
    finally:
      self.members.discard(conn)
      print(f'{addr} 𝚕𝚎𝚏𝚝 𝚝𝚑𝚎 𝚋𝚛𝚘𝚊𝚍𝚌𝚊𝚜𝚝')
      conn.close()
    
  def broadcast(self,message,sender_conn):
    for member in self.members.copy():
      if member != sender_conn:
        try:
          member.sendall(message)
        except Exception as error:
          self.members.discard(member)
          member.close()

class publicChannel:
  def __init__(self,listen_port):
    self.listen_port = listen_port
    self.users = set()
    
  def publicUdp(self):
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.bind(('0.0.0.0', int(self.listen_port)))
      print(f'𝙿𝚞𝚋𝚕𝚒𝚌 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 𝚕𝚒𝚜𝚝𝚎𝚗𝚒𝚗𝚐 𝚊𝚝 𝚙𝚘𝚛𝚝 {self.listen_port}')
      while True:
        message = s.recvfrom(1024)
        if not message:
          break
        self.display_message(message)
    except Exception as error:
      print(error)
    finally:
      print('𝙿𝚞𝚋𝚕𝚒𝚌 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 𝚌𝚕𝚘𝚜𝚎𝚍')
      s.close()
      
  def display_message(self,message):
    compose_to = message.decode('utf-8')
    print(f'{compose_to}')
    
    
def slr(ar,col):
  for char in ar:
    sys.stdout.write('%s%s%s'%(col,char,plain))
    sys.stdout.flush()
    time.sleep(0.005)
        
  sys.stdout.write('\n')
  
def start_up():
  subprocess.run(['cls' if os.name == 'nt' else 'clear'])
    
  slr('================================================',green)
  slr('=============================  =================',green)
  slr('=============================  =================',green)
  slr('=============================  =============  ==',green)
  slr('==   ===    ===  =  ===   ===  ======   ===    =',green)
  slr('=  =  ==  =  ==  =  ==  =  ==    ===  =  ===  ==',green)
  slr('==  ====  =  ===    ==  =====  =  =====  ===  ==',green)
  slr('===  ===    ======  ==  =====  =  ===    ===  ==',green)
  slr('=  =  ==  =====  =  ==  =  ==  =  ==  =  ===  ==',green)
  slr('==   ===  ======   ====   ===  =  ===    ===   =',green)
  slr('================================================',green)
  slr('𝙱𝚎𝚝𝚊 𝚟𝚎𝚛𝚜𝚒𝚘𝚗 1.0',green)

session = PromptSession()

def compose_message(message,myport):
  composed = f'[{timestamp()}]{username}: {message}'.encode('utf-8')
  return composed

def private_message_setup():
  with patch_stdout():
    while True:
      try:
        channel_ip = session.prompt('𝙲𝚑𝚊𝚗𝚗𝚎𝚕\'𝚜 𝚋𝚒𝚗𝚍𝚎𝚍 𝚒𝚙 𝚊𝚍𝚍𝚛𝚎𝚜𝚜, 𝚕𝚎𝚊𝚟𝚎 𝚎𝚖𝚙𝚝𝚢 𝚒𝚏 𝚢𝚘𝚞\'𝚛𝚎 𝚘𝚗 𝚝𝚑𝚎 \n𝚜𝚊𝚖𝚎 𝚗𝚎𝚝𝚠𝚘𝚛𝚔 : ') or '0.0.0.0'
        fr_port = session.prompt('𝙲𝚑𝚊𝚗𝚗𝚎𝚕\'𝚜 𝚕𝚒𝚜𝚝𝚎𝚗𝚒𝚗𝚐 𝚙𝚘𝚛𝚝 : ')
        if fr_port.lower() == 'quit':
          break
        int(fr_port)
        if verify_port(fr_port):
          break
      except Exception:
        print('𝚃𝚑𝚊𝚝 𝚒𝚜 𝚒𝚗𝚟𝚊𝚕𝚒𝚍')
    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((channel_ip, int(fr_port)))
        while True:
          message = session.prompt(f'\n[{timestamp()}]𝚈𝚘𝚞 : ')
          if message.lower() == 'quit':
            s.close()
            break
          s.sendall(compose_message(message,server_port))
    except Exception as err:
      print('%s'%err)
    finally:
      s.close()

def add_to_channel(my_port,channel_ip,channelport):
  def display_message(message):
    compose_to = message.decode('utf-8')
    print(f'{compose_to}')
      
  def receive_data(join):
    try:
      while True:
        message = join.recv(1024)
        if not message:
          break
        display_message(message)
    except Exception:
      pass
      
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as join:
      join.connect((channel_ip, int(channelport)))
      threading.Thread(target=receive_data,args=(join,),daemon=True).start()
      with patch_stdout():
        while True:
          message = session.prompt(f'[{username}]𝚈𝚘𝚞 : ')
          if message.lower() == 'quit':
            join.close()
            break
          join.sendall(compose_message(message,my_port))      
  except Exception as error:
    print(error)
  finally:
    join.close()
def create_join_broadcast():
  while True:
    try:
      channel_ip = session.prompt('𝙱𝚒𝚗𝚍 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 𝚝𝚘 𝚊𝚗 𝚒𝚙 𝚊𝚍𝚍𝚛𝚎𝚜𝚜,𝚘𝚝𝚑𝚎𝚛𝚠𝚒𝚜𝚎 𝚕𝚎𝚊𝚟𝚎 𝚎𝚖𝚙𝚝𝚢 𝚒𝚏 𝚢𝚘𝚞\'𝚛𝚎 𝚞𝚗𝚜𝚞𝚛𝚎 : ')
      channelport = input('𝙴𝚗𝚝𝚎𝚛 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 𝚙𝚘𝚛𝚝 : ')
      if verify_port(int(channelport)):
        break
    except Exception:
      pass
  channel = broadcastChannel(channelport)
  threading.Thread(target=channel.broadcast_tcp,daemon=True).start()
   
  add_to_channel(server_port,channel_ip,channelport)
    
def main_menu():
  import textwrap
  print(textwrap.dedent(f"""
  {green}𝙼𝚢 𝚞𝚜𝚎𝚛𝚗𝚊𝚖𝚎 : {username}{green}
  
  1) 𝙼𝚎𝚜𝚜𝚊𝚐𝚎 𝚊 𝚙𝚛𝚒𝚟𝚊𝚝𝚎 𝚌𝚑𝚊𝚗𝚗𝚎𝚕(𝚔𝚎𝚎𝚙 𝚊𝚕𝚒𝚟𝚎).
  2) 𝙲𝚛𝚎𝚊𝚝𝚎 𝚊 𝚙𝚛𝚒𝚟𝚊𝚝𝚎 𝚋𝚛𝚘𝚊𝚍𝚌𝚊𝚜𝚝 𝚌𝚑𝚊𝚗𝚗𝚎𝚕.
  3) 𝙹𝚘𝚒𝚗 𝚋𝚛𝚘𝚊𝚍𝚌𝚊𝚜𝚝 𝚌𝚑𝚊𝚗𝚗𝚎𝚕(𝚔𝚎𝚎𝚙 𝚊𝚕𝚒𝚟𝚎).
  4) 𝙹𝚘𝚒𝚗 𝚝𝚑𝚎 𝚑𝚊𝚛𝚔𝚎𝚛𝚋𝚢𝚝𝚎 𝚌𝚘𝚖𝚖𝚞𝚗𝚒𝚝𝚢 𝚏𝚘𝚛 𝚖𝚘𝚛𝚎 𝚝𝚘𝚘𝚕𝚜/𝚞𝚙𝚍𝚊𝚝𝚎𝚜.
  
  {red}𝚀𝚞𝚒𝚝{green} 𝚌𝚕𝚘𝚜𝚎𝚜 𝚝𝚑𝚎 𝚊𝚌𝚝𝚒𝚟𝚎 𝚌𝚘𝚗𝚗𝚎𝚌𝚝𝚒𝚘𝚗 𝚝𝚘 𝚓𝚘𝚒𝚗𝚎𝚍 𝚌𝚑𝚊𝚗𝚗𝚎𝚕.{plain}
  {red}𝚀𝚞𝚒𝚝{green} 𝚏𝚛𝚘𝚖 [𝚖𝚎𝚗𝚞] 𝚝𝚘 𝚜𝚑𝚞𝚝𝚍𝚘𝚠𝚗 𝚝𝚑𝚎 𝚠𝚑𝚘𝚕𝚎 𝚙𝚛𝚘𝚐𝚛𝚊𝚖.{plain}"""))
 
  while True:
    with patch_stdout():
      option = session.prompt('[𝙼𝚎𝚗𝚞] : ')
      if option == '1':
        private_message_setup()
      elif option == '2':
        create_join_broadcast()
      elif option == '3':
        try:
          while True:
            channel_ip = session.prompt('𝙲𝚑𝚊𝚗𝚗𝚎𝚕\'𝚜 𝚋𝚒𝚗𝚍𝚎𝚍 𝚒𝚙 𝚊𝚍𝚍𝚛𝚎𝚜𝚜, 𝚕𝚎𝚊𝚟𝚎 𝚎𝚖𝚙𝚝𝚢, 𝚒𝚏 𝚢𝚘𝚞\'𝚛𝚎 𝚘𝚗 𝚝𝚑𝚎 \n𝚜𝚊𝚖𝚎 𝚗𝚎𝚝𝚠𝚘𝚛𝚔 : ') or '0.0.0.0'
            channel_port = input('𝙲𝚑𝚊𝚗𝚗𝚎𝚕 𝚙𝚘𝚛𝚝 : ')
            if verify_port(int(channel_port)):
              break
          add_to_channel(server_port,channel_ip,channel_port)
        except Exception:
          pass
      elif option == '4':
        subprocess.run(['xdg-open', 'https://whatsapp.com/channel/0029Vb5f98Z90x2p6S1rhT0S'])
      elif option.lower() == 'quit':
        sys.exit()

if __name__=='__main__':
  start_up()
  username = input('%s𝙳𝚒𝚜𝚙𝚕𝚊𝚢 𝚗𝚊𝚖𝚎 : %s'%(green,plain))
  if username == '':
    if os.path.exists('extras/name.txt'):
      with open('extras/name.txt', 'r') as choice:
        line_ = [line for line in choice.readlines() if line.strip()]
        username = random.choice(line_)
    else:
      username = ''.join(random.choice(string.digits + string.ascii_lowercase) for _ in range(6))
  username = username[:6]
  try:
    while True:
      try:
        server_port = input('%s𝙴𝚗𝚝𝚎𝚛 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 𝚙𝚘𝚛𝚝 𝚎.𝚐 8080 : %s'%(green,plain)) or random_port()
        if verify_port(server_port):
          private = privateChannel(server_port)
          threading.Thread(target=private.tcp_server,daemon=True).start()
          time.sleep(1)
          main_menu()
      except ValueError:
        print('𝚃𝚑𝚊𝚝 𝚒𝚜 𝚒𝚗𝚟𝚊𝚕𝚒𝚍')
  except Exception as e:
    sys.exit()