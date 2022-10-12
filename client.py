import sys
import pathlib
from imdb import Extract, Parse, Load


if __name__ == '__main__':
    input_file, output_file = sys.argv[1:]
    pages = Extract(input_file=pathlib.Path(f"input/{input_file}.csv")).execute()
    df =  Parse(html_pages=pages).execute()
    Load(output_filename=pathlib.Path(f"output/{output_file}.parquet"), df=df).execute()
