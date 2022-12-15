#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import json


# In[2]:


def get_imdb():
    try:
        with open('imdb_cache.html', 'rb') as f:
            read = f.read()
    except:
        url = 'http://www.imdb.com/chart/top'
        response = requests.get(url)
        read = response.text
        with open('imdb_cache.html', 'wb') as f:
            f.write(response.content)
    soup = BeautifulSoup(read, "html.parser")
    return soup


# In[3]:


soup = get_imdb()
movies = soup.select('td.titleColumn')
#IMDB_number = [i.attrs.get('href')[7:16] for i in soup.select('td.titleColumn a')]
IMDB_number = [i.attrs.get('href').split('/')[2] for i in soup.select('td.titleColumn a')]
crew = [i.attrs.get('title') for i in soup.select('td.titleColumn a')]
ratings = [i.attrs.get('data-value')
        for i in soup.select('td.posterColumn span[name=ir]')]


# In[4]:


list = []
for i in range(len(movies)):
    movie_string = movies[i].get_text()
    movie = str().join(movie_string.split()[1:])
    movie_title = movie[:-6]
    year = int(movie[-5:-1])
    place = int(movie_string.split()[0][:-1])
    data = {"place": place,
            "IMDB_number": IMDB_number[i], 
            "title": movie_title,
            "rating": round(float(ratings[i]), 1),
            "year": year,
            "director": re.search('^[^(]+', crew[i]).group()[:-1],
            "stars": ', '.join([item[1:] for item in crew[i].split(',')[1:]]),
            }
    list.append(data)


# In[5]:


df = pd.DataFrame(list)
#df.to_csv('imdb_top_250_movies.csv',index=False)


# In[6]:


def get_omdb():
    try:
        with open("omdb_cache.json", 'r') as f:
            cache_contents = f.read()
            cache_dict = json.loads(cache_contents)
    except:
        cache_dict = {}
        for i in range(len(df)):###
            number = df.iloc[i]['IMDB_number']
            response = requests.get("http://www.omdbapi.com/?i=" + number + "&apikey=2a48f97e")
            json_str = response.text
            json_dict = json.loads(json_str)
            cache_dict[number] = json_dict
        with open("omdb_cache.json", 'w') as f:
            dumped_json_cache = json.dumps(cache_dict)
            f.write(dumped_json_cache)
    return cache_dict


# In[7]:


omdb_dict = get_omdb()


# In[8]:


lst_omdb = []
for movie in omdb_dict.values():
    IMDB_number = movie['imdbID']
    rated = movie['Rated'] #R, PG-13, Approved
    if movie['Runtime'] == 'N/A':
        runtime = None
    else:
        runtime = int(re.search('\d+', movie['Runtime']).group())
    genre = movie['Genre']
    language = movie['Language']
    country = movie['Country']
    nominated_oscar = ((re.search('Nominated for \d+ Oscars', movie['Awards']) != None) or (re.search('Won \d+ Oscars', movie['Awards']) != None))
    won_oscar = (re.search('Won \d+ Oscars', movie['Awards']) != None)
    plot = movie['Plot']
    if movie['imdbVotes'] == 'N/A':
        IMDB_votes = None
    else:
        IMDB_votes = int(str().join(movie['imdbVotes'].split(',')))
    
    try:
        box_office = int(str().join(movie['BoxOffice'][1:].split(',')))
    except:
        box_office = None
    #if movie['BoxOffice'] == 'N/A':
    #    box_office = None
    #else:
    #    box_office = int(str().join(movie['BoxOffice'][1:].split(',')))
    data = {"IMDB_number": IMDB_number,
            "rated": rated, 
            "runtime": runtime,
            "genre": genre,
            "language": language,
            "country": country,
            "nominated_oscar": nominated_oscar,
            "won_oscar": won_oscar,
            "IMDB_votes": IMDB_votes,
            "box_office":box_office,
            "plot": plot,
            }
    lst_omdb.append(data)


# In[9]:


df_omdb = pd.DataFrame(lst_omdb)


# In[10]:


merge = df.merge(df_omdb, on = 'IMDB_number')


# In[11]:


merge.to_csv('collected_data.csv')

