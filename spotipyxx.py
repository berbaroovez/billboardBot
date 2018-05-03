import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import billboard
import tweepy as tp
username=''
#get username from terminal
#edit


def sendTweet(playlistID,apiIn):
    
    apiIn.update_status("https://open.spotify.com/user/12101891873/playlist/"+playlistID," Hello World")

def TrackList(spotifyObject):
    cleanAry =[]
    chart= billboard.ChartData('hot-100')
    for song in chart:
        if "Featuring" in song.artist:
            artistString = song.artist
            cleanStr=artistString.replace("Featuring","feat")
            if "Swae" in cleanStr:
                print("---------------------------")
                cleanStr=cleanStr.replace("Swae Lee Or","")
                
            cleanAry.append((song.title,cleanStr))
        elif "&" in song.artist:
            artistString = song.artist
            cleanStr=artistString.replace("&","")
            cleanAry.append((song.title,cleanStr))
        elif "Swae" in song.artist:
            cleanStr=song.artist.replace("Swae Lee Or","")
            cleanAry.append((song.title,cleanStr))
        else:
            cleanAry.append((song.title,song.artist))
    

    trackAry=[]
    song =""
    for i in range(len(cleanAry)):
        song = cleanAry[i][0]+" "+cleanAry[i][1]
        print(song)
        searchResults = spotifyObject.search(song,1,0,"track")
        
        trackID=searchResults['tracks']['items'][0]['id']
        
        trackAry.append(trackID)
    #trackID =['2XW4DbS6NddZxRPm5rMCeY']
    return trackAry
#Creates a Playlist and saves the ID for future use
#searchQuery = input("Enter in an playlist name: ")
#playCreate = spotifyObject.user_playlist_create(username,searchQuery,public="True")
#playlistID = playCreate['id']
#print(playlistID)

#print(json.dumps(searchResults, sort_keys=True, indent=4))

def main():
    print("g")
#----------Tweeter keys
    consumer_key=''
    consumer_secret=''
    access_token=''
    access_secret=''
    auth = tp.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_secret)
    api = tp.API(auth)

    scope = "playlist-modify-public"
    try:
        token = util.prompt_for_user_token(username,scope,client_id='d476b87da04741b696ce0f0555714000',client_secret='471ec40ad7bc462884e556ce567e79ba',redirect_uri='https://www.google.com/')
    except:
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username,scope,client_id='d476b87da04741b696ce0f0555714000',client_secret='471ec40ad7bc462884e556ce567e79ba',redirect_uri='https://www.google.com/')

    sp = spotipy.Spotify(auth=token)


    #user =spotifyObject.current_user()

    playlistID = '2y5KLgJY1nCmJwlL4qGpks'
    #Gets track ID

    trackAry = TrackList(sp)
    sp.user_playlist_add_tracks(username,playlistID,trackAry,position=None)
    sendTweet(playlistID,api)

if __name__ == "__main__":
    main()
