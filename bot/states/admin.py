from aiogram.fsm.state import State, StatesGroup

# Admin states are not strictly needed for the current command parsing approach
# but can be used for more complex multi-step admin operations if needed.
class AdminAddQuestion(StatesGroup):
    waiting_for_field = State()
    waiting_for_en_question = State()
    waiting_for_uz_question = State()
    waiting_for_max_words = State()

