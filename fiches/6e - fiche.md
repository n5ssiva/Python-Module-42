# Module 06 — Cours complet sur les imports Python

## Comment lire ce document

Tu lis dans l'ordre, du début à la fin. Chaque section s'appuie sur la précédente. Si tu sautes, tu vas être perdu. À la fin, tu dois être capable de répondre à n'importe quelle question de ta défense — pas juste réciter le code.

Le document est divisé en 4 grandes parties :

1. **Le modèle mental** — ce qu'il faut comprendre AVANT de regarder du code
2. **Les 4 mystères du sujet, expliqués en profondeur**
3. **Walkthrough du projet, fichier par fichier**
4. **Préparation à la défense** — questions probables avec réponses

---

# PARTIE 1 — Le modèle mental

## 1.1 Pourquoi les imports existent

Tu écris du code. Au début, tu mets tout dans un seul fichier `main.py`. Ça marche pour 50 lignes. À 500 lignes, c'est ingérable. À 5000, c'est mort.

Donc tu **découpes** ton code en plusieurs fichiers. Chaque fichier fait une chose. Mais maintenant t'as un problème : comment le fichier `main.py` utilise une fonction définie dans `utils.py` ?

C'est ça que les imports résolvent. Un import = "va chercher du code dans un autre fichier et rends-le disponible ici".

C'est tout. C'est pas magique. C'est juste un mécanisme pour **partager du code entre fichiers**.

## 1.2 Module vs Package

Deux mots à ne JAMAIS confondre.

**Module** = un seul fichier `.py`. Un module = un fichier. Un fichier = un module.

- `elements.py` est un module.
- `potions.py` est un module.

**Package** = un dossier qui contient des modules ET un fichier spécial qui s'appelle `__init__.py`.

- `alchemy/` est un package, parce qu'il contient `__init__.py`.
- `alchemy/grimoire/` est un package (sous-package d'`alchemy`).

Pourquoi ce truc bizarre `__init__.py` ? Parce que sans lui, Python ne sait pas que ton dossier est un package qu'il peut importer. Avec lui, Python dit "ah ok, ce dossier est un package, je peux faire `import alchemy`".

> **Note** : depuis Python 3.3, les dossiers sans `__init__.py` peuvent aussi être importés (c'est ce qu'on appelle des "namespace packages"). Mais à 42, et dans 99% des projets pros, on garde toujours `__init__.py`. C'est plus propre, plus explicite, et ça permet de contrôler ce qui est exposé.

## 1.3 Ce qui se passe vraiment quand tu fais `import`

C'est LA section la plus importante du document. Si tu comprends ça, tu comprends 80% du projet.

Imagine que tu lances `python3 ft_alembic_4.py` qui contient juste :

```python
import alchemy
```

Voici ce que Python fait, étape par étape, dans l'ordre :

**Étape 1** : Python regarde dans `sys.modules`, qui est un **dictionnaire global** où il garde la trace de tous les modules déjà chargés. Est-ce qu'`alchemy` est déjà dedans ? Non, première fois.

**Étape 2** : Python cherche un dossier ou un fichier qui s'appelle `alchemy` dans `sys.path`. `sys.path` est une **liste de chemins** où Python va fouiller. Cette liste contient (dans l'ordre) :

1. Le dossier du script qu'on vient de lancer (donc le dossier où se trouve `ft_alembic_4.py`)
2. Les chemins de la variable d'environnement `PYTHONPATH`
3. Les dossiers d'install standards de Python (où sont `os`, `sys`, etc.)

Python trouve un dossier `alchemy/` dans le dossier courant. Bingo.

**Étape 3** : Comme c'est un dossier, Python crée un objet "module" vide nommé `alchemy`, le met dans `sys.modules['alchemy']`, et commence à **exécuter** `alchemy/__init__.py` ligne par ligne, comme un script normal.

**Étape 4** : Pendant que `__init__.py` s'exécute, chaque `def`, `import`, ou affectation crée des **attributs** dans cet objet module. À la fin, `sys.modules['alchemy']` contient tous les noms qui ont été définis ou importés dans `__init__.py`.

**Étape 5** : Python lie le nom local `alchemy` (dans le script appelant) à l'objet module. T'as maintenant accès à `alchemy.X` pour chaque `X` qui était dans `__init__.py`.

**C'est tout.** Un import, c'est :

1. Cherche dans `sys.modules` (cache)
2. Sinon trouve le fichier dans `sys.path`
3. Exécute le fichier
4. Stocke le résultat dans `sys.modules`
5. Lie un nom local

Si tu retiens qu'**une seule chose** de ce document, retiens ces 5 étapes.

## 1.4 La différence entre `import x` et `from x import y`

C'est la même mécanique des 5 étapes, mais ce qui est lié au nom local est différent.

```python
import alchemy
# alchemy = l'objet module entier
# Tu accèdes à ses fonctions via alchemy.create_air()

from alchemy import create_air
# Python charge alchemy comme avant (5 étapes)
# Puis prend SEULEMENT create_air de dans, et le lie au nom local
# Tu accèdes à create_air() directement, sans préfixe

import alchemy.elements
# Python charge alchemy puis alchemy.elements
# Le nom local 'alchemy' est lié au package, alchemy.elements est accessible
# Tu fais alchemy.elements.create_earth()

from alchemy.elements import create_earth
# Charge alchemy puis alchemy.elements
# Lie create_earth localement
# Tu fais create_earth()
```

**Point crucial** : `from x import y` fait **toujours** d'abord un `import x` complet (toutes les 5 étapes). La différence est juste ce qui est mis dans ton namespace local après.

## 1.5 Pourquoi `sys.modules` est un cache

`sys.modules` est un dictionnaire qui survit pendant toute l'exécution du programme. La première fois qu'on fait `import alchemy`, ça déclenche les 5 étapes. Mais la deuxième fois ?

```python
import alchemy        # déclenche les 5 étapes
import alchemy        # JUSTE l'étape 1 et 5 — étape 1 trouve alchemy dans sys.modules, donc on saute 2/3/4
```

Ça veut dire :

- Les imports sont **rapides** quand on les répète (utile, parce qu'on importe partout)
- Le code de `__init__.py` ne s'exécute **qu'une seule fois**, même si 50 fichiers font `import alchemy`
- C'est ce mécanisme qui causera notre problème de circular import (on en parle plus loin)

## 1.6 Imports absolus vs relatifs

C'est juste deux **syntaxes** pour écrire le chemin du module à importer. Le résultat est le même.

**Absolu** = chemin complet depuis la racine du projet :

```python
from alchemy.elements import create_air
from alchemy.grimoire.light_spellbook import light_spell_record
```

**Relatif** = chemin depuis le package où on se trouve actuellement :

```python
# Si on est dans alchemy/transmutation/recipes.py
from .recipes import xxx           # même dossier (transmutation/)
from ..potions import strength_potion   # dossier parent (alchemy/)
from ..elements import create_air      # dossier parent (alchemy/)
```

Le `.` représente le package courant. Le `..` représente le package parent.

**Quand utiliser quoi ?**

- **Imports absolus** : par défaut. C'est ce que recommande PEP 8. Plus clair, plus explicite.
- **Imports relatifs** : à l'intérieur d'un package, quand tu sais que les fichiers vont rester ensemble. Avantage : si tu renommes le package, tu n'as pas à changer tes imports internes.

**Règle absolue qui te sauvera des heures** : les imports relatifs **ne marchent PAS dans un script lancé directement**. Ils ne marchent que dans un fichier qui fait partie d'un package.

```python
# Si tu lances python3 mon_script.py
# et que mon_script.py contient :
from .truc import x
# → ImportError: attempted relative import with no known parent package
```

C'est pour ça que dans le projet :

- Les fichiers `ft_*.py` à la racine utilisent **toujours** des imports absolus
- Les fichiers à l'intérieur d'`alchemy/` peuvent utiliser des relatifs

## 1.7 Le rôle exact d'`__init__.py`

C'est le fichier qui s'exécute quand on fait `import nom_du_package`. Il a 3 rôles principaux :

**Rôle 1 — Marquer le dossier comme package**. Sans lui (à 42), le dossier n'est pas reconnu comme package.

**Rôle 2 — Définir l'API publique**. Tout ce qui est défini ou importé dans `__init__.py` devient accessible via `package.X`. Ce qui n'y est pas... n'est pas accessible directement.

```python
# alchemy/__init__.py
from .elements import create_air
# create_earth NON importé ici exprès
```

```python
import alchemy
alchemy.create_air()    # ✅ marche
alchemy.create_earth()  # ❌ AttributeError, pas exposé
```

**Mais attention** : "pas exposé" ne veut pas dire "inaccessible". Ça veut dire "pas accessible **par cette voie**". Tu peux toujours faire :

```python
from alchemy.elements import create_earth   # ✅ accès direct au fichier
```

L'`__init__.py` ne **bloque** rien. Il choisit juste ce qui est facile d'accès via le nom du package.

**Rôle 3 — Code d'initialisation**. Si ton package a besoin d'exécuter du code au chargement (ouvrir un fichier de config, vérifier qu'une lib est installée, etc.), c'est dans `__init__.py` que ça va.

## 1.8 Les alias

Un alias = un autre nom pour la même chose. Syntaxe : `as`.

```python
from alchemy.potions import healing_potion as heal
```

Maintenant `heal` et `healing_potion` désignent **la même fonction**. C'est pratique pour :

- Raccourcir un nom long (`numpy as np`, classique)
- Renommer pour éviter un conflit avec un autre nom
- Créer une API publique avec des noms différents des noms internes (notre cas dans le projet)

Dans `alchemy/__init__.py` du projet :

```python
from .potions import healing_potion as heal
```

→ après `import alchemy`, on appelle `alchemy.heal()`. La fonction interne s'appelle toujours `healing_potion` dans `potions.py`, mais on l'expose comme `heal` dans l'API du package.

## 1.9 Les imports circulaires — le cauchemar

Dernier concept fondamental avant de passer aux mystères.

Imagine deux fichiers qui ont besoin l'un de l'autre :

```python
# A.py
from B import truc

def chose():
    return "chose"
```

```python
# B.py
from A import chose

def truc():
    return "truc"
```

Tu lances `python3 A.py`. Que se passe-t-il ?

1. Python commence à exécuter `A.py`.
2. **Avant même d'exécuter `def chose()`**, il tombe sur `from B import truc`.
3. Pour résoudre ça, il doit charger `B`. Il commence à exécuter `B.py`.
4. **Première ligne de `B.py`** : `from A import chose`.
5. Python regarde `sys.modules`, trouve `A`... mais `A` est encore en train d'être chargé. Il est dans `sys.modules` mais il est **partiellement initialisé** : à ce stade, `def chose()` n'a même pas encore été exécuté.
6. Python tente quand même : "donne-moi `chose` dans le module `A` partiellement chargé". Mais `chose` n'existe pas encore dans `A`.
7. **`ImportError: cannot import name 'chose' from partially initialized module 'A'`**.

C'est exactement le bug de `dark_spellbook` ↔ `dark_validator` du projet.

**Comment éviter ça ?** Trois techniques :

**Technique 1 — Import local (dans la fonction)**

Au lieu d'importer en haut du fichier, importe à l'intérieur de la fonction qui en a besoin :

```python
# light_validator.py
def validate_ingredients(ingredients):
    from .light_spellbook import light_spell_allowed_ingredients  # ← ici, pas en haut
    allowed = light_spell_allowed_ingredients()
    ...
```

Pourquoi ça marche ? Parce que l'import ne s'exécute **plus au chargement** du module. Il s'exécute seulement quand on **appelle** la fonction. Et quand on appelle la fonction, les deux modules ont eu le temps d'être complètement chargés. Plus de problème de "partiellement initialisé".

C'est ce qu'on a fait dans le côté **light** du projet.

**Technique 2 — Restructurer le code**

Si A et B ont besoin l'un de l'autre, c'est souvent qu'il y a un truc partagé qui devrait être dans un troisième fichier C, que A et B importent. Plus de cycle.

**Technique 3 — `import module` au lieu de `from module import x`**

```python
# A.py
import B  # ← juste import, pas from
def chose():
    return B.truc()  # accès retardé
```

Pourquoi ça marche ? Parce que `import B` te donne juste une **référence** au module B, sans lire dedans. Tu touches à `B.truc` au moment de l'appel de `chose()`, pas au chargement. À ce moment-là, B est complètement chargé.

---

# PARTIE 2 — Les 4 mystères du sujet, en profondeur

Le sujet introduit le projet comme "les 4 mystères sacrés". Maintenant que t'as le modèle mental, je peux les expliquer correctement.

## Mystère 1 — Le pouvoir d'`__init__.py`

Couvert section 1.7. Récap :

- Sans `__init__.py`, pas de package (à 42 du moins)
- Avec `__init__.py`, tout ce qui est dedans devient accessible via `package.X`
- Ce qui n'est pas dedans n'est pas exposé via le nom du package, mais reste accessible via import direct
- C'est le mécanisme de contrôle d'API publique

**Démontré dans le projet par** : `ft_alembic_4.py` qui plante sur `alchemy.create_earth()` parce que `__init__.py` n'expose que `create_air`.

## Mystère 2 — Imports en cascade (modules distants depuis modules distants)

C'est le mystère le plus simple à comprendre une fois qu'on a le modèle mental. Un fichier peut en importer un autre, qui en importe un autre, etc. Python charge tout dans l'ordre, met chaque module dans `sys.modules`, et c'est bon.

**Démontré dans le projet par** :

- `potions.py` importe les éléments
- `recipes.py` importe `potions` ET les éléments
- L'`__init__.py` d'`alchemy` importe `potions`, qui à son tour importe ses éléments

Quand tu fais `import alchemy`, ça déclenche en cascade le chargement de `elements.py`, `potions.py`, `transmutation/__init__.py`, `transmutation/recipes.py`. Tout ça est résolu avant que `import alchemy` ne te rende la main.

**Question piège possible** : "Si je fais `import alchemy` deux fois, est-ce que `elements.py` est exécuté deux fois ?" Réponse : non. Grâce à `sys.modules`, chaque fichier n'est exécuté qu'une seule fois pour toute la durée du programme.

## Mystère 3 — Absolu vs relatif

Couvert section 1.6. Récap :

- Absolu = chemin complet depuis la racine
- Relatif = chemin depuis le package courant (`.` même niveau, `..` parent)
- Relatif ne marche que dans un package, pas dans un script lancé directement
- Par défaut on préfère absolu (PEP 8)
- Relatif utile pour la portabilité interne d'un package

**Démontré dans le projet par** : `recipes.py` qui utilise les deux exprès :

```python
from alchemy.elements import create_air      # absolu
from ..potions import strength_potion        # relatif
from elements import create_fire             # absolu (vers le elements.py racine)
```

Le sujet demande "au moins un absolu et un relatif". On en a trois en tout pour bien montrer.

## Mystère 4 — Casser les imports circulaires

Couvert section 1.9. Le projet illustre les deux côtés :

**Côté light** : on casse le cycle en mettant l'import **dans** la fonction. Ça marche.

**Côté dark** : on garde les imports en haut du fichier des deux côtés. Ça plante avec un `ImportError` "circular import" très explicite.

**Pourquoi le sujet demande de faire les deux ?** Pour que tu voies, dans le même projet, à la fois le piège ET la solution. Le côté light prouve que tu sais résoudre le problème ; le côté dark prouve que tu sais le reconnaître quand tu le vois ailleurs.

---

# PARTIE 3 — Walkthrough du projet, fichier par fichier

Maintenant on revisite le projet entier en sachant ce qu'on fait. Pour chaque fichier, je donne le **pourquoi**, pas juste le quoi.

## `elements.py` (racine)

```python
def create_fire() -> str:
    return "Fire element created"

def create_water() -> str:
    return "Water element created"
```

Module simple, à la racine. Important : il existe **aussi** un `alchemy/elements.py` complètement différent. Le sujet veut nous faire toucher du doigt cette ambiguïté : selon comment on importe, on tombe sur l'un ou l'autre.

Quand tu fais `import elements` depuis un script à la racine, tu prends celui-ci. Quand tu fais `import alchemy.elements`, tu prends l'autre.

## `alchemy/elements.py`

```python
def create_earth() -> str:
    return "Earth element created"

def create_air() -> str:
    return "Air element created"
```

Module à l'intérieur du package `alchemy`. Différent du `elements.py` racine. Contient les éléments "internes" au package.

## `alchemy/__init__.py` (version finale, après les 4 parties)

```python
# flake8: noqa: F401
from .elements import create_air
from .potions import healing_potion as heal
from .potions import strength_potion
from .transmutation import lead_to_gold
```

C'est la **vitrine** du package. Quatre choix volontaires :

1. `create_air` exposé, mais **pas** `create_earth` (pédagogique, pour `ft_alembic_4`)
2. `healing_potion` exposé sous le nom `heal` (alias)
3. `strength_potion` exposé directement
4. `lead_to_gold` exposé en remontant depuis le sous-package `transmutation`

Le `# flake8: noqa: F401` désactive l'avertissement "imported but unused", parce que techniquement on n'utilise pas ces imports dans `__init__.py` lui-même — on les importe pour les **réexporter**. C'est la convention standard.

## `alchemy/potions.py`

```python
from .elements import create_earth, create_air
from elements import create_fire, create_water

def healing_potion() -> str:
    return f"Healing potion brewed with '{create_earth()}' and '{create_air()}'"

def strength_potion() -> str:
    return f"Strength potion brewed with '{create_fire()}' and '{create_water()}'"
```

Ce fichier mélange exprès :

- Import **relatif** vers `alchemy/elements.py` : `from .elements import ...`
- Import **absolu** vers `elements.py` racine : `from elements import ...`

Pourquoi ça marche ? Parce que :

- L'import relatif `.elements` regarde dans le package courant (`alchemy/`) → trouve `alchemy/elements.py`
- L'import absolu `elements` regarde dans `sys.path`, qui contient le dossier où le script principal a été lancé (la racine) → trouve `elements.py`

Donc les **deux** elements.py coexistent, et `potions.py` a accès aux quatre éléments en piochant dans les deux.

## `alchemy/transmutation/__init__.py`

```python
# flake8: noqa: F401
from .recipes import lead_to_gold
```

Sous-package. Expose `lead_to_gold`. Court mais nécessaire — sans lui, `from alchemy.transmutation import lead_to_gold` ne marcherait pas.

## `alchemy/transmutation/recipes.py`

```python
from alchemy.elements import create_air      # absolute import
from ..potions import strength_potion         # relative import
from elements import create_fire              # absolute (root elements.py)

def lead_to_gold() -> str:
    return (
        f"Recipe transmuting Lead to Gold: brew '{create_air()}' "
        f"and '{strength_potion()}' mixed with '{create_fire()}'"
    )
```

Le fichier "vitrine" du mystère absolu vs relatif. Trois imports volontaires :

- `from alchemy.elements import create_air` — absolu vers un module **du même package** (`alchemy`)
- `from ..potions import strength_potion` — relatif depuis le sous-package, on remonte d'un cran (`..`) pour atteindre `alchemy/potions.py`
- `from elements import create_fire` — absolu vers le module **racine** `elements.py`

Note : on aurait pu écrire `from alchemy.potions import strength_potion` à la place du relatif, ça marcherait pareil. Le sujet demande **explicitement** au moins un absolu et un relatif, donc on garde les deux pour démonstration.

## `alchemy/grimoire/__init__.py`

```python
# flake8: noqa: F401
from .light_spellbook import light_spell_record
```

Expose **uniquement** la fonction de magie blanche. La magie noire reste accessible mais seulement par import direct du fichier — c'est ça que `ft_kaboom_1.py` simule (un accès "secret" qui contourne l'API officielle, et qui plante).

## `alchemy/grimoire/light_spellbook.py`

```python
from .light_validator import validate_ingredients

def light_spell_allowed_ingredients() -> list[str]:
    return ["earth", "air", "fire", "water"]

def light_spell_record(spell_name: str, ingredients: str) -> str:
    result = validate_ingredients(ingredients)
    if "VALID" in result and "INVALID" not in result:
        return f"Spell recorded: {spell_name} ({result})"
    return f"Spell rejected: {spell_name} ({result})"
```

Import en haut du fichier vers `light_validator`. Note bien : `light_spellbook` importe `light_validator`. C'est la moitié du cycle.

## `alchemy/grimoire/light_validator.py`

```python
def validate_ingredients(ingredients: str) -> str:
    # Local import inside the function to break the circular dependency.
    from .light_spellbook import light_spell_allowed_ingredients

    allowed = light_spell_allowed_ingredients()
    lower_ing = ingredients.lower()
    for item in allowed:
        if item in lower_ing:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
```

L'autre moitié du cycle. **Mais** l'import est dans la fonction, pas en haut. C'est ce qui sauve la mise.

Au moment où `light_spellbook` charge `light_validator`, ce dernier ne déclenche aucun import retour vers `light_spellbook`. Le validateur est juste défini, point. Quand on appelle plus tard `validate_ingredients()`, les deux modules existent, l'import dans la fonction marche. Pas de cycle.

## `alchemy/grimoire/dark_spellbook.py`

```python
from .dark_validator import validate_ingredients

def dark_spell_allowed_ingredients() -> list[str]:
    return ["bats", "frogs", "arsenic", "eyeball"]
...
```

Import en haut du fichier, comme light. Pas de problème ici tout seul.

## `alchemy/grimoire/dark_validator.py`

```python
from .dark_spellbook import dark_spell_allowed_ingredients

def validate_ingredients(ingredients: str) -> str:
    allowed = dark_spell_allowed_ingredients()
    ...
```

**Voilà le piège** : import en haut du fichier vers `dark_spellbook`. Donc :

- `dark_spellbook` veut importer `dark_validator`
- `dark_validator` veut importer `dark_spellbook` au chargement
- Cycle. Boom.

C'est exactement le même code que le côté light, **sauf** que l'import est en haut au lieu d'être dans la fonction. Cette différence d'une seule ligne change tout.

## Les fichiers `ft_*.py`

Tous suivent le même pattern : un `main()`, un `if __name__ == "__main__"`, des prints qui matchent les exemples du sujet. Pas de logique compliquée. Le but n'est pas le code des scripts, c'est de **prouver** que les imports marchent.

---

# PARTIE 4 — Préparation à la défense

Voilà les questions que les évaluateurs à 42 Bruxelles posent typiquement sur ce module, avec les réponses préparées. Lis-les. Reformule-les avec tes mots. Si tu ne comprends pas une réponse, retourne à la partie correspondante du cours.

## Q1 : C'est quoi un module ? Un package ? La différence ?

Un **module** est un fichier `.py`. C'est l'unité minimale d'organisation de code en Python. Un module = un fichier.

Un **package** est un dossier qui contient plusieurs modules, et qui contient un fichier `__init__.py`. Le package permet de regrouper plusieurs modules sous un même namespace.

Dans le projet : `elements.py` est un module. `alchemy/` est un package qui contient les modules `elements.py`, `potions.py`, et le sous-package `grimoire/`.

## Q2 : À quoi sert `__init__.py` ?

Trois choses :

1. **Marquer le dossier comme package** — sans lui, Python ne le reconnaît pas comme tel (en pratique, à 42 du moins)
2. **Définir l'API publique** — tout ce qui est défini ou importé dans `__init__.py` devient accessible directement via `nom_du_package.X`
3. **Contenir le code d'initialisation** — il s'exécute automatiquement la première fois qu'on importe le package

## Q3 : Que se passe-t-il quand je fais `import alchemy` ?

Python suit cette séquence :

1. Regarde dans `sys.modules` si `alchemy` est déjà chargé
2. Sinon, cherche un dossier ou fichier `alchemy` dans `sys.path`
3. Trouve `alchemy/`, crée un objet module vide, le met dans `sys.modules`
4. Exécute `alchemy/__init__.py` ligne par ligne
5. Lie le nom local `alchemy` à l'objet module

Tous les autres imports (`from alchemy import x`, `from alchemy.elements import x`, etc.) font la même séquence en plus de charger les sous-modules nécessaires.

## Q4 : Différence entre import absolu et import relatif ?

L'**absolu** donne le chemin complet depuis la racine du projet : `from alchemy.elements import create_air`.

Le **relatif** donne le chemin depuis le package courant en utilisant des points : `from .elements import create_air` (même niveau), `from ..potions import x` (niveau parent).

PEP 8 recommande l'absolu par défaut. Le relatif est utile à l'intérieur d'un package, parce qu'il survit au renommage du package. Important : le relatif **ne marche pas dans un script lancé directement**, seulement à l'intérieur d'un package.

## Q5 : Pourquoi `ft_alembic_4.py` plante sur `create_earth` ?

Parce que dans `alchemy/__init__.py`, on n'importe que `create_air` (`from .elements import create_air`). On n'importe **pas** `create_earth`. Donc quand on fait `import alchemy`, l'objet module `alchemy` a un attribut `create_air` mais pas `create_earth`. L'appel `alchemy.create_earth()` cherche cet attribut, ne le trouve pas, et lève `AttributeError`.

`create_earth` existe toujours dans `alchemy/elements.py`, mais il n'est pas exposé au niveau du package. On peut toujours y accéder via `from alchemy.elements import create_earth`, mais pas via `alchemy.create_earth`.

## Q6 : Qu'est-ce qu'un import circulaire ? Pourquoi ça plante ?

Deux modules qui s'importent mutuellement. Le problème : quand Python charge le premier module, dès qu'il tombe sur l'import vers le second, il commence à charger le second. Le second tente alors d'importer un nom du premier — mais le premier est encore en cours de chargement, **partiellement initialisé**. Le nom demandé n'existe peut-être pas encore. Python lève `ImportError: cannot import name 'X' from partially initialized module 'Y'`.

Dans le projet, c'est exactement ce qui arrive entre `dark_spellbook` et `dark_validator`.

## Q7 : Comment as-tu cassé le cycle dans le côté light ?

J'ai déplacé l'import de `light_spellbook` **à l'intérieur** de la fonction `validate_ingredients`, au lieu de le mettre en haut du fichier. Comme ça, l'import ne s'exécute pas au chargement du module — il s'exécute seulement quand on **appelle** la fonction. À ce moment-là, les deux modules ont eu le temps d'être complètement chargés, donc plus de problème.

## Q8 : Quelles autres techniques existent pour casser un import circulaire ?

Trois techniques principales :

1. **Import local dans la fonction** (ce que j'ai fait pour le light)
2. **Restructurer le code** — extraire ce qui est commun aux deux modules dans un troisième module qui ne dépend ni de l'un ni de l'autre
3. **Utiliser `import module` plutôt que `from module import x`** — `import` te donne juste une référence au module, sans lire dedans tout de suite. Tu accèdes à `module.x` au moment de l'appel, pas au chargement.

## Q9 : Pourquoi `# flake8: noqa: F401` dans tes `__init__.py` ?

flake8 lève l'avertissement F401 quand il voit un import qui n'est pas utilisé dans le fichier. Mais dans un `__init__.py`, c'est volontaire — on importe **pour réexposer**. Le commentaire `# flake8: noqa: F401` désactive cet avertissement spécifique. C'est la convention standard pour les `__init__.py` qui font de la réexportation.

## Q10 : Pourquoi y a-t-il une erreur mypy sur `ft_alembic_4.py` ?

L'erreur dit `Module has no attribute "create_earth"`. C'est mypy qui fait son boulot d'analyseur statique : il regarde `alchemy/__init__.py`, voit qu'on n'expose que `create_air`, donc déduit que `alchemy.create_earth` n'existe pas. Quand on l'utilise dans le script, il signale l'erreur.

Cette erreur est **volontaire** et explicitement annoncée par le sujet ("A mypy error will also raise, again, on purpose"). C'est pédagogique : ça montre que mypy peut détecter ce genre de problème avant l'exécution.

## Q11 : Que contient `sys.modules` ? À quoi ça sert ?

`sys.modules` est un dictionnaire global qui contient tous les modules déjà chargés dans le programme. Clé = nom du module, valeur = l'objet module.

Son rôle est d'agir comme **cache** : quand on fait un import, Python regarde d'abord là-dedans avant de relire le fichier depuis le disque. C'est ce qui rend les imports rapides quand on les répète, et c'est aussi ce qui garantit qu'un module n'est exécuté qu'une seule fois pendant toute la durée du programme.

C'est aussi ce qui pose le problème des imports circulaires : quand un module est en cours de chargement, il est déjà dans `sys.modules` mais partiellement initialisé.

## Q12 : Qu'est-ce que `sys.path` ?

C'est une liste de chemins où Python cherche les modules à importer. L'ordre dans la liste compte : Python prend le premier match.

Contenu typique :

1. Le dossier du script lancé (premier !)
2. Les chemins listés dans la variable d'environnement `PYTHONPATH`
3. Les dossiers d'installation standards de Python (où sont les modules built-in et les packages installés via pip)

Le sujet **interdit** de modifier `sys.path` — il faut que la structure du projet suffise à elle-même.

## Q13 : Si je supprime `__init__.py` d'`alchemy/`, que se passe-t-il ?

Depuis Python 3.3, le dossier deviendrait un "namespace package" implicite. Techniquement `import alchemy.elements` continuerait de marcher. Mais on perdrait :

- Le contrôle de l'API publique (le rôle de "vitrine" disparait)
- La possibilité d'écrire `from alchemy import create_air` (puisqu'on n'a plus de fichier où définir cet alias)
- La possibilité d'avoir du code d'initialisation

À 42, on garde toujours `__init__.py`. Plus explicite, plus contrôlable.

## Q14 : Comment fonctionne `import alchemy.transmutation.recipes` exactement ?

Python doit charger trois choses dans l'ordre :

1. `alchemy/__init__.py` (parce que `alchemy` est un package)
2. `alchemy/transmutation/__init__.py` (parce que `transmutation` est un sous-package)
3. `alchemy/transmutation/recipes.py` (le module final)

Chacun est mis dans `sys.modules` après son chargement. À la fin, le nom local `alchemy` dans le script appelant est lié à l'objet `alchemy`, et l'on peut accéder à `alchemy.transmutation.recipes.lead_to_gold()` en suivant la chaîne.

## Q15 : Pourquoi `recipes.py` peut-il faire à la fois `from alchemy.elements import create_air` et `from ..elements import create_air` ? (en théorie)

Parce que les deux désignent le **même** fichier (`alchemy/elements.py`). C'est juste deux chemins différents pour y aller :

- L'absolu navigue depuis la racine
- Le relatif navigue depuis le package courant en remontant d'un cran (`..`)

C'est comme dire "Bruxelles, Belgique" vs "ma ville, mon pays" quand on est à Bruxelles. Deux références au même endroit.

---

# Conclusion

Le module 06 est court mais conceptuellement dense. Une fois que tu as compris :

- Les 5 étapes d'un import
- Le rôle de `sys.modules` comme cache
- Le rôle d'`__init__.py` comme vitrine
- Le mécanisme exact d'un import circulaire

...tu as compris l'essentiel de la machinerie d'imports en Python. Ces concepts vont te resservir partout — projets pros, autres langages similaires (TypeScript a une logique très proche), debug de bugs bizarres dans tes futurs projets.

Si pendant la défense tu hésites sur une question, retombe sur les 5 étapes. La plupart des questions s'y ramènent.

Bonne défense.