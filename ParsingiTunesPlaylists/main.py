'''
iTunes playlist parser that finds duplicate tracks
in a playlist, common tracks between two
playlists and shows rating and duration graphs of a playlist

Original author: Mahesh Venkitachalam

Slight modifications by me
'''

import argparse
import plistlib as pl
import numpy as np
from matplotlib import pyplot

def find_duplicates(filename):
    '''
    Finds duplicate tracks in a playlist and
    saves them to dups.txt
    '''

    print("Finding duplicate tracks in {}...".format(filename))

    plist = pl.readPlist(filename)

    tracks = plist['Tracks']
    track_names = {}

    for track in tracks.values():
        try:
            name = track['Name']
            duration = track['Total Time']

            if name in track_names:
                if duration//1000 == track_names[name][0]//1000:
                    count = track_names[name][1]
                    track_names[name] = (duration, count+1)
            else:
                track_names[name] = (duration, 1)

        except:
            pass

    duplicates = []

    for key, val in track_names.items():
        if val[1] > 1:
            duplicates.append((val[1], key))

    if duplicates:
        print("Found {} duplicates. Track names saved to dups.txt".format(len(duplicates)))
        dups_f = open("dups.txt", "w")

        for val in duplicates:
            dups_f.write("{} ({} times)\n".format(val[1], val[0]))
        dups_f.close()
    else:
        print("No duplicate tracks found.")

def find_common_tracks(filenames):
    '''
    Finds common tracks in two playlists and
    saves them to commons.txt
    '''
    track_name_sets = []

    for file_name in filenames:
        track_names = set()

        plist = pl.readPlist(file_name)
        tracks = plist['Tracks']

        for track in tracks.values():
            try:
                track_names.add(track['Name'])
            except:
                pass

        track_name_sets.append(track_names)

    common_tracks = set.intersection(*track_name_sets)

    if common_tracks:
        common_f = open("commons.txt", "w")

        for val in common_tracks:
            f_str = "{}\n".format(val)
            common_f.write(f_str)

        common_f.close()

        print("{} common tracks found.".format(len(common_tracks)),
              "Track names written to commons.txt.",
              sep="\n")

    else:
        print("No common tracks found.")

def plot_stats(filename):
    '''
    Draws graphs based on data collected from playlist file
    '''
    plist = pl.readPlist(filename)
    tracks = plist['Tracks']
    genres = {}
    ratings = []
    durations = []

    for track in tracks.values():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
            if track['Genre'] not in genres.keys():
                genres[track['Genre']] = 1
            else:
                genres[track['Genre']] += 1
        except:
            pass

    if ratings == [] or durations == []:
        print("No valid Album Rating/Total Time data in {}.".format(filename))
        return

    #Scatter plot
    x_dur = np.array(durations, np.int32)
    x_dur = x_dur / 60000.0

    y_rat = np.array(ratings, np.int32)


    pyplot.subplot(2, 1, 1)
    pyplot.plot(x_dur, y_rat, 'o')
    pyplot.axis([0, 1.05*np.max(x_dur), -1, 110])
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track rating')

    #Histogram
    pyplot.subplot(2, 1, 2)
    pyplot.hist(x_dur, bins=20)
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    #Horizontal bar graph
    fig_bar, ax_bar = pyplot.subplots(figsize=(6, 5))
    pos = np.arange(len(genres.keys()))
    ax_bar.barh(pos, genres.values(), tick_label=[name for name, count in genres.items()])
    ax_bar.set_yticks(pos)
    ax_bar.set_xlabel('Count')
    ax_bar.set_ylabel('Genres')

    #Pie chart
    #fig_pie, ax_pie = pyplot.subplots()
    #ax_pie.pie(genres.values(), labels=genres.keys(), autopct='%1.1f%%')
    #ax_pie.axis('equal')

    pyplot.tight_layout()
    pyplot.show()

def main():
    '''
    Main running function
    '''
    #Create parser
    desc_str = """This program analyzes playlist files (.xml)
    exported from iTunes."""
    parser = argparse.ArgumentParser(description=desc_str)

    #Add a mutually exclusive group of arguments
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--common', nargs='*', dest='pl_files', required=False)
    group.add_argument('--stats', dest='pl_file', required=False)
    group.add_argument('--dup', dest='pl_file_d', required=False)

    #Parse args
    args = parser.parse_args()

    if args.pl_files:
        find_common_tracks(args.pl_files)
    elif args.pl_file:
        plot_stats(args.pl_file)
    elif args.pl_file_d:
        find_duplicates(args.pl_file_d)
    else:
        print("These are not the tracks you are looking for.")


if __name__ == "__main__":
    main()
