# collectible-app-api
This was an extremely fun project where I built a more sophisticated backend
REST API that included testing.

This project is conceptually a collectibles backend. As digital and physical
collectibles become more mainstream, artists and collectors alike will want
a place where they can track all the items an artist has ever created, and view
which collectibles of a collection they own and which they would like to own.

Essentially, a 'pokedex' for collectibles and artists. Future plans were to
add an exclusive zone only for users who have collected enough of an artist's
work. If front end is ever implemented, I was imagining the website would subtly
change as your collections increased.

The original testing conditions were using an older build of Ubuntu, as well as
out of date versions of django, etc. I virtualized the OS in a docker container,
and I used postgresql for a database, to get experience working with something
besides sqlite. After I finished building the API, I upgraded to the newest
version of all the software on windows, and squashed all the bugs that
presented themselves. Essentially, those bugs were that I needed to delete
the django migration files and recreate the database, and then, because in
django primary key functionality changed, I needed to add
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField' to my settings file.

Something I thought was strange and interesting was that before while I was
testing the retrieval of a list of collections. Originally on line 75 of my
code(test_collection_api.py) was:
`collections = Collection.objects.all().order_by('-id')`
Which served its purpose in the previous build configuration as confirmed via
a later assertion. However, upon upgrading to the newest compatible versions of
all python packages, the docker image, and database, the test failed. All of a
sudden my expected results were flipped from the serializer, so I removed this
method, printed both items fully to personally confirm the correct functionality
myself, which it was. Not sure why this would happen, unless calling this
method on an already sorted list flips the sort, and something new with django
now sorts `.objects.all()` method call? If you know, email me!

The project is fully linted, there are 51 software tests implemented to test
and make sure the system does what I say it does. There are multiple endpoints
including Collections, Items, Tags and Users. Users can filter through their
added Tags, Items, and Collections via any associations they have, or
see the full lists of all objects of each type that are associated/created by
the User. My plan is to implement a feature that would make Collections, Items
and Tags public when an artist is ready to publish it to the site.

Also, I had the opportunity to brush up on the PIL library by adding images to
Collections(and soon Items), I've worked with PIL before and it's rather fun.

Many thanks to Mark Winterbottom for answering some of the questions I had
when I was setting this up.

Please note that the use of any names(of people, projects or products) during
testing is by no means any form of endorsement or condemnation. All numbers
were selected via a randomizer, and any numerical symbolism anyway may infer
from them is purely coincidental and unintentional.
