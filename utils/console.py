import os


class console:
    def log(self, message: str):
        print(message)

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def dir(self, dict_obj: dict):
        for key, value in dict_obj.items():
            print(f"{key}: {value}")
