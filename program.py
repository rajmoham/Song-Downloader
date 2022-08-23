from email import header
import shutil
import requests
from googleapiclient.discovery import build
from pytube import YouTube
import os
import base64

def INITIALIZE_VARIABLES():
    #Spotify
    global client_id
    client_id = os.environ.get("CLIENT_ID")

    global client_secret 
    client_secret = os.environ.get("CLIENT_SECRET")

    global base_64
    base_64 = Base64Encode(client_id, client_secret)

    #Youtube
    global api_key
    api_key  = os.environ.get("API_KEY_YT")
    global service_yt
    service_yt = build("youtube", "v3", developerKey=api_key)

def Base64Encode(CLIENT_ID, CLIENT_SECRET):
    key = CLIENT_ID + ":" + CLIENT_SECRET
    key_encoded_byte = base64.b64encode(key.encode("ascii"))
    key_encoded = key_encoded_byte.decode("ascii")
    return key_encoded

def Authorization():
    print("Connecting to Spotify...")
    auth_query = "https://accounts.spotify.com/api/token"
    try:
        auth_res = requests.post(auth_query, data={"grant_type":"client_credentials"}, headers={"Authorization":"Basic " + base_64})
        access_token = auth_res.json()["access_token"]
        print("Successfully Connected to Spotify")
        return access_token
    except:
        print("Error Connecting to Spotify, Please Try Again Later")
        print("----------The End----------")
        quit()

def Get_Playlist_Songs(access_token):
    #playlist_link = "https://open.spotify.com/playlist/63qp5ewWfM4aGrXWQ8rlrC?si=ab856c6055eb457a"
    #playlist_link = "https://open.spotify.com/playlist/1CFs9S4xEqd1zBY75rWNTN?si=19fd75c994174fb4"
    playlist_link = "https://open.spotify.com/playlist/0yXlKEvlgpWJ5eNRth61El?si=a24bd19e75884bdf"
    #playlist_link = input()

    playlist_id = playlist_link[34:56]
     
    print("Getting Data from Playlist...")

    offset = 0
    songs = {"name":"", "num_of_songs":0, "song":[], "artists":[]}
    try:
        while True:
            playlist_query = "https://api.spotify.com/v1/playlists/{}?fields=name".format(playlist_id)
            playlist_items_query = "https://api.spotify.com/v1/playlists/{}/tracks?limit=100&offset={}".format(playlist_id, offset * 100)

            playlist_res = requests.get(playlist_query, headers={"Authorization":"Bearer " + access_token})
            playlist_items_res = requests.get(playlist_items_query, headers={"Authorization":"Bearer "+ access_token})

            playlist_name = playlist_res.json()["name"]

            res_json = playlist_items_res.json()
            num_of_songs = len(playlist_items_res.json()["items"])          

            songs["name"] = playlist_name
            songs["num_of_songs"] = num_of_songs           
            for i in range(num_of_songs):
                x = 0
                artists = []
                while True:
                    try:
                        artists.append(res_json["items"][i]["track"]["artists"][x]["name"])
                        x += 1
                    except:
                        break
                songs["artists"].append(artists)
                songs["song"].append(playlist_items_res.json()["items"][i]["track"]["name"])
            if num_of_songs < 100:
                break
            else:
                offset += 1
    except:
        print("Error Connecting to Playlist")
        print("----------The End----------")
        quit()

    print("Playlist Data Successfully Obtained")
    return songs

def Display_Playlist(playlist):
    for i in range(playlist["num_of_songs"]):
        print("{:>4}.".format(i+1), playlist["song"][i], "-", playlist["artists"][i])

def Youtube(playlist_data):
    playlist_name = playlist_data["name"]
    path = os.path.expanduser("~\\Music\\" + playlist_name)    

    print("Creating Playlist Folder for '" + playlist_name + "'")

    if (os.path.isdir(path)):
        shutil.rmtree(path)
        """ print("Playlist already exists")
        print("----------The End----------")
        quit()  """
    else:
        os.mkdir(path)
    
    num_of_songs = playlist_data["num_of_songs"]
    
    for i in range(num_of_songs):
        song_name = playlist_data["song"][i]
        song_artists = playlist_data["artists"][i]
        yt_req = service_yt.search().list(part="snippet", q="{} {} audio".format(song_name, song_artists[0]), type="video", maxResults=1)
        res = yt_req.execute()
        vid_id = res["items"][0]["id"]["videoId"]
        yt = YouTube("http://youtube.com/watch?v=" + vid_id)
        video = yt.streams.filter(only_audio=True).first()
        try: 
            dl_file = video.download(output_path=path)
            print(dl_file)
            os.rename(dl_file, path + "\\" + song_name + ".mp3")
            print("Downloaded " + song_name)
        except:
            print("Could not download " + song_name)
            os.remove(dl_file)
        print("")
        
def main():
    INITIALIZE_VARIABLES()

    ACCESS_TOKEN = Authorization()
    Playlist_Data = Get_Playlist_Songs(ACCESS_TOKEN)
    Display_Playlist(Playlist_Data)
    #Youtube(Playlist_Data)

if __name__ == "__main__":
    main()
    print("----------The End----------")