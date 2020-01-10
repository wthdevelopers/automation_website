# retrieve_group_category
Retrieve all data from group, competition category, and category_group tables, and output as csv files.

### To retrieve data
Each column in the table would correspond to each column in the csv file by order. (refer to /backend/db_setup_scripts/setup.sql for order of columns)
```sudo ./main.sh```

### Misc
- To run test, 
  ```
  sudo ./test_input_data.sh
  sudo ./main.sh
  ```
- To revert to zero state (i.e. wipe all rows from group, competition_category, and category_group)
  ```sudo ./test_teardown.sh```
