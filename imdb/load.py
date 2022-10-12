import pathlib
import pandas as pd

class Load:
    def __init__(self, output_filename: pathlib.Path, df: pd.DataFrame) -> None:
        self.output_filename = output_filename
        self.df = df
    
    def execute(self):
        self.df.to_csv(self.output_filename, index=False)