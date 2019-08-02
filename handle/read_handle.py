import logging
from pyndn import Face, Name, Interest

class ReadHandle:
  def __init__(self, face, prefix):
    self.face = face
    self.prefix = prefix

  def listen(self):
    self.face.setInterestFilter(self.prefix, self.on_interest)

  def on_interest(self, _prefix, interest: Interest, face, _filter_id, _filter):
    name = interest.getName()