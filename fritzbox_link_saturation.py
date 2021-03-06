#!/usr/bin/env python
"""
  fritzbox_link_saturation - A munin plugin for Linux to monitor AVM Fritzbox
  WAN link saturation with QoS stats
  Copyright (C) 2019 Rene Walendy
  Author: Rene Walendy
  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0

  Add the following section to your munin-node's plugin configuration:

  [fritzbox_*]
  env.fritzbox_ip [ip address of the fritzbox]
  env.fritzbox_password [fritzbox password]
  env.fritzbox_user [fritzbox user, set any value if not required]

  This plugin supports the following munin configuration parameters:
  #%# family=auto contrib
  #%# capabilities=autoconf
"""

import os
import re
import sys
import json
import fritzbox_helper as fh

PAGE = 'internet/inetstat_monitor.lua'
PARAMS = {'useajax':1, 'action':'get_graphic', 'xhr':1, 'myXhr':1}
DATA_UP   = ['us_realtime_bps_curr', 'us_important_bps_curr', 'us_default_bps_curr', 'us_background_bps_curr']
LABELS_UP = ['realtime', 'high', 'default', 'low']
DATA_DN   = ['ds_bps_curr', 'ds_mc_bps_curr']
LABELS_DN = ['internet', 'iptv']

def average_bps(datapoints):
  avg = 0
  for d in datapoints:
    avg+=d
  avg = avg//len(datapoints)
  return avg

def print_link_saturation():
  """get the current DSL link saturation"""

  server = os.environ['fritzbox_ip']
  password = os.environ['fritzbox_password']
  user = os.environ['fritzbox_user']

  data = fh.get_page_with_login(server, user, password, PAGE, params=PARAMS)
  # all data is embedded in a one-element array, so strip that array away
  jsondata = json.loads(data)[0]

  # parse scientific notations of integers
  maxup = int(float(jsondata['upstream']))
  maxdown = int(float(jsondata['downstream']))

  print("multigraph saturation_up")
  for i in range(len(DATA_UP)):
    print('up_' + LABELS_UP[i] + '.value ' + str(average_bps(jsondata[DATA_UP[i]])))
  print("maxup.value " + str(maxup))
  print("multigraph saturation_down")
  for i in range(len(DATA_DN)):
    print('dn_' + LABELS_DN[i] + '.value ' + str(average_bps(jsondata[DATA_DN[i]])))
  print("maxdown.value " + str(maxdown))

def print_config():
  print("multigraph saturation_up")
  print("graph_title AVM Fritz!Box uplink saturation")
  print("graph_vlabel bits out per ${graph_period}")
  print("graph_category network")
  print("graph_args --base 1000 --lower-limit 0")
  print("graph_order " + ' '.join(LABELS_UP) + " maxdown")
  for l in LABELS_UP:
    print('up_' + l + '.label ' + l)
    print('up_' + l + '.type GAUGE')
    print('up_' + l + '.draw AREASTACK')
    print('up_' + l + '.cdef up_' + l + ',8,*')
  print("maxup.label MAX")
  print("maxup.type GAUGE")
  print("maxup.graph LINE1")

  print("multigraph saturation_down")
  print("graph_title AVM Fritz!Box downlink saturation")
  print("graph_vlabel bits in per ${graph_period}")
  print("graph_category network")
  print("graph_args --base 1000 --lower-limit 0")
  print("graph_order " + ' '.join(LABELS_DN) + " maxup")
  for l in LABELS_DN:
    print('dn_' + l + '.label ' + l)
    print('dn_' + l + '.type GAUGE')
    print('dn_' + l + '.draw AREASTACK')
    print('dn_' + l + '.cdef dn_' + l + ',8,*')
  print("maxdown.label MAX")
  print("maxdown.type GAUGE")
  print("maxdown.graph LINE1")

  if os.environ.get('host_name'):
      print("host_name " + os.environ['host_name'])


if __name__ == "__main__":
  if len(sys.argv) == 2 and sys.argv[1] == 'config':
    print_config()
  elif len(sys.argv) == 2 and sys.argv[1] == 'autoconf':
    print("yes")  # Some docs say it'll be called with fetch, some say no arg at all
  elif len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == 'fetch'):
    try:
      print_link_saturation()
    except:
      sys.exit("Couldn't retrieve fritzbox link saturation")
