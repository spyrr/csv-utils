#!/usr/bin/env python3
import pandas as pd
import sys
import os
import click


def save(filename: str, df: pd.DataFrame):
    print(f'[*] Save the output to {filename}')
    df.to_csv(filename, index=False)


def csv_concat(heads: str, path: str) -> pd.DataFrame:
    print(f'[+] Start to concat CSV files')
    curdir = os.getcwd()
    print(f'[|] Current dir, {curdir}')

    os.chdir(path)
    print(f'[|] Target directory, {os.getcwd()}')

    files = list(filter(lambda x: x.find('.csv') != -1, os.listdir()))

    concat = lambda c, _b: _b if c is None else pd.concat([c, _b])
    if heads is not None:
        print(f'[|] Headers: {heads}')
        heads = heads.strip().upper().split(',')
        concat = lambda c, _b: _b if c is None else pd.concat([c[heads], _b[heads]])

    c = None
    for fn in files:
        if os.path.isfile(fn) is False:
            print(f'[|] (!) {fn} not found.')
            sys.exit(2)
        print(f'[|] Read file, {fn}')

        _b = pd.read_csv(fn, dtype=str)
        _b.columns = map(str.upper, _b.columns)
        c = concat(c, _b)

    print(f'[*] Finish')
    os.chdir(curdir)
    return c 


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-c', '--columns', default=None, help='Head of columns (delimeter: ,)')
@click.option('-p', '--path', default='.', help='Path of input directory')
@click.option('-o', '--output', default='output.csv', help='Filename of output file')
def main(columns: str, path: str, output: str):
    """Concat CSV Files"""
    df = csv_concat(columns, path.strip())
    if df is None:
        print(f'[*] (!) Can`t find any CSV file.')
        print(click.get_current_context().get_help())
        sys.exit(-1)
    else:
        save(output, df)
    
    

if __name__ == '__main__':
    main()
