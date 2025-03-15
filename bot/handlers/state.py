from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    phone_number = State()
    city = State()


class ReviewState(StatesGroup):
    meditation_id = State()
    text = State()