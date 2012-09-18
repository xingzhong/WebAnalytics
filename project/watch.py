import tweet as t
import pprint

print "hello"
pp = pprint.PrettyPrinter(indent=2)
data = t.loadData()
for k, y in data.iteritems():
    if len( y['items'] )>0:
        print k
        pp.pprint (y)
#pp.pprint( data )
print len(data)