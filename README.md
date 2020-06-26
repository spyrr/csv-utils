# csv-utils
- csv-concat
- extract-columns

# Requirements
```bash
$ pip install -r requirements.txt
```

# Usage

```bash
# csv-concat.py:
$ python3 csv-concat.py -c "a,b" -p "test" -o "output.csv"

# extract-columns.py:
$ python3 extract-columns.py -c "a,b" -p "test"
### output: "results-<current time>/new" + original filename
```
