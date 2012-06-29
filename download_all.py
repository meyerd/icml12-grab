#!/usr/bin/python

from WebCursor import WebCursor
import sys, re, urllib, os, errno
from BeautifulSoup import BeautifulSoup

BASEURLS = [("http://icml.cc/2012/papers/","main_conference")]

linkre = re.compile('([0-9]+)\.pdf')

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: 
            raise

def lencheck(element, length=1):
    if len(element) < length:
        raise RuntimeError, "parse error %s" % (str(element))

def load(burl, folder):
    print "processing %s ..." % (burl)
    mkdir_p(folder)
    wc = WebCursor()
    html = wc.get(burl)
    if html == "":
        raise RuntimeError, "could not download %s" % (burl)
    
    soup = BeautifulSoup(html)
    # days = soup.findAll(u"table", attrs={u"class": u"menu"})
    papers = soup.findAll(u"div", attrs={u"class": u"paper"})
    lencheck(papers)
    for paper in papers:
        heading = paper.findAll(u"h2")
        lencheck(heading)
        title = heading[0].text.strip()
        pauthors = paper.findAll(u"p", attrs={u"class": u"authors"})
        lencheck(pauthors)
        authors = pauthors[0].text.strip()
        link = paper.findAll(u"a")
        lencheck(link)
        linkurl = link[0]['href'].strip()
        ret = linkre.search(linkurl)
        if not ret:
            if len(link) < 2:
                continue
            raise RuntimeError, "link parsing error %s" % (linkurl)
        papernumber = int(ret.groups()[0])
        fulllink = burl + "/" + str(papernumber) + u".pdf"
        outfile = os.path.join(folder, str(papernumber) + " - " + 
                               title + " - " + authors + ".pdf")
        print "downloading %s ..." % (outfile),
        sys.stdout.flush()
        if not os.path.exists(outfile):
            urllib.urlretrieve(fulllink, outfile)
            print "done."
        else:
            print "already there."

if __name__=='__main__':
    for burl,folder in BASEURLS:
        load(burl, folder)



