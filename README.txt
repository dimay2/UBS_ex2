1. copy files under dedicated directory where it will be executed. Example - c:\my_python\UBS_ex2\

2. import all necessary libraries
 
 - open Python prompt by typing python in command line
 
 - change current directory to the files directory (see №1 above)
   Example: # cd c:\my_python\UBS_ex2\
 
 - build "requirements" file for the required python libraries
  # pipreqs.exe --force .
  
 - install all required libraries/nodules
  # pip.exe install -r .\requirements.txt

3. set required app settings in the "settings" file

4. run the app
  Example: # python UBS_Ex1.py

5. Check the app execution logs in "general.log"