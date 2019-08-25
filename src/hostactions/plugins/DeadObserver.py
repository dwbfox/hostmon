class DeadObserver:
	def __init__(self, obvservable):
		obvservable.register(self)

	def update(self, event):
		if event.name != 'deadEvent':
			return
		print("Running dead host workflows!")
		print(str(event))