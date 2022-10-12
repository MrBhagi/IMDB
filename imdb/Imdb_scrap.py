#import neccessary library
from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv

#Open And Read Title.csv File
with open("input/TitleInput.csv") as file:
    csvreader = csv.DictReader(file)
    movie_title =[row["movie_title_name"].upper() for row in csvreader]

#Take User Input    
Enter_Movie_Title  = input("enter movies name: ")

#Check for User Enter Movie Exist Or Not  
if Enter_Movie_Title.upper() not in movie_title:
    movie_title.append(Enter_Movie_Title.upper())
    input_file=[Enter_Movie_Title.lower()]

    inputf= pd.DataFrame({"movie_title":input_file})
    input_save=f"input/{Enter_Movie_Title}.csv"
    inputf.to_csv(input_save,index=False)


file_path = f"input/{Enter_Movie_Title}.csv"
try:
    with open(file_path)as file:
        csvreader = csv.DictReader(file)
        url_list = [f"https://www.imdb.com/search/title/?title={row['movie_title']}" for row in csvreader]


    #create list we want to write into
    titles=[]
    genres =[]
    release_years=[]
    imdb_ratings =[]
    votes =[]
    descriptions=[]

    for url in url_list:
        try:
            # Getting content from the Url
            response = requests.get(url)
            soup = BeautifulSoup(response.content,"html.parser")

            # The pPrt Of The Html We Want To get the information from
            movies_div = soup.find_all('div',class_='lister-item mode-advanced')

            for movie in movies_div:
                #Scrap The Movie Title Name
                if movie.find('div',class_="lister-item-content"):
                    title = movie.h3.a.text
                    titles.append(title)

                #Scrap The Genres 
                    if movie.p.find('span',class_="genre")is not None:
                        genre = movie.p.find('span', class_ = 'genre').text.replace("\n", "").rstrip().split(',')
                        genres.append(genre)
                    else:
                        genres.append(None)

                #Scrap The Release Year
                    if movie.h3.find('span', class_= 'lister-item-year text-muted unbold')is not None:
                        year = movie.h3.find('span', class_= 'lister-item-year text-muted unbold').text
                        release_years.append(year[1:5])
                    else:
                        release_years.append(None)

                #scrap The Ratings
                    if movie.find('div',class_="inline-block ratings-imdb-rating")is not None:
                        rating = float(movie.strong.text)
                        imdb_ratings.append(rating)
                    else:
                        imdb_ratings.append(None)

                #Scrap The Votes



                #Scrap the Descriptions
                description = movie.select('.lister-item-content p:nth-of-type(2)')
                for desc in description:
                    desc=desc.get_text().replace('\n',"")
                    desc=desc.strip(" ")
                    descriptions.append(desc)
        except:
            print("Erorr while Scraping the Info Fix It ")


    #Createing The Data Set
    Movie_Data =pd.DataFrame({
        "Titles":titles,
        "Genre":genres,
        "Release years":release_years,
        'Imdb Ratings':imdb_ratings,
        #'Votes':votes,
        'Descriptions':descriptions
    })

    #Save Data 
    save_file =f"output/scraped_{Enter_Movie_Title}.csv"
    Movie_Data.to_csv(save_file,index=False)
    print("Your Data Has Been Scraped go to Output Folder")

except:
    print("Error:Enter Valid Movie Title Name OR File Does Not Exits OR Erorr while parsing")

finally:
    file.close()
