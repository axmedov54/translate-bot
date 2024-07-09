from aiogram.fsm.state import State, StatesGroup


class Translate(StatesGroup):
    lang = State()
    trans = State()
    audio = State()
