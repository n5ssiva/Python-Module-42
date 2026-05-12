# Module 07 — Cours complet sur les design patterns en Python

## Comment lire ce document

Comme pour le module 06 : tu lis dans l'ordre. Si tu sautes, tu rates le modèle mental.

Le document est divisé en 4 parties :

1. **Le modèle mental — POO avancée en Python**
2. **Les 3 design patterns du projet, en profondeur**
3. **Walkthrough du projet, fichier par fichier**
4. **Préparation à la défense**

---

# PARTIE 1 — Le modèle mental

## 1.1 Pourquoi ce module existe

Tu as appris l'héritage simple : une classe enfant qui hérite d'une classe parente. Ça marche pour 80% des cas. Mais quand un système devient gros, l'héritage simple ne suffit plus.

Imagine : tu as 50 types de créatures. Certaines peuvent se soigner, certaines peuvent se transformer, certaines peuvent voler. Tu vas pas créer une hiérarchie en arbre rigide où chaque créature appartient à une seule branche — ça ne reflète pas la réalité (une créature pourrait soigner ET voler).

Les **design patterns** résolvent ces problèmes d'architecture. Ce sont des solutions standardisées à des problèmes récurrents. Le projet en couvre trois :

- **Abstract Factory** (ex0) — créer des objets sans coupler le code aux classes concrètes
- **Mixins via héritage multiple** (ex1) — composer des comportements indépendants
- **Strategy Pattern** (ex2) — découpler une logique variable du code qui l'utilise

## 1.2 Rappel : classe abstraite vs concrète

Une **classe concrète** = une classe que tu peux instancier directement. Tu fais `obj = MaClasse()` et ça marche.

Une **classe abstraite** = une classe qui sert de **modèle**, qu'on ne peut PAS instancier directement. Elle déclare des méthodes que ses sous-classes **doivent** implémenter. Elle dit "voici la forme attendue", sans donner l'implémentation.

En Python, on utilise le module `abc` (Abstract Base Classes) :

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def cri(self) -> str:
        pass

class Chien(Animal):
    def cri(self) -> str:
        return "Wouf!"

# Animal()   → TypeError: Can't instantiate abstract class Animal
# Chien()    → ✅ marche
# Chien().cri()  → "Wouf!"
```

**Pourquoi c'est utile ?** Parce que ça **force** les sous-classes à implémenter certaines méthodes. Si tu oublies `cri()` dans `Chat(Animal)`, Python te crie dessus à l'instanciation. C'est un **contrat** qu'on impose au code futur.

## 1.3 Polymorphisme — le concept central de la POO

Le polymorphisme c'est : "le même appel de méthode produit un comportement différent selon le type réel de l'objet".

```python
def faire_crier(animal: Animal) -> None:
    print(animal.cri())   # peu importe si c'est Chien, Chat, Vache...

faire_crier(Chien())   # Wouf!
faire_crier(Chat())    # Miaou!
```

La fonction `faire_crier` n'a **aucune idée** de quel animal elle reçoit. Elle sait juste qu'il a une méthode `cri()`. Chaque animal sait comment se comporter, et le code "haut niveau" reste générique.

**C'est LE principe du module 07.** Le `battle()`, le `tournament()`, n'ont aucune idée des créatures concrètes qu'ils manipulent. Ils manipulent des `Creature`, point. Le polymorphisme fait le reste.

## 1.4 Héritage multiple — le truc qui fait peur mais qui est utile

En Python (contrairement à Java), une classe peut hériter de **plusieurs classes parentes** :

```python
class Volant(ABC):
    @abstractmethod
    def voler(self) -> str: pass

class Nageant(ABC):
    @abstractmethod
    def nager(self) -> str: pass

class Canard(Volant, Nageant):
    def voler(self) -> str: return "Vol vol"
    def nager(self) -> str: return "Coin coin glou"
```

`Canard` hérite à la fois de `Volant` ET de `Nageant`. Il peut faire les deux. Aucune branche d'arbre principale.

**Important** : en Python, c'est totalement autorisé et idiomatique. Dans d'autres langages (Java, C#), c'est interdit pour les classes mais autorisé pour les interfaces.

### Le MRO (Method Resolution Order)

Quand une classe hérite de plusieurs parents, dans quel ordre Python cherche-t-il les méthodes en cas de conflit ? Il suit le **MRO**, une liste linéarisée des parents.

```python
class A:
    def f(self) -> str: return "A"

class B:
    def f(self) -> str: return "B"

class C(A, B):
    pass

C().f()    # → "A"  (A vient avant B dans (A, B))
C.__mro__  # → (C, A, B, object)
```

Python regarde dans `C`, puis `A`, puis `B`, puis `object`. Premier qui répond gagne.

**Dans notre projet**, on n'a pas ce problème parce que `Creature` et `HealCapability` n'ont aucune méthode en commun. Mais c'est une question piège possible en défense.

## 1.5 Mixins — l'usage propre de l'héritage multiple

Un **mixin** est une classe abstraite légère qui ajoute UN comportement spécifique, conçue pour être combinée avec d'autres classes.

Caractéristiques d'un bon mixin :

- Il n'est **pas** la classe principale dont on hérite, c'est un **complément**
- Il définit un comportement orthogonal (= indépendant du reste)
- Il peut être combiné avec différentes classes principales

Dans le module 07 :

- `Creature` est la classe principale (la base)
- `HealCapability`, `TransformCapability` sont des **mixins** ajoutant des capacités
- `Sproutling(Creature, HealCapability)` combine "être une créature" + "savoir soigner"

Le sujet est explicite : "capability abstract classes will not inherit from the Creature base class!". C'est exactement la définition d'un mixin : indépendant, combinable.

## 1.6 `isinstance()` et duck typing

`isinstance(obj, Classe)` te dit si `obj` est une instance de `Classe` ou d'une de ses sous-classes.

```python
class Animal: pass
class Chien(Animal): pass

c = Chien()
isinstance(c, Chien)    # True
isinstance(c, Animal)   # True  (Chien hérite d'Animal)
isinstance(c, str)      # False
```

**Avec l'héritage multiple**, `isinstance` te dit si l'objet hérite de la classe d'une façon ou d'une autre :

```python
class Sproutling(Creature, HealCapability): pass

s = Sproutling()
isinstance(s, Creature)          # True
isinstance(s, HealCapability)    # True  ← clé pour les stratégies !
```

Dans le projet, `DefensiveStrategy.is_valid()` fait :

```python
return isinstance(creature, HealCapability)
```

→ "Cette créature sait-elle se soigner ? Si oui, je peux l'utiliser."

C'est élégant. La stratégie ne demande pas "es-tu un Sproutling ou un Bloomelle" — elle demande "as-tu la **capacité** de soigner". Ça marche pour toutes les créatures futures qui hériteraient de `HealCapability`.

## 1.7 `super().__init__()` et héritage multiple

En héritage simple, `super().__init__()` appelle le `__init__` du parent. En héritage multiple, c'est plus subtil.

**Dans le projet, on fait explicitement** :

```python
class Shiftling(Creature, TransformCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Shiftling", "Normal")
        TransformCapability.__init__(self)
```

Au lieu de `super().__init__()`, on appelle **explicitement** les deux constructeurs. Pourquoi ? Parce que les deux classes prennent des arguments différents (`Creature` veut `name` et `ctype`, `TransformCapability` veut rien). Avec `super()`, c'est galère à coordonner.

L'appel explicite est plus clair et garanti de marcher.

## 1.8 Composition vs héritage

Vieux débat en POO : "favor composition over inheritance" (préfère la composition à l'héritage).

- **Héritage** = "EST-UN" relationship. Sproutling **est une** Creature.
- **Composition** = "A-UN" relationship. Une voiture **a un** moteur.

Le module 07 utilise les deux :

- Héritage : `Sproutling(Creature)` — "est une créature"
- Composition (via Strategy pattern) : une stratégie **a une** créature qu'elle fait agir. La stratégie n'hérite pas de la créature, elle la **manipule**.

C'est ce qui rend le Strategy pattern si flexible. Tu peux changer la stratégie sans changer la créature, et vice versa.

---

# PARTIE 2 — Les 3 design patterns du projet, en profondeur

## Pattern 1 — Abstract Factory (ex0)

### Le problème qu'il résout

Tu veux créer des objets, mais tu ne veux **pas que le code qui les utilise connaisse les classes concrètes**. Pourquoi ? Parce que si demain tu ajoutes un nouveau type, tu n'as pas envie de modifier tout ton code client.

Mauvaise approche :

```python
def fight():
    if game_mode == "fire":
        a = Flameling()
        b = Pyrodon()
    elif game_mode == "water":
        a = Aquabub()
        b = Torragon()
    # etc, à chaque nouveau type tu reviens ici
```

C'est moche, ça scale pas, ça duplique la logique.

### La solution Abstract Factory

Tu crées une **classe abstraite** `CreatureFactory` qui définit l'**interface** de création (`create_base`, `create_evolved`). Puis tu crées une factory concrète **par famille** : `FlameFactory`, `AquaFactory`. Chaque factory sait quels objets concrets créer.

Le code client manipule juste des `CreatureFactory` :

```python
def test_factory(factory: CreatureFactory) -> None:
    base = factory.create_base()
    evolved = factory.create_evolved()
    # le code ne sait pas si c'est Flame ou Aqua
```

Ajouter un nouveau type ? Tu crées juste une nouvelle factory. Le code client ne bouge pas. C'est le **principe ouvert/fermé** (Open/Closed Principle) — ouvert à l'extension, fermé à la modification.

### Pourquoi le sujet exige de ne pas exposer les classes concrètes

> "Your ex0 package cannot expose concrete Creature directly, it must only expose factories."

C'est l'**encapsulation** du pattern. Si on exposait `Flameling`, le code client pourrait faire `Flameling()` directement, contournant la factory. Le couplage reviendrait. En cachant les classes concrètes, on **force** le client à passer par les factories.

C'est pour ça que `ex0/__init__.py` n'expose **que** :

- `Creature` (la classe abstraite, nécessaire pour le typing)
- `CreatureFactory`, `FlameFactory`, `AquaFactory`

Pas `Flameling`, pas `Pyrodon`, etc.

## Pattern 2 — Mixins via héritage multiple (ex1)

### Le problème qu'il résout

Toutes les créatures partagent une base (nom, type, attaque). Mais certaines ont des **capacités additionnelles** orthogonales : se soigner, se transformer, voler...

Avec de l'héritage simple, tu serais coincé :

```
Creature
├── HealingCreature        ← ajout du heal()
│   ├── Sproutling
│   └── Bloomelle
└── TransformingCreature   ← ajout du transform()
    ├── Shiftling
    └── Morphagon
```

Mais si une créature peut **à la fois** se soigner ET se transformer ? Impossible avec ça.

### La solution Mixins

Tu sépares les capacités dans des **classes abstraites indépendantes** :

- `HealCapability` (mixin) — déclare `heal()`
- `TransformCapability` (mixin) — déclare `transform()`, `revert()`

Une créature concrète **combine** la classe principale `Creature` avec autant de mixins qu'elle veut :

```python
class Sproutling(Creature, HealCapability): ...
class Shiftling(Creature, TransformCapability): ...
class HypothéticPokemon(Creature, HealCapability, TransformCapability): ...
```

Chaque mixin est indépendant. Chaque créature compose les capacités dont elle a besoin.

### Pourquoi le sujet insiste sur "pas d'héritage de Creature"

> "capability abstract classes will not inherit from the Creature base class!"

Parce que si `HealCapability` héritait de `Creature`, on perdrait l'orthogonalité. La capacité serait couplée à la créature, et on retomberait dans le piège de l'héritage simple.

En gardant les mixins **indépendants** de `Creature`, on peut imaginer demain les utiliser pour **autre chose** (Items qui guérissent ? Sorts qui transforment ?). C'est ça que le sujet veut illustrer.

### L'astuce des `isinstance()`

Dans le tournoi, on ne sait pas à l'avance si une créature peut soigner. On teste :

```python
if isinstance(creature, HealCapability):
    creature.heal()
```

C'est du polymorphisme. On ne regarde pas le **type concret** de la créature (Sproutling ? Bloomelle ? Future espèce ?), on regarde si elle a la **capacité**. Ouvert à l'extension.

## Pattern 3 — Strategy (ex2)

### Le problème qu'il résout

Tu as plusieurs façons de mener un combat (normale, agressive, défensive). Naïvement, tu mettrais une grosse fonction `fight()` avec des `if` partout :

```python
def fight(creature):
    if isinstance(creature, HealCapability):
        creature.attack()
        creature.heal()
    elif isinstance(creature, TransformCapability):
        creature.transform()
        creature.attack()
        creature.revert()
    else:
        creature.attack()
```

C'est lourd. Si on ajoute une 4e stratégie, on revient ici. Si on change la logique d'une stratégie, on revient ici. La fonction grossit indéfiniment.

### La solution Strategy

Chaque stratégie devient une **classe** qui sait comment se comporter. La classe `BattleStrategy` abstraite définit l'interface (`act`, `is_valid`). Les classes concrètes (`NormalStrategy`, `AggressiveStrategy`, `DefensiveStrategy`) implémentent leur logique.

Le code client devient :

```python
strategy.act(creature)
```

Une ligne. La stratégie sait quoi faire. Si tu veux ajouter une nouvelle stratégie : tu crées une nouvelle classe. Le tournoi n'a pas à changer.

### Le couple is_valid + act

C'est élégant. `is_valid` te dit en amont si une stratégie peut s'appliquer à une créature. `act` exécute la stratégie, mais lève une exception si la combinaison est invalide.

```python
class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature) -> bool:
        return isinstance(creature, TransformCapability)
    
    def act(self, creature) -> None:
        if not self.is_valid(creature):
            raise InvalidStrategyError(...)
        creature.transform()
        creature.attack()
        creature.revert()
```

Ça permet deux usages :

- Pré-validation : "puis-je utiliser cette stratégie ?" (sans crash)
- Exécution : "fais-le, sinon plante" (avec exception claire)

### Pourquoi la fonction de bataille devient triviale

Avec le Strategy pattern, `battle()` devient hyper compact :

```python
def battle(opponents):
    for (creature_a, strategy_a) in opponents:
        for (creature_b, strategy_b) in others:
            strategy_a.act(creature_a)
            strategy_b.act(creature_b)
```

Aucun `if` sur le type de créature ou de stratégie. Polymorphisme partout. Si tu rajoutes une `BerserkStrategy` demain, `battle()` ne bouge pas d'un caractère.

---

# PARTIE 3 — Walkthrough du projet, fichier par fichier

## ex0/creature.py

```python
class Creature(ABC):
    def __init__(self, name: str, ctype: str) -> None:
        self.name = name
        self.ctype = ctype

    def describe(self) -> str:
        return f"{self.name} is a {self.ctype} type Creature"

    @abstractmethod
    def attack(self) -> str:
        pass
```

Classe abstraite. Deux méthodes :

- `describe` — concrète. Toutes les créatures la partagent.
- `attack` — abstraite. Chaque créature doit l'implémenter.

C'est l'idée de base : du commun (concrete) + un contrat (abstract).

## ex0/concrete_creatures.py

Quatre classes : `Flameling`, `Pyrodon`, `Aquabub`, `Torragon`. Chacune implémente `attack` à sa façon.

Note importante : ces classes restent **internes** au package. `__init__.py` ne les expose pas.

## ex0/factories.py

```python
class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature: pass
    @abstractmethod
    def create_evolved(self) -> Creature: pass
```

L'abstraction. Toute factory doit savoir créer une base et une évolution.

`FlameFactory` et `AquaFactory` héritent et implémentent.

## ex0/**init**.py

```python
from .creature import Creature
from .factories import CreatureFactory, FlameFactory, AquaFactory
```

**N'expose pas** `Flameling`, `Pyrodon`, etc. Conformément au sujet.

## ex1/capabilities.py

Deux mixins :

```python
class HealCapability(ABC):
    @abstractmethod
    def heal(self, target=None) -> str: pass

class TransformCapability(ABC):
    def __init__(self) -> None:
        self._transformed: bool = False
    @abstractmethod
    def transform(self) -> str: pass
    @abstractmethod
    def revert(self) -> str: pass
```

`HealCapability` est super simple — juste une méthode abstraite.

`TransformCapability` a un état (`_transformed`). C'est ce que demande le sujet : "An attribute is used to make the state persistent and it impacts the attack implementation". L'attaque va lire cet attribut pour décider quoi dire.

## ex1/concrete_creatures.py

Héritage multiple en action :

```python
class Sproutling(Creature, HealCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Sproutling", "Grass")
    
    def attack(self) -> str: ...
    def heal(self, target=None) -> str: ...
```

`Sproutling` est **à la fois** une `Creature` (avec name, ctype, describe) et possède la capacité `HealCapability` (avec heal). Le contrat des deux classes abstraites est satisfait.

Pour `Shiftling` et `Morphagon` (transform), on appelle les **deux** constructeurs :

```python
Creature.__init__(self, "Shiftling", "Normal")
TransformCapability.__init__(self)
```

Parce que `TransformCapability.__init__` initialise `_transformed = False`. Sans cet appel, l'attribut n'existerait pas.

## ex1/factories.py

```python
class HealingCreatureFactory(CreatureFactory): ...
class TransformCreatureFactory(CreatureFactory): ...
```

Même pattern qu'ex0 — factories concrètes par famille.

## ex2/strategies.py

L'exception custom :

```python
class InvalidStrategyError(Exception): pass
```

Conformément au sujet : "a dedicated exception is raised with a clear message".

Les stratégies suivent le pattern `is_valid` + `act` :

```python
class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature) -> bool:
        return isinstance(creature, HealCapability)
    
    def act(self, creature) -> None:
        if not self.is_valid(creature):
            raise InvalidStrategyError(...)
        print(creature.attack())
        assert isinstance(creature, HealCapability)  # narrowing pour mypy
        print(creature.heal())
```

Le `assert isinstance(...)` est important pour mypy. Sans lui, mypy ne saurait pas que `creature` a une méthode `heal()` (elle est définie dans le mixin, pas dans `Creature`). L'`assert` informe mypy du type narrowing.

## tournament.py

La fonction `battle()` orchestre. Elle :

1. Instancie chaque créature une seule fois (sinon une seconde itération recréerait l'objet)
2. Fait combattre chaque paire (i, j) avec i < j (round-robin sans doublons)
3. Délègue le combat aux stratégies via `strategy.act(creature)`
4. Catch `InvalidStrategyError` au niveau du tournoi entier — un combat invalide stoppe le tournoi avec un message

---

# PARTIE 4 — Préparation à la défense

## Q1 : C'est quoi une classe abstraite ? Pourquoi en utiliser ?

Une classe abstraite est une classe qui ne peut pas être instanciée directement, mais qui sert de modèle. Elle peut contenir des méthodes abstraites (sans implémentation, juste la signature) que ses sous-classes **doivent** implémenter.

On en utilise pour deux raisons : (1) imposer un contrat — toute sous-classe **doit** implémenter certaines méthodes ; (2) factoriser du code commun dans la base abstraite (comme `describe` dans `Creature`).

En Python, on utilise `from abc import ABC, abstractmethod`. Une classe qui hérite d'`ABC` et qui a des `@abstractmethod` non implémentées ne peut pas être instanciée.

## Q2 : C'est quoi le polymorphisme ? Donne un exemple dans ton projet.

Le polymorphisme c'est le fait qu'un même appel de méthode produit un comportement différent selon le type réel de l'objet. Le code "haut niveau" reste générique.

Dans mon projet : `test_factory(factory: CreatureFactory)` prend n'importe quelle factory. Si je lui passe un `FlameFactory`, ses `create_base()` retourne un Flameling. Si je lui passe un `AquaFactory`, ça retourne un Aquabub. La fonction `test_factory` n'a aucune idée de la famille, mais elle fonctionne pour toutes — c'est ça le polymorphisme.

## Q3 : Explique le pattern Abstract Factory.

C'est un design pattern où on définit une classe abstraite (la "factory") qui déclare des méthodes de création. Des factories concrètes héritent et implémentent ces méthodes pour créer des objets concrets spécifiques à une famille.

Avantages :

- Le code client ne connaît que l'interface de la factory, pas les classes concrètes
- Ajouter une nouvelle famille = ajouter une nouvelle factory, sans modifier le code client
- Respect du principe ouvert/fermé : ouvert à l'extension, fermé à la modification

Dans mon projet, `CreatureFactory` est l'abstraction. `FlameFactory` crée des Flameling/Pyrodon, `AquaFactory` crée des Aquabub/Torragon. Le code de combat manipule juste des `CreatureFactory`.

## Q4 : Pourquoi tu n'exposes pas Flameling, Pyrodon, etc. depuis ex0 ?

Parce que le sujet l'exige, et ça a un sens fort : c'est l'**encapsulation** du pattern Abstract Factory. Si j'exposais les classes concrètes, un client pourrait écrire `Flameling()` directement, contournant la factory. Le couplage que la factory cherche à éviter reviendrait.

En cachant les classes concrètes, je **force** le client à passer par les factories. Et si demain je veux ajouter un nouveau type (Embergon), je le fais sans toucher au code client.

## Q5 : C'est quoi l'héritage multiple ? Pourquoi tu l'utilises ?

C'est quand une classe hérite de plusieurs classes parentes en même temps. En Python, c'est autorisé et idiomatique. Je l'utilise dans ex1 pour **combiner** la classe `Creature` (qui définit ce qu'est une créature) avec des **mixins** comme `HealCapability` ou `TransformCapability` (qui définissent des capacités).

Comme ça, `Sproutling(Creature, HealCapability)` est à la fois une créature ET sait se soigner, sans que j'aie besoin de créer une chaîne d'héritage rigide. Les capacités sont **orthogonales** (indépendantes) et combinables à volonté.

## Q6 : Pourquoi `HealCapability` n'hérite pas de `Creature` ?

Parce que c'est volontaire — c'est exigé par le sujet et c'est de la bonne conception. Une capacité comme "savoir soigner" n'est pas spécifique aux créatures : un Item pourrait soigner, un sort pourrait soigner. En gardant la capacité **indépendante** de `Creature`, je peux la réutiliser ailleurs.

C'est l'idée du **mixin** : une classe abstraite légère, conçue pour être combinée avec d'autres classes, qui ajoute UN comportement orthogonal.

## Q7 : Explique le pattern Strategy.

C'est un pattern où on encapsule différents algorithmes (ou comportements) dans des classes séparées, qui partagent une interface commune. Le code qui utilise un algorithme manipule l'interface abstraite — il n'a aucune idée de l'algorithme concret qu'il utilise.

Avantages : on peut changer la stratégie à la volée, ajouter de nouvelles stratégies sans toucher au code client, tester chaque stratégie en isolation.

Dans mon projet : `BattleStrategy` est l'abstraction, `NormalStrategy`, `AggressiveStrategy`, `DefensiveStrategy` sont les implémentations. La fonction `battle()` reçoit des stratégies et les fait jouer via `strategy.act(creature)` — sans `if` sur le type.

## Q8 : Comment marche `is_valid` et `act` dans tes stratégies ?

`is_valid(creature)` renvoie `True` si la créature peut être utilisée avec cette stratégie. Par exemple, `DefensiveStrategy.is_valid` renvoie `True` seulement si la créature hérite de `HealCapability` (testé via `isinstance`).

`act(creature)` exécute la stratégie. Avant d'agir, elle vérifie `is_valid` — si invalide, elle lève `InvalidStrategyError` avec un message clair. Sinon, elle déroule sa logique (attaque, ou attaque + heal, ou transform + attack + revert).

Le couple `is_valid` + `act` permet deux usages : tester une combinaison sans crash (`is_valid`), ou tenter l'exécution avec exception en cas d'erreur (`act`).

## Q9 : Comment ta fonction `battle()` gère les erreurs ?

`battle()` met sa boucle de combats dans un `try`/`except InvalidStrategyError`. Si une stratégie lève cette exception au milieu du tournoi, on attrape, on affiche le message "Battle error, aborting tournament: ...", et le tournoi s'arrête.

C'est exactement le comportement attendu par le sujet, comme montré dans "Tournament 1 (error)".

## Q10 : Pourquoi un `assert isinstance(...)` dans `DefensiveStrategy.act` ?

C'est pour mypy. La signature de `act` prend une `Creature`. Mypy sait que `Creature` n'a pas de méthode `heal()` (elle est dans le mixin `HealCapability`). Donc quand j'écris `creature.heal()`, mypy se plaint : "Creature has no attribute heal".

L'`assert isinstance(creature, HealCapability)` est un **type narrowing** : ça dit à mypy "à partir d'ici, traite `creature` comme un `HealCapability`". Mypy accepte et l'erreur disparaît.

À l'exécution, l'`assert` ne plante jamais parce qu'on a déjà vérifié avec `is_valid` au début. C'est juste un indice de typage.

## Q11 : Différence entre héritage et composition ?

- **Héritage** = "est-un" : Sproutling **est une** Creature
- **Composition** = "a-un" : Une stratégie **a une** créature qu'elle manipule (passée en argument)

L'héritage crée un lien fort entre classes parentes et enfants. La composition crée un lien faible : deux objets indépendants qui collaborent.

Le projet utilise les deux. L'héritage pour la hiérarchie Creature → Flameling. La composition pour le Strategy pattern — la stratégie ne contient pas la créature, elle la reçoit en argument et l'utilise.

Principe général : préférer la composition quand possible, parce qu'elle est plus flexible. L'héritage est rigide.

## Q12 : Pourquoi tu fais `Creature.__init__(self, ...)` au lieu de `super().__init__(...)` ?

Parce qu'en héritage multiple, `super()` devient ambigu et galère quand les classes parentes ont des signatures de constructeur différentes. `Creature.__init__` prend `name` et `ctype`. `TransformCapability.__init__` prend rien.

En appelant **explicitement** les constructeurs avec leur classe, je supprime toute ambiguïté. C'est plus verbeux mais plus clair, et garanti de marcher. Pour les évaluateurs c'est aussi plus pédagogique — on voit exactement quel constructeur fait quoi.

## Q13 : Pourquoi tu utilises `isinstance` plutôt que de regarder le type concret ?

Parce que je veux que mes stratégies marchent pour **toute** créature qui a une certaine capacité, pas seulement pour les créatures actuelles. Si demain quelqu'un crée `Wavyling(Creature, HealCapability)`, ma `DefensiveStrategy` doit fonctionner immédiatement, sans modification.

`isinstance(creature, HealCapability)` répond à la vraie question : "cette créature a-t-elle la capacité ?". Vérifier `type(creature) == Sproutling` répondrait à une mauvaise question : "est-ce cette créature précise ?". L'un est ouvert à l'extension, l'autre est rigide.

## Q14 : Tu peux ajouter une nouvelle créature/stratégie sans toucher au reste du code ?

Oui, et c'est précisément le but de tous les patterns utilisés.

- **Nouvelle créature avec capacité existante** : crée la classe `Wavyling(Creature, HealCapability)`, crée sa factory si besoin. Le reste du code marche sans modif.
- **Nouvelle capacité** : crée le mixin abstrait `FlyCapability`, crée des créatures qui en héritent, optionnellement crée une stratégie qui l'exploite. Aucun fichier existant ne bouge.
- **Nouvelle stratégie** : hérite de `BattleStrategy`, implémente `is_valid` et `act`. `battle()` la traite comme les autres.

C'est le principe **ouvert/fermé** : le code est ouvert à l'extension, fermé à la modification.

## Q15 : Comment ton tournoi évite-t-il de faire combattre une créature deux fois contre la même autre ?

Avec une double boucle où j'utilise `i` et `j` avec `j = i + 1`. Comme ça, chaque paire (i, j) est visitée une seule fois. C'est l'algorithme classique du tournoi round-robin : N créatures = N*(N-1)/2 combats.

---

# Conclusion

Le module 07 te fait toucher trois piliers de la POO moderne : abstraction, héritage multiple, et composition via interfaces. Ces concepts ne sont pas spécifiques à Python — tu les retrouveras en Java, C#, TypeScript, Swift, Rust (avec des variantes : traits, interfaces, protocols).

Les questions clés en défense vont tester si tu comprends **pourquoi** ces patterns existent, pas juste comment les coder. Garde en tête :

- **Abstract Factory** = découpler la création des objets
- **Mixins** = composer des comportements orthogonaux
- **Strategy** = découpler une logique variable du code qui l'utilise

Tous ces patterns partagent le même but : **réduire le couplage et augmenter la flexibilité**. Si tu te poses la question "pourquoi pas juste mettre un gros `if`/`else` ?", la réponse est toujours : parce que ça ne scale pas, ça pourrit avec le temps, et ça casse à chaque nouvelle exigence.

Bonne défense.