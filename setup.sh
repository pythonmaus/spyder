#!/bin/bash
red='\e[31m'
yellow='\e[33m'
green='\e[32m'
blue='\e[34m'
plain='\e[0m'

usage (){
  echo -e "Enter: $0 -m requirements.txt"
}
while getopts "m:" opt;do
  case $opt in 
    m)
      FILE=$OPTARG
      if [[ -f "$FILE" ]];then
        echo -e "${yellow}Installing required modules${plain}"
        pip install -r $FILE
      else
        echo -e "${red}$FILE not found ${plain}"
        exit
      fi
    ;;
    *)
      usage
    ;;
  esac
done
  
if [[ $OPTIND -eq 1 ]];then
  usage
  exit
fi

end(){
  echo -e "${red}$0 Task completed... Should terminate now${plain}"
  rm $0
}

if [[ $? -ge 1 ]];then
  echo -e "${red}There was an issue updating your packages ${plain}"
  exit
fi

if ! command -v python3 &>/dev/null ;then 
  echo -e "${red}Python3 is not installed yet ${plain}"
  pip install python3
  if [[ $? -ge 1 ]];then 
    pip install python
  fi
fi

if ! command -v cloudflared &>/dev/null;then
  echo -e "${red}Cloudflare service not found... Shall install that${plain}"
  pkg install cloudflared
  if [[ $? -ge 1 ]];then 
    echo -e "${red}An error was encounter trying to install cloudlfare service${plain}"
  else
    echo -e "${red}Installation complete${plain}"
  fi
fi

read -p "Would you like to update your packages y/n: " option
if [[ -n $option ]];then
  if [[ ${option,,} == "y" ]] || [[ ${option,,} == "yes" ]];then
    echo -e "${yellow}Shall begin with updating thy packages${plain}"
    apt update
    apt upgrade -y
  else
    end
  fi
else
  end
fi