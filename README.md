
## A betting_challenge application for Check24 challenge 
App to bet on sports, UEFA Euro 2024 in this example.

### Used Technologies
- Python, flet, pandas and firebase

    - Python and Flet was chosen, since the UI wasn't the main goal of this challenge and Flet lets the devs to create multi-platform apps powered by Flutter.

    - Flet also has in-build solutions for broadcasting messages to all the app instances.

    - Pandas was used for working with data, mainly for leaderboards

    - Firebase was chosen as an easy and free (in this case) solution for the DB, which can potentially handle lots of requests and users.

- Limitations: 
    - Problems if communities/names use "_" symbol
    - App shows today's games in dashboard (date is hardcoded as string, not checking devices current time)
    - Some minor bugs can be present, even though those were mostly fixed

### Demonstation Video ###
> [!IMPORTANT]
> During first video recording, I used all my free reads for the day from firestore. So smal part of the demonstration of the betting logic and admin mode was recorded separately (in PART 2).

**[1 PART](https://youtu.be/FzVyrGkc5HU)** link for the first part of the video

**[2 PART](https://youtu.be/2UKAy48pVD8)** link for the second part of the video


### App currently offers:
- [x] login/signup functions (only login is needed, no password)
- [x] Admin mode for updating games and results of the games
- [x] *Accessed though NavBar*: Communities and leaderboards (each community page has their leaderboard: ranked, sorted and paginated as stated in challenge) 
- [x] User can join up to 5 comunities and create their own, that they automatically join (limit for joining: 5 communities per user), there is a separate page for that
- [x] *Accessed though NavBar*: Dashboard with today's games and leaderboards previews for each community
- [x] *Accessed though NavBar*: List of all games in Euro 2024 with possibility to bet on the game
- [x] Funciton for betting on games, logic for updating points after a game finishes (8, 6, 4, 0 according to challenge)
- [x] Custom Widget for showing Leaderboards
- [x] Another Paginated DataTable Widget (for games listing) was taken from [here](https://github.com/bobwatcherx/FletPaginatedTable/tree/master)
- [x] Storage of data in firestore
- [x] App updates itself without reloading, when some data is changed 

### What can be further done:
- [ ] UI is still far from perfect in some parts (for example, time and date should be shown more appealing for the user)
- [x] ~~Sometimes app doesn't update the page/data by itself without reloading~~ Fixed
- [ ] The latter function is hard to test, as the app is not deployed, so there still might be some bugs
- [ ] Checking actual time and not using hard coded string
- [ ] Pinning friends was not implemented, since I was confused, how it should work together with pagination. But both search and pinning is possible to implement.
- [ ] Also sorting of users with the same rank is done by name in the leaderboards, not by registration date, as stated in the challenge. This can be easily changed, just by additional saving of registration time in the firestore and sorting by it (as sorting is mainly done with pandas)
- [ ] Code can be further cleaned/structured/optimised (~~for example, if a user joins a community, currently the whole community data is updated.~~*Partly fixed: now the whole data is not fetched for the user itself, only needed data. Didn't get fixed, when the other than logged in user joins any community.* For better performance, only the new user data should be fetched and added to the config.communities_data)
- [ ] Using Flet's client storage functions (Flet uses shared_preferences Flutter package) instead of config to store session data
- [ ] Add snack_bar to show information about updates of games from user side (when admin updates something) and to show that _ symbol is not allowed in user community names, when user tries to save a name with _

### Images
> [!NOTE]
> Only some basic screenshots, I will add more, if i will change the UI

<img src="/images/image.png" width="30%" height="30%"><img src="/images/image-3.png" width="35%" height="35%">


### To run the app:

```
flet run [app_directory]
```
