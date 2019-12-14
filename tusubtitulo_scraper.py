# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time

index_url = "https://www.tusubtitulo.com/series.php"
base_url = "https://www.tusubtitulo.com" 
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_info(element_to_clean,index=0):
    return(int(re.sub('[A-Z]|[a-z]|\s|í', '', cleanhtml(str(element_to_clean)).split(",")[index])))

def get_shows():
    #index_url = "https://www.tusubtitulo.com/series.php"
    #base_url = "https://www.tusubtitulo.com" 

    soup = BeautifulSoup(requests.get(index_url ).text, 'html.parser')
    
    tbl_list = list(soup.findAll('td'))
    
    links_list = [ i.findAll('a') for i in tbl_list if re.search('<td class="line0">',str(i))]
    show_name = [re.sub("\[|\]","",cleanhtml(str(i))) for i in links_list]
    show_link = [str(i).split('\"')[1] for i in links_list]
    
    info_list = [ i for i in tbl_list if re.search('<td class="newsDate">',str(i))]
    Temporadas_list = [ get_info(i,0) for i in info_list]
    capitulos_list  = [ get_info(i,1) for i in info_list]


    index_data = pd.DataFrame({"show_name" : show_name,
                               "show_link" : show_link ,
                               "Temporadas_list" : Temporadas_list,
                               "capitulos_list"  : capitulos_list,
                               "Procesed" : False})
    return(index_data)

shows = get_shows()

show_url = shows.iloc[12].show_link
def get_capitulos_list(show_url):
    req = requests.get(base_url + show_url)
    BeautifulSoup(req.text, 'html.parser')
    req.text
    soup = BeautifulSoup(requests.get(base_url + show_url).text, 'html.parser')
    
i=1

def get_subtitle_list(i):
    
    episode_url = base_url+"/episodes/"+str(i)
    soup = BeautifulSoup(requests.get(episode_url).text, 'html.parser')
    soup_links = soup.findAll('a')
    
    get_titles = soup.findAll("span",{"class":"left titulo grid_4"})
    if len(get_titles) == 0 :
        return(None)
    
    get_titles = get_titles[0].getText()
    show_name,season_name,chapter_number = [i.replace("\n","").strip() for i in get_titles.split(",")]
      
    sub_info = [i.replace("\n","").strip() for i in soup.findAll("h1",{"id":"cabecera-subtitulo"})[0].getText().split("-")]
    
    chapter_name = ''.join(sub_info[1:])
    chapter_code = sub_info[0].split(" ")[-1]
    
    list_of_subs = list(soup.findAll("ul",{"class":"sslist"}))
    
    list_of_links = [i.findAll("a") for i in list_of_subs ]
    list_of_links = sum(list_of_links, [])
    list_of_links = [i for i in list_of_links if re.search("Descargar",str(i))]
    list_of_links = [ a['href'] for a in list_of_links]
      
    show_soup   = [i for i in soup_links if re.search('show',str(i))]
    show_id     = [a['href']   for a in show_soup]
    
    season_soup = [i for i in soup_links if re.search('season',str(i))]
    season_id   = [a['href']   for a in season_soup]
    
    
    [i.findAll("li",{"class":"rng download green"}) for i in list_of_subs]
    lenguage_list_availability = [str(i).find("li-estado green")>0  for i in list_of_subs]
    
    lenguage_list = [' '.join([j.getText() for j in i.findAll("b")]) for i in list_of_subs ]
    lenguage_list = [x for x, y in zip(lenguage_list, lenguage_list_availability) if y]
    
    data = pd.DataFrame({"link_id" : i,
                         "show_id" : show_id[0],
                         "show_name" : show_name ,
                         "season_id" : season_id[0],
                         "season_name" : season_name,
                         "chapter_name" : chapter_name,
                         "chapter_code" : chapter_code,
                         "lenguage" : lenguage_list,
                         "links" : list_of_links,
                         "Procesed" : False})
    
    return(data)


subtitle_data_list = get_subtitle_list(1)
data_list = []
data_list.append(get_subtitle_list(1))
actual_len = 0
new_len = 1

while actual_len < new_len:
    start = time.time()
    actual_len = len(data_list)
    max_index = data_list[-1]['link_id'].max() + 1
    print(str(max_index) + ";" + str(actual_len) )
    for i in range(max_index,max_index + 20):
        data_frame = get_subtitle_list(i)
        if data_frame is not None:
            data_list.append(data_frame)
    new_len = len(data_list)
    stop = time.time()
    duration = stop-start
    print(duration)


    #do some stuff
pd.concat(data_list)

69008/10

i = 45
get_subtitle_list(i)



