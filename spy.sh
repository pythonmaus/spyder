#!/bin/bash || #!/usr/env/bin/bash
green='\e[32m'
blue='\e[34m'
cyan='\e[36m'
red="\e[31m"
yellow='\e[33m'
plain='\e[0m'
hidden='\e[30m'

update_ui (){
  clear
  echo -e "$green
 ___  ___  _ _  ___  ___  ___                 .
/ __>| . \| | || . \| __>| . \\           +    -
\__ \|  _/\   /| | || _> |   /         . @    = *
<___/|_|   |_| |___/|___>|_\_\\         : #-.. -@=:
𝚂𝚙𝚢𝚍𝚎𝚛  𝙽𝚎𝚝𝚠𝚘𝚛𝚔                        :   @@@   *
$cyan𝙳𝚎𝚟 - 𝚂𝚑𝚊𝚍𝚎 $green                          =.- @%@#@ : =
$cyan𝙶𝚒𝚝𝚑𝚞𝚋 - 𝚑𝚊𝚛𝚔𝚎𝚛𝚋𝚢𝚝𝚎  $green                     :@*@-
                                        -* @@@ %
                                      :  # @*@ @ @.
                                       @ % :@- # +
${yellow}1.𝙿𝚒𝚗𝚐 𝚒𝚙 $green                                @    @
${yellow}2.𝚆𝚑𝚘 𝚊𝚖 𝚒 $green                              : @   #
${yellow}3.𝙲𝚊𝚙𝚝𝚞𝚛𝚎 𝚒𝚙 𝚋𝚢 𝚕𝚒𝚗𝚔  $green                    .   :
${yellow}4.𝚆𝚒𝚏𝚒/𝙽𝚎𝚝𝚠𝚘𝚛𝚔 𝙰𝚝𝚝𝚊𝚌𝚔 $green                     . .
${yellow}5.𝚂𝚙𝚢𝚌𝚑𝚊𝚝 𝚋𝚎𝚝𝚊
${yellow}6.𝙹𝚘𝚒𝚗 𝚝𝚑𝚎 𝚑𝚊𝚛𝚔𝚎𝚛𝚋𝚢𝚝𝚎 𝚌𝚘𝚖𝚖𝚞𝚗𝚒𝚝𝚢 𝚏𝚘𝚛 𝚖𝚘𝚛𝚎 𝚝𝚘𝚘𝚕𝚜/𝚞𝚙𝚍𝚊𝚝𝚎𝚜
${yellow}7.𝙴𝚡𝚒𝚝
${yellow}[+]𝚆𝚒𝚏𝚒 𝚋𝚛𝚞𝚝𝚎 𝚏𝚘𝚛𝚌𝚎 (𝚌𝚘𝚖𝚒𝚗𝚐 𝚜𝚘𝚘𝚗)
${yellow}[+]𝙱𝚕𝚞𝚎𝚝𝚘𝚘𝚝𝚑 𝚊𝚝𝚝𝚊𝚌𝚔 (𝚌𝚘𝚖𝚒𝚗𝚐 𝚜𝚘𝚘𝚗)
"
}
update_ui

timestamp(){
  echo -e "$(date +%a"."%H:%M)"
}
root_status(){
  if ! command sudo c &>/dev/null;then
    echo -e "${blue}𝙽𝚘𝚝 𝚛𝚘𝚘𝚝𝚎𝚍${plain}"
  else 
    echo -e "${blue}𝚁𝚘𝚘𝚝𝚎𝚍${plain}"
  fi
}

kill_switch (){
  kill $! 2>/dev/null
  kill $(cat temps/server.pid 2>/dev/null) 2>/dev/null
  kill $(cat temps/cloudflare.pid 2>/dev/null) 2>/dev/null
  rm temps/*.log 2>/dev/null && rm temps/*.pid 2>/dev/null 
  rm temps/swifi.json 2>/dev/null 
  echo ""
  take_option
}
loading(){
  x=0
  while [[ x -le $1 ]];do
    echo -ne "${green}   [     $2     ]...$(($1 - x))𝚜𝚎𝚌𝚜 ${plain}\r"
    trap kill_switch SIGINT
    sleep 1
    (( x++ ))
  done
  echo ""
}
traffic_monitor (){
  echo -e "${blue}[☯] 𝚁𝚎𝚝𝚛𝚒𝚎𝚟𝚎𝚍 𝚒𝚙 𝚊𝚍𝚍𝚛𝚎𝚜𝚜𝚎𝚜 𝚜𝚑𝚊𝚕𝚕 𝚊𝚙𝚙𝚎𝚊𝚛 𝚋𝚎𝚕𝚘𝚠 ${plain}"
  if [[ -r extras/ip.json ]];then
    len=$(jq 'length' extras/ip.json)
    while true;do
      lengt=$(jq 'length' extras/ip.json)
      if [[ $lengt -gt $len ]];then
        ((len+=1))
        ipn=$(jq -r 'to_entries | sort_by(keys) | .[-1].value.ip' extras/ip.json)
        echo "    ${ipn} "
      fi
      sleep 1
      trap kill_switch SIGINT
    done
  fi
}
server_loader (){
  if [[ -n $2 ]] && [[ $(expr length $2) -eq 4 ]];then
    python server.py -p $2 > temps/server.log 2>&1 & 
    echo $! > temps/server.pid
    echo -e "${blue}[¿] 𝚂𝚝𝚊𝚛𝚝𝚒𝚗𝚐 𝚝𝚑𝚎 𝚜𝚎𝚛𝚟𝚎𝚛..."
    sleep 5
    local="http://127.0.0.1:$2"
  
    status=$(tail -n 5 temps/server.log)
    if [[ "$status" == *"Restarting with stat"* ]];then
      echo -e "[☯] 𝚂𝚎𝚛𝚟𝚎𝚛 𝚑𝚊𝚜 𝚋𝚎𝚎𝚗 𝚜𝚝𝚊𝚛𝚝𝚎𝚍 : ${plain}${local}"
          
      if [[ -f 'url.json' ]];then
        echo -e "${blue}[☯] 𝙰𝚍𝚖𝚒𝚗 𝚙𝚊𝚐𝚎 ${plain}${local}/admin/$(jq -r '.url' url.json)"
        if [[ $3 == "cloudflare" ]];then
          echo -e "${blue}[♚] 𝚃𝚞𝚗𝚗𝚎𝚕 𝚑𝚘𝚜𝚝 𝚜𝚎𝚛𝚟𝚎𝚛 - 𝚌𝚕𝚘𝚞𝚍𝚏𝚕𝚊𝚛𝚎${plain}"
          cloudflared tunnel --url 127.0.0.1:$2 > temps/cloudflare.log 2>&1 &
          echo $! > temps/cloudflare.pid
          loading 15 "𝚂𝚎𝚝𝚞𝚙 𝚒𝚗 𝚙𝚛𝚘𝚐𝚛𝚎𝚜𝚜"
          tunnel=$(grep -oP 'https://[a-zA-Z0-9_-]+\.trycloudflare\.[a-z]{3}' temps/cloudflare.log)
          
          echo -e "${blue}[♚] 𝚂𝚎𝚗𝚍 𝚝𝚑𝚒𝚜 𝚝𝚘 𝚢𝚘𝚞𝚛 𝚝𝚊𝚛𝚐𝚎𝚝 : ${plain}${tunnel}"
          echo -e "${blue}[♚] 𝚃𝚞𝚗𝚗𝚎𝚕 𝚊𝚍𝚖𝚒𝚗 𝚙𝚊𝚐𝚎 : ${plain}$tunnel/admin/$(jq -r '.url' url.json)"
        fi
      echo -e "${blue}[×] 𝙴𝚗𝚝𝚎𝚛 ${red}𝙲𝚃𝚁𝙻-𝙲$blue 𝚝𝚘 𝚌𝚕𝚘𝚜𝚎 𝚜𝚎𝚛𝚟𝚎𝚛${plain}"
      fi
      traffic_monitor
    else
      inf=$(cat temps/server.log)
      if [[ "$inf" != *"already in use"* ]] && [[ "$inf"  != *"Permission denied"* ]];then
        echo -ne "${red}[⎚] 𝚙𝚘𝚛𝚝  𝚌𝚊𝚗 𝚘𝚗𝚕𝚢 𝚋𝚎 𝚊𝚗 𝚒𝚗𝚝𝚎𝚐𝚎𝚛 𝚟𝚊𝚕𝚞𝚎;${yellow}"
        echo""
        read -p "𝙴𝚗𝚝𝚎𝚛 𝚊 𝚗𝚎𝚠 𝚙𝚘𝚛𝚝 >>> " nport
        if [[ -n $nport  ]];then
          server_loader -p $nport $3
        fi
      elif [[ "$inf" == *"Permission denied"* ]];then
        echo -e "${red}𝙲𝚛𝚒𝚝𝚒𝚌𝚊𝚕 𝚎𝚛𝚛𝚘𝚛: 𝙿𝚎𝚛𝚖𝚒𝚜𝚜𝚒𝚘𝚗 𝚍𝚎𝚗𝚒𝚎𝚍"
      else
        echo -ne "${red}[✗] 𝚞𝚗𝚊𝚋𝚕𝚎 𝚝𝚘 𝚜𝚝𝚊𝚛𝚝 𝚜𝚎𝚛𝚟𝚎𝚛 : 𝚙𝚘𝚛𝚝 $2 𝚒𝚜 𝚊𝚕𝚛𝚎𝚊𝚍𝚢 𝚒𝚗 𝚞𝚜𝚎;${yellow}"
        echo""
        read -p "𝙴𝚗𝚝𝚎𝚛 𝚊 𝚗𝚎𝚠 𝚙𝚘𝚛𝚝 >>> " np
        if [[ -n $np  ]];then
          server_loader -p $np $3
        else 
          exit 0
        fi
      fi
    fi
  else
    echo -e "${blue}𝙿𝚘𝚛𝚝 𝚖𝚞𝚜𝚝 𝚋𝚎 4 𝚒𝚗 𝚕𝚎𝚗𝚐𝚝𝚑"
  fi
}
setup_ngrok(){
  install(){
    $(wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip)
    if ! [[ $? -gt 0 ]];then
      $(unzip ngrok-stable-linux-arm.zip) && rm ngrok-stable-linux-arm.zip
      $(chmod +x ngrok)
      $(mv ngrok $PREFIX/bin)
    fi
  }
  install
  if ! [[ $? -gt 0 ]];then
    echo -e "${green}Installation and setup completed${plain}"
  else
    tried=0
    while [[ tried -lt 2 ]];do
      ((tried+=1))
      echo -e "${red}An error was encountered...shall try again${plain}"
      install
    done
    echo -e "${red}Failed to install ngrok...Tried × $tried ${plain}"
    exit
  fi
}
swifi(){
  echo -e "$red
 ___  _    _  __  ___  __          [BRDCT]
/ __)( \/\/ )(  )(  _)(  )           ||
\__ \ \    /  )(  ) _) )(           /||\\
(___/  \/\/  (__)(_)  (__)         /_||_\\  
                                    \||/
                                     ||
𝙳𝚎𝚏𝚊𝚞𝚕𝚝 𝚙𝚘𝚛𝚝 : 80                  [WiFi]
 ${green} 
1) 𝙲𝚘𝚗𝚗𝚎𝚝𝚒𝚘𝚗 𝚋𝚊𝚜𝚎𝚍 𝚊𝚝𝚝𝚊𝚌𝚔
2) 𝙲𝚘𝚗𝚗𝚎𝚌𝚝𝚒𝚘𝚗𝚕𝚎𝚜𝚜, 𝚞𝚗𝚛𝚎𝚕𝚒𝚊𝚋𝚕𝚎 𝚋𝚞𝚝 𝚏𝚊𝚜𝚝 
  ${yellow}"
read -p "[$(timestamp)@𝚂𝚠𝚒𝚏𝚒] : " swifi_opt
if  [[ -n $swifi_opt ]] && [[ $swifi_opt == 1 ]] || [[ $swifi_opt == 2 ]];then
  echo -ne "${blue}𝙴𝚗𝚝𝚎𝚛 𝚝𝚊𝚛𝚐𝚎𝚝 𝚒𝚙 𝚊𝚍𝚍𝚛𝚎𝚜𝚜 𝚘𝚛 𝚑𝚘𝚜𝚝𝚗𝚊𝚖𝚎 : ${plain}" && read ip
  if [[ -n $ip ]];then
    echo -ne "${blue}𝙴𝚗𝚝𝚎𝚛 𝚝𝚊𝚛𝚐𝚎𝚝 𝚙𝚘𝚛𝚝 𝚘𝚛 𝚕𝚎𝚊𝚟𝚎 𝚎𝚖𝚙𝚝𝚢${plain} : " && read port
    if [[ -z $port ]];then
      port=80
    fi
  fi
  if [[ -n $ip ]];then
    if [[ $swifi_opt == 1 ]];then
      python swifi.py $ip $port "tcp" >temps/swifi.log 2>&1 &
      loading 15 "𝚂𝚌𝚊𝚕𝚒𝚗𝚐 𝚛𝚎𝚜𝚘𝚞𝚛𝚌𝚎𝚜"
      handle_swifi
      trap kill_switch SIGINT
    elif [[ $swifi_opt == 2 ]];then
      python swifi.py $ip $port "udp" >temps/swifi.log 2>&1 &
      handle_swifi
      trap kill_switch SIGINT
    fi
  fi
fi
}
handle_swifi(){
  while true;do
    status=$(jq -r '.status' temps/swifi.json 2>/dev/null)
    if [[ "$status" == "connection timeout" ]];then
      echo -e "${red}𝙲𝚘𝚗𝚗𝚎𝚌𝚝𝚒𝚘𝚗 𝚝𝚒𝚖𝚎𝚘𝚞𝚝${plain}"
      kill_switch
    elif [[ "$status" == "address not found" ]];then
      echo -e "${red}𝙰𝚍𝚍𝚛𝚎𝚜𝚜 𝚗𝚘𝚝 𝚏𝚘𝚞𝚗𝚍${plain}"
      kill_switch
    elif [[ "$status" == "sent" ]];then
      loading 30 "𝙼𝚘𝚗𝚒𝚝𝚘𝚛𝚒𝚗𝚐 𝚒𝚝 𝚙𝚛𝚘𝚐𝚛𝚎𝚜𝚜"
      handle_swifi
    elif [[ "$status" == "completed" ]];then
      echo -e "${green}𝙾𝚙𝚎𝚛𝚊𝚝𝚒𝚘𝚗 𝚌𝚘𝚖𝚙𝚕𝚎𝚝𝚎𝚍${plain}"
      kill_switch
    fi
    sleep 5
  done
}
take_option(){
  echo -ne "$green[$(timestamp)] >>> " && read option
  if [[ -n option ]];then
    case $option in 
      1)
        echo -ne "${blue}Provide an ip address : ${plain}" && read ip_prov
        ping -c1 $ip_prov 2>/dev/null
        if ! [[ $? -ge 1 ]] || [[ $? -ge 1 ]];then
          take_option
        fi
      ;;
      2)
        root_status
        echo -e "${blue}User : $(whoami)"
        echo -e "Hostname : $(hostname)"
        echo -e "Operating system : $(uname)"
        echo -e "Kernel version : $(uname -r)${plain}"
        take_option
      ;;
      3)
        server_opt(){
          echo -e "$green"
          echo "𝙲𝚊𝚙𝚝𝚞𝚛𝚎 𝚟𝚒𝚌𝚝𝚒𝚖'𝚜 𝚙𝚞𝚋𝚕𝚒𝚌 𝚒𝚙 𝚋𝚢 𝚕𝚒𝚗𝚔"
          echo ""
          echo "1) 𝚈𝚘𝚞 𝚑𝚘𝚜𝚝 "
          echo " 2) 𝚃𝚞𝚗𝚗𝚎𝚕 𝚑𝚘𝚜𝚝 - 𝙽𝚐𝚛𝚘𝚔"
          echo "  3) 𝚃𝚞𝚗𝚗𝚎𝚕 𝚑𝚘𝚜𝚝 - 𝚌𝚕𝚘𝚞𝚍𝚏𝚕𝚊𝚛𝚎"
          echo "  4) 𝙲𝚘𝚗𝚏𝚒𝚐𝚞𝚛𝚎/𝚌𝚑𝚊𝚗𝚐𝚎 𝚗𝚐𝚛𝚘𝚔 𝚊𝚞𝚝𝚑 𝚝𝚘𝚔𝚎𝚗"
          echo " 5) 𝙷𝚎𝚕𝚙"
          echo "6) 𝙴𝚡𝚒𝚝" 
          echo -ne "$yellow[$(timestamp)@𝚂𝚎𝚛𝚟𝚎𝚛] : $plain" && read option
          if [[ -n $option ]];then
            case $option in 
              1)
                server_loader -p 5000
              ;;
              2)
                #$(chmod +x $PREFIX/bin/ngrok)
                #server_loader -p 5000 ngr
                echo -e "${red}𝚄𝚗𝚍𝚎𝚛-𝚍𝚎𝚟𝚎𝚕𝚘𝚙𝚖𝚎𝚗𝚝... 𝚂𝚠𝚒𝚝𝚌𝚑𝚒𝚗𝚐 𝚝𝚘 𝚌𝚕𝚘𝚞𝚍𝚏𝚕𝚊𝚛𝚎 𝚝𝚞𝚗𝚗𝚎𝚕 ${plain}"
                loading 5 "𝚆𝚊𝚒𝚝"
                server_loader -p 5000 "cloudflare"
              ;;
              3)
              server_loader -p 5000 "cloudflare"
              ;;
              4)
                if ! command -v ngrok &>/dev/null;then
                  echo "Ngrok missing...shall proceed to install"
                  setup_ngrok
                else
                  echo -ne "𝙽𝚐𝚛𝚘𝚔 𝚊𝚞𝚝𝚑 𝚝𝚘𝚔𝚎𝚗 >>> ${hidden}" && read ngrok_token
                  if [[ -n $ngrok_opt ]];then
                    ngrok config add-authtoken $ngrok_token
                    server_opt
                  fi
                fi
              ;;
              5)
                xdg-open https://github.com/harkerbye
              ;;
              6)
                take_option
              ;;
              *)
                if [[ -n $option ]];then
                  echo -e "$red$option is an unknown command$plain"
                else
                  take_option
                fi
              ;;
            esac
          fi
        }
        server_opt
        ;;
      4)
        swifi
        ;;
      5)
        python messaging.py
      ;;
      6)
        xdg-open https://whatsapp.com/channel/0029Vb5f98Z90x2p6S1rhT0S
      ;;
      7)
      exit
      ;;
      'menu')
        update_ui
        take_option
      ;;
      *)
        if [[ -n $option ]];then
          echo -e "$red$option is an unknown command$plain"
          take_option
        else
          take_option
        fi
        ;;
    esac
  else
    echo "Enter a valid option"
  fi
}

while true;do
  take_option
done
