# Module 09 — Cours complet sur Pydantic

## Comment lire ce document

Pydantic est un outil **très utilisé en production** (FastAPI l'utilise massivement, ainsi que quasiment toutes les APIs Python modernes). Comprendre ce module, c'est gagner une compétence directement transférable en pro.

Le document est divisé en 4 parties :

1. **Le modèle mental — qu'est-ce que Pydantic et pourquoi c'est génial**
2. **Les 3 niveaux de complexité du projet en profondeur**
3. **Walkthrough des 3 exercices**
4. **Préparation à la défense**

---

# PARTIE 1 — Le modèle mental

## 1.1 Le problème que Pydantic résout

Imagine que tu reçois un dictionnaire de données depuis une API externe ou un fichier JSON :

```python
data = {
    "station_id": "ISS001",
    "crew_size": "6",       # ← oups, c'est une string
    "power_level": 150.0,    # ← oups, > 100%
    "last_maintenance": "2024-01-15T10:30:00",
}
```

Comment vérifier que tout est valide ? Sans Pydantic, tu dois écrire à la main :

```python
if not isinstance(data["station_id"], str):
    raise ValueError("station_id doit être un string")
if len(data["station_id"]) < 3 or len(data["station_id"]) > 10:
    raise ValueError("station_id entre 3 et 10 caractères")
try:
    crew_size = int(data["crew_size"])
except ValueError:
    raise ValueError("crew_size doit être un nombre")
if crew_size < 1 or crew_size > 20:
    raise ValueError("crew_size entre 1 et 20")
# ... répété pour chaque champ
```

Ça marche, mais c'est **30 lignes de code répétitif** pour valider 5 champs. Et tu vas oublier des cas. Et c'est pas lisible.

**Avec Pydantic** :

```python
class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime

# Validation en UNE ligne :
station = SpaceStation(**data)
# → soit ça crée l'objet, soit ça lève ValidationError avec un message précis
```

Tu **déclares** la structure attendue, et Pydantic fait toute la validation automatiquement. Avec en plus :

- **Conversion de types** automatique ("6" → 6, "2024-01-15..." → datetime)
- **Messages d'erreur clairs** ("Input should be less than or equal to 20")
- **Type hints** qui marchent avec ton IDE et mypy

C'est pour ça que Pydantic est devenu **l'outil par défaut** en Python moderne pour tout ce qui touche aux données.

## 1.2 Le concept de "data class validée"

Pydantic est inspiré des **dataclasses** Python (qui sont juste des classes avec des champs typés), mais ajoute :

- La **validation** automatique au moment de l'instanciation
- La **conversion** de types
- La **sérialisation** facile en JSON ou dict

Un `BaseModel` Pydantic c'est essentiellement :

1. Une classe Python normale
2. Avec des champs typés (`crew_size: int`)
3. Qui valide automatiquement à l'instanciation

```python
class Station(BaseModel):
    name: str
    crew: int

s = Station(name="ISS", crew=6)       # ✅
s2 = Station(name="ISS", crew="abc")  # ❌ ValidationError
```

## 1.3 Pydantic v1 vs v2 — pourquoi c'est important

Pydantic a deux versions majeures avec une syntaxe différente :

||v1 (ancien)|v2 (moderne)|
|---|---|---|
|Validation custom|`@validator`|`@model_validator`|
|Config|`class Config:`|`model_config = ConfigDict(...)`|
|Sérialisation|`.dict()`, `.json()`|`.model_dump()`, `.model_dump_json()`|

Le sujet exige **explicitement Pydantic v2** (page 7). Si tu utilises `@validator` (v1), c'est marqué comme déprécié et tu vas avoir des warnings. **Toujours `@model_validator`**.

## 1.4 Les concepts clés à maîtriser

### BaseModel

C'est la classe parente de tous tes modèles. Tu en hérites et tu ajoutes des champs typés.

```python
from pydantic import BaseModel

class MyModel(BaseModel):
    field1: str
    field2: int
```

### Field

Permet de configurer un champ : contraintes, valeur par défaut, description.

```python
from pydantic import Field

class MyModel(BaseModel):
    age: int = Field(..., ge=0, le=120)
    name: str = Field(..., min_length=1, max_length=50)
    status: str = Field(default="active")
```

Les contraintes courantes :

- `ge` (greater or equal) / `gt` (greater than)
- `le` (less or equal) / `lt` (less than)
- `min_length` / `max_length` (pour strings et listes)
- `pattern` (regex pour strings)

Le `...` (Ellipsis) signifie "champ obligatoire, pas de valeur par défaut". C'est important : sans ça, Pydantic ne lève pas d'erreur si le champ est manquant.

### @model_validator

Décorateur pour ajouter une **validation custom** qui s'exécute après que tous les champs aient été individuellement validés.

```python
from pydantic import model_validator

class MyModel(BaseModel):
    a: int
    b: int

    @model_validator(mode="after")
    def check_a_less_than_b(self) -> "MyModel":
        if self.a >= self.b:
            raise ValueError("a doit être < b")
        return self
```

**Trois points cruciaux** :

1. `mode="after"` = validator exécuté **après** la validation des champs individuels (donc `self.a` et `self.b` sont déjà les bons types)
2. `raise ValueError(...)` à l'intérieur déclenche une `ValidationError` Pydantic
3. **Le validator DOIT retourner `self`** à la fin, sinon Pydantic plante

### Enum

Pour limiter un champ à un ensemble de valeurs possibles. Pydantic vérifie automatiquement que la valeur est dans l'enum.

```python
from enum import Enum

class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class MyModel(BaseModel):
    status: Status
```

Le `str, Enum` est important : ça permet à Pydantic d'accepter une string brute en entrée et de la convertir en enum.

### Nested models

Un modèle peut contenir d'autres modèles. Pydantic valide récursivement.

```python
class Address(BaseModel):
    street: str
    city: str

class Person(BaseModel):
    name: str
    address: Address
    friends: list["Person"]  # forward reference

# Pydantic valide Address et chaque Person dans friends automatiquement
```

C'est ce qui rend Pydantic puissant pour les structures complexes (JSON profonds, configurations imbriquées, etc.).

## 1.5 Les erreurs Pydantic

Quand une validation échoue, Pydantic lève une `ValidationError`. Cette exception contient des **détails structurés** :

```python
try:
    Station(crew_size=25)
except ValidationError as e:
    for err in e.errors():
        print(err)
    # {'type': 'less_than_equal', 'loc': ('crew_size',), 'msg': 'Input should be less than or equal to 20', ...}
```

Chaque erreur a :

- `type` : le code d'erreur (`less_than_equal`, `value_error`, etc.)
- `loc` : le chemin vers le champ qui a échoué (utile pour nested)
- `msg` : le message lisible

Le préfixe `"Value error, "` apparaît automatiquement devant les messages venant d'un `raise ValueError` dans un `@model_validator`. C'est pour ça que dans le code on fait `err["msg"].replace("Value error, ", "")` pour avoir un message propre.

## 1.6 Pourquoi Pydantic existe dans la vraie vie

Trois cas d'usage majeurs :

**1. APIs REST avec FastAPI** — FastAPI utilise Pydantic pour valider automatiquement les requêtes HTTP. Tu déclares ton modèle, FastAPI génère automatiquement la documentation OpenAPI/Swagger.

**2. Configuration d'applications** — Au lieu de lire des variables d'env à la main, tu déclares un modèle Pydantic qui les valide automatiquement (`pydantic-settings`).

**3. Traitement de données** — Lecture de fichiers JSON/CSV/YAML, validation que les données ont la bonne forme avant de les processer.

Sur LinkedIn, "Pydantic" apparaît dans 90% des offres Python "backend". C'est une compétence pro.

---

# PARTIE 2 — Les 3 exercices en profondeur

## Ex0 — Validation basique (BaseModel + Field)

**Objectif pédagogique** : maîtriser la déclaration d'un modèle avec des contraintes de champ.

**Concepts vus** :

- `BaseModel`
- `Field(..., ge=X, le=Y, min_length=Z, max_length=W)`
- Champ optionnel avec `str | None = Field(default=None, ...)`
- Champ avec valeur par défaut (`is_operational: bool = True`)
- **Conversion automatique** : passer `"2024-01-15T10:30:00"` (string) à un champ `datetime` fonctionne — Pydantic convertit
- **Gestion des erreurs** avec `try/except ValidationError`

**Question pédagogique du sujet** : _"How does Pydantic's automatic type conversion work? What happens when you pass a string timestamp to a datetime field?"_

**Réponse** : Pydantic essaie de convertir les types compatibles. Pour `datetime`, il accepte une string ISO 8601 (`"2024-01-15T10:30:00"`) et la parse en `datetime`. Si la string est invalide (`"hier"`), il lève `ValidationError`. Même mécanisme pour `int` (accepte `"6"` → `6`), `float`, `bool` (accepte `"true"`, `1`, etc.).

## Ex1 — Validation custom (@model_validator)

**Objectif pédagogique** : aller au-delà des contraintes de champ pour valider des **règles métier** qui dépendent de plusieurs champs.

**Concepts vus** :

- `Enum` avec `str, Enum` pour rester sérialisable
- `@model_validator(mode="after")` avec règles combinées
- `raise ValueError(...)` qui devient une `ValidationError`
- `return self` obligatoire

**Pourquoi `mode="after"` plutôt que `"before"` ?**

- `before` : validator s'exécute **avant** la conversion des types. Tu reçois les données brutes (dict).
- `after` : validator s'exécute **après** la validation et conversion. Tu reçois `self` avec tous les attributs déjà typés.

Pour les règles métier, `after` est presque toujours ce qu'on veut.

**Pourquoi `Enum(str, Enum)` au lieu de juste `Enum` ?**

Pour qu'une valeur d'enum soit comparable à une string : `contact.contact_type == "radio"` marche, et la sérialisation JSON sort `"radio"` au lieu de `<ContactType.RADIO: 1>`. C'est universellement préféré pour les enums Pydantic.

**Les 4 règles métier de l'ex1** :

1. ID doit commencer par "AC" → simple `startswith`
2. Physical → must be verified → vérifie une condition combinée
3. Telepathic → at least 3 witnesses
4. Strong signal (> 7.0) → must have a message

Toutes ces règles sont impossibles avec juste `Field()`, parce qu'elles **dépendent d'autres champs**. C'est exactement ce que `@model_validator` permet.

## Ex2 — Nested models

**Objectif pédagogique** : composer des modèles entre eux pour représenter des structures complexes.

**Concepts vus** :

- `crew: list[CrewMember]` — Pydantic valide chaque élément récursivement
- `Field(..., min_length=1, max_length=12)` sur une liste — borne le nombre d'éléments
- Validators qui inspectent les éléments d'une liste (`[c for c in self.crew if c.rank == ...]`)

**Le comportement clé** : si **un seul** `CrewMember` dans la liste est invalide, **toute** la `SpaceMission` échoue à la validation, avec un message qui pointe précisément vers la position fautive (`loc: ("crew", 2, "age")`).

**Question pédagogique du sujet** : _"How does Pydantic handle validation of nested models? What happens when a CrewMember fails validation within a SpaceMission?"_

**Réponse** : Pydantic valide les modèles imbriqués récursivement, en profondeur d'abord. Quand tu fais `SpaceMission(crew=[...])`, Pydantic commence par valider chaque dict de `crew` en `CrewMember`. Si un seul échoue, toute la création de `SpaceMission` plante avec un `ValidationError` qui contient le chemin précis vers le champ fautif (`loc: ("crew", 2, "age")` = troisième crew member, champ `age`). Pydantic ne fait JAMAIS de validation partielle — c'est tout ou rien.

---

# PARTIE 3 — Walkthrough rapide des fichiers

## ex0/space_station.py

Structure :

- Modèle `SpaceStation` avec 8 champs et leurs contraintes
- Fonction `display_station(station)` pour formater l'affichage
- `main()` qui crée une station valide, puis tente d'en créer une invalide (crew_size > 20) pour montrer le message d'erreur

Points subtils :

- `last_maintenance: datetime` reçoit une string ISO et la convertit
- `notes: str | None = Field(default=None, max_length=200)` : optionnel mais avec contrainte si présent
- Capture de `ValidationError` avec `for err in e.errors()` pour afficher juste le message

## ex1/alien_contact.py

Structure :

- Enum `ContactType` (radio, visual, physical, telepathic)
- Modèle `AlienContact` avec ses 9 champs
- `@model_validator(mode="after")` avec 4 règles métier
- `main()` qui montre un cas valide (radio) et un cas invalide (telepathic avec 1 témoin)

Points subtils :

- `ContactType(str, Enum)` pour que les valeurs soient des strings
- L'enum se compare directement avec `==` : `self.contact_type == ContactType.PHYSICAL`
- Le validator vérifie les 4 règles dans l'ordre, lève au premier échec
- Le message d'erreur affiché supprime le préfixe `"Value error, "` ajouté par Pydantic

## ex2/space_crew.py

Structure :

- Enum `Rank` (5 niveaux)
- Modèle `CrewMember` (simple, pas de validator)
- Modèle `SpaceMission` qui contient `crew: list[CrewMember]`
- `@model_validator` sur `SpaceMission` avec 4 règles
- `main()` qui crée 3 crew members, monte une mission valide, puis une mission invalide (que des cadets/officiers, pas de leader)

Points subtils :

- `crew: list[CrewMember]` — Pydantic valide chaque élément
- Le validator utilise `self.crew` qui contient déjà des objets `CrewMember` validés
- Filter pattern : `leaders = [c for c in self.crew if c.rank in (...)]`
- Validation cross-field : `duration_days > 365` ET `experienced count < half of crew`

---

# PARTIE 4 — Préparation à la défense

## Q1 : C'est quoi Pydantic et à quoi ça sert ?

Pydantic est une librairie Python de validation de données par déclaration de modèles. On définit des classes avec des champs typés, et Pydantic valide automatiquement les données à l'instanciation : conversion de types, contraintes (min, max, longueurs), et règles métier custom.

En pratique, c'est utilisé pour valider les entrées d'APIs (FastAPI l'utilise), les fichiers de config, ou n'importe quel flux de données externe avant traitement.

## Q2 : Différence entre Pydantic v1 et v2 ?

V2 a refait le moteur de validation en Rust, donc beaucoup plus rapide. La syntaxe a aussi changé : `@validator` → `@model_validator(mode="after")`, `.dict()` → `.model_dump()`, et la config se fait via `model_config = ConfigDict(...)` au lieu d'une inner class. Le sujet exige v2 explicitement.

## Q3 : Comment fonctionne `Field()` ?

`Field()` permet de configurer un champ : ajouter des contraintes (`ge`, `le`, `min_length`...), définir une valeur par défaut, ou marquer le champ comme obligatoire. Le `...` (Ellipsis) en premier argument signifie "obligatoire, pas de défaut". Sans ça, le champ est traité comme ayant une valeur par défaut implicite et n'est plus requis.

## Q4 : C'est quoi `@model_validator` et quand l'utiliser ?

C'est un décorateur pour ajouter une validation **custom** qui s'applique à l'ensemble du modèle (pas à un seul champ). On l'utilise quand la règle dépend de **plusieurs champs** ou implémente une logique métier qui dépasse les simples contraintes de `Field`.

Avec `mode="after"`, le validator s'exécute après que Pydantic ait validé et converti les champs individuels. Le validator reçoit `self` avec tous les attributs typés, et **doit retourner `self`** à la fin.

## Q5 : Pourquoi ton code fait `return self` à la fin du validator ?

Parce que Pydantic l'exige. Le validator peut potentiellement **modifier** `self` (corriger une valeur, normaliser, etc.), donc Pydantic attend que tu lui rendes l'instance finale. Si tu ne retournes pas `self`, Pydantic lève une `TypeError` parce qu'il reçoit `None` au lieu d'un modèle.

## Q6 : Que se passe-t-il si je passe une string `"6"` à un champ `int` ?

Pydantic essaie de convertir. `"6"` est convertible en `int(6)`, donc la conversion réussit silencieusement. C'est la **type coercion** automatique. Pour `"abc"`, c'est non-convertible, donc Pydantic lève `ValidationError`.

Le même mécanisme marche pour `datetime` (accepte les strings ISO 8601), `bool` (accepte "true", "false", 1, 0), `float`, etc.

## Q7 : Comment ton code valide la liste de crew members ?

Pydantic valide récursivement. Quand je fais `SpaceMission(crew=[member1, member2, ...])`, Pydantic parcourt la liste et valide chaque élément comme un `CrewMember`. Si un seul élément échoue (par exemple un âge à 15 ans), **toute** la création de `SpaceMission` échoue avec une erreur qui pointe précisément vers `crew[2].age` ou similaire.

Je n'ai pas besoin d'écrire de code pour la validation des éléments — Pydantic le fait automatiquement parce que `crew: list[CrewMember]` annonce explicitement le type de chaque élément.

## Q8 : Comment ton code vérifie qu'il y a au moins un Commander ou Captain dans la mission ?

Dans le `@model_validator`, je filtre la liste avec une list comprehension :

```python
leaders = [c for c in self.crew if c.rank in (Rank.COMMANDER, Rank.CAPTAIN)]
if not leaders:
    raise ValueError("Mission must have at least one Commander or Captain")
```

À ce stade, `self.crew` contient déjà des `CrewMember` validés, donc `c.rank` est un `Rank` enum garanti. Je compare directement avec `Rank.COMMANDER`.

## Q9 : Pourquoi `class ContactType(str, Enum)` et pas juste `class ContactType(Enum)` ?

Pour que les valeurs de l'enum soient **aussi** des strings. Trois avantages :

1. La sérialisation JSON sort `"radio"` au lieu de `<ContactType.RADIO: 1>`
2. La comparaison `contact.contact_type == "radio"` fonctionne
3. Pydantic peut accepter une string brute en entrée et la convertir en enum

C'est devenu le pattern standard pour les enums Pydantic.

## Q10 : Et si je passe `"RADIO"` (majuscules) au lieu de `"radio"` ?

Par défaut, Pydantic est **case-sensitive** pour les enums. `"RADIO"` lèverait une `ValidationError`. Si on voulait être tolérant, on pourrait faire un `@model_validator(mode="before")` qui normalise les strings en lowercase avant la validation des champs. Mais le sujet ne le demande pas.

## Q11 : Différence entre `mode="before"` et `mode="after"` ?

- `before` : le validator s'exécute **avant** que Pydantic ait validé/converti les champs. Il reçoit un dict brut. Utile pour **transformer** ou normaliser les données d'entrée.
- `after` : le validator s'exécute **après**. Il reçoit `self` avec tous les attributs typés et validés. Utile pour les **règles métier** qui combinent plusieurs champs déjà validés.

Pour mes 3 validators (ex1 et ex2), j'utilise `after` parce que je veux travailler avec des données déjà typées (par exemple comparer `self.contact_type == ContactType.PHYSICAL`).

## Q12 : Que contient une `ValidationError` ?

C'est une exception structurée. La méthode `.errors()` retourne une liste de dicts avec :

- `type` : code d'erreur (`less_than_equal`, `value_error`, ...)
- `loc` : tuple représentant le chemin vers le champ fautif (utile pour les nested)
- `msg` : message lisible
- `input` : la valeur qui a échoué

Dans mes scripts, je parcours `e.errors()` et j'affiche `err["msg"]` (en retirant le préfixe `"Value error, "` ajouté quand l'erreur vient d'un `raise ValueError` dans un validator).

## Q13 : Pourquoi tu utilises `e.errors()` plutôt que `print(e)` ?

`print(e)` affiche tous les détails avec contexte, c'est verbeux. `e.errors()` me donne les erreurs structurées sous forme de liste de dicts, et je peux extraire juste le message principal pour matcher l'output attendu par le sujet.

C'est aussi ce qu'on fait en API : on extrait les messages pour les renvoyer au client dans un format propre.

## Q14 : C'est quoi un "nested model" ?

Un modèle Pydantic qui contient **un autre modèle** (ou une liste/dict de modèles) comme champ. Dans ex2, `SpaceMission` contient `crew: list[CrewMember]`. C'est un nested model.

Pydantic valide les modèles imbriqués **récursivement** : pour valider `SpaceMission`, il faut d'abord valider chaque `CrewMember` de la liste. Si une seule erreur survient à n'importe quel niveau, toute la chaîne échoue.

C'est très puissant pour représenter des structures de données complexes : configurations imbriquées, JSON profonds, hiérarchies métier.

## Q15 : Pourquoi Pydantic plutôt que des `if isinstance(...)` manuels ?

Trois raisons principales :

1. **Beaucoup moins de code** : 5 lignes de déclaration valent 50 lignes de validation manuelle
2. **Messages d'erreur uniformes et clairs** : on n'a pas à les écrire à la main
3. **Composition et réutilisation** : on peut combiner des modèles, hériter, etc.

Quatrième raison : Pydantic est **massivement utilisé** dans l'écosystème Python moderne. C'est devenu un standard de facto. Apprendre Pydantic = compétence directement utilisable en pro.

---

# Conclusion

Pydantic c'est juste : déclarer la **forme** que doivent avoir tes données, et laisser la lib valider à ta place. Plus tu codes des structures complexes, plus Pydantic devient rentable.

Pour la défense, retiens trois choses :

1. **BaseModel + Field** = validation déclarative des champs individuels
2. **@model_validator(mode="after")** = règles métier sur plusieurs champs
3. **Nested models** = composition récursive avec validation automatique

Si on te demande "à quoi ça sert dans la vraie vie ?", dis : "Tout ce qui est API REST moderne avec FastAPI, configuration d'applications, ou validation de données externes (JSON, fichiers de config). C'est devenu standard dans tout l'écosystème Python data/backend."

Bonne défense.

---

# Module 09 — Fiche défense, point par point selon la grille d'évaluation

Cette fiche suit **l'ordre exact** de la grille d'évaluation 42. Tu peux la dérouler de haut en bas pendant la défense.

---

## PRÉLIMINAIRES

### "Check que les fichiers sont présents"

L'évaluateur va vérifier la présence de :

- ✅ `ex0/space_station.py`
- ✅ `ex1/alien_contact.py`
- ✅ `ex2/space_crew.py`

**Action** : montre l'arborescence avec `ls ex0 ex1 ex2` ou `tree`.

### "Verify that the code runs without errors"

L'évaluateur va lancer :

```bash
python3 ex0/space_station.py
python3 ex1/alien_contact.py
python3 ex2/space_crew.py
```

**Action préventive** : avant la défense, fais-le toi-même dans un fresh venv pour confirmer que tout tourne. Active le venv avant : `source venv/bin/activate`.

### "Test both valid AND invalid data scenarios"

Tes 3 scripts démontrent **déjà** les deux scénarios dans leur `main()`. Pour chaque exo : un cas valide qui s'affiche, puis un cas invalide qui catch la `ValidationError`.

### "Look for proper use of Pydantic features"

Tu utilises :

- ✅ `BaseModel` partout (`class SpaceStation(BaseModel):`)
- ✅ `Field(...)` avec contraintes (`Field(..., ge=1, le=20)`)
- ✅ `@model_validator(mode="after")` dans ex1 et ex2

### "Ensure deprecated `@validator` is NOT used"

Tu utilises **uniquement** `@model_validator(mode="after")`. Aucun `@validator` v1 nulle part. À vérifier avec :

```bash
grep -rn "@validator" ex0 ex1 ex2
```

→ doit retourner rien.

---

## EXERCISE 0 — Space Station Data

### Q : "Does SpaceStation model inherit from BaseModel?"

**Réponse** :

> "Oui. `class SpaceStation(BaseModel):`. BaseModel est la classe parente obligatoire de tout modèle Pydantic. C'est elle qui apporte la validation automatique à l'instanciation, la conversion de types, et les méthodes de sérialisation (`model_dump`, `model_dump_json`)."

### Q : "Do all required fields use Field() with proper constraints?"

**Réponse** :

> "Oui. Chaque champ requis utilise `Field(..., ...)` avec ses contraintes :
> 
> - `station_id`: `min_length=3, max_length=10`
> - `name`: `min_length=1, max_length=50`
> - `crew_size`: `ge=1, le=20` (greater/less or equal)
> - `power_level` et `oxygen_level`: `ge=0.0, le=100.0`
> - `notes`: optionnel avec `default=None, max_length=200`
> 
> Le `...` (Ellipsis) en premier argument signifie 'champ obligatoire, pas de valeur par défaut'."

### Q : "Does the model accept valid space station data?"

**Démonstration** : ton script crée une station valide (ISS001, crew=6, power=85.5, etc.). Elle s'affiche correctement.

### Q : "Does invalid data (crew_size > 20) raise validation errors?"

**Démonstration** : ton script tente de créer une station avec `crew_size=25`. Pydantic lève `ValidationError` avec le message `"Input should be less than or equal to 20"`.

### Q : "Output shows both successful creation AND validation errors?"

✅ Oui, c'est exactement ce que fait `main()` : un cas valide qui s'affiche, suivi du cas invalide avec le message d'erreur.

### Q : "Code contains a valid AND invalid SpaceStation, error properly handled, NOT hardcoded output"

✅ Le `try/except ValidationError` capture l'exception et extrait le message via `e.errors()`. Rien n'est hardcodé en `print()` direct.

---

## CODE QUALITY — Exercise 0

### Q : "Are field constraints appropriate?"

**Réponse** :

> "Toutes les contraintes matchent exactement le sujet :
> 
> - `crew_size`: 1 à 20
> - `power_level` et `oxygen_level`: 0.0 à 100.0 (pourcentages)
> - `station_id`: 3 à 10 caractères
> - `name`: 1 à 50 caractères"

### Q : "Optional field in 'notes'?"

**Réponse** :

> "Oui : `notes: str | None = Field(default=None, max_length=200)`. C'est un champ optionnel — il peut être absent ou null, mais s'il est présent, il doit faire max 200 caractères."

### Q : "Datetime field properly handled? What happens with a string timestamp?"

**Réponse clé** :

> "Pydantic fait de la **conversion automatique de types**. Quand je passe la string `'2024-01-15T10:30:00'` au champ `last_maintenance: datetime`, Pydantic la parse comme une string ISO 8601 et la convertit en objet `datetime`. Si la string était invalide (ex: `'hier'`), Pydantic lèverait une `ValidationError`.
> 
> C'est valable pour d'autres types aussi : `'6'` (string) → `6` (int), `'true'` → `True` (bool), etc. C'est ce qu'on appelle la **type coercion**."

### Q : "Code well-structured and readable?"

**Réponse** :

> "Le code est organisé en 3 parties : le modèle, une fonction `display_station` pour l'affichage, et un `main()` qui démontre les deux cas. Les noms sont explicites et les contraintes lisibles."

---

## EXERCISE 1 — Alien Contact Data

### Q : "Does AlienContact use @model_validator for custom validation?"

**Réponse** :

> "Oui. J'ai une méthode `check_business_rules` décorée par `@model_validator(mode='after')`. Elle s'exécute après que Pydantic ait validé tous les champs individuellement, et elle implémente les règles métier qui dépendent de plusieurs champs."

### Q : "ContactType enum properly defined and used?"

**Réponse** :

> "Oui. `class ContactType(str, Enum)` avec 4 valeurs : RADIO, VISUAL, PHYSICAL, TELEPATHIC. L'héritage de `str` est important : ça permet la sérialisation JSON propre et la comparaison directe avec des strings."

### Q : "Each value of the enum properly defined?"

**Réponse** : montre l'enum :

```python
class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"
```

4 valeurs, chacune en lowercase comme valeur string.

### Q : "Custom validation rules work?"

**Réponse** :

> "Mes 4 règles métier sont :
> 
> 1. `contact_id` doit commencer par 'AC' → vérifié avec `startswith('AC')`
> 2. Si type physical, doit être verified
> 3. Si telepathic, au moins 3 témoins
> 4. Signal > 7.0 doit avoir un message reçu
> 
> Chaque règle non respectée lève un `ValueError` avec un message clair, qui devient une `ValidationError` Pydantic."

### Q : "Does message_received combine Optional typing AND max_length=500?"

**Réponse** :

> "Oui : `message_received: str | None = Field(default=None, max_length=500)`. Le `str | None` rend le champ optionnel (syntaxe Python 3.10+), le `default=None` donne une valeur par défaut, et `max_length=500` impose la limite quand le champ est présent."

### Q : "Demonstration shows valid contacts AND validation errors?"

✅ Oui. `main()` montre un contact valide (RADIO, 5 witnesses, message), puis tente un contact invalide (TELEPATHIC avec 1 seul témoin) qui lève l'erreur attendue.

### Q : "No deprecated @validator decorators used?"

✅ Aucun. Uniquement `@model_validator(mode="after")`. À vérifier :

```bash
grep -n "@validator" ex1/alien_contact.py
```

---

## CUSTOM VALIDATION RULES — Exercise 1 (les tests en live !)

**Attention : l'évaluateur va probablement te demander de tester chaque règle en live.** Sois prêt à modifier ton code à la volée pour montrer.

### Test 1 : "Try creating a contact with ID NOT starting with 'AC' — does it fail?"

**Action** : modifie `contact_id="AC_2024_001"` en `contact_id="XX_2024_001"` (length 11 OK), relance.

**Résultat attendu** : `Contact ID must start with 'AC'`

### Test 2 : "Try telepathic contact with < 3 witnesses — does it fail?"

C'est **déjà** dans ton `main()` (TELEPATHIC + 1 witness). L'erreur sort.

### Test 3 : "Try strong signal without message — does it fail?"

**Action** : crée un contact avec `signal_strength=8.5` et **retire** `message_received="..."`.

**Résultat attendu** : `Strong signals (> 7.0) should include received messages`

### Test 4 : "Try physical contact NOT verified — does it fail?"

**Action** : crée un contact avec `contact_type=ContactType.PHYSICAL` et `is_verified=False` (ou omet-le, par défaut False).

**Résultat attendu** : `Physical contact reports must be verified`

### Test 5 : "Create a contact without specifying is_verified. Is it False by default?"

**Réponse** :

> "Oui. Dans la déclaration du modèle : `is_verified: bool = False`. Donc si je ne précise pas, Pydantic met `False` par défaut. Je peux le démontrer en omettant le champ dans la création."

### Test 6 : "Does the validator properly return 'self'?"

**Réponse** :

> "Oui. Regardez la dernière ligne de `check_business_rules` : `return self`. C'est **obligatoire** en Pydantic v2 : le validator peut modifier l'instance, donc Pydantic exige qu'on lui rende l'instance finale. Sans `return self`, Pydantic lève une `TypeError` au moment de la création."

### Test 7 : "Are the error messages clear and helpful?"

**Réponse** :

> "Chaque `ValueError` que je lève contient un message complet en anglais qui explique exactement ce qui a échoué : `'Telepathic contact requires at least 3 witnesses'`, `'Physical contact reports must be verified'`, etc. L'utilisateur sait précisément quoi corriger."

---

## EXERCISE 2 — Space Crew Management

### Q : "CrewMember and SpaceMission models properly defined?"

**Réponse** :

> "Oui, deux modèles distincts. `CrewMember` représente un membre individuel avec ses 7 champs (member_id, name, rank, age, specialization, years_experience, is_active). `SpaceMission` représente la mission globale avec son équipage, et contient `crew: list[CrewMember]` — c'est un **nested model**."

### Q : "Does the crew field accept a list of CrewMember objects (nested)?"

**Réponse** :

> "Oui : `crew: list[CrewMember] = Field(..., min_length=1, max_length=12)`. Pydantic valide récursivement chaque élément de la liste comme un CrewMember. Si un seul échoue, toute la création de SpaceMission échoue."

### Q : "5 ranks implemented?"

**Réponse** : montre l'enum :

```python
class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"
```

5 valeurs : cadet, officer, lieutenant, captain, commander.

### Q : "Mission validation rules work? Test each of them."

Tes 4 règles dans `check_safety` :

**Rule 1 : Mission ID must start with 'M'**

- Test : modifie `mission_id="M2024_MARS"` en `mission_id="X2024_MARS"`
- Erreur attendue : `Mission ID must start with 'M'`

**Rule 2 : At least one Commander or Captain**

- Déjà testé dans le `main()` invalide (que des cadets/officiers)
- Erreur : `Mission must have at least one Commander or Captain`

**Rule 3 : Long missions (> 365 days) need 50% experienced crew (5+ years)**

- Test : crée une mission avec `duration_days=400` et un équipage de jeunes (years_experience < 5)
- Erreur : `Long missions (> 365 days) need 50% experienced crew (5+ years)`

**Rule 4 : All crew members must be active**

- Test : crée un CrewMember avec `is_active=False`, ajoute-le à une mission
- Erreur : `All crew members must be active`

### Q : "Demonstration shows mission creation with crew details?"

✅ Oui, `display_mission()` affiche toutes les infos : ID, destination, durée, budget, taille équipage, et chaque membre avec son grade et spécialisation.

### Q : "Invalid missions properly rejected?"

✅ Oui, le 2e cas du `main()` montre une mission sans leader → `ValidationError` levée et catchée.

---

## NESTED MODELS FUNCTIONALITY — Exercise 2 (les tests en live !)

### Test 1 : "Can you create individual CrewMember objects?"

**Réponse** :

> "Oui. Dans mon `main()`, je crée trois CrewMember séparément (commander, lieutenant, officer) avant de les passer à SpaceMission. Pydantic valide chacun individuellement avec ses contraintes (âge entre 18 et 80, member_id 3-10 chars, etc.)."

### Test 2 : "Does SpaceMission properly validate its crew list?"

**Réponse** :

> "Oui. Pydantic valide chaque élément de `crew` comme un CrewMember. Si je passe un dict invalide dans la liste, par exemple un age à 15 ans, Pydantic lèvera une erreur avec le chemin exact : `loc: ('crew', 1, 'age')` — élément 1, champ age."

### Test 3 : "Create a SpaceMission with one active Commander AND one inactive Captain. What happens?"

**Réponse importante** :

> "Ma règle 4 dit 'All crew members must be active'. Donc même si j'ai un Commander actif (qui satisfait la règle 'at least one Commander or Captain'), la présence d'un Captain inactif viole la règle 4. La mission est rejetée avec : `All crew members must be active`."

**Démonstration** :

```python
commander = CrewMember(member_id="CR001", name="Sarah", rank=Rank.COMMANDER, age=42, specialization="Cmd", years_experience=15, is_active=True)
captain_inactive = CrewMember(member_id="CR002", name="John", rank=Rank.CAPTAIN, age=45, specialization="Nav", years_experience=20, is_active=False)
SpaceMission(crew=[commander, captain_inactive], ...)  # → erreur
```

### Test 4 : "Are mission validation rules logical and working?"

**Réponse** :

> "Les 4 règles couvrent les vraies contraintes de safety d'une mission spatiale :
> 
> 1. Convention de nommage (mission ID)
> 2. Leadership minimum (Commander ou Captain)
> 3. Expérience requise pour missions longues (réaliste : on n'envoie pas que des jeunes sur Mars)
> 4. Tout l'équipage doit être opérationnel (active)
> 
> Chaque règle a un sens métier clair."

### Test 5 : "Try to create a SpaceMission WITHOUT specifying status. Is it 'planned' by default?"

**Réponse** :

> "Oui. Dans la déclaration : `mission_status: str = 'planned'`. Si je ne précise pas, Pydantic utilise la valeur par défaut. Je peux le démontrer en omettant le champ : la mission est créée avec `mission_status='planned'`."

### Test 6 : "Try to create a SpaceMission over budget. What happens?"

**Réponse** :

> "Le champ est `budget_millions: float = Field(..., ge=1.0, le=10000.0)`. Si je passe `budget_millions=15000.0`, Pydantic lève `ValidationError: Input should be less than or equal to 10000.0`. La validation est automatique grâce à `le=10000.0`."

**Démonstration** : `SpaceMission(..., budget_millions=15000.0)` → erreur.

### Test 7 : "Does the code handle edge cases appropriately?"

**Réponse** :

> "Oui. Quelques edge cases gérés :
> 
> - Liste crew vide : refusée par `min_length=1` sur le champ crew
> - Liste crew > 12 : refusée par `max_length=12`
> - Mission de 365 jours pile : n'est PAS considérée 'longue' (> 365 strict)
> - String ISO invalide pour `launch_date` : ValidationError automatique
> - Tous les champs ont des bornes (ge/le, min_length/max_length)"

---

## CODE QUALITY AND BEST PRACTICES

### "Python 3.10 or higher?"

**Réponse** :

> "Oui. J'utilise la syntaxe `str | None` au lieu de `Optional[str]`, qui est seulement disponible en Python 3.10+. Vérifiable avec `python3 --version`."

### "Code adheres to flake8 (no errors)?"

**Réponse** :

> "Oui. `flake8 .` retourne aucun warning. J'ai vérifié les longueurs de ligne (< 80 caractères), l'indentation, les espaces."

**Action préventive** : lance `flake8 .` toi-même AVANT la défense.

### "Type hints REQUIRED for all functions and methods?"

**Réponse** :

> "Oui. Chaque fonction a son type de retour annoté (`-> None`, `-> AlienContact`, etc.) et chaque paramètre est typé. Les modèles Pydantic eux-mêmes utilisent les annotations pour tout."

### "Docstrings NOT required for this module"

✅ Pas de docstrings dans mon code (c'est même mieux : moins de bruit).

### "Code following Python naming conventions?"

**Réponse** :

> "Oui :
> 
> - Classes en **PascalCase** : `SpaceStation`, `ContactType`, `CrewMember`
> - Fonctions et variables en **snake_case** : `display_station`, `crew_size`, `years_experience`
> - Constantes en **UPPER_CASE** dans l'Enum : `RADIO`, `COMMANDER`"

### "Validation rules clearly implemented?"

**Réponse** : pointe ton `@model_validator` :

> "Chaque règle est une simple condition `if` dans le validator, avec un `raise ValueError` au message clair. Lisible en quelques secondes."

### "Demonstration output clear and informative?"

**Réponse** :

> "L'output suit exactement l'exemple du sujet : un header avec `=`, les détails de l'objet, puis le cas d'erreur séparé. Chaque ligne est explicite."

---

## PYDANTIC USAGE

### Q : "Field() constraints used appropriately?"

**Réponse** :

> "Oui. J'utilise `Field()` partout où il y a une contrainte :
> 
> - `Field(..., min_length=X, max_length=Y)` pour les strings
> - `Field(..., ge=X, le=Y)` pour les nombres
> - `Field(default=None, max_length=Z)` pour les optionnels
> - `Field(..., min_length=1, max_length=12)` même sur la liste `crew` (limites de taille)
> 
> Le `...` (Ellipsis) marque le champ comme obligatoire."

### Q : "Is @model_validator used correctly?"

**Réponse complète** :

> "Oui, j'utilise `@model_validator(mode='after')`. Ce mode signifie que le validator s'exécute **après** la validation et conversion des champs individuels, donc je travaille avec des données déjà typées (`self.crew` contient déjà des CrewMember validés, pas des dicts bruts).
> 
> Les règles checkées dans le validator sont des règles métier qui dépendent de plusieurs champs simultanément — c'est pour ça qu'on ne peut pas les faire avec un simple `Field()`. Et `return self` à la fin, c'est obligatoire."

### Q : "Are enums used where appropriate?"

**Réponse** :

> "Oui, deux enums :
> 
> - `ContactType` dans ex1 pour les 4 types de contact
> - `Rank` dans ex2 pour les 5 grades
> 
> Les deux héritent de `str, Enum` pour la sérialisation JSON et la comparaison facile. C'est l'idiom Pydantic standard."

### Q : "Does the code avoid deprecated Pydantic v1 features?"

**Réponse** :

> "Oui. Aucun `@validator` (v1, déprécié). J'utilise uniquement `@model_validator(mode='after')` qui est la syntaxe v2. Aucun `.dict()` non plus (v1) — Pydantic v2 utilise `.model_dump()` que je n'utilise pas dans ce projet de toute façon."

---

## UNDERSTANDING AND LEARNING

### Q : "Do the examples demonstrate proper Pydantic usage?"

**Réponse** :

> "Oui. Chaque exo illustre un concept clé :
> 
> - Ex0 : `BaseModel + Field` pour la validation de base
> - Ex1 : `@model_validator + Enum` pour les règles métier custom
> - Ex2 : Nested models avec validation récursive
> 
> Les 3 ensemble couvrent les usages standards de Pydantic en pro."

### Q : "Are the validation rules meaningful and well-thought-out?"

**Réponse** :

> "Oui. Chaque règle a un sens métier réel :
> 
> - 'Mission ID must start with M' = convention de nommage interne
> - 'At least one Commander or Captain' = leadership obligatoire
> - 'Long missions need 50% experienced crew' = safety, on n'envoie pas que des jeunes sur Mars
> - 'All crew must be active' = pas de personnel inactif en mission
> 
> Ce sont des règles qu'on pourrait trouver dans un vrai système de gestion de missions spatiales."

### Q : "Does the code show progression from basic to advanced concepts?"

**Réponse** :

> "Clairement. Ex0 = validation simple via contraintes. Ex1 = on ajoute la validation custom multi-champs et les enums. Ex2 = on compose des modèles ensemble (nested), et on a des règles encore plus complexes qui inspectent une liste d'objets. Chaque exo introduit une nouvelle couche."

### Q : "Would this code serve as a good learning example?"

**Réponse** :

> "Oui. Le code est lisible, sans surcharge inutile. Chaque modèle illustre un point précis. Les fonctions `display_*` séparent l'affichage de la logique. Les `main()` montrent à chaque fois un cas valide ET un cas invalide pour que la démo soit complète."

---

## CHECKLIST FINALE AVANT LA DÉFENSE

À faire **dans cet ordre** juste avant la correction :

```bash
# 1. Active le venv
source venv/bin/activate

# 2. Vérifie que Pydantic v2 est bien installé
python3 -c "import pydantic; print(pydantic.VERSION)"
# → doit afficher 2.x.x

# 3. Linters propres
flake8 .
# → silencieux

mypy .
# → pas d'erreur (ou erreurs sur imports Pydantic, à expliquer si demandé)

# 4. Tous les exos tournent
python3 ex0/space_station.py
python3 ex1/alien_contact.py
python3 ex2/space_crew.py
# → chaque output doit matcher l'exemple du PDF

# 5. Vérifie qu'il n'y a pas de @validator déprécié
grep -rn "@validator" ex0 ex1 ex2
# → doit retourner RIEN

# 6. Vérifie le venv ignoré
git ls-files | grep -E "venv/|__pycache__|.mypy_cache"
# → doit retourner RIEN
```

## TIPS GÉNÉRAUX POUR LA DÉFENSE

1. **Respire calmement** entre les questions. Tu as le temps.
2. **Si tu ne sais pas**, dis-le honnêtement : "Je ne suis pas sûr, mais je pense que c'est X parce que Y". L'honnêteté + raisonnement = mieux qu'une fausse certitude.
3. **Montre le code en parallèle** de tes explications. Pointe les lignes pertinentes.
4. **Pour les tests live**, sois rassurant : si tu hésites, dis "je vais modifier rapidement le code pour montrer". Personne ne t'en voudra.
5. **Le sourire et l'attitude** comptent à 42. Tu peux être détendu sans être désinvolte.

Bonne défense !