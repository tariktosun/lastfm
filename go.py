import matplotlib.pyplot as plt
from process import *
full_data = load_data('json/scrobbles')
(sid_timeseries, time_timeseries, sid_to_mbid, mbid_to_meta) = get_timeseries(full_data)
(sid_bundles, time_bundles) = get_bundles(time_timeseries, sid_timeseries)
