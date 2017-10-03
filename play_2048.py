from random import randint
from time import sleep
import numpy
import pandas
import pickle
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from sklearn import cross_validation, linear_model, svm, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

__manual__ = False

__mongo_client__ = MongoClient()
__2048_database__ = __mongo_client__.game_2048
__2048_moves_collection__ = __2048_database__.moves

def is_game_over(driver):
	game_over = True
	try:
		driver.find_element_by_css_selector('div.game-over')
	except:
		game_over = False
	return game_over

def parse_table_from_page(driver):
	html_tile_container = driver.find_element_by_css_selector('div.tile-container')
	html_tiles = html_tile_container.find_elements_by_css_selector('div.tile')
	tiles = [[0 for _ in range(4)] for _ in range(4)]
	for tile in html_tiles:
		classes = tile.get_attribute('class').split()
		tiles[int(classes[2].split('-')[3])-1][int(classes[2].split('-')[2])-1] = int(classes[1].split('-')[1])
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

def main():
	driver = webdriver.Chrome()
	driver.get('http://2048game.com/')
	
	if not __manual__:
		collection_data = __2048_moves_collection__.find()
		df = pandas.DataFrame(list(collection_data))
		df.drop(['_id', 'table', 'choice'], 1, inplace=True)
		x, y = df.drop(['n_choice'], 1).values, df['n_choice'].values

		classifier = VotingClassifier([('knc', neighbors.KNeighborsClassifier()),
		                            ('lsvc', svm.LinearSVC()),
		                            ('rfc', RandomForestClassifier()),
		                            ('dtc', DecisionTreeClassifier())])
		classifier.fit(x, y)
	
	last_table = None
	while not is_game_over(driver):
		table = parse_table_from_page(driver)
		if not __manual__:
			# print_table(table)
			choice = classifier.predict([[table[0][0], table[0][1], table[0][2], table[0][3], table[1][0], table[1][1], table[1][2], table[1][3], table[2][0], table[2][1], table[2][2], table[2][3], table[3][0], table[3][1], table[3][2], table[3][3]]])
			if table == last_table:
				choice = randint(1, 4)
			print(choice)
			if choice == 1:
				up(driver)
			elif choice == 2:
				right(driver)
			elif choice == 3:
				down(driver)
			elif choice == 4:
				left(driver)
			last_table = table
		else:
			choice = input()
			if choice == 'w':
				up(driver)
				__2048_moves_collection__.insert({'table': table, 'choice': 'U', 'n_choice': 1, 'cell_1_1': table[0][0], 'cell_1_2': table[0][1], 'cell_1_3': table[0][2], 'cell_1_4': table[0][3], 'cell_2_1': table[1][0], 'cell_2_2': table[1][1], 'cell_2_3': table[1][2], 'cell_2_4': table[1][3], 'cell_3_1': table[2][0], 'cell_3_2': table[2][1], 'cell_3_3': table[2][2], 'cell_3_4': table[2][3], 'cell_4_1': table[3][0], 'cell_4_2': table[3][1], 'cell_4_3': table[3][2], 'cell_4_4': table[3][3]})
			elif choice == 'd':
				right(driver)
				__2048_moves_collection__.insert({'table': table, 'choice': 'R', 'n_choice': 2, 'cell_1_1': table[0][0], 'cell_1_2': table[0][1], 'cell_1_3': table[0][2], 'cell_1_4': table[0][3], 'cell_2_1': table[1][0], 'cell_2_2': table[1][1], 'cell_2_3': table[1][2], 'cell_2_4': table[1][3], 'cell_3_1': table[2][0], 'cell_3_2': table[2][1], 'cell_3_3': table[2][2], 'cell_3_4': table[2][3], 'cell_4_1': table[3][0], 'cell_4_2': table[3][1], 'cell_4_3': table[3][2], 'cell_4_4': table[3][3]})
			elif choice == 's':
				down(driver)
				__2048_moves_collection__.insert({'table': table, 'choice': 'D', 'n_choice': 3, 'cell_1_1': table[0][0], 'cell_1_2': table[0][1], 'cell_1_3': table[0][2], 'cell_1_4': table[0][3], 'cell_2_1': table[1][0], 'cell_2_2': table[1][1], 'cell_2_3': table[1][2], 'cell_2_4': table[1][3], 'cell_3_1': table[2][0], 'cell_3_2': table[2][1], 'cell_3_3': table[2][2], 'cell_3_4': table[2][3], 'cell_4_1': table[3][0], 'cell_4_2': table[3][1], 'cell_4_3': table[3][2], 'cell_4_4': table[3][3]})
			elif choice == 'a':
				left(driver)
				__2048_moves_collection__.insert({'table': table, 'choice': 'L', 'n_choice': 4, 'cell_1_1': table[0][0], 'cell_1_2': table[0][1], 'cell_1_3': table[0][2], 'cell_1_4': table[0][3], 'cell_2_1': table[1][0], 'cell_2_2': table[1][1], 'cell_2_3': table[1][2], 'cell_2_4': table[1][3], 'cell_3_1': table[2][0], 'cell_3_2': table[2][1], 'cell_3_3': table[2][2], 'cell_3_4': table[2][3], 'cell_4_1': table[3][0], 'cell_4_2': table[3][1], 'cell_4_3': table[3][2], 'cell_4_4': table[3][3]})
			elif choice == 'exit':
				break
	
	driver.quit()

if __name__ == "__main__":
    main()
