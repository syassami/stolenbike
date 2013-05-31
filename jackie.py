from BeautifulSoup import BeautifulSoup 
from urllib2 import urlopen               
import smtplib
import datetime
import time
import threading
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
	text = 'This is for jackies stolen bike. '
	if 7 < int(time.ctime()[11:13]) and int(time.ctime()[11:13]) < 23:
		text += 'App should be sending'
	else:
		text += 'App should not be sending'
	return text

def scrapeAndMake(sites):
	found = []
	for site in sites:
		html = urlopen(site)                      
		soup = BeautifulSoup(html)               
		postings = soup("span", {"class":"pl"})

		for post in postings:
			text = post.getText()
			criteria = ['road bike','green tires','54','53','21 in','54cm','53cm','medium','small','pink','vintage road','giant','vittoria','steel','12 speed','12-speed','shimano 105','shimano-105','orange','road','Road bike','Road Bike','Roadbike','road Bike','ROADBIKE','ROAD BIKE','speed']
			for crit in criteria:
		 		if crit in text:
		 			found.append((str(text),str(site[:-5]+post.a['href'])))
	toSend = ''
	for i in range(len(found)):
		toSend += found[i][0] + ' ' + found[i][1] + '\n'
	return toSend

def send_email(toSend,recipients):
    gmail_user = "findmystolenbike@gmail.com"
    gmail_pwd = "stolenBike"
    FROM = 'findmystolenbike@gmail.com'
    TO = recipients 
    SUBJECT = "Bike Alert test" + datetime.datetime.now().strftime('%b-%d-%I%M%p-%G')
    TEXT = toSend

    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"


def doAll():
	if 7 < int(time.ctime()[11:13]) and int(time.ctime()[11:13]) < 23:
		sites = ['http://santabarbara.craigslist.org/bia/','http://santamaria.craigslist.org/bia/','http://losangeles.craigslist.org/bia/','http://slo.craigslist.org/bia/','http://orangecounty.craigslist.org/bia']
		foundbikes = scrapeAndMake(sites)
		send_email(foundbikes,['syassami@gmail.com','jacquelyn0lee@gmail.com'])
		threading.Timer(10800, doAll).start()

doAll()
