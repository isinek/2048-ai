from sys import argv
from time import sleep
import uuid
import numpy
import pandas
import pickle
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

__mongo_client__ = MongoClient()
__2048_database__ = __mongo_client__.game_2048
__2048_moves_collection__ = __2048_database__.moves
__2048_scaled_moves_collection__ = __2048_database__.scaled_moves
__2048_results_collection__ = __2048_database__.results

def is_game_over(driver):
	game_over = True
	try:
		driver.find_element_by_css_selector('div.game-over')
	except:
		game_over = False
	return game_over

def parse_table_from_page(driver, scaled):
	html_tile_container = driver.find_element_by_css_selector('div.tile-container')
	html_tiles = html_tile_container.find_elements_by_css_selector('div.tile')
	tiles = [[0 for _ in range(4)] for _ in range(4)]
	max_val = 0
	for tile in html_tiles:
		classes = tile.get_attribute('class').split()
		tiles[int(classes[2].split('-')[3])-1][int(classes[2].split('-')[2])-1] = int(classes[1].split('-')[1])
		if int(classes[1].split('-')[1]) > max_val:
			max_val = int(classes[1].split('-')[1])
	if scaled:
		for i in range(4):
			for j in range(4):
				tiles[i][i] /= max_val
	return tiles

def print_table(table):
	print('\n'.join(['\t'.join([str(value) for value in row]) for row in table]), '\n')

def up(driver):
	actions = ActionChains(driver)
	actions.send_keys(Keys.ARROW_UP)
	actions.perform()

def right(driver):
	actions = ActionChains(driver)
	actions.send_keys(Keys.ARROW_RIGHT)
	actions.perform()

def down(driver):
	actions = ActionChains(driver)
	actions.send_keys(Keys.ARROW_DOWN)
	actions.perform()

def left(driver):
	actions = ActionChains(driver)
	actions.send_keys(Keys.ARROW_LEFT)
	actions.perform()

def main(manual, scaled, shuffle, number_of_repeats, pickled_classifier):
	while number_of_repeats != 0:
		driver = webdriver.Chrome()
		driver.get('http://2048game.com/')
		game_id = str(uuid.uuid4())
		pickle_file = None
		classifier = None
		if not manual:
			if not pickled_classifier is None:
				pickle_file = open(pickled_classifier, 'rb')
			if pickle_file is None:
				if scaled:
					collection_data = __2048_scaled_moves_collection__.find()
				else:
					collection_data = __2048_moves_collection__.find()
				df = pandas.DataFrame(list(collection_data))
				df.drop(['_id', 'table', 'choice', 'game_id'], 1, inplace=True)
				if 'generated' in df:
					df.drop(['generated'], 1, inplace=True)
				if shuffle:
					df = df.sample(frac=1)
				x_train, x_test, y_train, y_test = cross_validation.train_test_split(numpy.array(df.drop(['n_choice'], 1).values), numpy.array(df['n_choice'].values), test_size=0.2)
				
				if number_of_repeats%2:
					classifier = RandomForestClassifier()
				else:
					classifier = LogisticRegression()

				classifier.fit(x_train, y_train)
				score = classifier.score(x_test, y_test)
				print('Prediction score:', score)
			else:
				classifier = pickle.load(pickle_file)
		last_table = None
		illegal_choices = 0
		move_counter = 0
		while not is_game_over(driver):
			table = parse_table_from_page(driver, scaled)
			if not manual:
				# print_table(table)
				choice = classifier.predict(numpy.array(table).reshape(1, -1))
				if table == last_table:
					illegal_choices += 1
				else:
					illegal_choices = 0
				if illegal_choices == 1:
					choice = 3
				elif illegal_choices == 2:
					choice = 2
				elif illegal_choices == 3:
					choice = 4
				elif illegal_choices == 4:
					choice = 1
				elif illegal_choices > 4:
					break
				
				#print(choice)
				if choice == 1:
					up(driver)
				elif choice == 2:
					right(driver)
				elif choice == 3:
					down(driver)
				elif choice == 4:
					left(driver)
				last_table = table
				sleep(.05)
			else:
				choice = input()
				if choice == 'w':
					up(driver)
					__2048_moves_collection__.insert({'game_id': game_id, 'table': table, 'choice': 'U', 'n_choice': 1, 'cell_1_1': table[0][0], 'cell_1_2': table[0][1], 'cell_1_3': table[0][2], 'cell_1_4': table[0][3], 'cell_2_1': table[1][0], 'cell_2_2': table[1][1], 'cell_2_3': table[1][2], 'cell_2_4': table[1][3], 'cell_3_1': table[2][0], 'cell_3_2': table[2][1], 'cell_3_3': table[2][2], 'cell_3_4': table[2][3], 'cell_4_1': table[3][0], 'cell_4_2': table[3][1], 'cell_4_3': table[3][2], 'cell_4_4': table[3][3]})
				elif choice == 'd':
					right(driver)
					__2048_moves_collection__.insert({'game_id': game_id, 'table': table, 'choice': 'R', 'n_choice': 2, 'cell_1_1': table[0][0], 'cell_1_2': table[0][1], 'cell_1_3': table[0][2], 'cell_1_4': table[0][3], 'cell_2_1': table[1][0], 'cell_2_2': table[1][1], 'cell_2_3': table[1][2], 'cell_2_4': table[1][3], 'cell_3_1': table[2][0], 'cell_3_2': table[2][1], 'cell_3_3': table[2][2], 'cell_3_4': table[2][3], 'cell_4_1': table[3][0], 'cell_4_2': table[3][1], 'cell_4_3': table[3][2], 'cell_4_4': table[3][3]})
				elif choice == 's':
					down(driver)
					__2048_moves_collection__.insert({'game_id': game_id, 'table': table, 'choice': 'D', 'n_choice': 3, 'cell_1_1': table[0][0], 'cell_1_2': table[0][1], 'cell_1_3': table[0][2], 'cell_1_4': table[0][3], 'cell_2_1': table[1][0], 'cell_2_2': table[1][1], 'cell_2_3': table[1][2], 'cell_2_4': table[1][3], 'cell_3_1': table[2][0], 'cell_3_2': table[2][1], 'cell_3_3': table[2][2], 'cell_3_4': table[2][3], 'cell_4_1': table[3][0], 'cell_4_2': table[3][1], 'cell_4_3': table[3][2], 'cell_4_4': table[3][3]})
				elif choice == 'a':
					left(driver)
					__2048_moves_collection__.insert({'game_id': game_id, 'table': table, 'choice': 'L', 'n_choice': 4, 'cell_1_1': table[0][0], 'cell_1_2': table[0][1], 'cell_1_3': table[0][2], 'cell_1_4': table[0][3], 'cell_2_1': table[1][0], 'cell_2_2': table[1][1], 'cell_2_3': table[1][2], 'cell_2_4': table[1][3], 'cell_3_1': table[2][0], 'cell_3_2': table[2][1], 'cell_3_3': table[2][2], 'cell_3_4': table[2][3], 'cell_4_1': table[3][0], 'cell_4_2': table[3][1], 'cell_4_3': table[3][2], 'cell_4_4': table[3][3]})
				elif choice == 'exit':
					break
			move_counter += 1
		
		score = int(driver.find_element_by_css_selector('div.score-container').text.split('\n')[0])
		print('Score:', score)
		print('Number of moves:', move_counter)
		if not manual:
			__2048_results_collection__.insert({'score': score, 'n_moves': move_counter, 'game_id': game_id, 'scaled_data': scaled, 'shuffled_data': shuffle})
		if not manual and pickle_file is None:
			classifier_name = ''
			if number_of_repeats%2:
				classifier_name = 'RandomForestClassifier'
			else:
				classifier_name = 'LogisticRegression'
			with open(str(score) + '_score_2048_game' + ['', '_s'][scaled] + ['', '_sh'][shuffle] + '_' + classifier_name + '.pickle', 'wb') as f:
				pickle.dump(classifier, f)
		driver.quit()
		number_of_repeats -= 1

if __name__ == "__main__":
	n = -1
	if '-n' in argv:
		n = int(argv[argv.index('-n')+1])
	pickled_classifier = None
	if '-pc' in argv:
		pickled_classifier = argv[argv.index('-pc')+1]
	main('-m' in argv, '-s' in argv, '-sh' in argv, n, pickled_classifier)
