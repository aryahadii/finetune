import argparse
import csv
import re

from spotify_provider import SpotifyData, SpotifyAPI


def streaming_history(spotify_data_export_dir, output_tsv_path=None):
    sd = SpotifyData(spotify_data_export_dir=spotify_data_export_dir)
    played = sd.played_songs_in_library()

    output = []
    for track, play_count in played:
        output.append((track.uri, track.artist, track.name, play_count))

    if output_tsv_path:
        with open(output_tsv_path, 'w') as file:
            w = csv.writer(file, delimiter='\t')
            w.writerow(["URI", "ARTIST", "NAME", "PLAY_COUNT"])
            w.writerows(output)
    else:
        print(output)


def library_purge(input_tsv_path):
    tracks_uri = []

    with open(input_tsv_path, 'r') as purge_file:
        r = csv.reader(purge_file, delimiter='\t')
        next(r)  # skip the headers

        for track in r:
            if re.match(r'spotify:track:\w{22}', track[0]):
                tracks_uri.append(track[0])

    prompt = input(f"Are you sure to delete {len(tracks_uri)} tracks from your Spotify library? [y/n] ")
    if prompt != 'y':
        exit(0)

    SpotifyAPI().remove_user_saved_tracks(tracks_uri)


def main():
    global_parser = argparse.ArgumentParser(prog='finetune',
                                            description="Finetune, a Spotify library organizer.")
    subparsers = global_parser.add_subparsers(dest="command")

    streaming_history_parser = subparsers.add_parser(
        'streaming-history', help="list streaming history")
    streaming_history_parser.add_argument('--spotify-data-dir', required=True,
                                          help="path to downloaded spotify data")
    streaming_history_parser.add_argument('-o', '--output-tsv-file',
                                          help="output to file instead of stdout")

    library_purge_parser = subparsers.add_parser(
        'library', help="operation on Spotify library")
    library_purge_parser.add_argument(
        'purge', help="purge tracks listed in file")
    library_purge_parser.add_argument(
        'track_list', type=str, nargs=1, help="list of tracks")

    args = global_parser.parse_args()
    if args.command == "streaming-history":
        streaming_history(getattr(args, 'spotify_data_dir'),
                          getattr(args, 'output_tsv_file'))
    elif args.command == "library":
        if args.purge:
            library_purge(getattr(args, 'track_list')[0])


if __name__ == '__main__':
    main()
