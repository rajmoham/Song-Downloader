## **Song-Downloader**
A project used to learn how functionality of APIs by incorporting my interest for listening to music. </br>

### **Spotify API**
- :green_square: Pass `Client ID` and `Client Secret` to get `Access Token`. </br>
- :green_square: Use `Access Token` to obtain playlist information. </br>
- :orange_square: **Playlist Information passed on :** </br>
&emsp;&emsp; :ballot_box_with_check: Playlist name </br>
&emsp;&emsp; :ballot_box_with_check: Songs in playlist </br>
&emsp;&emsp; :ballot_box_with_check: Artist(s) for each song </br>
&emsp;&emsp; :black_large_square: Album name </br>
&emsp;&emsp; :black_large_square: Album cover </br>

### **YouTube API**
- :green_square: Pass `API Key` to get access to YouTube services
- :green_square: Search for each song using song name and artist(s) and get the first result

### **Downloading the song**
- :green_square: Create directory in Music folder with playlist name
- :orange_square: **For each song :** </br>
&emsp;&emsp; :ballot_box_with_check: Change file name (title of YouTube video) to song name </br>
&emsp;&emsp; :black_large_square: Add metadata (artists, album name, album cover) </br>

### **Bugs/Errors**
- Songs with illegal characters download but returns an error when attempting to rename
- Some playlists will return less songs than whats in the playlist
