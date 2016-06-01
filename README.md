# Madness

Django web application that generates a random NCAA March Madness bracket according to team seeds.  The chance of a team advancing in the tournament is proportional to that team's seed.  For more details, read the help system.

## Running Application
Code is running at:

https://youmadbro.herokuapp.com

## Installation

You can download and run this using standard Django manage.py runserver quick and easy.

## Todo

* Create a user profile page
* Verify options are logical when creating using options
  * Don't let user manually select a team with a very low seed - takes forever
  * Verify mutually exclusive teams
* Add some javascript to avoid reloading pages
* Print tourney to a file
* Add caching

## License

See LICENSE.txt
