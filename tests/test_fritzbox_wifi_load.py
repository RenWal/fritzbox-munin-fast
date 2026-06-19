#!/usr/bin/env python3
"""
Unit tests for wifi_load module
"""

import os
import unittest
import pytest
from fritzbox_wifi_load import FritzboxWifiLoad, average_load
from fritzbox_interface import FritzboxInterface


@unittest.mock.patch.dict(os.environ, {
  "wifi_freqs": "24 5",
  "wifi_modes": "freqs neighbors"
})
@pytest.mark.parametrize("fixture_version", ["7530ax-7.80"], indirect=True)
class TestFritzboxWifiLoad:

  @unittest.mock.patch.dict(os.environ, {
    "wifi_modes": "INVALID"
  })
  def test_config_with_invalid_modes_only(self, fixture_version: str, capsys): # pylint: disable=unused-argument
    wifi_load = FritzboxWifiLoad(FritzboxInterface())
    wifi_load.print_config()

    assert capsys.readouterr().out == ""

  def test_config_both_modes(self, fixture_version: str, capsys): # pylint: disable=unused-argument
    wifi_load = FritzboxWifiLoad(FritzboxInterface())
    wifi_load.print_config()

    assert capsys.readouterr().out == """multigraph bandwidth_24ghz
graph_title WIFI 24GHz bandwidth usage
graph_vlabel percent
graph_category network
graph_args --lower-limit 0 --upper-limit 100 --rigid
graph_order 24ghz_recv 24ghz_send
24ghz_recv.label receive
24ghz_recv.type GAUGE
24ghz_recv.draw AREASTACK
24ghz_send.label send
24ghz_send.type GAUGE
24ghz_send.draw AREASTACK
multigraph neighbors_24ghz
graph_title WIFI 24GHz neighbor APs
graph_vlabel number of APs
graph_category network
graph_args --lower-limit 0
graph_order 24ghz_samechan 24ghz_otherchans
24ghz_samechan.label same channel
24ghz_samechan.type GAUGE
24ghz_samechan.draw AREASTACK
24ghz_otherchans.label other channels
24ghz_otherchans.type GAUGE
24ghz_otherchans.draw AREASTACK
multigraph bandwidth_5ghz
graph_title WIFI 5GHz bandwidth usage
graph_vlabel percent
graph_category network
graph_args --lower-limit 0 --upper-limit 100 --rigid
graph_order 5ghz_recv 5ghz_send
5ghz_recv.label receive
5ghz_recv.type GAUGE
5ghz_recv.draw AREASTACK
5ghz_send.label send
5ghz_send.type GAUGE
5ghz_send.draw AREASTACK
multigraph neighbors_5ghz
graph_title WIFI 5GHz neighbor APs
graph_vlabel number of APs
graph_category network
graph_args --lower-limit 0
graph_order 5ghz_samechan 5ghz_otherchans
5ghz_samechan.label same channel
5ghz_samechan.type GAUGE
5ghz_samechan.draw AREASTACK
5ghz_otherchans.label other channels
5ghz_otherchans.type GAUGE
5ghz_otherchans.draw AREASTACK
"""

  @unittest.mock.patch.dict(os.environ, {
    "wifi_modes": "freqs"
  })
  def test_config_freqs_only(self, fixture_version: str, capsys): # pylint: disable=unused-argument
    wifi_load = FritzboxWifiLoad(FritzboxInterface())
    wifi_load.print_config()

    output = capsys.readouterr().out
    assert "multigraph bandwidth_24ghz" in output
    assert "multigraph bandwidth_5ghz" in output
    assert "multigraph neighbors" not in output

  @unittest.mock.patch.dict(os.environ, {
    "wifi_modes": "neighbors"
  })
  def test_config_neighbors_only(self, fixture_version: str, capsys): # pylint: disable=unused-argument
    wifi_load = FritzboxWifiLoad(FritzboxInterface())
    wifi_load.print_config()

    output = capsys.readouterr().out
    assert "multigraph neighbors_24ghz" in output
    assert "multigraph neighbors_5ghz" in output
    assert "multigraph bandwidth" not in output

  @unittest.mock.patch.dict(os.environ, {
    "wifi_freqs": "24",
    "wifi_modes": "freqs"
  })
  def test_config_single_freq(self, fixture_version: str, capsys): # pylint: disable=unused-argument
    wifi_load = FritzboxWifiLoad(FritzboxInterface())
    wifi_load.print_config()

    output = capsys.readouterr().out
    assert "multigraph bandwidth_24ghz" in output
    assert "5ghz" not in output

  def test_print_stats_both_modes(self, fixture_version: str, capsys): # pylint: disable=unused-argument
    wifi_load = FritzboxWifiLoad(FritzboxInterface())
    wifi_load.print_stats()

    assert capsys.readouterr().out == """multigraph bandwidth_24ghz
24ghz_recv.value 72
24ghz_send.value 50
multigraph neighbors_24ghz
24ghz_samechan.value 3
24ghz_otherchans.value 1
multigraph bandwidth_5ghz
5ghz_recv.value 55
5ghz_send.value 40
multigraph neighbors_5ghz
5ghz_samechan.value 2
5ghz_otherchans.value 1
"""

  def test_average_load_calculation(self): # pylint: disable=no-self-use
    datapoints = ["45:23", "50:30", "55:25"]
    recv, send = average_load(datapoints)

    assert recv == 50  # (45+50+55)//3 = 150//3 = 50
    assert send == 26  # (23+30+25)//3 = 78//3 = 26
