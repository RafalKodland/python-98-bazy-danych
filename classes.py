class Player:
    hp = 100
    attack = 5
    coins = 50
    name = "Player1"

    def greet(self):
        print(f"Witaj, nazywam się {self.name}")

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            print(f"{self.name} został pokonany")

    def __repr__(self):
        return f"<Player: {self.name}>"


player1 = Player()
player2 = Player()
player3 = Player()

player1.name = "John"
player2.name = "Anna"
player3.name = "Jack"

player1.greet()
player2.greet()
player3.greet()