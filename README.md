# karaoke-finder
back end code for searching/finding stuff in my karaoke collection

Probably not useful to anyone else....


-- For Mary



notes:

#initial list for the DB
#giant pile of shell glop to get a file list for easy import - should turn in to 3 columns in tsv
(cd ~/kar; find .) | grep -i cdg | sort | awk -F / '{print $3 "\t" $4}' | sed 's/-/\t/' > filelist.tsv
