from aiogram.dispatcher.filters.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    full_name = State()
    birth_date = State()
    gender = State()
    specialty = State()
    address = State()
    phone = State()
    email = State()
    purpose = State()
    interests = State()
    experience = State()
    participation_type = State()
