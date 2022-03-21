# customSintaxDB
Given a list of species get sequences and complete taxonomic 
classification of a list of entries

# Getting started

To dowload this repository from GitHub, the following commands can be run.

    git clone https://github.com/diegomic/customSintaxDB.git

`customSintaxDB.py` can run in any computer with python 3 (>3.6) installed. The following 
additional packages are required:
- biopython (tested with v.1.79)
- argparse

To install all the required package run:
    
    pip install -r requirements.txt


## Usage: 
```
usage: customSintaxDB.py [-h] -l LIST -o OUTPUT -g GENE [--email EMAIL] [--api_key API_KEY]
                        [--max_tries MAX_TRIES] [--sleep_between_tries SLEEP_BETWEEN_TRIES]

optional arguments:
  -h, --help            show this help message and exit
  -l LIST, --list LIST  File with the list of entry to search (default: None)
  -o OUTPUT, --output OUTPUT
                        Output File basename (default: None)
  -g GENE, --gene GENE  gene to search in entrez (default: None)

Entrez - NCBI's E-utilities:
  --email EMAIL         Email to use for make queries through to NCBI's E-utilities, 
                        if email is empty a warning is raised by the Entrez module. To make 
                        use of NCBI's E-utilities, NCBI requires you to specify your email 
                        address with each request. (default: None)
  --api_key API_KEY     API key to use for make queries through to NCBI's E-utilities, 
                        if empty a warning is raised by the Entrez module. Personal API key 
                        from NCBI. If not set, only 3 queries per second are allowed. 
                        Ten queries per seconds otherwise with a valid API key. (default: None)
  --max_tries MAX_TRIES
                        Configures how many times failed requests will be automatically 
                        retried on error. (default: 3)
  --sleep_between_tries SLEEP_BETWEEN_TRIES
                        The delay, in seconds, before retrying a request on error. 
                        (default: 15)
```

# Citing 

TODO  ADD citations 


