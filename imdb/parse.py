from typing import List
from bs4 import BeautifulSoup
import pandas as pd

class Parse:
    def __init__(self, html_pages: List[str]) -> None:
        self.html_pages = html_pages
        
    def execute(self) -> pd.DataFrame:
        data = []
        for page in self.html_pages:
            soup = BeautifulSoup(page,"html.parser")
            movies_div = soup.find_all('div',class_='lister-item mode-advanced')

            for movie in movies_div:
                title, genre, year, rating, description = [None] * 5

                if movie.find('div',class_="lister-item-content"):
                    title = movie.h3.a.text

                    genre = movie.p.find('span', class_ = 'genre')
                    if genre:
                        genre = [g.strip().lower() for g in genre.text.strip().split(",")]
                    else:
                        genre = []

                    
                    year = movie.h3.find('span', class_= 'lister-item-year text-muted unbold')
                    if year:    
                        year = year.text[1:5].strip()
                    
                    rating = movie.find('div',class_="inline-block ratings-imdb-rating")
                    if rating:
                        rating = rating.text.strip()
                    
                    description = movie.find_all('p',class_='text-muted')[-1].text.strip()
                    vote = movie.find('span',attrs = {'name':'nv'})
                    if vote:
                        vote = vote.attrs.get("data-value")
                        
                    data.append(
                        {
                            'title':title,
                            'genre':genre,
                            'year':year,
                            'rating':rating,
                            'description':description,
                            'votes':vote
                        }
                    )

        return pd.DataFrame(data=data)

                

                    
                    