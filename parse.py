# encoding: utf-8
#

import re
import localType
from localType import sourceUrl
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
from run import _tableName

engine = create_engine("sqlite://"+"/"+_tableName)
Session = sessionmaker(bind=engine)
session = Session()
urls = session.query(sourceUrl).filter().all()


notFound = list()
for individual in urls:
    url = individual._blog_url
    res = re.match('(.*(blog|post|blob|research|article|report|intelligence)[^/]*/)',str(url),re.I)
    if res != None:
        print res.group(1)
        individual._source_path = res.group(1)
    else:
        notFound.append(url)
        individual._source_path = 'Not Found'
print '\n\n'
for x  in  notFound:
    print 'NOT FOUND: '+x

session.commit()
session.close()
