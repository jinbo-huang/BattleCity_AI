import random
import time
import multiprocessing
import sys

class ai_agent():
	mapinfo = []
	encoded_map = []
	#map_width = 0
	#map_height = 0

	def __init__(self):
		self.mapinfo = []
		self.encoded_map = []
		self.map_width = 13
		self.map_height = 13
	# rect:					[left, top, width, height]
	# rect_type:			0:empty 1:brick 2:steel 3:water 4:grass 5:froze
	# castle_rect:			[12*16, 24*16, 32, 32]
	# mapinfo[0]: 			bullets [rect, direction, speed]]
	# mapinfo[1]: 			enemies [rect, direction, speed, type]]
	# enemy_type:			0:TYPE_BASIC 1:TYPE_FAST 2:TYPE_POWER 3:TYPE_ARMOR
	# mapinfo[2]: 			tile 	[rect, type] (empty don't be stored to mapinfo[2])
	# mapinfo[3]: 			player 	[rect, direction, speed, Is_shielded]]
	# shoot:				0:none 1:shoot
	# move_dir:				0:Up 1:Right 2:Down 3:Left 4:None
	# keep_action:			0:The tank work only when you Update_Strategy. 	1:the tank keep do previous action until new Update_Strategy.

	# def Get_mapInfo:		fetch the map infomation
	# def Update_Strategy	Update your strategy


			
			
	def operations (self,p_mapinfo,c_control):	

		while True:
		#-----your ai operation,This code is a random strategy,please design your ai !!-----------------------			
			self.Get_mapInfo(p_mapinfo)

			bullets = self.mapinfo[0]
			enemies = self.mapinfo[1]
			tiles = self.mapinfo[2]
			player = self.mapinfo[3][0]
			player_left = player[0][0]
			player_top = player[0][1]

			self.encode_map(bullets, enemies, tiles, player)

			self.print_encoded_map()
			# raw_input()
			#print "player left:%s" %(player_left)
			#print "player top:%s" %(player_top)

			# print self.mapinfo[0]
			# time.sleep(0.001)	
			
			#q=0
			#for i in range(10000000):
			#	q+=1
			
			shoot = random.randint(0,1)
			move_dir = random.randint(0,4)
			#keep_action = 0
			keep_action = 1
			#-----------
			self.Update_Strategy(c_control,shoot,move_dir,keep_action)
		#------------------------------------------------------------------------------------------------------


	def encode_map(self, bullets, enemies, tiles, player):
		result = [['_' for x in range(self.map_width)] for y in range(self.map_height)]

		for bullet in bullets:
			b_left = bullet[0][0]
			b_top = bullet[0][1]
			result[b_top / 32][b_left / 32] = 'B'

		for enemy in enemies:
			e_left = enemy[0][0]
			e_top = enemy[0][1]
			result[e_top / 32][e_left / 32] = 'E'

		for tile in tiles:
			t_left = tile[0][0]
			t_top = tile[0][1]
			t_type = tile[1]
			if (t_type == 1 or t_type == 2):
				result[t_top / 32][t_left / 32] = '@'
	
		player_left = player[0][0]
		player_top = player[0][1]

		result[player_top / 32][player_left / 32] = 'P'
		
		self.encoded_map = result

	def print_encoded_map(self):
		for i in range(13):
			for j in range(13):
				sys.stdout.write(self.encoded_map[i][j])
			sys.stdout.write("\n")

	def Get_mapInfo(self,p_mapinfo):
		if p_mapinfo.empty()!=True:
			try:
				self.mapinfo = p_mapinfo.get(False)
			except Queue.Empty:
				skip_this=True

	def Update_Strategy(self,c_control,shoot,move_dir,keep_action):
		if c_control.empty() ==True:
			c_control.put([shoot,move_dir,keep_action])
			return True
		else:
			return False

