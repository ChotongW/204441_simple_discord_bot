from jikanpy import Jikan

def upcoming():
    jikan = Jikan()
    anime_info_list = []
    upcoming = jikan.seasons(extension='upcoming')
    for i in upcoming["data"]:
        anime_info = {
            "Title": i['title'],
            "images": i['images']['jpg']['image_url']
        }
        anime_info_list.append(anime_info)
    return anime_info_list

