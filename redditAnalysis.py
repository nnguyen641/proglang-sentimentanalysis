# https://www.jcchouinard.com/reddit-api-without-api-credentials/
# https://towardsdatascience.com/scraping-reddit-data-1c0af3040768
import json
import pandas as pd
import requests
import praw

# reddit = praw.Reddit(client_id='vfWol7HCvFymztQRr3nDig',
#                      client_secret='BzYjL82Od4kXIlE1QSieuH6wpKTG5A', user_agent='sentiment-nn')

# get 10 hot posts from a subreddit
# def get_hot_posts(subr):
#     posts = reddit.subreddit(subr).hot(limit=10)
#     for post in posts:
#         print(post.title)

# def create_db(subr):
#     posts = []
#     subreddit = reddit.subreddit(subr)
#     for post in subreddit.hot(limit=10):
#         posts.append([post.title, post.score, post.id, post.subreddit,
#                  post.url, post.num_comments, post.selftext, post.created])
#     posts = pd.DataFrame(posts, columns=[
#                      'title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
#     return posts

def get_reddit(subreddit, listing, limit, timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers={'User-agent': 'yourbot'})
    except:
        print('An Error Occured')
    return request.json()


def get_post_titles(r):
    '''
    Get a List of post titles
    '''
    posts = []
    for post in r['data']['children']:
        x = post['data']['title']
        posts.append(x)
    return posts

def get_post_body(r):
    posts = []
    for post in r['data']['children']:
        x = post['data']['selftext']
        posts.append(x)
    return posts

def get_results(r):
    '''
    Create a DataFrame Showing Title, URL, Score and Number of Comments.
    '''
    myDict = {}
    for post in r['data']['children']:
        myDict[post['data']['title']] = {
            'url': post['data']['url'], 'score': post['data']['score'], 'comments': post['data']['num_comments'], 'body': post['data']['selftext']}
    df = pd.DataFrame.from_dict(myDict, orient='index')
    return df

def get_words(r):
    posts = get_post_body(r)
    words = [w
             for body in posts
             for w in body.split()]
    return words

def getSubreddit():
    sub = input("Enter a subreddit to search for: ")
    return sub

def getLim():
    lim = input("Enter a limit number of posts (1-1000) to search for: ")
    while ( (convert(lim) < 1) or (convert(lim) > 1000)):
        print("Not in range. Please try again.\n")
        lim = input("Enter a limit number of posts (1-1000) to search for: ")
    return lim

def getTime():
    time = input("Enter a time (hour, day, week, month, year) to search for: ")
    times = ["hour", "day", "week", "month", "year"]
    while (time.lower() not in (x.lower() for x in times)):
        print("Invalid time. Please try again. \n")
        time = input(
            "Enter a time (hour, day, week, month, year) to search for: ")
    return time


def getListing():
    listing = input(
        "Enter a listing (controversial, best, hot, new, random, rising) to search for: ")
    listings = ["controversial", "best", "hot", "new", "rising"]
    while (listing.lower() not in (x.lower() for x in listings)):
        print("Invalid listing. Please try again. \n")
        listing = input(
            "Enter a listing (controversial, best, hot, new, rising) to search for: ")
    return listing

def convert(value):
    types = [int, float, str]  # order needs to be this way
    if value == '':
        return None
    for t in types:
        try:
            return t(value)
        except:
            pass

def main():
    subreddit = getSubreddit()
    limit = getLim()
    timeframe = getTime()  # hour, day, week, month, year, all
    listing = getListing()  # controversial, best, hot, new, random, rising, top
    
    r = get_reddit(subreddit, listing, limit, timeframe)

    #posts = get_post_body(r)

    words = get_words(r)
    # for w in words:
    #     print(w)
    
    score_file = open('AFINN/AFINN-111.txt')
    scores = {}  # initialize an empty dictionary


    for line in score_file:
        term, score = line.split("\t")
        # The file is tab-delimited.
        # "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
    
    score = 0


    for word in words:
        uword = word.encode('utf-8')
        if word in scores.keys():
            score = score + scores[word]
    print("SCORE: ", float(score))


    # for body in posts:
    #     print("______________________________")
    #     print(body)
    #     print("______________________________")

main()