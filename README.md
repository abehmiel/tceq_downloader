# TCEQ database downloader

## Requirements:

`python >= 3.6.1`

`click pandas requests xlrd`

## Instructions: 

- clone or extract the repository to a working directory

- Make a query into TCEQ here: https://www2.tceq.texas.gov/oce/eer/

- Download the .xls file near the top of the page to the working directory

- Create and activate a conda environment for the project: 

`conda env create -f environment.yml`

`conda activate tceq`

- Use the command line to run main.py with arguments:

`python main.py --input-filename="sample.xls" --output-filename="out.csv" --sleep-time=5`

`--input-filename` - the file from your query in the working directory or a path to it

`--output-filename` - the named output file csv (output file will have an index)

`--sleep-time` - seconds to sleep between requests. Probably should be at least 3, default is 5

- if you have a new query (new date ranges for example) then put the new xls file in the working directory and run the code again to get rich data from the new query
