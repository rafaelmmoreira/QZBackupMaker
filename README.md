# QZBackupMaker
A webscraping Python script to backup all posts on Queenzone forum.

Today, October 10, 2020 Richard Orchard announced Queenzone will be shut on November 1st, 2020.

Should someone be interested in backing its contents up, this script will do that automatically.

Disclaimer: it will do so by brute force! It will access each page on each thread on each forum, parse username, timestamp and post content and generate a .json file for each post. It also adds the "[QUOTE]" tags, Queenzone style. Therefore, it will certainly take several hours to run and could potentially make the server itself slow. I highly advice you to ask Richard for permission before running the script right to the end! So far I've only done small tests only on the first page of each forum or on the last 3 pages to make sure it correctly gets every thread and knows when it reached the last page and can move on to the next forum and I do not intend on running it on the entire forum myself.
