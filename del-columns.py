#!/usr/bin/env python3
import pandas as pd
import pandas.errors
import sys
import click


def process(heads: str, filename: str, output):
    print(f'[*] Start to remove target columns, "{heads}", from CSV files')

    try:
        df = pd.read_csv(filename, dtype=str, error_bad_lines=False)
        o = df.drop(heads.split(','), axis=1)

        o.to_csv(output, index=False)
        print(f'[*] Save the contents to {output}')
    except KeyError:
        print(f'(!) KeyError has been occurred.')
        sys.exit(-1)
    except pandas.errors.EmptyDataError:
        print(f'(!) empty file.')
    except pandas.errors.ParserError:
        print(f'(!) file parsing error')

    print(f'[*] Finish')


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-c', '--columns', default=None, help='Head of columns (delimeter: ,)')
@click.option('-f', '--filename', default=None, help='Input filename')
@click.option('-o', '--output', default='output.csv', help='Input filename')
def main(columns: str, filename: str, output: str):
    """Remove columns"""
    if columns is None or filename is None:
        print(click.get_current_context().get_help())
        sys.exit(-1)

    process(columns, filename.strip(), output)
    

if __name__ == '__main__':
    main()
    sys.exit(0)