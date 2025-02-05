class LoupGarou : 

    def __init__(self, name, role, is_alive):
        self.name = name
        self.role = role
        self.is_alive = is_alive
    
    def hello(self):
        print('Hello, I am a Loup Garou')

if __name__ == '__main__':
    loup = LoupGarou('Loup', 'LoupGarou', True)
    loup.hello()