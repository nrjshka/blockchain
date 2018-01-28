from block import Block

class Chain(object):

	def __init__(self, blocks):
		self.blocks = blocks

	def is_valid(self):
		for index, cur_blocks in enumerate(self.blocks[1:]):
			prev_block = self.blocks[index]

			if prev_block.index+1  != cur_blocks.index:
				return False
			
			if not cur_blocks.is_valid():
				return False

			if prev_block.hash != cur_blocks.prev_hash:
				return False
		
		return True

	def self_save(self):
		for b in self.blocks:
			b.self_save()

		return True

	def find_block_by_index(self, index):
		if len(self) <= index:
			return self.blocks[index]
		else:
			return False

	def find_block_by_hash(self, hash):
		for b in self.blocks:
			if b.hash == hash:
				return b
		return False

	def __len__(self):
		return len(self.blocks)

	def __eq__(self, other):
		if len(self) != len(other):
			return False
		
		for self_block, other_block in zip(self.blocks, other.blocks):
			if self_block != other_block:
				return False

		return True

	def __gt__(self, other):
		return len(self.blocks) > len(other.blocks)

	def __ge__(self, other):
		return self.__eq__(other) or self.__gt__(other)

	def max_index(self):
		return self.blocks[-1].index

	def add_block(self, new_blocks):
		self.blocks.append(new_blocks)
		return True

	def block_list_dict(self):
		return [b.to_dict() for b in self.blocks]

