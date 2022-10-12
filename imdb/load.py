from doctest import FAIL_FAST
import pathlib
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


class Load:
    def __init__(self, output_filename: pathlib.Path, df: pd.DataFrame) -> None:
        self.output_filename = output_filename
        self.df = df
    
    def execute(self):
        my_schema = pa.schema([
                ('title',pa.string()),
                ('genre',pa.list_(pa.string())),
                ('year',pa.int32()),
                ('rating',pa.float32()),
                ("description",pa.string()),
                ('votes',pa.int32())])
                
        table = pa.Table.from_pandas(self.df,my_schema)
        pq.write_table(table,self.output_filename)

        