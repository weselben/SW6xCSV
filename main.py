import requests
from requests.structures import CaseInsensitiveDict
from multiprocessing import Process
from time import sleep as sleep
import datetime
import json

# Shopware IDs
taxid = "15c0bb9029a845cda7104cf707999dd9"
saleschannelid = "6d8478bd752d4c17a19ad3f7e6af851a"
manufacturaid = "e31fe228f4b042c1ac2ef61143aa5fb3"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def getauthkey():
    from config import clientsecret, clientid
    url = "https://url.online/api/oauth/token"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    data = '{"grant_type": "client_credentials", ' \
           '"client_id": "' + clientid + '", ' \
                                         '"client_secret": "' + clientsecret + '" }'
    print("Loop Sektion wird gestartet!")
    print("[-------------------------------------------]")
    while True:
        print("Loop gestartet!")
        resp = requests.post(url, headers=headers, data=data)
        f = open("authkey", "w")
        now = datetime.datetime.now()
        print("Access-Token gespeichert!")
        f.write(resp.json()['access_token'])
        f.close()
        print(f"Wird nächstes mal um {now + datetime.timedelta(seconds=595)}")
        print("[-------------------------------------------]")
        sleep(595)


def mainfunc():
    def bearertoken():
        authkey = open("authkey", "r").read()
        print("Access-Token wurde geladen")
        return authkey

    def getartikels():
        print("getartikels gestartet")

        url = "https://url.online/api/product"

        headers = CaseInsensitiveDict()
        bearertoken()
        headers["Authorization"] = "Bearer " + bearertoken()
        headers["Content-type"] = "application/json"

        resp = requests.get(url, headers=headers)
        f = open("art.json", 'w')
        f.write(str(json.dumps(resp.json(), sort_keys=True, indent=4)))
        f.close()
        print("getartikels beendet")
        print("[-------------------------------------------]")

    def rawexportdatavars():
        datas = open("art-import.json", "r").read()
        print("Jsondatei geladen")
        return datas

    def rawexportdatanovars():
        datas = open("artohnevar.json", "r").read()
        print("Jsondatei geladen")
        return datas

    def importartfromcsv():
        print("Import aus CSV gestartet")
        import csv
        rows = []
        with open("export.csv", 'r') as xenimpfile:
            redcsv = csv.reader(xenimpfile)
            header = next(redcsv)
            print("stringreplace gestartet")
            for row in redcsv:
                artnumb = row[0]
                artname = row[3]
                pricenetraw = row[4]
                pricenet = pricenetraw.replace(',', '.')
                artdiscrip = "Beschreibung folgt in kürze!"
                artdiscrip = row[5]
                if "DEL" in artnumb:
                    print(f"Skipped [DEL]: {row}")
                elif "Orignal" and "Ersatzteil" in str(artname):
                    print(f"Skipped [Ersatzteil]: {row}")
                elif \
                        "-85" in str(artnumb) \
                                or "-80" in str(artnumb) \
                                or "-48" in str(artnumb) \
                                or "-86" in str(artnumb) \
                                or "-22" in str(artnumb) \
                                or "-28" in str(artnumb) \
                                or "-99" in str(artnumb) \
                                or "-90" in str(artnumb) \
                                or "-92" in str(artnumb) \
                                or "-50" in str(artnumb) \
                                or "-54" in str(artnumb) \
                                or "-56" in str(artnumb) \
                                or "-58" in str(artnumb) \
                                or "-68" in str(artnumb) \
                                or "-77" in str(artnumb) \
                                or "-27" in str(artnumb) \
                                or "-70" in str(artnumb) \
                                or "-85" in str(artnumb) \
                                or "-97" in str(artnumb) \
                                or "-17" in str(artnumb) \
                                or "-45" in str(artnumb) \
                                or "-15" in str(artnumb) \
                                or "-30" in str(artnumb) \
                                or "-40" in str(artnumb) \
                                or "-60" in str(artnumb) \
                                or "-95" in str(artnumb) \
                                or "-91" in str(artnumb) \
                                or "-82" in str(artnumb) \
                                or "-1" in str(artnumb) \
                                or "-2" in str(artnumb) \
                                or "-3" in str(artnumb) \
                                or "-4" in str(artnumb) \
                                or "-5" in str(artnumb) \
                                or "-6" in str(artnumb) \
                                or "-23" in str(artnumb) \
                                or "-7" in str(artnumb):
                    print(f"Skipped [Variante]: {row}")
                elif "Zwischend" in str(artname):
                    print("[-------------------------------------------]")
                    print(f"Passed [Dämmatte]: {row}")
                    editedexport = rawexportdatanovars().replace('{artnumb}', f"{artnumb}")
                    editedexport = editedexport.replace('{artname}', f"{artname}")
                    editedexport = editedexport.replace('{pricenet}', f"{float(pricenet)}")
                    editedexport = editedexport.replace('{pricebrut}', f"{round(float(pricenet) * float(1.19), 2)}")
                    print("Artikeltransfer wurde gestartet")
                    url = "https://url.online/api/product"
                    headers = CaseInsensitiveDict()
                    bearertoken()
                    headers["Authorization"] = "Bearer " + bearertoken()
                    headers["Content-type"] = "application/json"
                    resp = requests.post(url, headers=headers, data=str(editedexport))
                    try:
                        print(f'Responsecode: {resp.status_code}')
                    except Exception as e:
                        print(f"Error: {e}")
                        pass
                elif "Montage" in str(artname) and "Montagekle" not in str(artname):
                    print("[-------------------------------------------]")
                    print(f"Passed [Montage]: {row}")
                    editedexport = rawexportdatanovars().replace('{artnumb}', f"{artnumb}")
                    editedexport = editedexport.replace('{artname}', f"{artname}")
                    editedexport = editedexport.replace('{pricenet}', "0")
                    editedexport = editedexport.replace('{pricebrut}', "0")
                    print("Artikeltransfer wurde gestartet")
                    url = "https://url.online/api/product"
                    headers = CaseInsensitiveDict()
                    bearertoken()
                    headers["Authorization"] = "Bearer " + bearertoken()
                    headers["Content-type"] = "application/json"
                    resp = requests.post(url, headers=headers, data=str(editedexport))
                    try:
                        print(f'Responsecode: {resp.status_code}')
                    except Exception as e:
                        print(f"Error: {e}")
                        pass
                elif "Himmel" in str(artname) or "HIMMEL" in str(artname):
                    print("[-------------------------------------------]")
                    print(f"Passed [Himmel]: {row}")
                    editedexport = rawexportdatanovars().replace('{artnumb}', f"{artnumb}")
                    editedexport = editedexport.replace('{artname}', f"{artname}")
                    editedexport = editedexport.replace('{pricenet}', f"{float(pricenet)}")
                    editedexport = editedexport.replace('{pricebrut}', f"{round(float(pricenet) * float(1.19), 2)}")
                    print("Artikeltransfer wurde gestartet")
                    url = "https://url.online/api/product"
                    headers = CaseInsensitiveDict()
                    bearertoken()
                    headers["Authorization"] = "Bearer " + bearertoken()
                    headers["Content-type"] = "application/json"
                    resp = requests.post(url, headers=headers, data=str(editedexport))
                    try:
                        print(f'Responsecode: {resp.status_code}')
                    except Exception as e:
                        print(f"Error: {e}")
                        pass
                elif "MT" in str(artnumb):
                        print("[-------------------------------------------]")
                        print(f"Passed [{str(artname)}]: {row}")
                        editedexport = rawexportdatanovars().replace('{artnumb}', f"{artnumb}")
                        editedexport = editedexport.replace('{artname}', f"{artname}")
                        editedexport = editedexport.replace('{pricenet}', f"{float(pricenet)}")
                        editedexport = editedexport.replace('{pricebrut}', f"{round(float(pricenet) * float(1.19), 2)}")
                        print("Artikeltransfer wurde gestartet")
                        url = "https://url.online/api/product"
                        headers = CaseInsensitiveDict()
                        bearertoken()
                        headers["Authorization"] = "Bearer " + bearertoken()
                        headers["Content-type"] = "application/json"
                        resp = requests.post(url, headers=headers, data=str(editedexport))
                        try:
                            print(f'Responsecode: {resp.status_code}')
                        except Exception as e:
                            print(f"Error: {e}")
                            pass
                else:
                    print("[-------------------------------------------]")
                    print(f"Passed [{str(artname)}]: {row}")
                    pricenet_22 = float(pricenet) + float(26)
                    pricenet_85 = float(pricenet) + float(26)
                    pricenet_48 = float(pricenet) + float(26)
                    pricenet_80 = float(pricenet) + float(26)
                    pricenet_68 = float(pricenet) + float(50)
                    pricenet_50 = float(pricenet) + float(50)
                    pricenet_77 = float(pricenet) + float(26)
                    pricenet_91 = float(pricenet) + float(40)

                    editedexport = rawexportdatavars().replace('{artnumb}', f"{artnumb}")
                    editedexport = editedexport.replace('{artname}', f"{artname}")
                    editedexport = editedexport.replace('{artdiscrip}', f"{artdiscrip}")

                    editedexport = editedexport.replace('{pricenet}', f"{float(pricenet)}")
                    editedexport = editedexport.replace('{pricebrut}', f"{round(float(pricenet) * float(1.19), 2)}")

                    editedexport = editedexport.replace('{pricenet_22}', f"{float(pricenet_22)}")
                    editedexport = editedexport.replace('{pricebrut_22}',
                                                        f"{round(float(pricenet_22) * float(1.19), 2)}")

                    editedexport = editedexport.replace('{pricenet_85}', f"{float(pricenet_85)}")
                    editedexport = editedexport.replace('{pricebrut_85}',
                                                        f"{round(float(pricenet_85) * float(1.19), 2)}")

                    editedexport = editedexport.replace('{pricenet_48}', f"{float(pricenet_48)}")
                    editedexport = editedexport.replace('{pricebrut_48}',
                                                        f"{round(float(pricenet_48) * float(1.19), 2)}")

                    editedexport = editedexport.replace('{pricenet_80}', f"{float(pricenet_80)}")
                    editedexport = editedexport.replace('{pricebrut_80}',
                                                        f"{round(float(pricenet_80) * float(1.19), 2)}")

                    editedexport = editedexport.replace('{pricenet_68}', f"{float(pricenet_68)}")
                    editedexport = editedexport.replace('{pricebrut_68}',
                                                        f"{round(float(pricenet_68) * float(1.19), 2)}")

                    editedexport = editedexport.replace('{pricenet_50}', f"{float(pricenet_50)}")
                    editedexport = editedexport.replace('{pricebrut_50}',
                                                        f"{round(float(pricenet_50) * float(1.19), 2)}")

                    editedexport = editedexport.replace('{pricenet_77}', f"{float(pricenet_77)}")
                    editedexport = editedexport.replace('{pricebrut_77}',
                                                        f"{round(float(pricenet_77) * float(1.19), 2)}")

                    editedexport = editedexport.replace('{pricenet_91}', f"{float(pricenet_91)}")
                    editedexport = editedexport.replace('{pricebrut_91}',
                                                        f"{round(float(pricenet_91) * float(1.19), 2)}")
                    print("Artikeltransfer wurde gestartet")

                    url = "https://url.online/api/product"

                    headers = CaseInsensitiveDict()
                    bearertoken()
                    headers["Authorization"] = "Bearer " + bearertoken()
                    headers["Content-type"] = "application/json"
                    resp = requests.post(url, headers=headers, data=str(editedexport))
                    try:
                        print(f'Responsecode: {resp.status_code}')
                    except Exception as e:
                        print(f"Error: {e}")
                        pass

    importartfromcsv()


if __name__ == '__main__':
    p1 = Process(target=getauthkey)
    p1.start()
    p2 = Process(target=mainfunc)
    sleep(0.5)
    p2.start()
    p1.join()
    p2.join()
