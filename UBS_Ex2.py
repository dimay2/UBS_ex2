#libraries import
import requests
import json
from datetime import date, datetime, timedelta
#import urllib.parse
import csv
import logging
import certifi

#======== load settings from file =======
settings_file=open("settings")
settings_data=json.load(settings_file)
settings_file.close()

#global params initialization from "settings" (json) file
scan_id=settings_data['scan_id']
nessus_host=settings_data['nessus_host']
api_access_key=settings_data['api_access_key']
api_secret_key=settings_data['api_secret_key']

#global params definition
url = "https://"+nessus_host+":8834"
payload = {}
headers= {"X-ApiKeys": "accessKey="+api_access_key+"; secretKey="+api_secret_key}

# Open CSV file in write mode
csv_file = open('HostVulnerabilities.csv', 'w', newline='')
# # Create a CSV writer object pointer
csv_writer = csv.writer(csv_file)
output_str=['Scan name', 'Scanned host', 'Scan start time', ' Vulnerability name', 'Vulnerability Description', 'CVSS base score', 'CVE IDs/References']
csv_writer.writerow(output_str)

#logging
log_file=open("general.log",mode="w")
logging.basicConfig(filename='general.log', level=logging.INFO)

# ==== API call function - get CVE list====
def nessus_api_func():
    global url
    global payload
    global headers

    params = {}
    #print(certifi.where())
    try:
        # Fetch specific scan data by scan_id
        response_scan = requests.request("GET", url+"/scans/"+scan_id, headers=headers, data = payload, params=params, verify=False)
        if response_scan.status_code == 200:
            myjson = response_scan.json()
            #print(response.url)
            logging.info('API call URL - %s' %(response_scan.url))
            scan_name=myjson['info']['name']
            scan_targets=myjson['info']['targets']
            scan_start_time=datetime.fromtimestamp(myjson['info']['scanner_start'])
            #print(scan_name, scan_targets, scan_start_time)
            for vul_item in myjson['vulnerabilities']:
                base_score = ""   #declare empty base_score param
                vul_description = ""
                cve_id = ""
                base_score = ""

                vul_id=vul_item['plugin_id']
                vul_name=vul_item['plugin_name']
                print(vul_id,vul_name)
                response_plugin = requests.request("GET", url+"/plugins/plugin/"+str(vul_id), headers=headers, data = payload, params=params, verify=False)
                myjson_plugin = response_plugin.json()
                logging.info('API call URL - %s' %(response_plugin.url))
                for vul_attrib in myjson_plugin['attributes']:
                    if(vul_attrib['attribute_name']=="description"):
                        vul_description=vul_attrib['attribute_value']
                        vul_description=vul_description[:400]
                        #print(vul_description)
                    elif(vul_attrib['attribute_name']=="cvss3_base_score"):
                        base_score=vul_attrib['attribute_value']
                    elif(vul_attrib['attribute_name']=="cvss_base_score" and base_score==""):
                        base_score=vul_attrib['attribute_value']
                    elif(vul_attrib['attribute_name']=="cve"):
                        cve_id=vul_attrib['attribute_value']
                vulnerability_lst=[scan_name,scan_targets,scan_start_time,vul_name,vul_description,base_score,cve_id]
                csv_writer.writerow(vulnerability_lst)
        else:
            print("Nessus API scans call error code =",response_scan.status_code)
    except requests.exceptions.RequestException as e:
        logging.error('Nessus API call error: '+ str(e))
        raise SystemExit(e)

# ====== MAIN function ==========
def main():
    nessus_api_func()
    
    # Close the file
    csv_file.close()
    log_file.close()

#======= MAIN execution =======
if __name__ == "__main__":
    main()