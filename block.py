import hashlib
import os
import json
import datetime as date
from config import *

class Block(object):
	def __init__(self, dictionary):
		for key, value in dictionary.items():
			if key in BLOCK_VAR_CONVERSIONS:
				setattr(self, key, BLOCK_VAR_CONVERSIONS[key](value))
			else:
				setattr(self, key, value)

		if not hasattr(self, 'nonce'):
			self.nonce = "None"

		if not hasattr(self, 'hash'):
			self.hash = self.create_self_hash()

	def header_string(self):
		return str(self.index) + self.prev_hash + self.data + str(self.timestamp) + str(self.nonce)

	def generate_header(self, index, prev_hash, data, timestamp, nonce):
		return str(index) + prev_hash + data + str(timestamp) + str(nonce)

	def update_self_hash(self):
		sha = hashlib.sha256()
		sha.update(self.header_string().encode('utf-8'))
		self.hash = sha.hexdigest()
		return self.hash

	def create_self_hash(self):
		sha = hashlib.sha256()
		sha.update(self.header_string())
		return sha.hexdigest()

	def self_save(self):
		chaindata_dir = 'chaindata'
		index_string = str(self.index).zfill(6)
		filename = '%s/%s.json' % (chaindata_dir, index_string) 
		with open(filename, 'w') as block_file:
			json.dump(self.__dict__(), block_file)

	def is_valid(self):
		self.update_self_hash()
		return str(self.hash[0 : NUM_ZEROS]) == '0' * NUM_ZEROS

	def __repr__(self):
		return "Block<index: %s>, <hash: %s>" % (self.index, self.hash)

	def __eq__(self, other):
		return ( self.index == other.index and 
				 self.timestamp  == other.timestamp  and
				 self.prev_hash  == other.prev_hash  and
				 self.hash  == other.hash  and
				 self.nonce  == other.nonce  and
				 self.data  == other.data
			    )

	def __ne__(self, other):
		return not self.__eq__(other)

	def __dict__(self):
		info = {}
		info['index'] = str(self.index)
		info['timestamp'] = str(self.timestamp)
		info['prev_hash'] = str(self.prev_hash)
		info['hash'] = str(self.hash)
		info['nonce'] = str(self.nonce)
		info['data'] = str(self.data)

		return info

	def __str__(self):
		return "Block<prev_hash: %s, hash : %s" % (self.prev_hash, self.hash)

def create_first_block():
	block_data = {}
	block_data['index'] = 0
	block_data['timestamp'] = date.datetime.now()
	block_data['data'] = 'First block data'
	block_data['prev_hash'] = ""
	block_data['nonce'] = 0
	block = Block(block_data)

	return block

if __name__ == '__main__':
	chaindata_dir = 'chaindata'

	if not os.path.exists(chaindata_dir):
		os.mkdir(chaindata_dir)

	if os.listdir(chaindata_dir) == []:

		first_block = create_first_block()
		first_block.self_save()
