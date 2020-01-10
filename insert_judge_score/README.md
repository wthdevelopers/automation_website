# insert_judge_score
Takes judge and score data from Jame's server and inputs into database.

### To insert data
1. Ensure that each column in the csv files would correspond to each column in the table by order. (refer to /backend/db_setup_scripts/setup.sql for order of columns in table)
2. Ensure that the file holding judge data and score data are csv files named "judge_data.csv" and "score_data.csv" respectively. Also refer to /insert_judge_score/sample_data to ensure both files are formatted correctly.
3. Run ```sudo ./input_data.sh```

### Misc
To revert judge and score tables to initial state (which is empty), run ```sudo ./teardown.sh```
