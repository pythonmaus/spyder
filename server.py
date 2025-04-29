from flask import Flask, make_response, request,render_template
from extras.dyurl import url
import json
from datetime import datetime
import argparse
import os

app = Flask(__name__)
unique_url = url.write_url()

if not os.path.exists('extras/ip.json'):
  with open('extras/ip.json', 'w') as cp:
    cp.write('{}')
    cp.close()

def write_file(ip,time):
  with open('extras/ip.json', 'w') as captured:
    json.dump({'1':{'ip':f'{ip}','captured':f'{time}'}},captured,indent=2)
    captured.closed()
      
@app.route('/')
def home():
  user_ip = request.headers.get('X-Forwarded-For') if request.remote_addr == '127.0.0.1' else request.remote_addr
  if user_ip != None:
    fir,sec,thir,fou = user_ip.split('.')
  
  t_cap=datetime.now().strftime("%Y-%m-%d(%H:%M:%S)")
  try:
    if len(fir) == 3:
      with open('extras/ip.json', 'r') as captured:
        try:
          load=json.load(captured)
          note=0
          i=0
          while i < len(load.keys()):
            note+=1
            i+=1
          captured.close()
          with open('extras/ip.json', 'w') as update:
            load.update({f'{note+1}':{'ip':f'{user_ip}','captured':f'{t_cap}'}})
            json.dump(load,update,indent=2)
            update.close()
        except Exception:
          write_file(user_ip,t_cap)
          return render_template('home.html', refresh = True), 200
    else:
      pass
  except Exception:
    write_file(user_ip,t_cap)
    return render_template('home.html', refresh = True), 200
  
  return render_template('home.html'), 200
  
  
@app.route(f'/admin/<url>')
def check_stats(url):
  if url == unique_url:
    with open('extras/ip.json', 'r') as captured:
      ip_cap=json.load(captured)
      
    return render_template('admin.html',ip_cap=ip_cap)
  return render_template('admin.html', page_expired = True)
  
  
@app.route('/<username>')  
def user(username):
  return "<h2>Hello there, %s!</h2>" %username
  
if __name__=='__main__':
  parser = argparse.ArgumentParser(description="Custom port for flask app")
  parser.add_argument('-p',type=int,default=5000,help="-p port : custom port for the app")
  args = parser.parse_args()
  app.run(debug=True, port=args.p,host="0.0.0.0")