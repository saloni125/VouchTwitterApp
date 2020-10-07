import re
from datetime import datetime
from json import dumps
from config import CONSUMER_KEY, CONSUMER_SECRET
from config import TWEETS_SINCE_DAYS, TWEETS_COUNT, TOP_COUNT
from config import CALLBACK_URL
from django.contrib.auth import logout
from django.shortcuts import redirect
import tweepy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import Domain, Tweet


def top_tweets_list(request):


    tweets_top_urls = Tweet.objects.all().\
                            values('user_id', 'user_screen_name', 'user_name').\
                            annotate(total=Count('url')).\
                            order_by('-total')[:TOP_COUNT]

    domains_top_names = Domain.objects.all().\
                            values('domain_name').\
                            annotate(total=Count('domain_name')).\
                            order_by('-total')[:TOP_COUNT]

    return render(request,
                'app/top_tweets_list.html',
                    {
                    'tweets':tweets_top_urls,
                    'domains':domains_top_names
                    }
                )

def user_tweets_list(request):
    # post = get_object_or_404(Post, pk=pk)
    if request.session.get('user_id'):
        tweets =  Tweet.objects.filter(user_id=request.session.get('user_id', -1))
        return render(request, 'app/user_tweets_list.html', {'tweets':tweets})
    
    else:
        response = HttpResponseRedirect('/')
        return response



def auth(request):
	# start the OAuth process, set up a handler with our details
	oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)
	# direct the user to the authentication url
	# if user is logged-in and authorized then transparently goto the callback URL
	auth_url = oauth.get_authorization_url(True)
	response = HttpResponseRedirect(auth_url)
	# store the request token
	request.session['request_token'] = oauth.request_token
	return response

def callback(request):

    verifier = request.GET.get('oauth_verifier')
    tweets_data = []
    user_id = ''

    if verifier:
        oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        token = request.session.get('request_token')

        # remove the request token now we don't need it
        request.session.delete('request_token')
        oauth.request_token = token
        
        # get the access token and store
        try:
            oauth.get_access_token(verifier)
            # fetch tweets from user timeline 
            tweets_data, user_id = fetch_tweets(oauth)
    
            for tweet, domain in tweets_data:
                Tweet.objects.get_or_create(**tweet)
                Domain.objects.get_or_create(**domain)
            
            request.session['user_id'] = user_id
        
        except tweepy.TweepError:
            print('Error, failed to get access token')
        
        except Exception as e:
            print(e)

        
    
    response = HttpResponseRedirect('/')
    return response

def sign_out(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    response = HttpResponseRedirect('/')
    return response
    
def fetch_tweets(oauth):
    api = tweepy.API(oauth)
    user_timeline_response = api.user_timeline(count=TWEETS_COUNT, tweet_mode='extended')
    user_id = user_timeline_response[0].user.id_str
    filtered_tweets = filter_tweets(user_timeline_response)
    return filtered_tweets, user_id 


def filter_tweets(response):

    tweets_data = []
    
    for status in response:
        urls = status.entities.get('urls')
        days_since_tweet = (datetime.now() - status.created_at).days
        
        if urls and urls[0].get('expanded_url') and days_since_tweet <= TWEETS_SINCE_DAYS:
            tweet = {}
            domain = {}
            tweet['tweet_id'] = status.id_str
            tweet['text'] = status.full_text
            tweet['url'] = urls[0].get('expanded_url')
            tweet['user_id'] = status.user.id_str
            tweet['user_name'] = status.user.name
            tweet['user_screen_name'] = status.user.screen_name
            domain['tweet_id'] = status.id_str
            domain['domain_name'] = resolve_domain_name(tweet['url'])
            tweets_data.append((tweet, domain))
    
    return tweets_data

def resolve_domain_name(url_str):
    m = re.search('https?://([A-Za-z_0-9.-]+).*', url_str)
    if m:
        return m.group(1)
    return 'example.com'

    
