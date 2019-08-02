import plyvel
import logging
from handle.notification_handle import NotificationHandle
from handle.read_handle import ReadHandle
from handle.sync_handle import SyncHandle
from pyndn import Face, Name, Interest
from pyndn.security import KeyChain

class DLedger:
  def __init__(self):
    self.prefix = None
    self.face = None
    self.keychain = None

    self.db = None

    self.read_handle = None
    self.sync_handle = None
    self.notification_handle = None

  def init_db(self):
    import os
    db_dir = os.path.expanduser('~/.dledger/')
    if not os.path.exists(db_dir):
      os.makedirs(db_dir)
    self.db = plyvel.DB(db_dir, create_if_missing=True)

  def init_network(self, prefix):
    self.prefix = prefix
    self.face = Face()
    self.keychain = KeyChain()
    self.face.setCommandSigningInfo(self.keychain, self.keychain.getDefaultCertificateName())
    self.face.registerPrefix(self.prefix, None, self.on_register_failed)

  def init_handles(self):
    self.read_handle = ReadHandle(self.face, self.prefix)
    self.read_handle.listen()
    self.sync_handle = SyncHandle(self.face, self.prefix)
    self.sync_handle.listen()
    self.notification_handle = NotificationHandle(self.face, self.prefix)
    self.notification_handle.listen()

  def gen_new_record(self):
    pass

  @staticmethod
  def on_register_failed(prefix):
    logging.error("Prefix registration failed: %s", prefix)

if __name__ == "__main__":
    ledger = DLedger()
    ledger.init_network(Name("/ndn/dledger"))
    ledger.init_db()