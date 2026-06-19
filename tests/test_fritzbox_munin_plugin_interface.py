#!/usr/bin/env python3
"""
Unit tests for munin_plugin_interface module
"""

import os
import sys
import unittest
from unittest.mock import Mock
from fritzbox_munin_plugin_interface import main_handler, print_debug, MuninPluginInterface


class TestMainHandler:

  def test_main_handler_config(self, capsys): # pylint: disable=no-self-use
    mock_plugin = Mock(spec=MuninPluginInterface)
    sys.argv = ['plugin_name', 'config']

    main_handler(mock_plugin)

    mock_plugin.print_config.assert_called_once()
    mock_plugin.print_stats.assert_not_called()

  def test_main_handler_autoconf(self, capsys): # pylint: disable=no-self-use
    mock_plugin = Mock(spec=MuninPluginInterface)
    sys.argv = ['plugin_name', 'autoconf']

    main_handler(mock_plugin)

    assert capsys.readouterr().out == "yes\n"
    mock_plugin.print_config.assert_not_called()
    mock_plugin.print_stats.assert_not_called()

  def test_main_handler_fetch(self, capsys): # pylint: disable=no-self-use
    mock_plugin = Mock(spec=MuninPluginInterface)
    sys.argv = ['plugin_name', 'fetch']

    main_handler(mock_plugin)

    mock_plugin.print_stats.assert_called_once()
    mock_plugin.print_config.assert_not_called()

  def test_main_handler_no_args(self, capsys): # pylint: disable=no-self-use
    mock_plugin = Mock(spec=MuninPluginInterface)
    sys.argv = ['plugin_name']

    main_handler(mock_plugin)

    mock_plugin.print_stats.assert_called_once()
    mock_plugin.print_config.assert_not_called()

  def test_main_handler_exception_handling(self, capsys): # pylint: disable=no-self-use
    mock_plugin = Mock(spec=MuninPluginInterface)
    mock_plugin.print_stats.side_effect = RuntimeError("Test error")
    sys.argv = ['test_plugin.py', 'fetch']

    try:
      main_handler(mock_plugin)
      assert False, "Should have exited"
    except SystemExit as e:
      assert "Test error" in str(e)
      assert "test_plugin.py" in str(e) or "Mock" in str(e)


class TestPrintDebug:

  @unittest.mock.patch.dict(os.environ, {"MUNIN_DEBUG": "1"})
  def test_print_debug_with_env_var(self, capsys): # pylint: disable=no-self-use
    print_debug("Debug message")

    assert capsys.readouterr().out == "Debug message\n"

  @unittest.mock.patch.dict(os.environ, {}, clear=True)
  def test_print_debug_without_env_var(self, capsys): # pylint: disable=no-self-use
    print_debug("Debug message")

    assert capsys.readouterr().out == ""

  @unittest.mock.patch.dict(os.environ, {"MUNIN_DEBUG": "0"})
  def test_print_debug_with_env_var_false(self, capsys): # pylint: disable=no-self-use
    print_debug("Debug message")

    assert capsys.readouterr().out == ""

  @unittest.mock.patch.dict(os.environ, {"MUNIN_DEBUG": "1"})
  def test_print_debug_with_dict(self, capsys): # pylint: disable=no-self-use
    data = {"key": "value", "number": 42}
    print_debug(data)

    output = capsys.readouterr().out
    assert '"key": "value"' in output
    assert '"number": 42' in output

  @unittest.mock.patch.dict(os.environ, {"MUNIN_DEBUG": "1"})
  def test_print_debug_with_list(self, capsys): # pylint: disable=no-self-use
    data = [1, 2, 3, "test"]
    print_debug(data)

    output = capsys.readouterr().out
    assert "1" in output
    assert "test" in output
