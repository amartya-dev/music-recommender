# music-recommender
An application to create a music recommendation system 

# To Do
- [x] Add a method to get songs year wise bollywood
- [x] Add a class to in general store the songs in a csv file (to be later written in database)
- [ ] Add a method to get english songs
- [ ] Add a utility function to download songs from specified urls
- [ ] A django app for playing songs, creating playlist and rating songs
- [ ] Make a recommender system with SVD++ to deal with cold start problems
- [ ] Integrating the recommendation with Django application

# Current functionalities and usage

As specified in the To Do section, the repo currently gets information of bollywood songs for any specified year and then adds the same in a csv file which can be specified and used later.

## Usage for 
- ```utils/get_hindi_songs.py``` :
```
    username@hostname $ python get_hindi_songs.py -h
    usage: get_hindi_songs.py [-h] [--year YEAR] [--dir DIR] [--file FILE]

    Get Hindi songs

    optional arguments:
      -h, --help   show this help message and exit
      --year YEAR  Get data for an year.
      --dir DIR    Specify output directory
      --file FILE  Specify file name
 ```
 
 The requirements will be added later according to the whole project
