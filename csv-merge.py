#!/usr/bin/env python3
import pandas as pd
import sys
import os
import click


def save(filename: str, df: pd.DataFrame):
    print(f'[*] Save the output to {filename}')
    df.to_csv(filename, index=False)


def merge(heads: str, path: str) -> pd.DataFrame:
    print(f'[+] Start to merge CSV files')
    curdir = os.getcwd()
    print(f'[|] Current dir, {curdir}')

    os.chdir(path)
    print(f'[|] Directory placed in target files, {os.getcwd()}')

    files = list(filter(lambda x: x.find('.csv') != -1, os.listdir()))

    concat = lambda merged, _b: _b if merged is None else pd.concat([merged, _b])
    if heads is not None:
        print(f'[|] Headers: {heads}')
        heads = heads.strip().upper().split(',')
        concat = lambda merged, _b: _b if merged is None else pd.concat([merged[heads], _b[heads]])

    merged = None
    for fn in files:
        if os.path.isfile(fn) is False:
            print(f'[|] (!) {fn} not found.')
            sys.exit(2)
        print(f'[|] Read file, {fn}')

        _b = pd.read_csv(fn, dtype=str)
        _b.columns = map(str.upper, _b.columns)
        merged = concat(merged, _b)

    print(f'[*] Finish')
    os.chdir(curdir)
    return merged


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-c', '--columns', default=None, help='Head of columns (delimeter: ,)')
@click.option('-p', '--path', default='.', help='Path of input directory')
@click.option('-o', '--output', default='output.csv', help='Filename of merged CSV file')
def main(columns: str, path: str, output: str):
    """Merge CSV Files from the path to output"""
    merged_df = merge(columns, path.strip())
    if merged_df is None:
        print(f'[*] (!) Can`t find any CSV file.')
        print(click.get_current_context().get_help())
        sys.exit(-1)
    else:
        save(output, merged_df)
    
    

if __name__ == '__main__':
    main()
