
class Node(object):
	def __init__(self):
		self.left = None # Typ: Node, wierzchołek znajdujący się po lewej stornie
		self.right = None # Typ: Node, wierzchołek znajdujący się po prawej stornie
		
	def perform_split(self, data):
		# Znajdź najlepszy podział data
		# if uzyskano poprawę funkcji celu (bądź inny, zaproponowany przez Ciebie warunek):
			#podziel dane na dwie części d1 i d2, zgodnie z warunkiem
			#self.left = Node()
			#self.right = Node()
			#self.left.perform_split(d1)
			#self.right.perform_split(d2)
		#else:
			#obecny Node jest liściem, zapisz jego odpowiedź
	
	def predict(self, example):
		pass
		"""
		if not Node jest liściem:
			if warunek podziału jest spełniony:
				return self.right.predict(example)
			else:
				return self.left.predict(example)
		return zwróć wartość (Node jest liściem)
		"""
		
		
		
if __name__ == "__main__":	
	### Implementacja wczytywania danych i losowy podział na dane uczące i testowe
	

	#data = ...
	#test_data=...
	print('Data loading complete!')

	tree_root = Node()
	tree_root.perform_split(data)
	print('Training complete!')

	### Implementacja zmierzenia trafności klasyfikacji (!) na danych testowych i uczących np.
	# for element in test_data:
	#      y = tree_root.predict(element)
	

