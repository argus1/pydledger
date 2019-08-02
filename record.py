from pyndn import Data, Name, Signature, KeyLocator, Sha256WithEcdsaSignature, Sha256WithRsaSignature
from pyndn.security import KeyChain, SigningInfo

class DRecord:
  def __init__(self):
    self.data = None
    self.key = None
    self.producer = None
    self.endorse_count = 0
    self.approvers = None

  def from_data(self, record_data):
    self.data = record_data
    self.key = self.data.getName().toUri()
    sig = self.data.getSignature()
    if isinstance(sig, Sha256WithEcdsaSignature) or isinstance(sig, Sha256WithRsaSignature):
      self.producer = sig.getKeyLocator().getKeyName().getPrefix(-2).toUri()
    self.endorse_count = 0
    self.approvers = set()

  def get_preceding_record_keys(self):
    pass

if __name__ == "__main__":
  data = Data()
  data.setName(Name("/test/my/data"))
  keychain = KeyChain()
  keychain.signByIdentity(data, Name("/example"))
  record = DRecord()
  record.from_data(data)
  print(record.producer)