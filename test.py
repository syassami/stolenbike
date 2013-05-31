import re
import datetime
import time
import string
import urllib
import urllib2

results = re.compile('<p.+<div>', re.DOTALL)

#results = re.compile('<p>.+<div>sort by')
delay = 100


def search_section(city,query):
    t = datetime.datetime.now()
    tyme = time.mktime(t.timetuple())

    url = "http://" + city + ".craigslist.org/search/" + "bia" + "?query=" + query.replace(' ', ',')
    print url
    #Setup headers to spoof Mozilla
    dat = None
    ua = "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.4) Gecko/20091007 Firefox/3.5.4"
    head = {'User-agent': ua}

    errorcount = 0

    #Get page
    req = urllib2.Request(url, dat, head)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        if errorcount < 1:
            errorcount = 1
            print "Request failed, retrying in " + str(delay) + " seconds"
            time.sleep(int(delay))
            response = urllib2.urlopen(req)
    except urllib2.URLError, e:
        if errorcount < 1:
            errorcount = 1
            print "Request failed, retrying in " + str(delay) + " seconds"
            time.sleep(int(delay))
            response = urllib2.urlopen(req)

    msg = response.read()
    print msg
    errorcount = 0

    res = results.findall(msg)
    res = str(res)
    res = res.replace('[', '')
    res = res.replace(']', '')
    res = res.replace(chr(92)+'t', chr(9))
    res = res.replace(chr(92)+'n', chr(13))
    res = res.replace(chr(92)+'r', chr(13))
    res = res.replace(chr(39), '')

    outp = open("results" + str(tyme) + ".html", "a")
    outp.write(city)
    outp.write(str(res))
    outp.close()

search_section('santabarbara','road bike')