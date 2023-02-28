from dotenv import load_dotenv
import os
import base64
import requests
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Contept-Type": "application/x-www-form-unlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data, timeout = 100)
    json_result = json.loads(result.content)
    return json_result["access_token"]


def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    
    if len(json_result) == 0:
       print("No artist with this name exists...")
       return None
    return json_result[0]

def search_fo_countries(token, song_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={song_name}&type=track&limit=1"

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"][0]["album"]["available_markets"]

    with open("spotify_countries.json", "w") as file:
        file.write(json.dumps(json_result, indent=4))
    
    return json_result

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = requests.get(url, headers= headers)
    json_result = json.loads(result.content)['tracks'][0]['album']['name']

    with open("spotify_result.json", "w") as file:
        file.write(json.dumps(json_result, indent=4))

    return json_result

def spotify_json(token, artist_name):
    url = "https://api.spotify.com/v1/search/"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query

    result = requests.get(query_url, headers = headers)
    json_result = json.loads(result.content)#["tracks"]["items"]

    with open("spotify_result.json", "w") as file:
        file.write(json.dumps(json_result, indent=4))

    select_set = set()
    for dict_element in json_result:
        for item in dict_element:
            select_set.add(item)

    print("Your selection set is :")
    print("id, name, best_track, country")
    print("Choose what you want to see :")

    choice = input()

    while choice:

        if choice == 'id':
            print(f"artist id = {json_result['artists']['items'][0]['id']}")

        if choice == 'name':
            print(f"artist id = {json_result['artists']['items'][0]['name']}")

        if choice == 'best_track':
            song = get_songs_by_artist(token, json_result['artists']['items'][0]['id'])
            print(song)
        if choice == 'country':
            best_track = get_songs_by_artist(token, json_result['artists']['items'][0]['id'])
            countries = search_fo_countries(token, best_track)
            print(countries)





        # result_element = json_result[0]
        # if choice in ['id', 'name']:
        #     with open("spotify_result.json", "w") as file:
        #         file.write(json.dumps(result_element["album"]["artists"][0][choice], indent=4))
        # elif choice == "country":
        #     with open("spotify_result.json", "w") as file:
        #         file.write(json.dumps(result_element["album"]["available_markets"], indent=4))
        # elif choice == "best_track":
        #     get_songs_by_artist(token, artist_id)

        # print("Check your spotify_result.json")
        print("Your selection set is :")
        print("id, name, best_track, country")
        print("Choose what you want to see :")

        choice = input()

token = get_token()
result = search_for_artist(token, "ACDC")
artist_id = result["id"]
# get_songs_by_artist(token, artist_id)

# for idx, song in enumerate(songs):
#     print(f"{idx + 1}. {song['name']}")

artist = input("artist -> ")
spotify_json(token, artist)
