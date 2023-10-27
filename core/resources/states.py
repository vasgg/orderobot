from aiogram.filters.state import State, StatesGroup


class States(StatesGroup):
    freelancer_mode = State()
    customer_mode = State()
    rename_account = State()
    new_order_draft = State()
    change_order_name = State()
    change_order_budget = State()
    change_order_description = State()
    change_order_link = State()
    add_funds_to_balance = State()
    delete_published_order = State()
