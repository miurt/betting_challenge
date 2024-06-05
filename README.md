A betting_challenge application for Check24 challenge (app to bet on sports, UEFA Euro 2024 in this example).

- Python, flet and firebase for the database

--Python and Flet was chosen, since the UI wasn't the main goal of this challenge and Flet lets the devs to create multi-platform apps powered by Flutter.

--Flet also has in-build solutions for broadcasting messages to all the app instances.

--Firebase was chosen as an easy and free (in this case) solution for the DB, which can potentially handle lots of requests and users.

- Limitations: problems if communities/names use "_" symbol; app shows today's games in dashboard (date is hardcoded as string, not checking devices current time)


I will add the video on Wednesday's evening, 05.06 :)
Still some bugs are present (especially for leaderboards and broadcasting updates), will be fixed on Wednesday

To run the app:

```
flet run [app_directory]
```
