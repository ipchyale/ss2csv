# ss2csv
Scripts for processing SpectraShop color files

## Basic usage from terminal

``python ss2csv.py [infile] [outfile]``

The outfile is optional. If left blank, the script will save a CSV file with the same basename as the TXT file you supply. Otherwise, it will save a CSV to whatever path you supply for outfile.

## Basic usage via import

```
import sys
sys.path.append("/path/to/parent/dir/where/ss2csv/dir/lives")
from ss2csv.ss2csv import file2table

df = file2table(ssfile.txt)
```

So for example, on my machine, the git directory for ss2csv (which you should clone) lives in my home directory. So I write:

```
import sys
sys.path.append("/Users/damoncrockett")
from ss2csv.ss2csv import file2table

df = file2table(ssfile.txt)
```
