1. copy files under dedicated directory where it will be executed. Example - c:\my_python\UBS_ex2\

2. import all necessary libraries
 
 - open Python prompt by typing python in command line
 
 - change current directory to the files directory (see №1 above)
   Example: # cd c:\my_python\UBS_ex2\
 
 - build "requirements" file for the required python libraries
  # pipreqs.exe --force .
  
 - install all required libraries/nodules
  # pip.exe install -r .\requirements.txt

3. set required app settings in the "settings" file, based on previously made specific vulnerabilities scan on Nessus
 Example of Scan summary : https://192.168.0.105:8834/#/scans/reports/5/scan-summary , where 192.168.0.105 is the host where Nessus was installed (by default its installed on "localhost")
  
  Settings parameters:
  scan_id - obtained from the scan summary string and its "5" in our example
  nessus_host - IP of the host where Nessus scanner installed ("localhost" or "192.168.0.105" like in example above)
	api_access_key & api_secret_key - are generated under scanner UI
			API generation link example: https://192.168.0.105:8834/#/settings/my-account/api-keys
			  or for same host scanner - https://localhost:8834/#/settings/my-account/api-keys
	
4. run the app
  Example: # python UBS_Ex2.py

5. Check the app execution logs in "general.log"