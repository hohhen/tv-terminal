"""       DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
                    Version 2, December 2004 

 Copyright (C) 2015 Amir Uqdah <amir.uqdah@pacbell.net> 

 Everyone is permitted to copy and distribute verbatim or modified 
 copies of this license document, and changing it is allowed as long 
 as the name is changed. 

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 

  0. You just DO WHAT THE FUCK YOU WANT TO. 

"""

import click
import urllib2
import urllib
import sqlite3
import re
import os
import webbrowser

class Config(object):
    def __init__(self):
        self.verbose = False


config = click.make_pass_decorator(Config, ensure=True)
@click.group()
@click.option('--verbose', is_flag=True, help='display extra information')
@config
def cli(config, verbose):
    """
    \b
             _____                   _       _     _             
            |_   _|                 (_)     (_)   (_)            
              | | ___ _ __ _ __ ___  ___   ___ ___ _  ___  _ __  
              | |/ _ \ '__| '_ ` _ \| \ \ / / / __| |/ _ \| '_ \ 
              | |  __/ |  | | | | | | |\ V /| \__ \ | (_) | | | |
              \_/\___|_|  |_| |_| |_|_| \_/ |_|___/_|\___/|_| |_|
     \b
              the world's first terminal based streaming service  
                               ~ v0.1 Interference ~ 
                    
                               :.     `+`
                               -/    -+                             
                               `s   :/                              
                                y` +:                               
                                o/y-  .--....`                      
                              oNNMMNNNMMNNNNmyo::++sy               
                              :sMMMMMMMMMMMMMMMh+MMMy               
                              :yMMMMMMMMMMMMMMMNoMmNs               
                              :hMMMMMMMMMMMMMMMM.s:d/               
                              .sMMMMMMMMMMMMMMMN`oom-               
                               :mNMMMMMMMMMMMMNs ../-               
                              syssssyydddhyssssssssys               
                               `    ./:ymm/-`      `                
                               .+sdNMM- :s /Mmy+`                   
                               yMMMMMMs `m` mMMMh                   
                               mMMMMMMN``M: hMMMM.                  
                              -MMMMMMMM/.My hMMMMy                  
                              yMMMMMMMMo:Mm hMMMMh                  
                              NMMMMMMMM+/MM-mMMMMm                  
                              NMMMMMMMM/oMMoNMMMMM:                 
                              /MMMMMMMMdhMMmMMMMMN`                 
                              `dMMMMMMMMMMMMMMMMMy                  
                                dMMMMMMMMMMMMMMMMy                  
                                -mMMMMMMMMMMMMMNy/                  
                                 .MMMMMMMMMMMMMo                    
                                 `MMMMMMNMMMMMM/                    
                                 .MMMMMMsdMMMMM:                    
                                 :MMMMMm.oMMMMM:                    
                                 .MMMMM: -MMMMM.                    
                                 .MMMMM. .MMMMM.                    
                                 :MMMMm  .MMMMN`                    
                                 sMMMM+  .MMMMd                     
                                 hMMMM/   NMMMh                     
                                 mMMMM:   mMMMd                     
                                `NMMMN`   mMMMM`                                                   

    Termivision, or "tv", is a dead simple CLI that allows you to watch almost any of your favorite tv shows for free without the bother of searching for them online. You can watch, discover, and schedule(wip) your tv shows"""
    config.verbose = verbose
@cli.command()
@click.option('--here', default=False,is_flag=True,help='download via terminal')
@click.argument('name',default='',metavar='[series]')
@click.argument('season',default='',metavar='[season]')
@click.argument('episode',default='',metavar='[episode]')
@config
def download(config,name,season,episode,here):
    """ download any television show"""
    if name and season and episode:
        print os.path.dirname(os.path.realpath(__file__)) + '\\television.db' 
        conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + '\\television.db')
        cursor = conn.cursor()
        se = "%%Season %s Episode %s%%" % (season,episode)
        sn = name 
        cursor.execute("SELECT episode_link_direct,name,episode_name FROM show WHERE episode_name LIKE ? AND name LIKE ?", (se,sn))
        r = cursor.fetchone()
        if(config.verbose):
            click.echo("Attempting to download: %s %s" % (r[1],r[2]))
        response = urllib2.urlopen(urllib2.Request(r[0].strip('[]').replace("'",""))).read()
        download_link =  re.findall("\"file\" .*$",response,re.MULTILINE) #really stupid allmuyvideo vulnerability 
        download_link = download_link[0]
        if not here:
            webbrowser.open_new_tab(download_link.split(":",1)[1].replace('"','').strip(",\"\" "))
        else:
            print os.getcwd() + "\\"+ r[2].replace(u'\u2013','-').replace(u"\u2019", "'") + ".mp4"
            urllib.urlretrieve(download_link.split(":",1)[1].replace('"','').strip(",\"\" "), os.getcwd() + "\\"+ r[2] + ".mp4",download_update)
    else:
        click.secho("Invalid Input. Try using tv download --help",bg='red',fg='white')
@cli.command()
@config
def random(config):
    '''watch any random tv show and episode'''
    conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + '\\television.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM show ORDER BY RANDOM() LIMIT 1")
    r = cursor.fetchone()
    if(config.verbose):
        click.echo("Now watching: %s" % (r[4]))
    webbrowser.open_new_tab(r[0].strip('[]').replace("'",""))
@cli.group
@cli.command()
@click.argument('name',default='',metavar='[series]')
@click.argument('season',default='',metavar='[season]')
@click.argument('episode',default='',metavar='[episode]')
@config
def watch(config,name,season,episode):
    """ watch any television show"""
    if name and season and episode:
        conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + '\\television.db')
        cursor = conn.cursor()
        se = "%%Season %s Episode %s%%" % (season,episode)
        sn = name
        cursor.execute("SELECT episode_link_direct,name,episode_name FROM show WHERE episode_name LIKE ? AND name LIKE ?", (se,sn))
        r = cursor.fetchone()
        click.echo(r[0])
        if(config.verbose):
            click.echo("Now watching: %s %s" % (r[1],r[2]), bg='green',fg='white')
        webbrowser.open_new_tab(r[0].strip('[]').replace("'",""))
    else:
        click.secho("Invalid Input. Try using tv watch --help",bg='red',fg='white')
@cli.command()
@click.argument('name',metavar='[series]',required=True)
@click.argument('season',default='%',required=False,metavar="[season]")
@config
def list(config,name,season):
    """ explore any television show"""
    if config.verbose:
        click.echo("Now listing %s Season %s" % (name,season))
    conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + '\\television.db')
    series_name = "\"" + name + "\""
    season_name = season.replace("",'%% %%')
    click.echo()
    cursor = conn.cursor()
    for i,row in enumerate(cursor.execute("SELECT episode_name FROM show WHERE name LIKE %s AND episode_name LIKE \'%%Season %s %%\'" % (series_name,season))):
        click.echo(row[0].replace(u'\u2013','-').replace(u"\u2019", "'"))
        if i % 20 == 0 and i != 0:
            click.echo('Continue listing? [yn]', nl=False)
            c = click.getchar()
            click.echo()
            if c == 'y':
                click.secho("\nContinued",bg='green',fg='white')
                continue
            elif c == 'n':
                click.secho("\nTerminated",bg='red',fg='white')
                break
            else:
                click.secho("\nInvalid Input!",bg='red',fg='white')
                break
@cli.command()
@click.argument('series',required='true')
def update(series):
    ''' update database with new show and/or episodes '''
    import scrapy
    from scrapy.selector import Selector
    from scrapy.crawler import CrawlerProcess
    class SeriesUpdater(scrapy.Spider):
        name = "updater"
        series = None     
        start_urls=["http://stream-tv2.co/"]
        def __init__(self, *args, **kwargs):
            super(SeriesUpdater,self).__init__(*args,**kwargs)
            series = kwargs.get('series')
        def parse(self, response):
            sel = Selector(response)
            shows = response.xpath('//ul/li')
            names=dict()
            for show in shows:
                name = [s.encode('utf-8') for s in show.xpath('a/text()').extract()]
                link = show.xpath('a/@href').extract()
                names[str(name).decode('utf-8').strip('[]')]=link
            # search for series name
            for key, value in names.iteritems():
                if series in key.strip():
                  click.secho("\nFound %s" % str(key).strip('[]').encode('utf-8'),bg='green',fg='white')
                  click.echo('Shall we continue? [yn]', nl=False)
                  c = click.getchar()
                  click.echo()
                  if c == 'y':
                        click.secho("\nContinued",bg='green',fg='white')
                  elif c == 'n':
                        click.secho("\nTerminated",bg='red',fg='white')
                        break;
                  else:
                        click.secho("\nInvalid Input!",bg='red',fg='white')
                        break;
                  yield scrapy.Request(str(value[0]),meta={ 'root_link' : value, 'name' : str(key).strip('[]\'\'').encode('utf-8')},callback=self.parse_episodes,priority=200)
                  names.clear()
                  break;

        def parse_episodes(self,response):
            from lxml import html
            import requests
            conn = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + '\\television.db')
            cursor = conn.cursor()
            click.secho("\nGrabbing Episodes..",bg='green',fg='white')
            print str(response.meta['root_link']).strip('[]')
            episodes=response.xpath('//div[contains(@class,"entry")]//ul/li')
            for episode in episodes:
                 title = episode.xpath('a/text()').extract()
                 link = episode.xpath('a/@href').extract()
                 click.secho(title[0].replace(u'\u2013','-').strip('[]').replace(u"\u2019", "'"),bg='green',fg='white')
                 click.secho(link[0],bg='cyan',fg='white')
                 click.secho("Grabbing Direct Link",bg='red',fg='white')
                 if "http" not in link[0]: 
                    continue
                 try:
                    page = requests.get(link[0],allow_redirects=False)
                    tree = html.fromstring(page.text)
                    direct = tree.xpath('//div[contains(@class,"postTabs_divs postTabs_curr_div")]/iframe/@src')
                    click.echo('INSERT INTO show VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (direct,str(link[0].strip().decode('utf-8')),response.meta['root_link'],response.meta['name'],title[0]))
                    cursor.execute('INSERT INTO show VALUES(?,?,?,?,?);', (str(direct[0]).strip("'[]"),str(link[0].strip("'")),str(response.meta['root_link'][0]).strip("'").encode('utf-8'),str(response.meta['name']).strip("[]'").encode('utf-8'),str(title[0].replace(u'\u2013','-').strip('[]').replace(u"\u2019", "'"))))
                    conn.commit()
                 except Exception, e:
                    print e
                    continue

            click.echo(series)
            cursor.close()

    process = CrawlerProcess()
    process.crawl(SeriesUpdater(series='test'))
    process.start() 
@cli.command()
@click.argument('series',required='true')
@config
def info(config,series):
    """get a brief summary on any tv series"""
    import requests #lazy load because this is the only time we use the library
    payload = {'q': series}
    r = requests.get("http://api.tvmaze.com/singlesearch/shows",params=payload)
    jo = r.json()
    NUM_RE = re.compile(r'/(\d+)/')
    click.echo("Rating: %s" % NUM_RE.sub('',str(jo['rating']).encode('utf-8','ignore')))
    click.echo("Language: %s" % jo['language'])
    click.echo("Runtime: %s" % jo['runtime'])
    click.echo("Status: %s" % jo['status'])
    click.echo("Genre(s):")
    for genre in jo['genres']:
        click.echo("     o %s" % genre)

    TAG_RE = re.compile(r'<[^>]+>')
    click.echo(TAG_RE.sub('',"Summary: " + jo['summary']))
#Callback Functions
def download_update(count, blockSize, totalSize):
    click.echo("Now downloading... " + str(count*blockSize*100/totalSize) + "%")
