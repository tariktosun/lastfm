# processing for last.fm data.
import glob
import json
import numpy as np

def load_data(directory):
    """ Loads all json data files in the directory. """
    full_data = []
    files = glob.glob(directory+"/*")
    for f in files:
        data = json.load(open(f))
        full_data += data[:]
    return full_data

def get_timeseries(data):
    """ Returns: (sid_timeseries, time_timeseries, sid_to_mbid, mbid_to_meta) """
    N = len(data)   # number of listens
    time_timeseries = [0]*N   # timeseries of times
    sid_timeseries = [0]*N    # song id timeseries
    mbid_to_meta = {}
    sid_to_mbid = ['']*N

    sid_count = 0
    skips = 0
    for i,d in enumerate(data):
        try:
            track = d['track']
            mbid = track['mbid']
            time = d['timestamp']['unixtimestamp']
        except:
            print str(i)
            skips +=1
            continue
        if time < 1e9:
            print str(i)
            skips += 1
            continue
        # check if this is a new mbid:
        if not mbid_to_meta.has_key(mbid):
            sid_count+=1
            sid_to_mbid[sid_count]=mbid
            metadata = {}
            metadata['name'] = track['name']
            metadata['artist'] = track['artist']
            metadata['sid'] = sid_count
            # store it:
            mbid_to_meta[mbid] = metadata
        this_sid = mbid_to_meta[mbid]['sid']
        sid_timeseries[i-skips] = this_sid
        time_timeseries[i-skips] = time
    # trim:
    sid_to_mbid = sid_to_mbid[0:sid_count+1]
    sid_timeseries = sid_timeseries[0:-skips]
    time_timeseries = time_timeseries[0:-skips]
    return (sid_timeseries, time_timeseries, sid_to_mbid, mbid_to_meta)

def get_bundles(time_timeseries, sid_timeseries):
    """ Returns: (sid_bundles, time_bundles) """
    # Create bundles:
    THRESH = 1800 # half an hour
    sid_bundles = [[] for _ in range(len(time_timeseries))]
    time_bundles = [[] for _ in range(len(time_timeseries))]
    i=-1
    last = -THRESH
    for time, sid in zip(time_timeseries, sid_timeseries):
        if time-last > THRESH:
            i+=1
        time_bundles[i].append(time)
        sid_bundles[i].append(sid)
        last = time
    # trim:
    sid_bundles  = sid_bundles[0:i+1]
    time_bundles = time_bundles[0:i+1]
    return (sid_bundles, time_bundles)

def get_binary(sid_bundles, P):
    """ P is number of features. returns NxP full np.array. """
    N = len(sid_bundles)
    #P = len(sid_to_mbid)

    binary = np.zeros((N,P))

    #Populate the matrix:
    for n,b in enumerate(sid_bundles):
        for sid in b:
            binary[n, sid] = 1
    return binary

