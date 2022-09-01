# six-degrees

This is a program that takes in an artist, and returns a path from Coldplay to the artist, if it exists. To do this, I created a database that store all of Coldplay's collaborations, and all of their collaboration's collaborations and so on until 6 layers were stored. The program uses Breadth-First-Search to navigate this vast web of artists to find the shortest path between Coldplay and the artist.
