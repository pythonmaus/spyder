import random
import string
import json

class url:
  def __init__(self):
    return self
  
  def write_url():
    parsed ='spyder:' + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)for _ in range(7))
      
    with open('url.json', 'w') as pass_url:
      format_ = {
        "url" : f"{parsed}"
      }
      json.dump(format_, pass_url, indent=2)
      pass_url.close()
      
      return parsed
      
if __name__==('__main__'):
  url()