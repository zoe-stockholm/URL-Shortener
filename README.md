url-shortener
=============
This is a URL shortening app using Django rest framework
The URL shortener use a cleaned wordlist (cleaned_words.txt) to create a unique key.

On the front page, user can type in a URL which the user want to make shorten.
After submitted, the result page will give the user the shortened URL.
If the user then visit the shortened URL, will be redirected to the original URL.

Some exception cases:
If invalid or missing URL input, will return to a failed page with error message.
If URL input has been shortened, will return to a existed page with inforamtion of original URL and shortened URL.


Prerequisites
=============
##if didn't install virtualenv before, then run this command
$ pip install virtualenv

$ cd Dev_private
$ virtualenv venv

##activate virtualenv
$ source activate.sh

##install all libraries and tools which this project needs
$ cd Dev_Fyndiq
$ pip install -r requirements.txt

##cleans the wordlist(words.txt) and create a new wordlist(cleaned_words.txt),and loads it into the database.
$ cd shortener
$ cd data
$ cat words.txt | tr A-Z a-z | sed 's/[^a-zA-Z0-9]//g' > cleaned_words.txt



Settings
========

If you want to test one scenario, When all the words in the wordlist have been used up as keys,
the oldest existing key/URL should be deleted and that key should be reused for new URL submissions.

Please comment out line 48-49 in views.py and comment in line 51-52 in views.py
and comment out line 69-81 in integration_tests/tests.py
and run
$ python manage.py test shortener.tests.integration_tests.tests.URLShortenerTestCase.test_all_words_in_wordslsit_are_used




Good to go
=============
## run migrate before run server
$ cd ..
$ cd ..
$ python manage.py migrate

##run all testsuits
$ python manage.py test

##run server
$ python manage.py runserver

## attention
If you want to visit the shortened URL, please type 127.0.0.1:8000/key (key is a word from the cleaned wordsllist)



