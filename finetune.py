import argparse
import csv

from spotify_provider import SpotifyData


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


def main():
    parser = argparse.ArgumentParser(
        description="Finetune, a Spotify library organizer.")

    parser.add_argument('streaming_history',
                        metavar='streaming-history', help="list streaming history")

    parser.add_argument('--spotify-data-dir', required=True,
                        help="path to downloaded spotify data")
    parser.add_argument('-o', '--output-tsv-file',
                        help="output to file instead of stdout")

    args = parser.parse_args()

    if args.streaming_history:
        streaming_history(getattr(args, 'spotify_data_dir'),
                          getattr(args, 'output_tsv_file'))


if __name__ == '__main__':
    main()
