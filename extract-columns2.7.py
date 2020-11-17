#!/usr/bin/env python
from __future__ import print_function
import pandas as pd
import pandas.errors
import sys
import os
import click
import datetime


def process(heads, path):
    print('[*] Start to extract columns from CSV files')
    curdir = os.getcwd()
    try:
        resdir = curdir + '/results-' + datetime.datetime.now().strftime('%y%m%d-%H%M%S')
        os.mkdir(resdir)
    except FileExistError:
        resdir = curdir + '/results-' + datetime.datetime.now().strftime('%y%m%d-%H%M%S')
        os.mkdir(resdir)

    print('[*] Result directory, ' + resdir)

    os.chdir(path)
    print('[*] Target directory, ' + os.getcwd())

    files = list(filter(lambda x: x.find('.csv') != -1, os.listdir()))
    heads = heads.strip().upper().split(',')

    for fn in files:
        if os.path.isfile(fn) is False:
            print('[*] (!) ' + fn + ' not found.')
            sys.exit(2)
        print('    File, ' + fn + ' => ', end='')
        try:
            _b = pd.read_csv(fn, dtype=str, error_bad_lines=False)
            _b.columns = map(str.upper, _b.columns) # to upper case, foreach headers

            df = pd.DataFrame(columns=heads)
            df = pd.concat([df, _b])

            df[heads].to_csv(resdir + '/new_' + fn, index=False)
            print('saved to new_' + fn)
            del df
        # except KeyError:
        #     print(f'(!) there is no matching header(s): {heads}')
        except pandas.errors.EmptyDataError:
            print('(!) empty file.')
        except pandas.errors.ParserError:
            print('(!) file parsing error')

    print('[*] Finish')


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-c', '--columns', default=None, help='Head of columns (delimeter: ,)')
@click.option('-p', '--path', default='.', help='Path of input directory')
def main(columns, path):
    """Extract columns"""
    if columns is None:
        print(click.get_current_context().get_help())
        sys.exit(-1)

    process(columns, path.strip())
    

if __name__ == '__main__':
    main()
