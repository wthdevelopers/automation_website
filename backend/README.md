### Setting up
- Install dependencies by running:
  ```sudo ./setup.sh```
- Make a copy of /backend/config_template.py as /backend/config.py, change the parameters of the classes that you'll be using.
  - Classes
    - If you'll be running the server for production, alter parameters for class Production
    - If you'll be running the server to execute tests, alter parameters for class RemoteTest
  - Paramters
    - USER: Username to connect to MySQL db
    - PW: Password
    - HOST: IP address of the MySQL server
    - DB_NAME 

### Running backend server
```./run_app.sh```

### Running existing tests
- Set up DB as above
- Configure config.py to contain the correct parameter values for class RemoteTest
- Run backend server for running tests (on your own computer) by running ```./run_app_test.sh```
- On the same computer, run ```python3 run_backend_tests.py```
