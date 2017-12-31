import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

# Replace client id, clien secret, and username with your info.
client_id = ''
client_secret = ''
username = ''
scope = 'user-library-read'
redirect_uri = 'http://localhost/'

client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)

token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
print('retrieved token: ' ,token)

savefile = open('currentlySavedTracks.txt', 'w')

if token:
    sp = spotipy.Spotify(token)
    offsetCount = 0
    results = sp.current_user_saved_tracks(limit=50,offset=offsetCount)

    totalTracks = results['total']

    while offsetCount <= totalTracks:
        for item in results['items']:
            track = item['track']
            trackNameArtist = track['name'] + ' - ' + track['artists'][0]['name']
            trackURI = track['uri'][14:] # 14 skips the 'spotify:track:'
            fullPrint = trackNameArtist + ', ' + trackURI

            savefile.write(fullPrint.encode('utf8') + '\n')
            print(fullPrint)

        offsetCount += 50
        results = sp.current_user_saved_tracks(limit=50,offset=offsetCount)
else:
    print 'no bueno on the token, guy'

print('total tracks saved: ' + str(totalTracks))

newList = open('currentlySavedTracks.txt', 'rb')
try:
    oldList = open('prevTrackList.txt', 'rb')
except IOError:
    oldList = open('prevTrackList.txt', 'w')
    oldList.close()
    oldList = open('prevTracklist.txt', 'rb')
    print('new prev track list created')

try:
    lostList = open('lostTracks.txt', 'rb')
except IOError:
    lostList = open('lostTracks.txt', 'w')
    lostList.close()
    lostList = open('lostTracks.txt', 'rb')
    print('new lost track list created')

currentTracks = set(newList.read().decode('utf-8').splitlines())
oldTracks = set(oldList.read().decode('utf-8').splitlines())
lostTracks = set(lostList.read().decode('utf-8').splitlines())

recoveredTracks = lostTracks & currentTracks
newLostTracks = (oldTracks - currentTracks) | lostTracks - recoveredTracks

oldList.close()
lostList.close()
newList = open('prevTracklist.txt', 'w')
newLostList = open('lostTracks.txt', 'w')

if len(newLostTracks) > 0:
    for track in sorted(list(newLostTracks)):
        newLostList.write(track.encode('utf8') + '\n')

if len(currentTracks) > 0:
    for track in sorted(list(currentTracks)):
        newList.write(track.encode('utf8') + '\n')

print('The total number of lost tracks is ' + str(len(newLostTracks)))
print('The total number of currently saved tracks is ' + str(len(currentTracks)))
