import requests
from lxml import etree
from rich.progress import track
import argparse
import os

# Should work on all Buzzsprout-Sites. I have tested a couple of other rss-feeds as well.
# Most testing was done with the page of my own podcast "Null Uhr Eins":
# "https://feeds.buzzsprout.com/1940667.rss"
# call like "python -u "https://feeds.buzzsprout.com/1940667.rss" -fp null_uhr_eins_all_episodes"


def downloadEpisodesFromRSS(feed, fpath, nr):
    # Download rss-feed as xml
    response = requests.get(feed)
    content = response.content.decode()
    content = content.replace('<?xml version="1.0" encoding="UTF-8" ?>', '')
    content = content.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
    xml = etree.fromstring(content)
    matches = xml.xpath('//item')

    print(f'''found {len(matches)} episode(s) ''')

    # how many episodes to download
    if nr is None or int(nr) > len(matches):
        nr = len(matches)
    else:
        nr = int(nr)

    print(f'''downloading {nr}/{len(matches)} episode(s) ''')

    # loop over episodes
    for item in track(matches[0:nr], 'downloading'):
        url = item.xpath('./enclosure')[0].attrib['url']

        # for sorting purposes
        season = item.xpath('./*[local-name() = "season"]')
        if len(season) > 0:
            season = season[0].text
            season = str(int(season)).zfill(2)
        else:
            season = '00'

        episode = item.xpath('./*[local-name() = "episode"]')
        if len(episode) > 0:
            episode = episode[0].text
            episode = str(int(episode)).zfill(2)
        else:
            episode = '00'

        # creating file-name, combining with path
        fn = f'''S{season}E{episode}_{url.split('/')[-1]} '''
        fp = os.path.join(fpath, fn)

        # download
        r = requests.get(url, allow_redirects=True)
        open(fp, 'wb').write(r.content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='url to the rss-feed')
    parser.add_argument('-fp', '--filepath', help='path to save downloaded files', default='.')
    parser.add_argument('-n', '--nr', help='number of newest episode to download', default=None)
    args = parser.parse_args()

    if not args.url:
        print('please provide rss-feed url (-u)')
    else:
        if not os.path.exists(args.filepath):
            os.mkdir(args.filepath)

        if args.url.startswith('"') or args.url.startswith("'"):
            args.url = args.urls[1:-1]

        downloadEpisodesFromRSS(args.url, args.filepath, args.nr)
        print('done')


if __name__ == '__main__':
    main()
