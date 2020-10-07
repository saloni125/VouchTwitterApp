# Assignment
# Introduction
The app should let the user login with Twitter.
Once authenticated, the app pulls just the tweet's that contain URLs from a users stream for the past 7 days
Once stored, the application should then compute and display
Actual Tweets containing links and Which user has shared the most links
,List of Top Domains that have been shared so far.
# Prerequisites
Install Python and Django.
# How to run on your System
## Clone the repository
git clone https://github.com/saloni125/VouchTwitterApp
## Install the requirements
python -m pip install -r requirements.txt
## Setup Database
### python manage.py makemigrations
It is responsible for creating new migrations based on the changes you have made to your models.

### python manage.py migrate
Migrate - It is responsible for applying migrations, as well as unapplying and listing their status.
## Start the Development Server
python manage.py runserver

Open http://127.0.0.1:8000/ 