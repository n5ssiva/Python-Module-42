def validate_ingredients(ingredients: str) -> str:
    # Local import inside the function to break the circular dependency.
    from .light_spellbook import light_spell_allowed_ingredients

    allowed = light_spell_allowed_ingredients()
    lower_ing = ingredients.lower()
    for item in allowed:
        if item in lower_ing:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
