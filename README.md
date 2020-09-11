# TCEQ database downloader

## Requirements:

`click pandas requests`

## Instructions: 

- Make a query into TCEQ here: https://www2.tceq.texas.gov/oce/eer/

- Download the .xlsx file near the top of the page to the working directory

- Use the command line to run main.py with arguments:

`python main.py --input-filename="sample.xlsx" --output-filename="out.csv" --sleep-time=10`

`--input-filename` - the file from your query in the working directory or a path to it

`--output-filename` - the named output file csv (output file will have an index)

`--sleep-time` - seconds to sleep beetween requests. Probably should be at least 3, default is 10
