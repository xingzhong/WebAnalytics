import tweet as t
import pprint

print "hello"
pp = pprint.PrettyPrinter(indent=2)
data = t.loadData()
counter = 0
for k, y in data.iteritems():
    if len( y['items'] )>0:
        counter = counter + 1
        print k
        pp.pprint (y)
#pp.pprint( data )
print "%s in %s"%(counter, len(data))
