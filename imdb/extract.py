from typing import List
import requests
import pathlib
import pandas as pd
import time

class Extract:
    def __init__(self, input_file: pathlib.Path) -> None:
        self.input_file = input_file
    
    def _titles(self) -> List[str]:
        df = pd.read_csv(self.input_file)
        return df.title.tolist()
    
    @staticmethod
    def get_page(title) -> str:
        resposnse = requests.get(f"https://www.imdb.com/search/title/?title={title}", headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"})
        return resposnse.text

    def execute(self) -> List[str]:
        html_page = []
        titles = self._titles()
        for title in titles:
            html_page.append(self.get_page(title))
            time.sleep(0.3)
        return html_page