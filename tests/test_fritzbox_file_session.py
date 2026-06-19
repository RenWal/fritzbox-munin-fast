#!/usr/bin/env python3
"""
Unit tests for file_session module
"""

import os
import stat
import tempfile
import shutil
import unittest
import pytest
from fritzbox_file_session import FritzboxFileSession, get_session_dir


class TestFritzboxFileSession:

  @unittest.mock.patch.dict(os.environ, {
    "MUNIN_PLUGSTATE": tempfile.gettempdir() + "/test_munin_state"
  })
  def test_save_and_load(self): # pylint: disable=no-self-use
    session = FritzboxFileSession("fritz.box", "testuser", 443)
    test_session_id = "1234567890ABCDEF"

    if os.path.exists(get_session_dir()):
      shutil.rmtree(get_session_dir())

    session.save(test_session_id)
    loaded_session = session.load()

    assert loaded_session == test_session_id

    shutil.rmtree(get_session_dir())

  @unittest.mock.patch.dict(os.environ, {
    "MUNIN_PLUGSTATE": tempfile.gettempdir() + "/test_munin_state"
  })
  def test_load_nonexistent_returns_none(self): # pylint: disable=no-self-use
    session = FritzboxFileSession("fritz.box", "testuser", 443)

    if os.path.exists(get_session_dir()):
      shutil.rmtree(get_session_dir())

    loaded_session = session.load()
    assert loaded_session is None

  @unittest.mock.patch.dict(os.environ, {
    "MUNIN_PLUGSTATE": tempfile.gettempdir() + "/test_munin_state"
  })
  def test_clear_when_file_exists(self): # pylint: disable=no-self-use
    session = FritzboxFileSession("fritz.box", "testuser", 443)
    test_session_id = "1234567890ABCDEF"

    if os.path.exists(get_session_dir()):
      shutil.rmtree(get_session_dir())

    session.save(test_session_id)
    assert session.load() == test_session_id

    session.clear()
    assert session.load() is None

    if os.path.exists(get_session_dir()):
      shutil.rmtree(get_session_dir())

  @unittest.mock.patch.dict(os.environ, {
    "MUNIN_PLUGSTATE": tempfile.gettempdir() + "/test_munin_state"
  })
  def test_clear_when_file_missing(self): # pylint: disable=no-self-use
    session = FritzboxFileSession("fritz.box", "testuser", 443)

    if os.path.exists(get_session_dir()):
      shutil.rmtree(get_session_dir())

    session.clear()

  def test_server_with_double_underscore_raises(self): # pylint: disable=no-self-use
    with pytest.raises(ValueError, match='Reserved string'):
      FritzboxFileSession("fritz__box", "testuser", 443)

  def test_user_with_double_underscore_raises(self): # pylint: disable=no-self-use
    with pytest.raises(ValueError, match='Reserved string'):
      FritzboxFileSession("fritz.box", "test__user", 443)

  @unittest.mock.patch.dict(os.environ, {
    "MUNIN_PLUGSTATE": tempfile.gettempdir() + "/test_munin_state"
  })
  def test_different_ports_different_files(self): # pylint: disable=no-self-use
    session_80 = FritzboxFileSession("fritz.box", "testuser", 80)
    session_443 = FritzboxFileSession("fritz.box", "testuser", 443)

    if os.path.exists(get_session_dir()):
      shutil.rmtree(get_session_dir())

    session_80.save("SESSION_80")
    session_443.save("SESSION_443")

    assert session_80.load() == "SESSION_80"
    assert session_443.load() == "SESSION_443"

    shutil.rmtree(get_session_dir())

  @unittest.mock.patch.dict(os.environ, {
    "MUNIN_PLUGSTATE": tempfile.gettempdir() + "/test_munin_state"
  })
  def test_secure_permissions(self): # pylint: disable=no-self-use
    session = FritzboxFileSession("fritz.box", "testuser", 443)
    test_session_id = "1234567890ABCDEF"

    if os.path.exists(get_session_dir()):
      shutil.rmtree(get_session_dir())

    session.save(test_session_id)

    # Verify directory has 0o700 permissions (owner-only access)
    dir_stat = os.stat(get_session_dir())
    dir_mode = stat.S_IMODE(dir_stat.st_mode)
    assert dir_mode == 0o700, f"Directory has permissions {oct(dir_mode)}, expected 0o700"

    # Verify session file has 0o600 permissions (owner read/write only)
    session_file = get_session_dir() + '/' + session._FritzboxFileSession__get_session_filename()
    file_stat = os.stat(session_file)
    file_mode = stat.S_IMODE(file_stat.st_mode)
    assert file_mode == 0o600, f"File has permissions {oct(file_mode)}, expected 0o600"

    shutil.rmtree(get_session_dir())
