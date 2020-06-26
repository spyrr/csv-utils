#!/usr/bin/env python3
import pandas as pd
import sys
import os
import click


def process(heads: str, path: str) -> pd.DataFrame:
    print(f'[*] Start to extract columns from CSV files')
    curdir = os.getcwd()
    print(f'[*] Current dir, {curdir}')

    os.chdir(path)
    print(f'[*] Target directory, {os.getcwd()}')

    files = list(filter(lambda x: x.find('.csv') != -1, os.listdir()))
    heads = heads.strip().upper().split(',')

    for fn in files:
        if os.path.isfile(fn) is False:
            print(f'[|] (!) {fn} not found.')
            sys.exit(2)
        print(f'[|] Read file, {fn}')

        _b = pd.read_csv(fn, dtype=str)
        _b.columns = map(str.upper, _b.columns) # to upper case, foreach headers

        print(f'[*] Save the output to new_{fn}')
        _b[heads].to_csv(f'new_{fn}', index=False)

    print(f'[*] Finish')


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-c', '--columns', default=None, help='Head of columns (delimeter: ,)')
@click.option('-p', '--path', default='.', help='Path of input directory')
def main(columns: str, path: str):
    """Extract columns"""
    if columns is None:
        print(click.get_current_context().get_help())
        sys.exit(-1)

    process(columns, path.strip())
    

if __name__ == '__main__':
    main()
