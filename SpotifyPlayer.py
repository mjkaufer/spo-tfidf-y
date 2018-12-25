import spotipy
import spotipy.util as util
from collections import OrderedDict
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from time import time
from scipy.signal import square

class SpotifyPlayer:
    def __init__(self, username="mjkaufer"):
        self.sp = None
        self.username = username
        self.lastIndex = {}

    def authenticate(self):
        scope = 'app-remote-control, user-modify-playback-state, streaming, user-read-playback-state, user-read-currently-playing, user-read-private'

        token = util.prompt_for_user_token(self.username, scope)

        if token:
            self.sp = spotipy.Spotify(auth=token)
            print("Successfully authenticated")
        else:
            print("Can't get token for", self.username)

    def getSP(self):
        return self.sp

    def getArtistDiscography(self, artistId="5K4W6rqBFWDnAN6FQUkS6x"):

        artistAlbums = self.sp._get("artists/{}/albums?include_groups=album,single".format(artistId))['items']
        albumTrackDict = {album['id']:None for album in artistAlbums}
        
        for albumId in albumTrackDict.keys():
            albumTracks = self.sp._get("albums/{}/tracks?limit=50".format(albumId))['items']
            albumTrackDict[albumId] = {albumTrack['id'] for albumTrack in albumTracks}

        return albumTrackDict
        # self.sp._put("me/player/shuffle?state=false")
        # self.sp._put("me/player/play", payload={"uris": uriList})

    def playlistQuery(self, queryString, desiredTracks, existingPlaylist={}, queryNum=50):
        if queryString not in self.lastIndex:
            self.lastIndex[queryString] = 0
        playlistQueryResult = self.sp.search(queryString, limit=queryNum, offset=self.lastIndex[queryString], type='playlist')['playlists']['items']

        self.lastIndex[queryString] += queryNum

        results = {playlist['id']:None for playlist in playlistQueryResult}

        for playlistId in results.keys():
            if playlistId in existingPlaylist:
                continue

            playlistTracks = self.sp._get('playlists/{}/tracks?fields=items.track.id'.format(playlistId))['items']
            numTracks = len(playlistTracks)

            relevantTracks = []
            for track in playlistTracks:
                # spotify sometimes has stuff like {track: None}
                if ('track' in track
                    and track['track'] is not None
                    and 'id' in track['track']
                    and track['track']['id'] in desiredTracks):

                    relevantTracks.append(track['track']['id'])

            # only care about playlists that have more than 1 relevant song
            if len(relevantTracks) > 1:
                results[playlistId] = {"tracks": relevantTracks, "total": numTracks}

        return {**{k: v for k, v in results.items() if v is not None}, **existingPlaylist}


# if __name__ == '__main__':
#     player = SpotifyPlayer()
#     player.authenticate()
#     print(player.getArtistDiscography())
# #     tracks = set("""4S8d14HvHb70ImctNgVzQQ
# # 78TTtXnFQPzwqlbtbwqN0y
# # 1PS1QMdUqOal0ai3Gt7sDQ
# # 2gZUPNdnz5Y45eiGxpHGSc
# # 3U21A07gAloCc4P7J8rxcn
# # 6C7RJEIUDqKkJRZVWdkfkH
# # 4EWCNWgDS8707fNSZ1oaA5
# # 722tgOgdIbNe3BEyLnejw4
# # 19a3JfW8BQwqHWUMbcqSx8
# # 2KpCpk6HjXXLb7nnXoXA5O""".split("\n"))
# #     runningPlaylistResults = {}
# #     for i in range(3):
# #         for genre in ["rap", "hip hop"]:
# #             runningPlaylistResults = player.playlistQuery(genre, tracks, runningPlaylistResults)

# #     print(runningPlaylistResults)
