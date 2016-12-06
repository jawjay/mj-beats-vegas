from bs4 import BeautifulSoup
import urllib
import csv

def get_table(base_url,mid="schedule"):
    r = urllib.urlopen(base_url).read()
    bs = BeautifulSoup(r,"html.parser")
    table = bs.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id'] == mid) 
    # rows = table.findAll(lambda tag: tag.name=='tr')
    if not table:
        return []
    rows =  []
    for row in table.find_all('tr'):
        rows.append([val.text.encode('utf8').strip() for val in row.find_all('td')])
    headers = [header.text.encode('utf8').strip() for header in table.find_all('th')]
    headers = headers[9:]
    # rows = [row for row in rows if row]
    crows = [[h]+r for h,r in zip(headers,rows[1:]) if r]
    # return crows
    # for h in headers:
    #     print h
    # for i in zip(headers,rows[1:]):
        # print i
    return crows
def sched2csv(table,date,path=''):
    with open(path+date+'.csv','wb') as f:
        writer = csv.writer(f)
        #writer.writerow(headers)    
        writer.writerows(row for row in table if row)


    get_table('http://www.basketball-reference.com/leagues/NBA_2001_games-april.html')

def getAllSchedules2csv(years = range(2001,2017),months = range(9)):
    years = [str(x) for x in years]
    ms = ['october','november','december','january','february','march','april','may','june']
    months = [ms[i] for i in months]
    def getSchedURL(year,month):
        return 'http://www.basketball-reference.com/leagues/NBA_'+year+'_games-'+month+'.html'
    for y in years:
        print(y)
        for m in months:
            r = urllib.urlopen(getSchedURL(y,m)).read()
            bs = BeautifulSoup(r,"html.parser")
            sched2csv(get_table(getSchedURL(y,m)),y+m,'schedules/')           
# getAllSchedules2csv(range(2005,2017))

# sched2csv(get_table('http://www.basketball-reference.com/leagues/NBA_2005_games-october.html'),'now','schedules/')