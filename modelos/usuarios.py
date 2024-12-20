class Usuario:
    def __init__(self,id= "", username="",password= ""):
        self.id = id
        self.username= username
        self.password=password
        self.password_hash= ""

    def __str__(self):
        return f"Usuario(id='{self.id}', username = '{self.username}', password_hash = '{self.password_hash}')"