import praw
from config_bot import *

# Reddit stuff
r = praw.Reddit(user_agent = "ARTCbot 1.3.0 by herumph",
        client_id = ID,
        client_secret = SECRET,
        username = REDDIT_USERNAME,
        password = REDDIT_PASS)

submission = r.submission(url='https://www.reddit.com/r/RumphyBot/comments/8gb347/mooseleague_test/')

def get_first_index(keyword, text):
    indices = [i for i, x in enumerate(text) if x.count(keyword)]# == keyword]
    try:
        index = indices[0]
    except:
        index = False
    return index

def main():
    authors = []
    times = []
    urls = []
    for comment in submission.comments:
        body = str(comment.body).lower()
        body = body.split()
        # handling extra spaces
        body = list(filter(None, body))
        if (body.count('time:')):
            # getting position in the list of a certain string
            index1 = get_first_index('time:',body)+1
            # if there is a comma in the same position or one position over from the first time,
            # there are two times
            index2 = get_first_index(',',body)
            # no space between first time and comma
            if (index2 and index2 == index1):
                times.append(body[index1][:-1]+','+body[index2+1])
            # space between first time and comma
            elif (index2 and index2 == index1+1):
                times.append(body[index1]+','+body[index2+1])
            else:
                times.append(body[index1])

            authors.append(str(comment.author))

        # url handling
        # strava but no youtube
        if (body.count('strava:') and not body.count('youtube:')):
            index = get_first_index('strava:',body)+1
            urls.append(body[index])
        # youtube but no strava
        elif (body.count('youtube:') and not body.count('strava:')):
            index = get_first_index('youtube:',body)+1
            urls.append(body[index])
        # both
        elif (body.count('strava:') and body.count('youtube:')):
            index1 = get_first_index('strava:',body)+1
            index2 = get_first_index('youtube:',body)+1
            urls.append(body[index1]+','+body[index2])
        # neither    
        else:
            urls.append('1')

    # writing out to csv
    with open ("raceResults.txt", "w") as f:
            for i in range(0,len(authors)):
                f.write(authors[i]+"|"+times[i]+"|"+urls[i]+'\n')
    return

main()