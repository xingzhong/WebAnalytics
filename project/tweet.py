# -- Data Visual for BIA660 ------
# Visualize the twitter data
# Xingzhong Xu (xxu7@stevens.edus)
#
# the following stuff will be stored 
#   only if they are all available
# 1. username / screen_name
# 2. recent tweets 
# 3. geo location / time 
# data struct :
# {uid:
#   {   name:   screen_name, 
#       items:  [
#           (tid1, geo1, time1), 
#           ... , 
#           (tidn, geon, timen)
#           ]
#   }
# }
# --------------------------------

import tweepy
import pprint
import pickle
import time


def getFriendList(api, uid):
    # given a uid, list all his friends and followers' id
    friends = api.friends_ids(uid)
    followers = api.followers_ids(uid)
    users = list(set(friends) | set(followers))
    return users[1:15]


def recordTimeLine(api, data, uid):
    if data.has_key(uid):
        return 1
    print "getUser"
    user = api.get_user(uid)
    items = []
    if user.geo_enabled:
        print "getTimeline"
        timeline = api.user_timeline(uid)
        for tl in timeline:
            if tl.coordinates:
                coor = tl.coordinates['coordinates']
                print "getGeoCode ", coor
                res  = api.reverse_geocode(lat=coor[1], long=coor[0])
                country = res['result']['places'][0]['country']
                fname = res['result']['places'][0]['full_name']
                items.append( (uid, fname, country, tl.created_at) )
    data[uid] = {'name':user.screen_name, 'items':items}
    


def loadData(name='bia660.pkl'):
    try :
        pkl_file = open(name, 'rb')
    except IOError:
        return {}
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data
    
def saveData(data, name='bia660.pkl'):
    output = open(name, 'wb')
    pickle.dump(data, output)
    output.close()
    return 1
    

def thread(api, data, uid=99004419, depth=3):
    if depth < 0:
        return 1
    print '\t'*(3-depth), uid
    for i in getFriendList(api, uid):
        recordTimeLine(api, data, i)
        thread(api, data, i, depth-1)

def getLimit(api):
    limit = api.rate_limit_status()
    pp.pprint(limit)
    return limit['remaining_hits'] , limit['reset_time_in_seconds']

if __name__ == '__main__':
    print "Hello Stevens"
    # constant key/secret for twitter app
    consumer_key = "verwURhvFVTuojYVJykZQ"
    consumer_secret = "RQDgjMrlen8QdZJM90rK9zxvCtSlJXfU7I7YO2STELk"
    access_token = "26635865-5GyKYJD8oqteN7VvklzWE7Vtsssovorvo90P8izoc"
    access_token_secret = "kLZebpapNT9bQpCYXSoaJJojIpebukyNrjb8HSmVwA"

    # prepare the api
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    pp = pprint.PrettyPrinter(indent=2)
    
    while(1):
        data = loadData()
        try :
            thread(api, data)
        except tweepy.error.TweepError as e:
            print e
            remain, restart = getLimit(api)
            if remain < 1 :
                secs = restart - time.time()
                print "sleep %s s"%secs
                for i in range(100):
                    time.sleep(secs/500)
                    print "%s of 500 ..."%i              
                print "wakeup"
        finally:
            pp.pprint( data )
            saveData(data)
    





