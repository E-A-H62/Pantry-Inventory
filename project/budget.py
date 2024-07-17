

class Budget():
    def __init__(self, amount):
        self.amount = float(amount)
    
    def __repr__(self):
        return f'<Budget {self.amount}>'
    
    def get(self):
        return float(self.amount)
    
    def edit_budget(self, new_amount):
        self.amount = new_amount

    def add(self, added_amount):
        self.amount = self.amount + added_amount

    def sub(self, sub_amount):
        self.amount = self.amount - sub_amount


"""budget = Budget(0)
print(budget)

budget.edit_budget(200.00)
print(budget)

budget.add(50)
print(budget)

budget.sub(50)
print(budget)"""