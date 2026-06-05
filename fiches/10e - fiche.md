# Module 10 — Cours complet sur la programmation fonctionnelle

## Comment lire ce document

Ce module enseigne **5 concepts** de programmation fonctionnelle en Python. C'est le module le plus dense conceptuellement, mais aussi le plus puissant à long terme : ces patterns sont utilisés partout en Python pro (décorateurs Flask/Django, fonctions React-like, etc).

Document en 4 parties :

1. **Le modèle mental — qu'est-ce que la programmation fonctionnelle**
2. **Les 5 concepts détaillés** (1 par exercice)
3. **Walkthrough des 5 exercices**
4. **Préparation à la défense**

---

# PARTIE 1 — Le modèle mental

## 1.1 La programmation fonctionnelle, c'est quoi

C'est un **paradigme de programmation** où on traite les fonctions comme des objets de première classe : on peut les **passer en argument**, les **stocker dans des variables**, les **retourner depuis d'autres fonctions**.

Comparé à l'orienté objet (où tu organises ton code autour de **classes et objets**), le fonctionnel organise ton code autour de **fonctions qui se composent**.

```python
# Approche impérative classique
result = []
for x in [1, 2, 3, 4]:
    if x > 2:
        result.append(x * 2)
# → [6, 8]

# Approche fonctionnelle
result = list(map(lambda x: x * 2, filter(lambda x: x > 2, [1, 2, 3, 4])))
# → [6, 8]
```

L'approche fonctionnelle est plus **déclarative** : on dit "filtre puis multiplie", au lieu de "boucle, vérifie, ajoute".

## 1.2 "Functions are first-class citizens"

Cette phrase revient partout. Elle signifie qu'en Python, les fonctions sont **traitées comme n'importe quelle valeur** :

```python
def hello():
    return "Bonjour"

# 1. Stocker dans une variable
greet = hello
greet()   # → "Bonjour"

# 2. Passer en argument
def call(f):
    return f()

call(hello)   # → "Bonjour"

# 3. Retourner depuis une autre fonction
def make_greeter():
    def inner():
        return "Salut"
    return inner

g = make_greeter()
g()   # → "Salut"

# 4. Stocker dans une liste / dict
funcs = [hello, make_greeter()]
funcs[0]()   # → "Bonjour"
```

Dans des langages comme Java (avant Java 8) ou C, c'était impossible — les fonctions étaient des constructions spéciales, pas des valeurs. En Python, **une fonction est un objet** comme une string ou un int.

## 1.3 Pourquoi c'est puissant

Trois avantages principaux :

**1. Code plus court et plus lisible** — pas besoin de définir des classes pour des traitements simples.

**2. Code plus réutilisable** — une fonction qui modifie une autre fonction peut être appliquée à n'importe quelle fonction.

**3. Code plus testable** — les fonctions pures (sans effets de bord) sont triviales à tester.

## 1.4 Les 5 concepts couverts par ce module

|Concept|Exo|À retenir|
|---|---|---|
|Lambda|ex0|Fonction anonyme one-liner|
|Higher-order|ex1|Fonctions qui prennent ou retournent des fonctions|
|Closures|ex2|Fonctions qui "se souviennent" de leur environnement|
|functools|ex3|Module stdlib avec reduce, partial, lru_cache, singledispatch|
|Decorators|ex4|Wrappers qui modifient le comportement d'une fonction|

---

# PARTIE 2 — Les 5 concepts en profondeur

## Concept 1 — Lambda (ex0)

### Qu'est-ce que c'est

Une **lambda** est une fonction **anonyme** (sans nom) écrite en une seule expression. Syntaxe :

```python
lambda <arguments>: <expression>
```

Équivalences :

```python
# Version classique (def)
def double(x):
    return x * 2

# Version lambda
double = lambda x: x * 2
```

Une lambda **retourne implicitement** la valeur de son expression. Tu ne peux pas mettre de `return`, ni d'instructions multi-lignes.

### Quand utiliser

Les lambdas brillent quand tu veux passer **une petite fonction en argument** à une autre fonction.

```python
# Trier par age (sans lambda)
def get_age(person):
    return person["age"]
people.sort(key=get_age)

# Trier par age (avec lambda) — plus court
people.sort(key=lambda p: p["age"])
```

C'est exactement ce que tu fais dans `artifact_sorter` :

```python
return sorted(artifacts, key=lambda a: a["power"], reverse=True)
```

### Limites

Une lambda ne peut faire qu'**une seule expression**. Pas de `if/else` multi-lignes, pas de boucles, pas d'assignations. Si tu as besoin de plus, utilise une `def`.

### Pourquoi le sujet impose les lambdas pour ex0

Pour te forcer à pratiquer le pattern. Dans la vraie vie, on alterne entre lambdas (pour les opérations simples) et `def` (pour les opérations complexes ou réutilisées). Mais pour apprendre, il faut savoir manier les deux.

## Concept 2 — Higher-order functions (ex1)

### Qu'est-ce que c'est

Une **higher-order function** est une fonction qui :

- prend une ou plusieurs **fonctions en argument**, OU
- **retourne** une fonction

Tu as déjà utilisé `map`, `filter`, `sorted(key=...)` : ce sont toutes des higher-order functions (elles prennent une fonction).

### Pourquoi c'est puissant

Tu peux **composer** des comportements sans écrire de classes ou de boucles. Exemple :

```python
def amplifier(spell, multiplier):
    def amplified(target, power):
        return spell(target, power * multiplier)
    return amplified

# Avec ça, tu peux créer une infinité de spells dérivés sans coder chaque variante :
mega_fireball = amplifier(fireball, 3)
hyper_fireball = amplifier(fireball, 10)
mega_heal = amplifier(heal, 3)
```

Tu **composes** des spells comme des Lego.

### Le concept de fonction qui retourne une fonction

Dans `power_amplifier`, tu vois :

```python
def power_amplifier(base_spell, multiplier):
    def amplified(target, power):
        return base_spell(target, power * multiplier)
    return amplified
```

`power_amplifier` ne fait **pas** le calcul lui-même. Elle **fabrique une nouvelle fonction** qui fera le calcul plus tard, avec le `multiplier` qu'on a passé.

C'est un pattern central en programmation fonctionnelle : on construit des fonctions à la volée, configurées avec des paramètres.

### `Callable` et `callable()`

- **`Callable`** : type hint qui dit "ce paramètre est une fonction (ou un truc appelable)". Import depuis `collections.abc` (pas `typing`, c'est déprécié).
- **`callable(obj)`** : built-in qui retourne `True` si `obj` est appelable, `False` sinon. Utile pour vérifier avant un appel.

```python
from collections.abc import Callable

def caller(f: Callable) -> str:
    if not callable(f):
        return "Not a function"
    return f()
```

## Concept 3 — Closures (ex2)

### Qu'est-ce que c'est

Une **closure** est une fonction **interne** qui **capture** des variables de la fonction **externe** qui l'a créée, et qui **persiste** ces variables même après que la fonction externe ait terminé.

Exemple basique :

```python
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

counter = make_counter()
counter()   # → 1
counter()   # → 2
counter()   # → 3
```

Bizarre, non ? `count` est défini dans `make_counter()`, qui a **terminé son exécution** après le `return increment`. Normalement, `count` devrait avoir disparu de la mémoire. Mais non : la fonction `increment` "se souvient" de `count` parce qu'elle l'a **capturé** dans sa closure.

### Pourquoi ça marche

Quand Python crée la fonction `increment`, il détecte qu'elle utilise une variable (`count`) de la fonction enveloppante. Au lieu de la libérer à la fin de `make_counter`, Python l'attache à `increment` dans une structure spéciale (`__closure__`).

Chaque appel à `make_counter()` crée **un nouveau `count` indépendant**. C'est pour ça que :

```python
counter_a = make_counter()
counter_b = make_counter()
counter_a()   # → 1
counter_a()   # → 2
counter_b()   # → 1   ← son propre count, séparé
```

### Le mot-clé `nonlocal`

Sans `nonlocal`, Python pense que tu **crées** une nouvelle variable locale quand tu fais `count += 1`. Du coup, il essaie de faire `count = count + 1` avec un `count` local qui n'existe pas encore → `UnboundLocalError`.

`nonlocal count` dit à Python : "non, c'est la variable `count` de la fonction enveloppante, modifie-la directement".

C'est **l'inverse** de `global` :

- `global` : modifier une variable de portée **module** (déconseillé, c'est de la pollution)
- `nonlocal` : modifier une variable de portée **fonction enveloppante** (totalement OK, c'est le pattern closure)

Le sujet **interdit `global` mais autorise `nonlocal`** parce que `nonlocal` est confiné à la closure (proprement encapsulé), alors que `global` pollue tout le module.

### Cas d'usage des closures

- Compteurs / accumulateurs avec état privé (sans classes)
- Factories de fonctions (`enchantment_factory` qui produit une fonction par type d'enchantement)
- Encapsulation de données privées (le `storage` de `memory_vault` n'est accessible que via `store` et `recall`)
- Pré-configuration de fonctions (similar à `functools.partial`, qu'on voit en ex3)

## Concept 4 — functools (ex3)

### Qu'est-ce que c'est

`functools` est un **module de la stdlib** Python qui fournit des outils pour la programmation fonctionnelle. Le module est massif, mais l'ex3 te demande 4 outils précis :

### `functools.reduce(func, iterable)`

**Réduit** une liste à une seule valeur en appliquant la fonction de manière cumulative :

```python
from functools import reduce
import operator

reduce(operator.add, [1, 2, 3, 4])   # → 10 (1+2+3+4)
reduce(operator.mul, [1, 2, 3, 4])   # → 24 (1*2*3*4)
```

Conceptuellement :

```
[1, 2, 3, 4] → 1+2=3 → 3+3=6 → 6+4=10
```

C'est le pattern **fold** en programmation fonctionnelle. Très utilisé pour agréger des données.

### `functools.partial(func, *args)`

**Pré-remplit** certains arguments d'une fonction et retourne une nouvelle fonction qui prend les arguments restants :

```python
from functools import partial

def greet(salutation, name):
    return f"{salutation}, {name}!"

hello = partial(greet, "Hello")
hello("Alice")   # → "Hello, Alice!"

bonjour = partial(greet, "Bonjour")
bonjour("Bob")   # → "Bonjour, Bob!"
```

Utilité : **spécialiser** des fonctions génériques. Tu prends une fonction qui prend 3 paramètres, tu en fixes 2, et tu as une nouvelle fonction qui prend 1 paramètre.

C'est conceptuellement proche des closures (les deux pré-configurent des fonctions), mais `partial` est plus concis.

### `functools.lru_cache`

**Décorateur** qui met en cache les résultats d'une fonction. Si on rappelle la fonction avec les mêmes arguments, elle ne re-calcule pas — elle ressort le résultat du cache.

```python
@functools.lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(50)   # rapide, calcul ~50 fois
# Sans @lru_cache : 2^50 = 10^15 appels récursifs → secondes/minutes
```

**LRU** = Least Recently Used : si le cache est plein, on jette l'entrée la moins récemment utilisée. Avec `maxsize=None`, le cache est illimité.

Tu peux inspecter le cache avec `fibonacci.cache_info()` qui te dit combien de hits, miss, etc.

### `functools.singledispatch`

Décorateur qui implémente le pattern **dispatch sur type** : selon le type du premier argument, la fonction appelle une implémentation différente.

```python
@functools.singledispatch
def process(value):
    return f"Unknown type: {type(value).__name__}"

@process.register
def _(value: int):
    return f"Int: {value * 2}"

@process.register
def _(value: str):
    return f"String: {value.upper()}"

process(5)        # → "Int: 10"
process("hi")     # → "String: HI"
process([1, 2])   # → "Unknown type: list"
```

C'est comme une "polymorphie de fonction" sans avoir besoin de classes. Très propre.

## Concept 5 — Decorators (ex4)

### Qu'est-ce que c'est

Un **décorateur** est une fonction qui **prend une fonction en argument** et **retourne une nouvelle fonction** qui ajoute du comportement avant/après/autour de l'originale.

Tu en as déjà utilisé : `@functools.lru_cache`, `@staticmethod`, `@property`, `@model_validator`...

### La syntaxe `@`

Quand tu écris :

```python
@my_decorator
def hello():
    return "Bonjour"
```

C'est **strictement équivalent à** :

```python
def hello():
    return "Bonjour"
hello = my_decorator(hello)
```

Le `@` est juste du sucre syntaxique. Le décorateur **remplace** la fonction par sa version "décorée".

### Anatomie d'un décorateur simple

```python
import functools

def spell_timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Casting {func.__name__}...")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result
    return wrapper

@spell_timer
def fireball(target):
    time.sleep(0.1)
    return f"Fireball cast on {target}!"

fireball("Goblin")
# → "Casting fireball..."
# → "Spell completed in 0.101 seconds"
# → "Fireball cast on Goblin!"
```

Le décorateur **enveloppe** la fonction originale dans un `wrapper`. Le `wrapper` fait des trucs avant l'appel, appelle la fonction, fait des trucs après, et retourne le résultat.

### `*args, **kwargs`

`*args` capture **tous les arguments positionnels** dans un tuple. `**kwargs` capture **tous les arguments nommés** dans un dict.

C'est essentiel dans les décorateurs : tu ne sais pas à l'avance combien d'arguments la fonction décorée va prendre. Avec `*args, **kwargs`, ton wrapper accepte **tout**.

### `functools.wraps`

Sans `@functools.wraps(func)`, le wrapper "écrase" les méta-données de la fonction originale :

```python
def my_deco(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_deco
def hello():
    """Dit bonjour"""
    pass

print(hello.__name__)    # → "wrapper"   ← ah, ça aurait dû être "hello"
print(hello.__doc__)     # → None        ← perdu la docstring
```

`@functools.wraps(func)` copie le nom, la docstring, les annotations, etc. de la fonction originale sur le wrapper. C'est une **bonne pratique systématique** dans les décorateurs.

### Décorateurs paramétrés

Si tu veux que ton décorateur prenne des arguments (comme `@retry_spell(max_attempts=3)`), tu as besoin d'**un niveau supplémentaire d'imbrication** :

```python
def retry_spell(max_attempts):           # 1. factory qui reçoit le param
    def decorator(func):                  # 2. décorateur réel
        @functools.wraps(func)
        def wrapper(*args, **kwargs):     # 3. wrapper qui exécute
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    pass
            return "Failed"
        return wrapper
    return decorator

@retry_spell(max_attempts=3)
def unstable():
    raise RuntimeError("oops")
```

Trois niveaux :

1. `retry_spell(max_attempts)` — appelée avec le param
2. `decorator(func)` — appelée par Python avec la fonction
3. `wrapper(*args, **kwargs)` — appelée quand on invoque la fonction décorée

### `@staticmethod`

Méthode de classe qui **n'a pas besoin de `self`**. C'est essentiellement une fonction normale qu'on range dans une classe pour des raisons d'organisation.

```python
class MageGuild:
    @staticmethod
    def validate_mage_name(name):
        return len(name) >= 3

# Appelable sans instance :
MageGuild.validate_mage_name("Alex")   # → True

# Aussi appelable avec une instance :
g = MageGuild()
g.validate_mage_name("Alex")   # → True (mais inutile)
```

Tu utilises `@staticmethod` quand une méthode est "logiquement liée à la classe" mais n'utilise ni `self` ni l'état de l'instance.

---

# PARTIE 3 — Walkthrough rapide des exercices

## ex0/lambda_spells.py

4 fonctions qui démontrent **lambda + built-ins** (`sorted`, `filter`, `map`, `max`, `min`).

Points clés :

- `sorted(..., key=lambda a: a["power"], reverse=True)` → tri descendant par power
- `filter(...)` retourne un itérateur, on le convertit en liste avec `list()`
- `map(...)` idem
- Pour `mage_stats`, on utilise `max(mages, key=lambda m: m["power"])` qui retourne le **dict complet** du mage le plus puissant, puis `["power"]` pour extraire la valeur

## ex1/higher_magic.py

4 fonctions qui prennent/retournent des fonctions, plus 3 spells de démo (`fireball`, `heal`, `shield`).

Le pattern systématique :

```python
def my_higher_order(some_func):
    def inner(target, power):
        # utilise some_func ici
        return ...
    return inner
```

Tout repose sur la **fonction interne** qui capture la fonction passée en argument.

## ex2/scope_mysteries.py

4 fonctions qui utilisent les closures.

Points subtils :

- `mage_counter` doit retourner 1 au premier appel → initialise `count = 0` et fait `count += 1` AVANT le `return count`
- `nonlocal count` est obligatoire pour modifier `count` depuis l'inner function
- `memory_vault` retourne un **dict de deux closures** qui partagent toutes les deux le même `storage` (encapsulation parfaite : `storage` n'est accessible que par `store` et `recall`)

## ex3/functools_artifacts.py

Démonstration des 4 outils functools clés :

- `spell_reducer` : `reduce` + `operator` + dict de mapping pour les opérations
- `partial_enchanter` : `partial` pour pré-remplir power et element
- `memoized_fibonacci` : décoré avec `@lru_cache`, récursion naturelle
- `spell_dispatcher` : `@singledispatch` + `@dispatch.register` pour chaque type

## ex4/decorator_mastery.py

3 décorateurs + 1 classe avec `@staticmethod`.

Les 3 décorateurs sont de complexité croissante :

- `spell_timer` : décorateur **simple** (un seul niveau)
- `power_validator(min_power)` : décorateur **paramétré** (deux niveaux)
- `retry_spell(max_attempts)` : décorateur paramétré avec **gestion d'erreurs** dans le wrapper

La classe `MageGuild` montre `@staticmethod` (méthode sans self) et un décorateur appliqué à une méthode d'instance.

---

# PARTIE 4 — Préparation à la défense

## Q1 : C'est quoi une lambda ?

Une lambda est une fonction anonyme one-liner. Syntaxe : `lambda x, y: x + y`. Elle retourne implicitement la valeur de son expression. Idéale pour des opérations courtes passées en argument à `sorted`, `map`, `filter`. Pour de la logique complexe ou réutilisée, on préfère une `def` classique.

## Q2 : Quand utiliser lambda vs def ?

**Lambda** :

- Opération courte (une seule expression)
- Usage unique (passée en argument et oubliée)
- Code clair quand inline

**def** :

- Logique multi-lignes ou conditionnelle complexe
- Fonction réutilisée plusieurs fois
- Tu as besoin de docstring ou de type hints détaillés
- Tu as besoin de l'appeler récursivement

## Q3 : C'est quoi une higher-order function ?

C'est une fonction qui prend une fonction en argument OU qui retourne une fonction. C'est rendu possible par le fait que les fonctions sont des **first-class citizens** en Python : on peut les manipuler comme n'importe quelle valeur.

Exemples standards : `map`, `filter`, `sorted` (qui prennent une fonction), et les **décorateurs** (qui retournent une fonction).

## Q4 : Pourquoi les fonctions sont "first-class citizens" en Python ?

Parce qu'on peut :

1. Les **assigner** à des variables
2. Les **passer en argument**
3. Les **retourner** depuis d'autres fonctions
4. Les **stocker** dans des structures de données (liste, dict)

C'est exactement le même traitement que pour les strings, les ints, les listes. Une fonction est un objet comme un autre.

## Q5 : D'où vient `Callable` et à quoi sert `callable()` ?

- **`Callable`** est importé depuis `collections.abc` (`from collections.abc import Callable`). C'est un **type hint** pour annoter qu'un paramètre attend une fonction. Avant Python 3.9, on l'importait depuis `typing`, mais c'est déprécié.
- **`callable(obj)`** est un **built-in** qui retourne `True` si `obj` peut être appelé (avec des parenthèses), `False` sinon. Utile pour vérifier qu'un objet est appelable avant d'essayer.

## Q6 : C'est quoi une closure ?

Une closure est une fonction interne qui **capture** des variables de la fonction enveloppante et qui les **garde en mémoire** même après que la fonction enveloppante ait terminé son exécution.

```python
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment
```

`increment` est une closure : elle se souvient de `count` même quand `make_counter` est terminée. Chaque appel à `make_counter` crée une closure indépendante avec son propre `count`.

## Q7 : Pourquoi `nonlocal` et pas `global` ?

- **`global`** modifie une variable de portée module. C'est dangereux : pollution globale, état partagé entre tout le programme, difficile à tracer.
- **`nonlocal`** modifie une variable de la fonction **enveloppante**, pas du module. C'est confiné à la closure, encapsulé proprement.

Le sujet interdit `global` parce que ça casse le paradigme fonctionnel (pas d'état global). Il autorise `nonlocal` parce que c'est l'outil idiomatique pour les closures.

## Q8 : C'est quoi `functools.reduce` ?

`reduce(func, iterable)` applique `func` cumulativement aux éléments de l'iterable, de gauche à droite, pour réduire la liste à une seule valeur.

```python
reduce(lambda a, b: a + b, [1, 2, 3, 4])
# → ((1+2)+3)+4 = 10
```

C'est le pattern **fold** en programmation fonctionnelle. Utile pour agréger : somme, produit, max, concaténation de strings, etc.

## Q9 : C'est quoi `functools.partial` ?

`partial(func, *args)` pré-remplit certains arguments d'une fonction et retourne une nouvelle fonction qui prend les arguments restants.

```python
add = lambda a, b: a + b
add5 = partial(add, 5)
add5(10)   # → 15 (équivalent de add(5, 10))
```

C'est utile pour **spécialiser** des fonctions génériques sans réécrire de code.

## Q10 : C'est quoi `functools.lru_cache` ?

C'est un décorateur qui met en cache les résultats d'une fonction. Si on rappelle la fonction avec les mêmes arguments, elle retourne le résultat du cache au lieu de recalculer.

Bénéfices :

- **Performance massive** sur des fonctions récursives (Fibonacci passe de O(2^n) à O(n))
- **Trivial à activer** : juste `@lru_cache(maxsize=None)` au-dessus de la fonction

LRU = Least Recently Used. Si on met `maxsize=N`, le cache jette l'entrée la plus ancienne quand il dépasse N entrées.

## Q11 : C'est quoi un décorateur ?

Un décorateur est une fonction qui prend une fonction en argument et retourne une nouvelle fonction "améliorée". Syntaxe avec `@` :

```python
@my_decorator
def hello():
    return "hi"

# Équivaut à :
def hello():
    return "hi"
hello = my_decorator(hello)
```

Les décorateurs permettent d'ajouter des comportements (logging, timing, validation, retry, caching) **sans modifier** la fonction originale. C'est la **séparation des préoccupations** en action.

## Q12 : Comment ça marche un décorateur paramétré ?

C'est un décorateur qui prend des arguments. Trois niveaux d'imbrication :

```python
def retry(max_attempts):                  # 1. factory de décorateur
    def decorator(func):                   # 2. décorateur réel
        def wrapper(*args, **kwargs):      # 3. wrapper qui exécute
            for _ in range(max_attempts):
                ...
        return wrapper
    return decorator

@retry(max_attempts=3)
def f(): ...
```

`retry(3)` retourne `decorator`. Python applique `decorator` à `f`. `decorator` retourne `wrapper`. Quand on appelle `f()`, c'est en fait `wrapper()` qui s'exécute.

## Q13 : À quoi sert `functools.wraps` ?

À **préserver les métadonnées** de la fonction originale (nom, docstring, annotations) sur le wrapper du décorateur. Sans `@functools.wraps(func)`, si tu décores `def hello()`, après décoration `hello.__name__` devient `'wrapper'` au lieu de `'hello'`.

C'est important pour le debug, la documentation auto-générée, et les outils qui inspectent les métadonnées (comme Flask).

## Q14 : C'est quoi `@staticmethod` ?

C'est un décorateur qui marque une méthode comme **statique** : elle n'a pas de `self`, elle n'accède pas à l'instance ni à la classe. C'est essentiellement une fonction normale logiquement groupée dans une classe.

```python
class Math:
    @staticmethod
    def add(a, b):
        return a + b

Math.add(2, 3)   # → 5 (pas besoin d'instance)
```

On l'utilise quand une fonction est conceptuellement liée à la classe mais n'a pas besoin d'accéder à `self`.

## Q15 : Différence entre `@staticmethod`, `@classmethod`, et méthode normale ?

- **Méthode normale** : reçoit `self` (l'instance), peut lire/modifier l'état de l'instance
- **`@classmethod`** : reçoit `cls` (la classe), pas l'instance. Utile pour les factory methods
- **`@staticmethod`** : reçoit rien de spécial, juste les arguments passés. Pure organisation

## Q16 : Comment les décorateurs permettent la séparation des concerns ?

Les décorateurs te permettent de **séparer** la logique métier (ce que fait la fonction) de l'**infrastructure** (logging, timing, validation, retry, caching).

Sans décorateurs, ta fonction `cast_spell` mélangerait :

- La logique du sort
- Le timing (pour mesurer la perf)
- La validation (power suffisant)
- Le retry (si ça plante)
- Le logging (pour debug)

Avec décorateurs :

```python
@spell_timer
@power_validator(min_power=10)
@retry_spell(max_attempts=3)
def cast_spell(power, spell_name):
    # JUSTE la logique du sort, pas le reste
    ...
```

Chaque préoccupation est dans son propre décorateur, **réutilisable** sur d'autres fonctions. C'est plus propre, plus testable, plus maintenable.

## Q17 : C'est quoi `functools.singledispatch` ?

C'est un décorateur qui implémente le **pattern dispatch sur type** : selon le type du premier argument, la fonction appelle une implémentation différente.

```python
@singledispatch
def handle(x):
    return "default"

@handle.register
def _(x: int): return "int"

@handle.register
def _(x: str): return "string"
```

C'est une alternative fonctionnelle aux longues chaînes de `isinstance` ou aux hierarchies de classes. Plus propre et plus extensible.

---

# Conclusion

Le module 10 est le **plus dense** de la série, mais ces patterns sont **omniprésents** en Python pro :

- Flask, Django, FastAPI utilisent **massivement** les décorateurs
- React et Vue utilisent des concepts proches des closures
- pandas et NumPy s'appuient sur `map`, `filter`, `reduce` pour le data processing
- pytest utilise des décorateurs partout (`@pytest.fixture`, `@pytest.mark.parametrize`)

Si tu retiens trois choses pour la défense :

1. **Lambda + higher-order + closures** = la base. Les fonctions sont des valeurs comme les autres.
2. **functools** = les outils puissants stdlib pour la prog fonctionnelle.
3. **Decorators** = pattern de séparation des concerns ultra-utilisé en pro.

Tu as fini ton blackhole. Bravo. Bonne défense.