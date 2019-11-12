Note: Any commands are run when the current directory is in /automation_website/backend folder. We assume that you're comfortable with changing directories in your command prompt (Linux or powershell). If you're not, don't hesitate to ask me (Jun De) or people around you for help and/or pick up a quick tutorial :)

### When developing code
1. Ensure that your computer has python3-venv
2. Enter the virtual environment to run your code.
   1. If you're using a Microsoft Windows command prompt window:
      ```venvBackend\Scripts\activate```
   2. Otherwise if you're using Linux OSes:
      ```source venv/bin/activate```
3. Do your development work
4. To exit the virtual environment
   ```deactivate```


### When deploying code on Docker (only for Linux OSes)
1. Ensure that requirements.txt states the latest set of python modules that our code requires
   ```
   source venvBackend\bin\activate
   pip3 freeze | grep -v "pkg-resources" > requirements.txt
   deactivate
   ```
2. ```sudo ./runapp.sh```
