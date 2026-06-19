import os

from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation
from fritzconnection.lib.fritzstatus import FritzStatus


# pylint: disable=too-few-public-methods
class FritzboxConfig:
  """the server address of the Fritzbox (ip or name)"""
  server = "fritz.box"
  """the port the Fritzbox webserver runs on"""
  port = None  # defaults to 80 for use_tls=False, 443 for use_tls=True
  """the user name to log into the Fritzbox webinterface"""
  user = ""
  """the password to log into the Fritzbox webinterface"""
  password = ""
  use_tls = True
  certificate_file = False
  timeout = 60

  def __init__(self):
    if os.getenv('fritzbox_ip'):
      self.server = str(os.getenv('fritzbox_ip'))
    if os.getenv('fritzbox_port'):
      self.port = int(os.getenv('fritzbox_port'))

    user_env = os.getenv('fritzbox_user')
    password_env = os.getenv('fritzbox_password')

    if user_env is None or user_env == 'None':
      raise ValueError("fritzbox_user environment variable must be set")
    if password_env is None or password_env == 'None':
      raise ValueError("fritzbox_password environment variable must be set")

    self.user = str(user_env)
    self.password = str(password_env)

    if os.getenv('fritzbox_certificate') and os.path.isfile(os.getenv('fritzbox_certificate')):
      self.certificate_file = str(os.getenv('fritzbox_certificate'))
    elif os.path.isfile(str(os.getenv('MUNIN_CONFDIR')) + '/box.cer'):
      self.certificate_file = str(os.getenv('MUNIN_CONFDIR')) + '/box.cer'
    if os.getenv('fritzbox_use_tls'):
      self.use_tls = str(os.getenv('fritzbox_use_tls')) == 'true'


def create_fritz_connection() -> FritzConnection:
  config = FritzboxConfig()
  return FritzConnection(address=config.server, user=config.user, password=config.password, use_tls=config.use_tls, timeout=config.timeout)


def create_fritz_status() -> FritzStatus:
  config = FritzboxConfig()
  return FritzStatus(address=config.server, user=config.user, password=config.password, use_tls=config.use_tls, timeout=config.timeout)


def create_fritz_homeautomation() -> FritzHomeAutomation:
  config = FritzboxConfig()
  return FritzHomeAutomation(address=config.server, user=config.user, password=config.password, use_tls=config.use_tls)
