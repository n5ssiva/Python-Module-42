from .dark_spellbook import dark_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    allowed = dark_spell_allowed_ingredients()
    lower_ing = ingredients.lower()
    for item in allowed:
        if item in lower_ing:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
