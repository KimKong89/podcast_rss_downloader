# podcast_rss_downloader
simple script for downloading all podcast-episodes from an rss-feed. call like:
```
python -u https://feeds.buzzsprout.com/1940667.rss -fp null_uhr_eins_all_episodes
```

-u is for providing the url to the rss-feed -fp, short for filepath, is the directory to where the files will be saved. You can also use the paremter -n to only download a set number of new episodes like:
```
python -u https://feeds.buzzsprout.com/1940667.rss -fp null_uhr_eins_all_episodes -n 1
```
This will only download the newest episode