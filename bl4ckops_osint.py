
import os
import sys
import time
import lxml
import colorama
import requests
import socks
import socket
import subprocess

from tqdm import tqdm
from bs4 import BeautifulSoup
from googlesearch import search
from colorama import Fore, Back, Style

# TOR Configuration
TOR_PROCESS = None

def start_tor_service():
    """Start TOR service if not already running"""
    global TOR_PROCESS
    try:
        # Check if TOR is already running
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = test_socket.connect_ex(("127.0.0.1", 9050))
        test_socket.close()
        
        if result == 0:
            print(Fore.GREEN + "[✓] TOR service already running on port 9050" + Style.RESET_ALL)
            return True
        
        print(Fore.CYAN + "[*] Starting TOR service..." + Style.RESET_ALL)
        TOR_PROCESS = subprocess.Popen(
            ["tor", "--SocksPort", "9050"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        for i in range(15):
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = test_socket.connect_ex(("127.0.0.1", 9050))
            test_socket.close()
            
            if result == 0:
                time.sleep(2)
                print(Fore.GREEN + "[✓] TOR service started successfully" + Style.RESET_ALL)
                return True
            
            time.sleep(1)
            print(Fore.CYAN + f"[*] Waiting for TOR... ({i+1}/15)" + Style.RESET_ALL, end='\r')
        
        print(Fore.RED + "\n[-] TOR startup timeout" + Style.RESET_ALL)
        return False
        
    except FileNotFoundError:
        print(Fore.RED + "[-] TOR not installed: sudo apt-get install tor" + Style.RESET_ALL)
        return False
    except Exception as e:
        print(Fore.RED + f"[-] Error: {e}" + Style.RESET_ALL)
        return False

def setup_tor_proxy():
    """Setup TOR SOCKS proxy"""
    try:
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket
        print(Fore.YELLOW + "[*] TOR proxy configured" + Style.RESET_ALL)
        return True
    except Exception as e:
        print(Fore.RED + f"[-] TOR setup failed: {e}" + Style.RESET_ALL)
        return False

def stop_tor_service():
    """Stop TOR service"""
    global TOR_PROCESS
    try:
        if TOR_PROCESS:
            TOR_PROCESS.terminate()
            TOR_PROCESS.wait(timeout=5)
    except:
        if TOR_PROCESS:
            TOR_PROCESS.kill()

def loading():
 
 loop = tqdm(total= 40000, position=0, leave=False)
 for k in range(40000):
   loop.set_description("Scrapping...".format(k))
   loop.update(1)
 
 loop.close

def leeker():
 
 print(Fore.WHITE + Back.GREEN + "\n" + "SELECT MODULE" + Style.RESET_ALL)
 print(Fore.GREEN + "\n===========================================================    ")
 print(Fore.GREEN +  "[1] : DUMP      | DUMP EMAIL PASS    | ID: A135 | ACTIVATE      ")
 print(Fore.GREEN +  "[2] : DUMP      | DUMP APACHE PASS   | ID: A166 | ACTIVATE      ")
 print(Fore.GREEN +  "[3] : DUMP      | DUMP SQL USER PASS | ID: A196 | ACTIVATE      ")
 print(Fore.GREEN +  "[4] : DUMP      | DUMP APIKEYS       | ID: A121 | ACTIVATE      ")
 print(Fore.GREEN +  "[5] : DUMP      | DUMP COOKIES       | ID: A115 | ACTIVATE      ")
 print(Fore.GREEN +  "============================================================\n  ")
 choose = input("[bl4ckops_osint] => ")
 if choose == "1":
 
   print(Fore.GREEN + "\n..:: DUMP EMAIL PASS ::..")
   print("\n[*] Scanning...\n")
   loading()
   data = "filetype:xls username password email"
   print("===============================================================================")
   for j in search(data, num_results=10, sleep_interval=2):
     print(j)
   print("===============================================================================\n")
   print("[*] All cookies scrapped\n")
   menu = input("[*] Please enter to continue...")
 
 elif choose == "2":
   
   print(Fore.GREEN + "\n..:: DUMP APACHE PASS ::..")
   print("\n[*] Scanning...\n")
   loading()
   data2 = "intext:" + "'" + "Index of /" + "'" + "+password.txt"
   print("===============================================================================")
   for j in search(data2, num_results=10, sleep_interval=2):
     print(j)
   print("===============================================================================\n")
   print("[*] All apache passwords scrapped\n")
   menu = input("[*] Please enter to continue...")
	
 elif choose == "3":
   
   print(Fore.GREEN + "\n..:: DUMP SQL USER PASS ::..")
   print("\n[*] Scanning...\n")
   loading()
   data3 = "filetype:sql user password"
   print("===============================================================================")
   for j in search(data3, num_results=10, sleep_interval=2):
     print(j)
   print("===============================================================================\n")
   print("[*] All sql user passwords scrapped\n")
   menu = input("[*] Please enter to continue...")
	
 elif choose == "4":
   
   print(Fore.GREEN + "\n..:: DUMP APIKEYS ::..")
   print("\n[*] Scanning...\n")
   loading()
   data4 = "intitle:" + "'" + "index of" + "'" + " intext:" + "apikey.txt"
   print("===============================================================================")
   for j in search(data4, num_results=10, sleep_interval=2):
      print(j)
   print("===============================================================================\n")
   print("[*] All api keys scrapped\n")
	
 elif choose == "5":
 
   print(Fore.GREEN + "\n..:: DUMP COOKIES ::..")
   print("\n[*] Scanning...\n")
   loading()
   data5 = "intitle:" "'" + "index of " + "'" + "intext:" + "'" + "cookies.txt" + "'"
   print("===============================================================================")
   for j in search(data5, num_results=10, sleep_interval=2):
      print(j)
   print("===============================================================================\n")
   print("[*] All cookies scrapped\n")
   menu = input("[*] Please enter to continue...")

def files():
 
 print(Fore.GREEN + "\n..:: FILE SCRAPPER::..")
 target = input(Fore.GREEN + "\n[*] Please target domain name: ")
 print(Fore.GREEN + "\n[+] target: " + target + " engine: google(stable)")
 print(Fore.GREEN + "\n[*] Waiting progress, please wait...\n")
 time.sleep(2)
 print("[*] File scrapper started\n")
 print("[*] Scrapping files(pdf): " + "[" + target + ".com" + "]\n")
 loading()
 data = "site:" + target + ".com " + "filetype:pdf"
 print("===============================================================================")
 for j in search(data, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(txt): " + "[" + target + ".com" + "]\n")
 loading()
 data2 = "site:" + target + ".com " + "filetype:txt"
 print("===============================================================================")
 for j in search(data2, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(doc): " + "[" + target + ".com" + "]\n")
 loading()
 data3 = "site:" + target + ".com " + "filetype:doc"
 print("===============================================================================")
 for j in search(data3, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(docx): " + "[" + target + ".com" + "]\n")
 loading()
 data4 = "site:" + target + ".com " + "filetype:docx"
 print("===============================================================================")
 for j in search(data4, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(xls): " + "[" + target + ".com" + "]\n")
 loading()
 data5 = "site:" + target + ".com " + "filetype:xls"
 print("===============================================================================")
 for j in search(data5, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(xlsx): " + "[" + target + ".com" + "]\n")
 loading()
 data6 = "site:" + target + ".com " + "filetype:xlsx"
 print("===============================================================================")
 for j in search(data6, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(ppt): " + "[" + target + ".com" + "]\n")
 loading()
 data7 = "site:" + target + ".com " + "filetype:ppt"
 print("===============================================================================")
 for j in search(data7, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(htm): " + "[" + target + ".com" + "]\n")
 loading()
 data8 = "site:" + target + ".com " + "filetype:htm"
 print("===============================================================================")
 for j in search(data8, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(html): " + "[" + target + ".com" + "]\n")
 loading()
 data9 = "site:" + target + ".com " + "filetype:html"
 print("===============================================================================")
 for j in search(data9, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(zip): " + "[" + target + ".com" + "]\n")
 loading()
 data10 = "site:" + target + ".com " + "filetype:zip"
 print("===============================================================================")
 for j in search(data10, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(tar): " + "[" + target + ".com" + "]\n")
 loading()
 data11= "site:" + target + ".com " + "filetype:tar"
 print("===============================================================================")
 for j in search(data11, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(flv): " + "[" + target + ".com" + "]\n")
 loading()
 data12 = "site:" + target + ".com " + "filetype:flv"
 print("===============================================================================")
 for j in search(data12, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(mp4): " + "[" + target + ".com" + "]\n")
 loading()
 data13 = "site:" + target + ".com " + "filetype:mp4"
 print("===============================================================================")
 for j in search(data13, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(jpg): " + "[" + target + ".com" + "]\n")
 loading()
 data14 = "site:" + target + ".com " + "filetype:jpg"
 print("===============================================================================")
 for j in search(data14, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(png): " + "[" + target + ".com" + "]\n")
 loading()
 data15 = "site:" + target + ".com " + "filetype:png"
 print("===============================================================================")
 for j in search(data15, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(mp3): " + "[" + target + ".com" + "]\n")
 loading()
 data16 = "site:" + target + ".com " + "filetype:mp3"
 print("===============================================================================")
 for j in search(data16, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(mp4): " + "[" + target + ".com" + "]\n")
 loading()
 data17 = "site:" + target + ".com " + "filetype:mp4"
 print("===============================================================================")
 for j in search(data17, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(gz): " + "[" + target + ".com" + "]\n")
 loading()
 data18 = "site:" + target + ".com " + "filetype:gz"
 print("===============================================================================")
 for j in search(data18, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(bz2): " + "[" + target + ".com" + "]\n")
 loading()
 data19 = "site:" + target + ".com " + "filetype:bz2"
 print("===============================================================================")
 for j in search(data19, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] All file types scrapped\n")
 menu = input("[*] Please enter to continue...")

def numbers():
 
 print(Fore.GREEN + "\n..:: NUMBER SCRAPPER ::..")
 target = input(Fore.GREEN + "\n[*] Please target domain name: ")
 number = input("[*] Please enter country code: ")
 print(Fore.GREEN + "\n[+] target: " + target + " engine: google(stable)")
 print(Fore.GREEN + "\n[*] Waiting progress, please wait...\n")
 time.sleep(2)
 print("[*] Number scrapper started\n")
 print("\n[*] Scrapping numbers(" + number + "): " + "[" + target + ".com" + "]\n")
 loading()
 data20 = "site:" + target + ".com " + "intext:Whatsapp " + number
 print("===============================================================================")
 for j in search(data20, num_results=10, sleep_interval=2):
    print(j)
 print("===============================================================================\n")
 print("[*] All phone numbers scrapped\n")
 menu = input("[*] Please enter to continue...")
 
def mails():

 print(Fore.GREEN + "\n..:: MAIL SCRAPPER ::..")
 target = input(Fore.GREEN + "\n[*] Please target domain name: ")
 print(Fore.GREEN + "\n[+] target: " + target + " engine: google(stable)")
 print(Fore.GREEN + "\n[*] Waiting progress, please wait...\n")
 time.sleep(2)
 print("[*] Mail scrapper started\n")
 print("[*] Scrapping mails(example@gmail.com): " + "[" + target + ".com" + "]\n")
 loading()
 data21 = "site:" + target + ".com " + "intext:@gmail"
 print("===============================================================================")
 for j in search(data21, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping mails(example@gmail.com): " + "[" + target + ".com" + "]\n")
 loading()
 data22 = "site:" + target + ".com " + "intext:@gmail"
 print("===============================================================================")
 for j in search(data22, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping mails(example@hotmail.com): " + "[" + target + ".com" + "]\n")
 loading()
 data23 = "site:" + target + ".com " + "intext:@hotmail.com"
 print("===============================================================================")
 for j in search(data23, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping mails(example@yandex.com): " + "[" + target + ".com" + "]\n")
 loading()
 data24 = "site:" + target + ".com " + "intext:@yandex.com"
 print("===============================================================================")
 for j in search(data24, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping mails(example@yahoo.com): " + "[" + target + ".com" + "]\n")
 loading()
 data25 = "site:" + target + ".com " + "intext:@yahoo.com"
 print("===============================================================================")
 for j in search(data25, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping mails(example@gmx.com): " + "[" + target + ".com" + "]\n")
 loading()
 data26 = "site:" + target + ".com " + "intext:@gmx.com"
 print("===============================================================================")
 for j in search(data26, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping mails(example@zoho.com): " + "[" + target + ".com" + "]\n")
 loading()
 data27 = "site:" + target + ".com " + "intext:@zoho.com"
 print("===============================================================================")
 for j in search(data27, num_results=10, sleep_interval=2):
   print(j) 
 print("===============================================================================\n") 
 print("[*] Scrapping mails(example@aol.com): " + "[" + target + ".com" + "]\n")
 loading()
 data28 = "site:" + target + ".com " + "intext:@aol.com"
 print("===============================================================================")
 for j in search(data28, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping mails(example@email.com): " + "[" + target + ".com" + "]\n")
 loading()
 data29 = "site:" + target + ".com " + "intext:@email.com"
 print("===============================================================================")
 for j in search(data29, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] All mails scrapped\n")
 menu = input("[*] Please enter to continue...")

def pages():
 
 print(Fore.GREEN + "\n..:: PAGES SCRAPPER ::..")
 target = input(Fore.GREEN + "\n[*] Please target domain name: ")
 print(Fore.GREEN + "\n[+] target: " + target + " engine: google(stable)")
 print(Fore.GREEN + "\n[*] Waiting progress, please wait...\n")
 time.sleep(2)
 print("[*] Pages scrapper started\n")
 print("\n[*] Scrapping blog pages: " + "[" + target + ".com" + "]\n")
 loading()
 data30 = "site:" + target + " intext:blog"
 print("===============================================================================")
 for j in search(data30, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping security pages: " + "[" + target + ".com" + "]\n")
 loading()
 data31 = "site:" + target + " intext:security"
 print("===============================================================================")
 for j in search(data31, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping complaint pages: " + "[" + target + ".com" + "]\n")
 loading()
 data32 = "site:" + target + " intext:complaint"
 print("===============================================================================")
 for j in search(data32, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping document pages: " + "[" + target + ".com" + "]\n")
 loading()
 data33 = "site:" + target + " intext:documents"
 print("===============================================================================")
 for j in search(data33, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping punishment pages: " + "[" + target + ".com" + "]\n")
 loading()
 data34 = "site:" + target + " intext:punishment"
 print("===============================================================================")
 for j in search(data34, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping database pages: " + "[" + target + ".com" + "]\n")
 loading()
 data35 = "site:" + target + " intext:database"
 print("===============================================================================")
 for j in search(data35, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping state pages: " + "[" + target + ".com" + "]\n")
 loading()
 data36 = "site:" + target + " intext:state"
 print("===============================================================================")
 for j in search(data36, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping hospital pages: " + "[" + target + ".com" + "]\n")
 loading()
 data37 = "site:" + target + " intext:hospital"
 print("===============================================================================")
 for j in search(data37, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping school pages: " + "[" + target + ".com" + "]\n")
 loading()
 data38 = "site:" + target + " intext:school"
 print("===============================================================================")
 for j in search(data38, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping airport pages: " + "[" + target + ".com" + "]\n")
 loading()
 data39 = "site:" + target + " intext:airport"
 print("===============================================================================")
 for j in search(data39, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping railway pages: " + "[" + target + ".com" + "]\n")
 loading()
 data40 = "site:" + target + " intext:railway"
 print("===============================================================================")
 for j in search(data40, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] All pages scrapped\n")
 menu = input("[*] Please enter to continue...")

def other():
 
 print(Fore.GREEN + "\n..:: OTHER SCRAPPER ::..")
 target = input(Fore.GREEN + "\n[*] Please target domain name: ")
 number = input("[*] Please enter country code: ")
 print(Fore.GREEN + "\n[+] target: " + target + " engine: google(stable)")
 print(Fore.GREEN + "\n[*] Waiting progress, please wait...\n")
 time.sleep(2)
 print("[*] Other scrapper started\n")
 print("[*] Scrapping releated pages: " + "[" + target + ".com" + "]\n")
 loading()
 data41 = "related:" + target +".com"
 print("===============================================================================")
 for j in search(data41, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping links: " + "[" + target + ".com" + "]\n")
 loading()
 data42 = "link:" + target +".com"
 print("===============================================================================")
 for j in search(data42, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping info page: " + "[" + target + ".com" + "]\n")
 loading()
 data43 = "info:" + target +".com"
 print("===============================================================================")
 for j in search(data42, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping user info\n")
 user = input("\n[*] Scrapping username: ")
 print("\n[*] Scrapping user: " + user)
 loading()
 data44 = user + "intext:"+target
 print("===============================================================================")
 for j in search(data42, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")  
 print("[*] All other scrapping complated\n")
 menu = input("[*] Please enter to continue...")

def password():
 
 print(Fore.GREEN + "\n..:: PASSWORD SCRAPPER ::..")
 target = input(Fore.GREEN + "\n[*] Please target domain name: ")
 print("[*] Scrapping passwords[1]: " + "[" + target + ".com" + "]\n")
 loading()
 data41 = "site" + target +".com filetype:password" 
 print("===============================================================================")
 for j in search(data41, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping passwords[2]: " + "[" + target + ".com" + "]\n")
 loading()
 data42 = "site" + target +".com filetype:passwords" 
 print("===============================================================================")
 for j in search(data42, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping passwords[3]: " + "[" + target + ".com" + "]\n")
 loading()
 data43 = "site" + target +".com inurl:/etc/passwd" 
 print("===============================================================================")
 for j in search(data43, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n") 
 print("[*] Scrapping passwords[4]: " + "[" + target + ".com" + "]\n")
 loading()
 data44 = "site" + target +".com filetype:log.txt" 
 print("===============================================================================")
 for j in search(data44, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n") 
 print("[*] All passwords scrapped\n")
 menu = input("[*] Please enter to continue...")

def section():
    print(Fore.WHITE + Back.GREEN + "\n" + "SELECT MODULE" + Style.RESET_ALL)
    print(Fore.GREEN + "\n===========================================================    ")
    print(Fore.GREEN + "[1] : FILES     | FILES SCRAPPING    | ID: A235 | ACTIVATE      ")
    print(Fore.GREEN + "[2] : NUMBERS   | NUMBERS SCRAPPING  | ID: A312 | ACTIVATE      ")
    print(Fore.GREEN + "[3] : EMAILS    | EMAILS SCRAPPING   | ID: A221 | ACTIVATE      ")
    print(Fore.GREEN + "[4] : PAGES     | PAGES SCRAPPING    | ID: A186 | ACTIVATE      ")
    print(Fore.GREEN + "[5] : OTHER     | OTHER SCRAPPING    | ID: A189 | ACTIVATE      ")
    print(Fore.GREEN + "[6] : PASS      | PASS  SCRAPPING    | ID: A102 | ACTIVATE      ")
    print(Fore.GREEN + "============================================================\n  ")
    choose = input("[bl4ckops_osint] => ")
    if choose == "1":
        files()
    elif choose == "2":
        numbers()
    elif choose == "3":
        mails()
    elif choose == "4":
        pages()
    elif choose == "5":
        other()
    elif choose == "6":
        password()
    else:
        print("\nInvalid option!")
   
def full_scrapper():
 
 print(Fore.GREEN + "\n..:: FULL SCRAPPER ::..")
 target = input(Fore.GREEN + "\n[*] Please target domain name: ")
 print(Fore.GREEN + "\n[+] target: " + target + " engine: google(stable)")
 print(Fore.GREEN + "\n[*] Waiting progress, please wait...\n")
 time.sleep(2)
 print("[*] File scrapper started\n")
 print("[*] Scrapping files(pdf): " + "[" + target + ".com" + "]\n")
 loading()
 data = "site:" + target + ".com " + "filetype:pdf"
 print("===============================================================================")
 for j in search(data, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(txt): " + "[" + target + ".com" + "]\n")
 loading()
 data2 = "site:" + target + ".com " + "filetype:txt"
 print("===============================================================================")
 for j in search(data2, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(doc): " + "[" + target + ".com" + "]\n")
 loading()
 data3 = "site:" + target + ".com " + "filetype:doc"
 print("===============================================================================")
 for j in search(data3, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(docx): " + "[" + target + ".com" + "]\n")
 loading()
 data4 = "site:" + target + ".com " + "filetype:docx"
 print("===============================================================================")
 for j in search(data4, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(xls): " + "[" + target + ".com" + "]\n")
 loading()
 data5 = "site:" + target + ".com " + "filetype:xls"
 print("===============================================================================")
 for j in search(data5, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(xlsx): " + "[" + target + ".com" + "]\n")
 loading()
 data6 = "site:" + target + ".com " + "filetype:xlsx"
 print("===============================================================================")
 for j in search(data6, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(ppt): " + "[" + target + ".com" + "]\n")
 loading()
 data7 = "site:" + target + ".com " + "filetype:ppt"
 print("===============================================================================")
 for j in search(data7, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(htm): " + "[" + target + ".com" + "]\n")
 loading()
 data8 = "site:" + target + ".com " + "filetype:htm"
 print("===============================================================================")
 for j in search(data8, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(html): " + "[" + target + ".com" + "]\n")
 loading()
 data9 = "site:" + target + ".com " + "filetype:html"
 print("===============================================================================")
 for j in search(data9, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(zip): " + "[" + target + ".com" + "]\n")
 loading()
 data10 = "site:" + target + ".com " + "filetype:zip"
 print("===============================================================================")
 for j in search(data10, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(tar): " + "[" + target + ".com" + "]\n")
 loading()
 data11= "site:" + target + ".com " + "filetype:tar"
 print("===============================================================================")
 for j in search(data11, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(flv): " + "[" + target + ".com" + "]\n")
 loading()
 data12 = "site:" + target + ".com " + "filetype:flv"
 print("===============================================================================")
 for j in search(data12, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(mp4): " + "[" + target + ".com" + "]\n")
 loading()
 data13 = "site:" + target + ".com " + "filetype:mp4"
 print("===============================================================================")
 for j in search(data13, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(jpg): " + "[" + target + ".com" + "]\n")
 loading()
 data14 = "site:" + target + ".com " + "filetype:jpg"
 print("===============================================================================")
 for j in search(data14, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(png): " + "[" + target + ".com" + "]\n")
 loading()
 data15 = "site:" + target + ".com " + "filetype:png"
 print("===============================================================================")
 for j in search(data15, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(mp3): " + "[" + target + ".com" + "]\n")
 loading()
 data16 = "site:" + target + ".com " + "filetype:mp3"
 print("===============================================================================")
 for j in search(data16, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(mp4): " + "[" + target + ".com" + "]\n")
 loading()
 data17 = "site:" + target + ".com " + "filetype:mp4"
 print("===============================================================================")
 for j in search(data17, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(gz): " + "[" + target + ".com" + "]\n")
 loading()
 data18 = "site:" + target + ".com " + "filetype:gz"
 print("===============================================================================")
 for j in search(data18, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping files(bz2): " + "[" + target + ".com" + "]\n")
 loading()
 data19 = "site:" + target + ".com " + "filetype:bz2"
 print("===============================================================================")
 for j in search(data19, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] All file types scrapped\n")
 print("[*] Please Wait 90 seconds for next action...\n")
 time.sleep(90)
 print("[*] Phone number scrapper started\n")
 number = input("[*] Please enter country code: ")
 print("\n[*] Scrapping numbers(" + number + "): " + "[" + target + ".com" + "]\n")
 loading()
 data20 = "site:" + target + ".com " + "intext:Whatsapp " + number
 print("===============================================================================")
 for j in search(data20, num_results=10, sleep_interval=2):
    print(j)
 print("===============================================================================\n")
 print("[*] All phone numbers scrapped\n")
 print("[*] Mail scrapper started\n") 
 print("[*] Scrapping mails(example@gmail.com): " + "[" + target + ".com" + "]\n")
 loading()
 data21 = "site:" + target + ".com " + "intext:@gmail"
 print("===============================================================================")
 for j in search(data21, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping mails(example@gmail.com): " + "[" + target + ".com" + "]\n")
 loading()
 data22 = "site:" + target + ".com " + "intext:@gmail"
 print("===============================================================================")
 for j in search(data22, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping mails(example@hotmail.com): " + "[" + target + ".com" + "]\n")
 loading()
 data23 = "site:" + target + ".com " + "intext:@hotmail.com"
 print("===============================================================================")
 for j in search(data23, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping mails(example@yandex.com): " + "[" + target + ".com" + "]\n")
 loading()
 data24 = "site:" + target + ".com " + "intext:@yandex.com"
 print("===============================================================================")
 for j in search(data24, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping mails(example@yahoo.com): " + "[" + target + ".com" + "]\n")
 loading()
 data25 = "site:" + target + ".com " + "intext:@yahoo.com"
 print("===============================================================================")
 for j in search(data25, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping mails(example@gmx.com): " + "[" + target + ".com" + "]\n")
 loading()
 data26 = "site:" + target + ".com " + "intext:@gmx.com"
 print("===============================================================================")
 for j in search(data26, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping mails(example@zoho.com): " + "[" + target + ".com" + "]\n")
 loading()
 data27 = "site:" + target + ".com " + "intext:@zoho.com"
 print("===============================================================================")
 for j in search(data27, num_results=10, sleep_interval=2):
   print(j) 
 print("===============================================================================\n") 
 print("[*] Scrapping mails(example@aol.com): " + "[" + target + ".com" + "]\n")
 loading()
 data28 = "site:" + target + ".com " + "intext:@aol.com"
 print("===============================================================================")
 for j in search(data28, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping mails(example@email.com): " + "[" + target + ".com" + "]\n")
 loading()
 data29 = "site:" + target + ".com " + "intext:@email.com"
 print("===============================================================================")
 for j in search(data29, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] All mails scrapped\n")
 print("[*]Please Wait 90 seconds for next action...\n")
 time.sleep(90)
 print("[*] Page scrapper started\n")
 print("\n[*] Scrapping blog pages: " + "[" + target + ".com" + "]\n")
 loading()
 data30 = "site:" + target + " intext:blog"
 print("===============================================================================")
 for j in search(data30, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping security pages: " + "[" + target + ".com" + "]\n")
 loading()
 data31 = "site:" + target + " intext:security"
 print("===============================================================================")
 for j in search(data31, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping complaint pages: " + "[" + target + ".com" + "]\n")
 loading()
 data32 = "site:" + target + " intext:complaint"
 print("===============================================================================")
 for j in search(data32, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping document pages: " + "[" + target + ".com" + "]\n")
 loading()
 data33 = "site:" + target + " intext:documents"
 print("===============================================================================")
 for j in search(data33, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping punishment pages: " + "[" + target + ".com" + "]\n")
 loading()
 data34 = "site:" + target + " intext:punishment"
 print("===============================================================================")
 for j in search(data34, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping database pages: " + "[" + target + ".com" + "]\n")
 loading()
 data35 = "site:" + target + " intext:database"
 print("===============================================================================")
 for j in search(data35, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping state pages: " + "[" + target + ".com" + "]\n")
 loading()
 data36 = "site:" + target + " intext:state"
 print("===============================================================================")
 for j in search(data36, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping hospital pages: " + "[" + target + ".com" + "]\n")
 loading()
 data37 = "site:" + target + " intext:hospital"
 print("===============================================================================")
 for j in search(data37, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping school pages: " + "[" + target + ".com" + "]\n")
 loading()
 data38 = "site:" + target + " intext:school"
 print("===============================================================================")
 for j in search(data38, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping airport pages: " + "[" + target + ".com" + "]\n")
 loading()
 data39 = "site:" + target + " intext:airport"
 print("===============================================================================")
 for j in search(data39, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping railway pages: " + "[" + target + ".com" + "]\n")
 loading()
 data40 = "site:" + target + " intext:railway"
 print("===============================================================================")
 for j in search(data40, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] All pages scrapped\n")
 print("[*] Please Wait 90 seconds for next action...\n")
 time.sleep(90)
 print("\n[*] Other scrapper started\n")
 print("[*] Scrapping releated pages: " + "[" + target + ".com" + "]\n")
 loading()
 data41 = "related:" + target +".com"
 print("===============================================================================")
 for j in search(data41, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping links: " + "[" + target + ".com" + "]\n")
 loading()
 data42 = "link:" + target +".com"
 print("===============================================================================")
 for j in search(data42, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping info page: " + "[" + target + ".com" + "]\n")
 loading()
 data43 = "info:" + target +".com"
 print("===============================================================================")
 for j in search(data43, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping user info\n")
 user = input("\n[*] Scrapping username: ")
 print("\n[*] Scrapping user: " + user)
 loading()
 data44 = user + "intext:"+target
 print("===============================================================================")
 for j in search(data44, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")  
 enter = input("[*] Do you want to progress further? just press enter... ")
 print("\n[*] Password finder started\n")
 print("[*] Scrapping passwords[1]: " + "[" + target + ".com" + "]\n")
 loading()
 data45 = "site" + target +".com filetype:password" 
 print("===============================================================================")
 for j in search(data45, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping passwords[2]: " + "[" + target + ".com" + "]\n")
 loading()
 data46 = "site" + target +".com filetype:passwords" 
 print("===============================================================================")
 for j in search(data46, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Scrapping passwords[3]: " + "[" + target + ".com" + "]\n")
 loading()
 data47 = "site" + target +".com inurl:/etc/passwd" 
 print("===============================================================================")
 for j in search(data47, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n") 
 print("[*] Scrapping passwords[4]: " + "[" + target + ".com" + "]\n")
 loading()
 data48 = "site" + target +".com filetype:log.txt" 
 print("===============================================================================")
 for j in search(data48, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n") 
 print("[*] All processing complated\n")
 menu = input("[*] Please enter to continue...")
 menu()

def class_mode():
  
  print("\n..:: CLASS MODE ::..\n") 
  search = input("[*] Enter dork: ") 
  headers = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
  }

  params = {
    'q': search,
    'gl': 'us',
    'hl': 'en',
  }

  html = requests.get('https://www.google.com/search', headers=headers, params=params)
  soup = BeautifulSoup(html.text, 'lxml')

  for result in soup.select('.tF2Cxc'):
    title = result.select_one('.DKV0Md').text
    link = result.select_one('.yuRUbf a')['href']
    print("\n===============================================================================") 
    print(title, link, sep='\n')
    print("===============================================================================\n")
  print("[+] Dork scrapping complated\n")
  menu = input("[*] Please enter to continue...")
 
def other_mode():
 
 print("\n..:: OTHER MODE ::..\n") 
 search = input("[*] Enter dork: ")
 print("\n===============================================================================") 
 for j in search(search, num_results=10, sleep_interval=2):
     print(j)
 print("===============================================================================\n") 
 print("[*] Dork scrapping complated\n")
 ex = input("[*] Please enter to continue...")

def person():
 
 print("\n..:: PERSON SEARCHER ::..\n") 
 name = input("[*] Enter name(or social account name): ")
 sur = input("[*] Enter surname: ")
 phone = input("[*] Enter phone nuber(If you don't know, enter the country code): ")
 data_name = "intext: " + name
 print("\n[*] Search name[1]: " + "[" + name + "]\n")
 loading()
 print("===============================================================================")
 for j in search(data_name, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 data_surname = "intext: " + name + " " + sur
 print("[*] Search name and surname[2]: " + "[" + name + "]" + "[" + sur + "]\n")
 loading()
 print("===============================================================================")
 for j in search(data_surname, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 data_phone = "intext: " + phone
 print("[*] Search phone number[3]: " + "[" + phone + "]\n")
 loading()
 print("===============================================================================")
 for j in search(data_phone, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 data_instagram = "site: instagram.com intext: " + name
 print("[*] Search social account [instagram][4]: " + "[" + name + "]\n")
 loading()
 print("===============================================================================")
 for j in search(data_instagram, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 data_facebook = "site: facebook.com intext: " + name
 print("[*] Search social account [facebook][5]: " + "[" + name + "]\n")
 loading()
 print("===============================================================================")
 for j in search(data_facebook, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 data_twitter = "site: twitter.com intext: " + name
 print("[*] Search social account [twitter][6]: " + "[" + name + "]\n")
 loading()
 print("===============================================================================")
 for j in search(data_instagram, num_results=10, sleep_interval=2):
   print(j)
 print("===============================================================================\n")
 print("[*] Person scrapping complated\n")
 menu = input("[*] Please enter to continue...")

def manual_tools():

 print(Fore.WHITE + Back.GREEN + "\nMANUAL SCRAPPERS" + Style.RESET_ALL)
 print(Fore.GREEN + "\n===========================================================     ")
 print(Fore.GREEN +  "[1] : CLASS MODE | REQUESTS METHOD    | ID: A419 | ACTIVATE      ")
 print(Fore.GREEN +  "[2] : OTHER MODE | MODULE METHOD      | ID: A316 | ACTIVATE      ")
 print(Fore.GREEN +  "============================================================\n   ")
 choose = input("[bl4ckops_osint] => ")
 if choose == "1":
    class_mode()
 elif choose == "2":
    other_mode()

def auto_tools():

 print(Fore.WHITE + Back.GREEN + "\nAUTOMATIC SCRAPPERS" + Style.RESET_ALL)
 print(Fore.GREEN + "\n===========================================================    ")
 print(Fore.GREEN +  "[1] : FULL      | FULL SCRAPPING     | ID: A104 | ACTIVATE      ")
 print(Fore.GREEN +  "[2] : SECTION   | SELECT SECTION     | ID: A158 | ACTIVATE      ")
 print(Fore.GREEN +  "[3] : LEEKER    | USER PASS SCRAPPER | ID: A107 | ACTIVATE      ")
 print(Fore.GREEN +  "[4] : PERSON    | PERSON SEARCHER    | ID: A113 | ACTIVATE      ")
 print(Fore.GREEN +  "============================================================\n  ")
 choose = input("[bl4ckops_osint] => ")
 if choose == "1":
    full_scrapper()
 elif choose == "2":
    section()	
 elif choose == "3":
    leeker()
 elif choose == "4":
    person()

def exit():
   
   print("\n[*] Goodbye!")	
   time.sleep(2)
   os.system("reset")
     
def menu():
 
 os.system("clear")
 time.sleep(1)
 print("\n\n")
 print(Fore.GREEN + "────▐██████────██████▌                                                        ")
 print(Fore.GREEN + "────████████──████████                                                        ")
 print(Fore.GREEN + "───▐██████████████████▌                                                       ")
 print(Fore.GREEN + "───████████▀▀▀▀████████              ==============================           ")
 print(Fore.GREEN + "──▐█████▀──▄██▄──▀█████▌                                                      ")
 print(Fore.GREEN + "──█████───▐████▌───█████             ---==   FRAMEWORK V1.0   ==---           ")
 print(Fore.GREEN + "─▐██████▄──▀██▀──▄██████▌                                                     ")
 print(Fore.GREEN + "─██████████▄▄▄▄██████████            ==============================           ")
 print(Fore.GREEN + "▐███████─▐██████▌─███████▌                                                    ")
 print(Fore.GREEN + "███████▌──▐████▌──▐███████             .: By H4TIHIT4M :.                 ")
 print(Fore.GREEN + "                           ")
 print(Fore.GREEN + "         BL4CKOPS         ")
 print(Fore.GREEN + "                           ")
 print(Fore.WHITE + Back.GREEN + "CHOOSE MODULE" + Style.RESET_ALL)
 print(Fore.GREEN + "\n===========================================================    ")
 print(Fore.GREEN +  "[1] : AUTO      | AUTO SCRAPPING     | ID: A158 | ACTIVATE      ")
 print(Fore.GREEN +  "[2] : MANUAL    | MANUAL SCRAPPING   | ID: A167 | ACTIVATE      ")
 print(Fore.GREEN +  "[3] : EXIT      | EXIT PROGRAM       | ID: A116 | ACTIVATE      ")
 print(Fore.GREEN +  "============================================================\n  ")
 choose = input("[bl4ckops_osint] => ")
 if choose == "1":
    auto_tools()
 elif choose == "2":
    manual_tools()
 elif choose == "3":
    exit()

if __name__ == "__main__":
    try:
        print(Fore.CYAN + "\n[*] Initializing TOR..." + Style.RESET_ALL)
        if not start_tor_service():
            print(Fore.YELLOW + "[!] Warning: TOR not available, continuing..." + Style.RESET_ALL)
        else:
            if not setup_tor_proxy():
                print(Fore.YELLOW + "[!] Warning: TOR proxy setup failed..." + Style.RESET_ALL)
        
        menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Interrupted" + Style.RESET_ALL)
    finally:
        stop_tor_service()
