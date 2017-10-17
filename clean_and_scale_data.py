from sys import argv
from pymongo import MongoClient

__mongo_client__ = MongoClient()
__2048_database__ = __mongo_client__.game_2048
__2048_moves_collection__ = __2048_database__.moves
__2048_scaled_moves_collection__ = __2048_database__.scaled_moves

def rotate(table, choice):
	rot_table = [[0, 0, 0, 0] for _ in range(4)]
	for i in range(4):
		for j in range(4):
			rot_table[j][-i-1] = table[i][j]
	if choice == 'U':
		return [table, 'R', 2]
	elif choice == 'R':
		return [table, 'D', 3]
	elif choice == 'D':
		return [table, 'L', 4]
	elif choice == 'L':
		return [table, 'U', 1]

def main(rotate_table, scale):
	collection_data = list(__2048_moves_collection__.find())
	__2048_scaled_moves_collection__.remove({ '_id': { '$ne': -1 } })
	prev_x = collection_data[0]
	for xi in range(len(collection_data)):
		x = collection_data[xi]
		same = True
		max_val = 0
		for i in range(4):
			for j in range(4):
				if xi > 0 and x['table'][i][j] != prev_x['table'][i][j]:
					same = False
				if x['table'][i][j] > max_val:
					max_val = x['table'][i][j]
		if xi > 0 and same:
			print(prev_x)
			__2048_moves_collection__.remove({ '_id': prev_x['_id'] });
		else:
			table = [[int(c) for c in r] for r in x['table'][:]]
			choice = str(x['choice'])
			n_choice = int(x['n_choice'])
			game_id = str(x['game_id'])
			for _ in range(4):
				scaled_object = { 'table': table, 'choice': choice, 'n_choice': n_choice, 'game_id': game_id, 'generated': True }
				for i in range(4):
					for j in range(4):
						if scale:
							scaled_object['table'][i][j] /= max_val
						scaled_object['cell_' + str(i) + '_' + str(j)] = scaled_object['table'][i][j]
				__2048_scaled_moves_collection__.insert_one(scaled_object)
				if not rotate_table:
					break
				table, choice, n_choice = rotate(table, choice)
		prev_x = x

if __name__ == "__main__":
	main('-r' in argv, '-s' in argv)