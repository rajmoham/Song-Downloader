from warnings import catch_warnings
import requests

#   *****Variables*****
client_id = "92e262d26a134321a4ba20f10446f825"
client_secret = "d08596b249fe4be98620297cb0e2e151"
base_64 = "OTJlMjYyZDI2YTEzNDMyMWE0YmEyMGYxMDQ0NmY4MjU6ZDA4NTk2YjI0OWZlNGJlOTg2MjAyOTdjYjBlMmUxNTE="
redirect_uri = "http://rajmoham.github.io"

def Authorization():
    print("Getting Access Token...")
    auth_query = "https://accounts.spotify.com/api/token"
    try:
        auth_res = requests.post(auth_query, data={"grant_type":"client_credentials"}, headers={"Authorization":"Basic " + base_64})
        access_token = auth_res.json()["access_token"]
        print("Successful")
        return access_token
    except:
        print("Error getting Access Token")
        print("----------The End----------")
        quit()

def Get_Playlist_Songs(access_token):
    #print("Input link to playlist:")
    playlist_link = "https://open.spotify.com/playlist/0h4uf5XmsH5a0Xacxrc4oF?si=78ba77f87d844107"
    #playlist_link = input()

    playlist_id = playlist_link[34:56]
     
    print("Getting Information from playlist...")
    offset = 0
    songs = {"song":[], "artists":[]}
    try:
        while True:
            playlist_query = "https://api.spotify.com/v1/playlists/{}/tracks?limit=100&offset={}".format(playlist_id, offset * 100)
            playlist_res = requests.get(playlist_query, headers={"Authorization":"Bearer "+ access_token})
            res_json = playlist_res.json()
            num_of_songs = len(playlist_res.json()["items"])
            for i in range(num_of_songs):
                x = 0
                artists = ""
                while True:
                    try:
                        artists += res_json["items"][i]["track"]["artists"][x]["name"] + ", "
                        x += 1
                    except:
                        break
                songs["artists"].append(artists[:-2])
                songs["song"].append(playlist_res.json()["items"][i]["track"]["name"])
            if num_of_songs < 100:
                break
            else:
                offset += 1
    except:
        print("Error Getting Playlist Songs")

    print("Playlist Data Successfully Retrieved")
    return songs

def Display_Playlist(playlist):
    for i in range(len(playlist["song"])):
        print("{:>4}.".format(i+1), playlist["song"][i], "-", playlist["artists"][i])

def main():
    ACCESS_TOKEN = Authorization()
    Playlist = Get_Playlist_Songs(ACCESS_TOKEN)
    Display_Playlist(Playlist)

if __name__ == "__main__":
    main()
    print("----------The End----------")