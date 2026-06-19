#!/usr/bin/env python3
"""
  Handling FRITZ!Box file sessions
"""

import fcntl
import os
import time
from typing import Optional, IO


def get_session_dir() -> str:
  return str(os.getenv('MUNIN_PLUGSTATE')) + '/fritzbox'


class FritzboxFileSession:
  __separator = "__"
  __server = ""
  __user = ""
  __port = None

  def __init__(self, server: str, user: str, port: int):
    if self.__separator in server or self.__separator in user:
      raise ValueError(f'Reserved string "{self.__separator}" in server or user name')

    self.__server = server
    self.__user = user
    self.__port = port

  def __get_session_filename(self) -> str:
    return self.__server + self.__separator + str(self.__port) + self.__separator + self.__user + '.sid'

  def _acquire_lock(self, file_obj: IO, timeout: float = 2.0) -> None:
    """Acquire an exclusive lock on the file with timeout."""
    start = time.time()
    while True:
      try:
        fcntl.flock(file_obj.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        return
      except BlockingIOError:
        if time.time() - start >= timeout:
          raise TimeoutError(f"Could not acquire lock on session file within {timeout} seconds")
        time.sleep(0.01)  # 10ms between retries

  def save(self, session_id):
    statedir = get_session_dir()
    os.makedirs(statedir, mode=0o700, exist_ok=True)

    statefilename = statedir + '/' + self.__get_session_filename()

    fd = os.open(statefilename, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w', encoding='utf8') as statefile:
      self._acquire_lock(statefile)
      statefile.write(session_id)

  def load(self) -> Optional[str]:
    statefilename = get_session_dir() + '/' + self.__get_session_filename()
    if not os.path.exists(statefilename):
      return None

    with open(statefilename, 'r', encoding='utf8') as statefile:
      self._acquire_lock(statefile)
      session_id = statefile.readline()
      return session_id

  def clear(self):
    filename = get_session_dir() + '/' + self.__get_session_filename()
    try:
      fd = os.open(filename, os.O_RDONLY)
      with os.fdopen(fd, 'r') as statefile:
        self._acquire_lock(statefile)
        os.remove(filename)
    except FileNotFoundError:
      pass
