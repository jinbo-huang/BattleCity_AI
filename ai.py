import random
import time
import multiprocessing
import sys
import Queue

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
		#               up right down left
		self.dir_top =  [-1, 0,  1,   0]
		self.dir_left = [0, 1,  0,   -1]

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


			#q=0
			#for i in range(1000):
			#	q+=1

			self.encode_map(bullets, enemies, tiles, player)

			# print player

			# self.print_encoded_map()
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
			keep_action = 1

			# 1. check nearest 3 blocks in every direction ( bullet, tank )
			# get encoded player position
			encoded_player_left = player_left / 32
			encoded_player_top = player_top / 32

			
			# check for bullets
			for i in range(4):
				current_left = encoded_player_left
				current_top = encoded_player_top
				for j in range(3):
					current_left = current_left + self.dir_left[i]
					current_top = current_top + self.dir_top[i]
					if (current_left < 0 or current_left >= 13 or current_top < 0 or current_top >= 13):
						break
					if (self.encoded_map[current_top][current_left] == 'B'):
						# print "found bullet"
						self.Update_Strategy(c_control, 1, i, 1)
						continue


			# check for tanks
			for i in range(4):
				current_left = encoded_player_left
				current_top = encoded_player_top
				for j in range(3):
					current_left = current_left + self.dir_left[i]
					current_top = current_top + self.dir_top[i]
					if (current_left < 0 or current_left >= 13 or current_top < 0 or current_top >= 13):
						break
					if (self.encoded_map[current_top][current_left] == 'E'):
						# print "found tank"
						self.Update_Strategy(c_control, 1, i, 1)
						continue


			# 2. check if the position of player's tank is on the multiplier of 32

			# get player's direction
			player_dir = player[1]

			adjust_top = encoded_player_top * 32
			adjust_left = encoded_player_left * 32

			# print "player_top: %d,  player_left: %d" %(player_top, player_left)

			up
			if (player_top - adjust_top < 6):
				# print("adjust up")
				self.Update_Strategy(c_control, 0, 0, keep_action)
				continue
			
			# down
			elif (player_top - adjust_top < -6):
				# print("adjust down")
				self.Update_Strategy(c_control, 0, 2, keep_action)
				continue
			
			# left
			elif (player_left - adjust_left > 6):
				# print("adjust left")
				self.Update_Strategy(c_control, 0, 3, keep_action)
				continue
			
			# right
			elif (player_left - adjust_left < -6):
				# print("adjust right")
				self.Update_Strategy(c_control, 0, 1, keep_action)
				continue

			# if ((player_dir == 0 or player_dir == 2) and (player_top % 32 < 27 and player_top % 32 > 5)):
			# 	print "adjust top. player_top: %d,  player_left: %d" %(player_top, player_left)
			# 	self.Update_Strategy(c_control, 0, player_dir, keep_action)
			# 	continue
			# 
			# elif ((player_dir == 1 or player_dir == 3) and (player_left % 32 < 27 and player_left % 32 > 5)):
			# 	print "adjust left. player_top: %d,  player_left: %d" %(player_top, player_left)
			# 	self.Update_Strategy(c_control, 0, player_dir, keep_action)
			# 	continue

			#else
			#	if (


			# 3. BFS
			move = self.bfs()
			if (move == -1):
				self.Update_Strategy(c_control, 0, move_dir, keep_action)
			else:
				self.Update_Strategy(c_control, 0, move, keep_action)
			#keep_action = 0
			

			#-----------
			# self.Update_Strategy(c_control,shoot,move_dir,keep_action)
		#------------------------------------------------------------------------------------------------------

	def bfs(self):
		q = Queue.Queue()

		player_left = 0
		player_top = 0

		for i in range(self.map_height):
			for j in range(self.map_width):
				if (self.encoded_map[i][j] == 'P'):
					player_top = i
					player_left = j
					break

		visited = [[False for x in range(self.map_width)] for y in range(self.map_height)]
		
		visited[player_top][player_left] = True
		for i in range(4):
			new_top = player_top + self.dir_top[i]
			new_left = player_left + self.dir_left[i]
			if (new_left < 0 or new_left >= 13 or new_top < 0 or new_top >= 13):
				continue
			if (self.encoded_map[new_top][new_left] != '@'):
				q.put([new_top, new_left, i])
				visited[new_top][new_left] = True

		result_move = -1

		while not q.empty():
			temp = q.get()
			current_top = temp[0]
			current_left = temp[1]
			direction = temp[2]
			visited[current_top][current_left] = True

			if (self.encoded_map[current_top][current_left] == 'E'):
				# print "found enemy"
				result_move = direction
				return result_move

			for i in range(4):
				new_top = current_top + self.dir_top[i]
				new_left = current_left + self.dir_left[i]
				if (new_left < 0 or new_left >= 13 or new_top < 0 or new_top >= 13):
					continue
				if (visited[new_top][new_left] == False and self.encoded_map[new_top][new_left] != '@'):
					q.put([new_top, new_left, direction])

		return result_move

	def encode_map(self, bullets, enemies, tiles, player):
		result = [['_' for x in range(self.map_width)] for y in range(self.map_height)]

		for bullet in bullets:
			b_left = bullet[0][0] / 32
			b_top = bullet[0][1] / 32
			if (b_left < 0 or b_left >= 13 or b_top < 0 or b_top >= 13):
				continue;
			result[b_top][b_left] = 'B'

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

