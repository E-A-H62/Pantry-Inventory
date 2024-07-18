from project import db
from project.models import Budget


def fetch_budget(id):
    return db.session.get(Budget, id)


def fetch_budget_id(user_id):
    budget_id = (
        db.session.query(Budget).filter_by(user_id=user_id).first()
    )
    return budget_id.id if budget_id else budget_id


def set_budget(user_id):
    new_budget = Budget(amount=0.00, user_id=user_id)
    db.session.add(new_budget)
    db.session.commit()
    return new_budget


def add_budget(added_amount, id):
    budget = fetch_budget(id)
    budget.amount += added_amount
    db.session.commit()


def sub_budget(sub_amount, id):
    budget = fetch_budget(id)
    budget.amount -= sub_amount
    db.session.commit()
