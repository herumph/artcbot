import artcbot
import praw
from datetime import datetime
from config_bot import *
import random

# Reddit stuff
r = praw.Reddit(user_agent = "ARTCbot 1.3.0 by herumph",
    client_id = ID,
    client_secret = SECRET,
    username = REDDIT_USERNAME,
    password = REDDIT_PASS)

sub = "artc"
#sub = "RumphyBot"
subreddit = r.subreddit(sub)

# Fetching arrays
already_done = artcbot.get_array("already_done")
# not ideal to get contributors every time but it's not a problem
contributors = [str(contributor) for contributor in r.subreddit(sub).contributor()]

# Looking at comments
for comment in r.subreddit(sub).comments(limit=25):
  if(comment.id not in already_done and str(comment.author) != "artcbot"):
    # marking comment as read if it's a reply
    # this ensures that the PM part does not respond as well
    comment.mark_read()
    already_done.append(comment.id)
    # Making sure the already_done file doesn't get too big.
    del already_done[0]
    artcbot.write_out("already_done",already_done)

    # Saving comment
    comment_list = str(comment.body)
    comment_list = comment_list.split()

    # passing off to get reply
    reply = artcbot.call_bot(comment_list, comment.author, contributors)

    # Responding if needed
    if(len(reply) > 1):
      reply += "\n\n---\n\n^^To ^^cut ^^down ^^on ^^spam ^^you ^^can ^^private ^^message ^^me ^^commands."
      comment.reply(reply)


# sorting through unread messages
for pm in r.inbox.unread(limit=25):
  pm.mark_read()
  # only responding to pm's, not comment replies
  if(not pm.was_comment):
    body = str(pm.body)
    body = body.split()

    reply = artcbot.call_bot(body, pm.author, contributors)

  # Responding
  if(len(reply) > 1):
    pm.author.message(pm.subject, reply)


# weekly threads
# array of 0,1 and random time to post thread
posted = artcbot.get_array("posted")

# outputting clean posted file at 3am EST
if(datetime.now().hour == 3 and posted[0] == '1'):
  # resetting file and new random minute
  posted = ['0',str(int(random.uniform(0,1)*60))]
  artcbot.write_out("posted",posted)

# earliest time to post thread, currently 6:30 EST
postHour = 6
postMin = 30+int(posted[1])
if(postMin >= 60): postHour += 1; postMin = postMin-60
# boolean to check if it's time to post
timeBool = (datetime.now().hour > postHour or \
        (datetime.now().hour == postHour and datetime.now().minute >= postMin))
#print(datetime.now().hour,datetime.now().minute,timeBool,postHour,postMin)

# function to submit and write posted file
def submitPost(title, selftext, clear):
  if(clear): # first removing other artcbot announcments
    for submission in r.subreddit(sub).new(limit=25):
      if(str(submission.author) == "artcbot" and submission.stickied):
        submission.mod.sticky(state=False)

  # getting GD flair id in order to auto flair the post
  flair_id = [flair['id'] for flair in subreddit.flair.link_templates if(flair['text'] == 'General Discussion')][0]
  subreddit.submit(title=title,selftext=selftext,send_replies=False,flair_id=flair_id)
  posted[0] = '1'
  artcbot.write_out("posted",posted)

  # making the thread an announcement
  for submission in r.subreddit(sub).new(limit=1):
    # extra check
    if(str(submission.author) == "artcbot"):
      submission.mod.sticky(state=True, bottom=True)
  return

# Tuesday Q&A
if(posted[0] != '1' and datetime.now().weekday() == 1 and timeBool):
  submitPost("Tuesday and Wednesday General Question and Answer"\
    ,"Ask any general questions you might have\n\n"+\
    "#Is your question one that's complex or might spark a good discussion? Consider posting it in a separate thread!",1)

# Thursday Q&A
if(posted[0] != '1' and datetime.now().weekday() == 3 and timeBool):
  submitPost("Thursday and Friday General Question and Answer"\
    ,"Ask any general questions you might have\n\n"+\
    "#Is your question one that's complex or might spark a good discussion? Consider posting it in a separate thread!",1)

# Weekender
if(posted[0] != '1' and datetime.now().weekday() == 4 and timeBool):
  submitPost("The Weekender","BEEP BEEP! It's weekend time! What are you up to?",0)

# Saturday media
if(posted[0] != '1'  and datetime.now().weekday() == 5 and timeBool):
  submitPost("Saturday Running Media","This thread fills the void that you were craving. Post any and all running media you want to share. This is including but not limited to, pictures and videos you took and other things you found interesting and wanted to share.",1)

# Sunday GD
if(posted[0] != '1' and datetime.now().weekday() == 6 and timeBool):
  submitPost("Sunday General Discussion","Talk about anything and everything here!",1)

# Monday sidebar race updates
if(posted[0] != '1' and datetime.now().weekday() == 0 and timeBool):
    # getting sidebar
    settings = r.subreddit(sub).mod.settings()
    sidebar = settings['description']
    sidebar = sidebar.split('\n') # need to parse

    # finding start of table and adding 2 to get to first race entry
    tableStart = sidebar.index('**Date**|**Username**|**Race**')+2
    for i in range(tableStart,len(sidebar)): # finding where the table ends
        if(sidebar[i].count('______________')):
            tableEnd = i # i and not i-1 for the benefit of the next loop
            break;

    # deleting old entries
    for i in range(tableStart,tableEnd):
        del sidebar[tableStart]

    # getting new races
    races = artcbot.call_bot(['!upcoming'], 'artcbot', contributors)
    races = races.split('\n')
    raceInd= races.index('-- | -- | -- | --')+1
    races = races[raceInd:-1] # -1 gets rid of newline at the end
    for i in range(len(races)):
        temp = races[i].split('|')
        races[i] = '|'.join(temp[:-1]) # getting rid of distance

    # inserting new races
    for i in range(tableStart,tableStart+len(races)):
        sidebar.insert(i,races[i-tableStart])
    sidebar = '\n'.join(sidebar) # joining back together and then updating
    r.subreddit(sub).mod.update(description=sidebar)

    # getting redesign sidebar
    widgets = r.subreddit(sub).widgets
    for widget in widgets.sidebar:
        if isinstance(widget, praw.models.TextArea):
            text_area = widget
            break;
    # updating the text
    text_area = text_area.mod.update(shortName='Information',text=sidebar)

    posted[0] = '1'
    artcbot.write_out("posted",posted)
