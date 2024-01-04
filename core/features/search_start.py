from typing import List

def search_for_stop(array: List):
	for item_origins in array:
		if item_origins != "*":
			for incident in item_origins:
				if incident != "*":
					continue
				exit("Ошибка: в original найден символ '*'")
		else:
			exit("Ошибка: в original найден символ '*'")