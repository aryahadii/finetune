# Finetune

A tool to better organize your Spotify library.

## Available Commands

### Streaming History

This command helps you to see your library tracks with their corresponding played count.
Since streaming history is not provided in the official Spotify Web API, you should request your data in [Spotify Privacy Panel](https://www.spotify.com/account/privacy/). Then extract the downloaded file to use in following commands:

``` bash
# to printout the history (may exceed your terminal max buffer size)
$ python finetune.py streaming-history --spotify-data-dir /path/to/my_spotify_data/
# OR
# to write the result in a human-readable TSV file
$ python finetune.py streaming-history --spotify-data-dir /path/to/my_spotify_data/ -o /path/to/streaming_history.tsv
```

### Library Purge

This command helps you to bulk remove tracks from your Spotify Liked Songs.

**Note:** Since this command uses Spotify Web API, you should create a Spotify App and provide the client auth info as describe [here](#creating-spotify-app).

To remove a list of tracks from your Liked Songs you should:

1. Use `streaming-history` to gather a list of your liked tracks and write the result into a TSV file.
2. **Remove** any line that represents a track that you **want to stay in your Liked Songs.**
3. Run library purge command to remove any URI presents in the purge list.

``` bash
$ python finetune.py library purge /path/to/purge_list.tsv
```

An example of purge list file:

``` tsv
URI NAME    ARTIST  PLAYCOUNT
spotify:track:00vHNMkYPuN1PRD1vmSNWq	Camel	Ice	15
spotify:track:3DQnKDqPNRPhK02UQf9ETf	Camel	Stationary Traveller	20
```

or, just URIs:

``` tsv
spotify:track:00vHNMkYPuN1PRD1vmSNWq
spotify:track:3DQnKDqPNRPhK02UQf9ETf
```

## Creating Spotify App

To make Spotify API call, you should have a Spotify app credential. To create a new app use [Spotify's Guide](https://developer.spotify.com/documentation/web-api/concepts/apps). Then put the _client_id_, _client_secret_ and _redirect_uri_ in a file named `client_auth.yaml` beside `finetune.py`.

Template of `client_auth.yaml`:

``` yaml
client_id: <ID>
client_secret: <SECRET>
redirect_uri: <URI>
```
