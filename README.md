
##A betting_challenge application for Check24 challenge 
App to bet on sports, UEFA Euro 2024 in this example.

###Used Technologies
- Python + flet and firebase for the database

    - Python and Flet was chosen, since the UI wasn't the main goal of this challenge and Flet lets the devs to create multi-platform apps powered by Flutter.

    - Flet also has in-build solutions for broadcasting messages to all the app instances.

    - Pandas was used for working with data, mainly for leaderboards

    - Firebase was chosen as an easy and free (in this case) solution for the DB, which can potentially handle lots of requests and users.

- Limitations: 
    - Problems if communities/names use "_" symbol
    - App shows today's games in dashboard (date is hardcoded as string, not checking devices current time)
    - Some small bugs are present, but app is mainly finished

###Demonstation Video
~~I will add the video on Wednesday's evening, 05.06~~
**Correction**: I used all my free reads from the data base, so i will upload the demonstration video **during Thursday**

###App currently offers:
- [x] login/signup functions (only login is needed, no password)
- [x] Admin mode for updating games and results of the games
- [x] *Accessed though NavBar*: Communities and leaderboards (each community page has their leaderboard: ranked, sorted and paginated as stated in challenge) 
- [x] User can join up to 5 comunities and create their own (as long as it is under 5), there is a separate page for that
- [x] *Accessed though NavBar*: Dashboard with today's games and leaderboards previews for each community
- [x] *Accessed though NavBar*: List of all games in Euro 2024 with possibility to bet on the game
- [x] Funciton for betting, logic for updating points
- [x] Custom Widget for showing Leaderboards
- [x] Another Paginated DataTable Widget (for games listing) was taken from [here](https://github.com/bobwatcherx/FletPaginatedTable/tree/master)

###What can be further done:
- [] UI is still far from perfect in some parts (for example, time and date should be shown more appealing for the user)
- [] Sometimes app doesn't update the page/data by itself without reloading
- [] The latter function is hard to test, as it is not so easy to start 2 separate instances of the app that will be subscibed to PuSub
- [] Checking actual time and not using hard coded string
- [] Pinning friends was not implemented, since I was confused, how it should work together with pagination. But both search and pinning is possible to implement.
- [] Also sorting of users with the same rank is done by name in the leaderboards, not by registration date, as stated in the challenge. This can be easily changed, just by additional saving of registration time in the firestore and sorting by it (as sorting is mainly done with pandas)
- [] Code can be further cleaned/structured/optimised (for example, if a user joins a community, currently the whole community data is updated. For better performance, only the new user data should be fetched and added to the config.communities_data)

###Images
Those are basically screenshots from video I was doing when I reached max readings, so not all the fuctions present here
![Starting page](/images/image-2.png)
![Login page](/images/image-4.png)
![Communities page (new user)](/images/image-1.png)
![Joining/adding community](/images/image.png)
![Firestore collections and documents (the misspell in the word comunity was fixed as well :) )](/images/image-3.png)


###To run the app:

```
flet run [app_directory]
```
