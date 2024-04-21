from random import choice, randint



def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    if '$test':
        return "Test úspěšný."
    elif '$kostky' in lowered:
        return f'Kostky říkají: {randint(1, 6)}'
    else:
        pass