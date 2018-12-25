# Spo-tfidf-y

## What is it?

I am trying to convert Spotify songs to vectors, so I can cluster like songs and analyze artist discography

## What's with the title?

tf-idf stands for [term frequency inverse document frequency](https://en.wikipedia.org/wiki/Tf%E2%80%93idf), and is the way I generate the vectors

The example I'm running my code on is Kanye's discography – I input his albums, and then I query spotify until I get playlists with multiple of his songs in them. This playlist is added to a matrix that I eventually use to define the vectors of songs.

This project will compare the clusters formed from the vectorized versions of Kanye's songs to the implied clusters defined by his albums.