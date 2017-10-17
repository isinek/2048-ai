from random import randint
from pymongo import MongoClient

__mongo_client__ = MongoClient()
__2048_database__ = __mongo_client__.game_2048
__2048_moves_collection__ = __2048_database__.moves

while True:
	table = [[0, 0, 0, 0] for r in range(4)]
	n_tiles = randint(8, 16)
	while n_tiles:
		r, c, v = randint(0, 3), randint(0, 3), randint(1, 10)
		if not table[r][c]:
			table[r][c] = 2**v
			n_tiles -= 1

	print('*'*30)
	print('\n'.join(['\t'.join([[str(c), '_'][c == 0] for c in r]) for r in table]))
	choice = input()
	if choice == 'w':
		__2048_moves_collection__.insert({'generated': True, 'table': table, 'choice': 'U', 'n_choice': 1, 'cell_1_1': table[0][0], 'cell_1_2': table[0][1], 'cell_1_3': table[0][2], 'cell_1_4': table[0][3], 'cell_2_1': table[1][0], 'cell_2_2': table[1][1], 'cell_2_3': table[1][2], 'cell_2_4': table[1][3], 'cell_3_1': table[2][0], 'cell_3_2': table[2][1], 'cell_3_3': table[2][2], 'cell_3_4': table[2][3], 'cell_4_1': table[3][0], 'cell_4_2': table[3][1], 'cell_4_3': table[3][2], 'cell_4_4': table[3][3]})
	elif choice == 'd':
		__2048_moves_collection__.insert({'generated': True, 'table': table, 'choice': 'R', 'n_choice': 2, 'cell_1_1': table[0][0], 'cell_1_2': table[0][1], 'cell_1_3': table[0][2], 'cell_1_4': table[0][3], 'cell_2_1': table[1][0], 'cell_2_2': table[1][1], 'cell_2_3': table[1][2], 'cell_2_4': table[1][3], 'cell_3_1': table[2][0], 'cell_3_2': table[2][1], 'cell_3_3': table[2][2], 'cell_3_4': table[2][3], 'cell_4_1': table[3][0], 'cell_4_2': table[3][1], 'cell_4_3': table[3][2], 'cell_4_4': table[3][3]})
	elif choice == 's':
		__2048_moves_collection__.insert({'generated': True, 'table': table, 'choice': 'D', 'n_choice': 3, 'cell_1_1': table[0][0], 'cell_1_2': table[0][1], 'cell_1_3': table[0][2], 'cell_1_4': table[0][3], 'cell_2_1': table[1][0], 'cell_2_2': table[1][1], 'cell_2_3': table[1][2], 'cell_2_4': table[1][3], 'cell_3_1': table[2][0], 'cell_3_2': table[2][1], 'cell_3_3': table[2][2], 'cell_3_4': table[2][3], 'cell_4_1': table[3][0], 'cell_4_2': table[3][1], 'cell_4_3': table[3][2], 'cell_4_4': table[3][3]})
	elif choice == 'a':
		__2048_moves_collection__.insert({'generated': True, 'table': table, 'choice': 'L', 'n_choice': 4, 'cell_1_1': table[0][0], 'cell_1_2': table[0][1], 'cell_1_3': table[0][2], 'cell_1_4': table[0][3], 'cell_2_1': table[1][0], 'cell_2_2': table[1][1], 'cell_2_3': table[1][2], 'cell_2_4': table[1][3], 'cell_3_1': table[2][0], 'cell_3_2': table[2][1], 'cell_3_3': table[2][2], 'cell_3_4': table[2][3], 'cell_4_1': table[3][0], 'cell_4_2': table[3][1], 'cell_4_3': table[3][2], 'cell_4_4': table[3][3]})
	elif choice == 'exit':
		break