from scene import *
import sound, random

img_path = 'img/'
block = ['blk1.PNG', 'blk2.PNG', 'blk3.PNG', 'blk4.PNG', 'blk5.PNG']
selected_block = ['blk1-2.PNG', 'blk2-2.PNG', 'blk3-2.PNG', 'blk4-2.PNG', 'blk5-2.PNG']

class Block (SpriteNode):
	def __init__(self, img1, img2, **kwargs):
		SpriteNode.__init__(self, img_path + img1, **kwargs)
		self.img_name = img1
		self.img_select = img2
		
class Star (SpriteNode):
	def __init__(self, **kwargs):
		SpriteNode.__init__(self, img_path + 'star.PNG', **kwargs)

class Game (Scene):
	def setup(self):
		self.background_color = '#000000'
		# self.background_img = SpriteNode('background.jpeg', position=(self.size.w / 2, self.size.h / 2), parent=self)
		# self.bgm = sound.play_effect('Lullaby.mp3', looping=True)
		self.push_botton = LabelNode('P   U   S   H', ('Futura', 30), parent=self)
		self.push_botton.position = (self.size.w / 2, 30)
		self.push_botton.color = '#ffffff'
		self.lines = [[] for _ in range(3)]
		self.selected = [0, 0, 0]
		self.to_move = []
		self.frame_count = 1
		self.score = 1
		for _ in range(3):
			self.update_down_block()
		
	def update(self):
		if len(self.to_move) > 1:
			if self.to_move[0] != self.to_move[1]:
				self.move_block(self.to_move[0], self.to_move[1])
			self.to_move = []
		if self.frame_count % 200 == 0:
			self.update_down_block()
			self.frame_count = 0
		self.frame_count += 1
		self.update_score()
		self.update_texture()
		self.update_block_position()

	def update_block_position(self):
		for i in range(len(self.lines)):
			for j in range(len(self.lines[i])):
				self.lines[i][j].position = (self.size.w/2 + 160 * (i - 1), self.size.h - (40 + 75 * j))

	def update_texture(self):
		for i in range(len(self.lines)):
			if len(self.lines[i]) > 0:
				if self.selected[i]:
					self.lines[i][-1].texture = Texture(img_path + self.lines[i][-1].img_select)
				else:
					self.lines[i][-1].texture = Texture(img_path + self.lines[i][-1].img_name)

	def update_down_block(self):
		for i in range(len(self.lines)):
			to_select = [i for i in range(len(block))]
			if len(self.lines[i]) > 1 and self.lines[i][0].img_name == self.lines[i][1].img_name:
				idx = block.index(self.lines[i][0].img_name)
				to_select.remove(idx)
			n = random.choice(to_select)
			self.lines[i].insert(0, Block(block[n], selected_block[n], parent=self))

	def update_score(self):
		if self.score % 10 == 0:
			star = Star(parent=self)
			star.position = (30, self.size.h - 30 * (self.score // 10))

	def move_block(self, before, after):
		if len(self.lines[before]) > 0:
			move_block = self.lines[before].pop()
			self.lines[after].append(move_block)
		self.selected = [0, 0, 0]
		if len(self.lines[after]) < 3: return
		if self.lines[after][-1].img_name != self.lines[after][-2].img_name: return
		if self.lines[after][-2].img_name != self.lines[after][-3].img_name: return
		for i in range(3):
			block = self.lines[after].pop()
			block.remove_from_parent()
		self.score += 1

	def touch_began(self, touch):
		left_side = self.size.w / 2 - 240
		if touch.location.y > 50:
			for i in range(len(self.lines)):
				if left_side + i * 160 <= touch.location.x < left_side + (i + 1) * 160:
					if len(self.lines[i]) == 0:
						if len(self.to_move) > 0:
							self.to_move.append(i)
					else:
						self.selected[i] = self.selected[i] ^ 1
						self.to_move.append(i)
		elif left_side <= touch.location.x < left_side + 480:
			self.update_down_block()

if __name__ == '__main__':
	run(Game(), show_fps=False)
