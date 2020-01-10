# insert_judge_info
Takes judge and score data from Jame's server and inputs into database.

### To insert data
1. Ensure that the file holding judge data and score data are csv files named "judge_data.csv" and "score_data.csv" respectively. Also refer to /insert_judge_info/sample_data to ensure both files are formatted correctly.
2. Run ```sudo ./input_data.sh```

### Misc
To revert judge and score tables to initial state (which is empty), run ```sudo ./teardown.sh```
