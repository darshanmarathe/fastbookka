import os

class console:
    def log(self, message: str):
        print(message)
    
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')