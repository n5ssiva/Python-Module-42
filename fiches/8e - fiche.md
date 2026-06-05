# Module 08 — Cours complet sur l'outillage Python en environnement de prod

## Comment lire ce document

Ce module est différent des précédents. Y'a peu de code et beaucoup de **concepts d'écosystème**. L'évaluateur va te poser des questions du genre "pourquoi un venv ?" et "différence pip / Poetry ?". Si tu sais répondre, tu valides. Sinon, peu importe que ton code marche.

Le document est divisé en 4 parties :

1. **Le modèle mental — pourquoi tous ces outils existent**
2. **Les 3 concepts du projet en profondeur** (venv, gestion deps, env vars)
3. **Walkthrough du projet, exo par exo**
4. **Préparation à la défense**

---

# PARTIE 1 — Le modèle mental

## 1.1 Le problème que tous ces outils résolvent

Tu codes un projet Python qui utilise pandas version 2.0.

Six mois plus tard, tu codes un autre projet, qui utilise une lib qui dépend de pandas version 1.5 (incompatible avec 2.0).

Si tu as **un seul Python sur ta machine**, avec **une seule version de pandas installée**, t'es coincé : soit le premier projet marche, soit le deuxième. Pas les deux.

**Solution** : chaque projet a son propre Python isolé, avec ses propres versions de libs. C'est exactement ce que fait un **virtual environment**.

Ensuite, comment **partager** ton projet avec un autre dev (ou avec ton toi-du-futur) ? Il doit pouvoir recréer le même environnement. C'est le rôle des fichiers de dépendances (`requirements.txt`, `pyproject.toml`).

Enfin, ton code a besoin d'infos sensibles (clé API, mot de passe DB). Tu peux pas les mettre dans le code (Git les verrait, GitHub les volerait). C'est le rôle des **variables d'environnement** et du fichier `.env`.

Voilà. Module 08 = ces 3 problèmes, ces 3 solutions.

## 1.2 Pourquoi c'est crucial dans la vraie vie

À 42, on te fait travailler dans le venv parce que c'est ce qui se passe en entreprise. Aucune boîte sérieuse ne déploie une application sans :

- Un environnement isolé
- Un fichier de deps versionné (pour que CI/CD installe exactement les mêmes versions)
- Des secrets passés en variables d'env (pour que la même app marche en dev local, staging, et prod, avec des configs différentes)

Si tu comprends ces 3 trucs, t'es prêt pour des projets pro. C'est pour ça que le module existe.

---

# PARTIE 2 — Les 3 concepts en profondeur

## Concept 1 — Les Virtual Environments (ex0)

### Qu'est-ce que c'est concrètement ?

Quand tu fais `python3 -m venv matrix_env`, Python crée un dossier `matrix_env/` qui contient :

- Un **exécutable Python** (copie ou lien vers ton Python système)
- Un dossier `lib/pythonX.Y/site-packages/` **vide**, où vont s'installer les libs
- Un script `bin/activate` qui modifie ton shell pour que `python` pointe vers cet exécutable au lieu de celui du système

Quand tu fais `source matrix_env/bin/activate` :

- Le `PATH` de ton shell est modifié pour mettre `matrix_env/bin/` en premier
- Donc `python3`, `pip`, etc. utilisent maintenant ceux du venv
- La variable `VIRTUAL_ENV` est définie

À partir de là, **tout ce que tu pip install va dans le venv**, pas dans le système. Quand tu `deactivate`, ton shell revient à la normale, et le Python système ne sait rien de ce que tu as installé.

### Comment détecter qu'on est dans un venv (ce que fait `construct.py`)

Python expose deux attributs dans le module `sys` :

- `sys.prefix` — chemin du Python actuellement utilisé
- `sys.base_prefix` — chemin du Python "originel" (système)

**Hors venv** : les deux sont égaux (`/usr/bin/python3` par exemple). **Dans un venv** : `sys.prefix` pointe vers le venv (`/path/to/matrix_env`), `sys.base_prefix` pointe vers le système.

D'où le test :

```python
def in_virtual_env() -> bool:
    return sys.prefix != sys.base_prefix
```

C'est **la méthode officielle** recommandée par la doc Python. Y'a aussi `sys.real_prefix` (ancien virtualenv) et la variable d'env `VIRTUAL_ENV`, mais `sys.prefix != sys.base_prefix` est le plus robuste.

### Pourquoi ne JAMAIS commit ton venv

Un venv contient des binaires propres à ta machine et ton OS. Si tu commits, ça pèse 50-200 MB de fichiers inutiles, et ça plante chez quelqu'un d'autre.

À la place, tu commits **uniquement** le fichier qui liste les deps (`requirements.txt` ou `pyproject.toml`). L'autre dev recrée le venv chez lui et installe les deps depuis ce fichier.

C'est pour ça que `.gitignore` contient systématiquement les dossiers venv (`venv/`, `.venv/`, `matrix_env/`, etc.).

## Concept 2 — Gestion des dépendances : pip vs Poetry (ex1)

### pip — le gestionnaire historique

`pip` est l'outil de base de Python. Il fait une chose : installer des packages depuis PyPI (Python Package Index, le dépôt public).

```bash
pip install pandas
pip install pandas==2.0.0   # version exacte
pip install "pandas>=2.0"   # version min
```

Pour partager les deps d'un projet, on liste tout dans `requirements.txt` :

```
pandas>=2.0.0
numpy>=1.25.0
matplotlib>=3.7.0
```

Et l'autre dev fait :

```bash
pip install -r requirements.txt
```

**Limite de pip** : il ne gère pas les **dépendances transitives** intelligemment. Si pandas dépend de numpy 1.26, mais que tu installes explicitement numpy 1.25, pip va te laisser dans un état incohérent sans broncher. Tu peux te retrouver avec des conflits silencieux qui pètent au runtime.

`requirements.txt` ne distingue pas non plus tes deps **directes** (celles que TU utilises) des deps **transitives** (celles que tes deps utilisent). Si t'utilises pandas, et que pandas utilise numpy, ton requirements peut contenir les deux mélangés. C'est moche à maintenir.

### Poetry — le gestionnaire moderne

Poetry résout ces problèmes. Il fait trois choses que pip ne fait pas :

**1. Il résout l'arbre de dépendances**. Avant d'installer, Poetry calcule un graphe complet : tu veux pandas, qui veut numpy ; tu veux requests, qui veut urllib3 ; etc. Si y'a un conflit, Poetry te le dit **avant** d'installer quoi que ce soit.

**2. Il sépare deps directes et transitives**. Dans `pyproject.toml` (le fichier de config), tu déclares **seulement ce que tu utilises directement**. Poetry calcule le reste tout seul.

**3. Il génère un fichier de lock (`poetry.lock`)**. Ce fichier liste **toutes** les deps (directes + transitives) avec leur **version exacte** et leur hash. N'importe qui sur n'importe quelle machine peut recréer **exactement** le même environnement. Reproductibilité garantie.

### Le `pyproject.toml`

C'est le fichier standard moderne pour décrire un projet Python. Il remplace plusieurs anciens fichiers (`setup.py`, `setup.cfg`, etc.). Exemple :

```toml
[tool.poetry]
name = "loading"
version = "0.1.0"
description = "Matrix data analysis"
authors = ["Toi <[email protected]>"]

[tool.poetry.dependencies]
python = "^3.10"
pandas = "^2.0.0"
numpy = "^1.25.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

Le `^2.0.0` veut dire "compatible avec 2.0.0" — accepte 2.x.x mais pas 3.0.0. Ça permet d'avoir des updates mineures sans casser les compats majeurs.

### Récap pip vs Poetry

||pip + requirements.txt|Poetry + pyproject.toml|
|---|---|---|
|Résolution de l'arbre de deps|Non|Oui|
|Sépare directes / transitives|Non|Oui|
|Lock file pour reproductibilité|Non (sauf `pip freeze`)|Oui (`poetry.lock`)|
|Format de config|Plain text|TOML standardisé|
|Vitesse|Plus rapide|Plus lent (résolution coûteuse)|
|Simplicité|Très simple|Plus complexe|
|Usage|Scripts simples, prototypes|Projets sérieux, libs publiées|

En vrai dans la vraie vie, beaucoup de devs utilisent **pip avec un lock file généré par `pip-tools` ou `pip freeze`** pour avoir un compromis. Mais Poetry reste plus propre par défaut.

## Concept 3 — Variables d'environnement et fichiers `.env` (ex2)

### Le problème

Ton code a besoin de :

- L'URL de la base de données
- Une clé API pour un service tiers
- Le mode (dev vs prod)

Si tu mets ces valeurs **en dur dans le code** :

- Tu peux pas changer la config sans modifier le code
- Tu vas commit des secrets sur GitHub, et des bots vont les voler en quelques heures (oui, c'est un truc qui arrive vraiment, GitHub a des systèmes anti-leak)
- La même app peut pas tourner en dev local et en prod avec des paramètres différents

### La solution : variables d'environnement

Les **variables d'environnement** sont des paires clé-valeur stockées au niveau du shell ou du système. Tu peux les définir avant de lancer ton programme :

```bash
DATABASE_URL=postgresql://localhost:5432/db python3 monapp.py
```

Dans Python, tu les lis via `os.environ` :

```python
import os
db_url = os.environ.get("DATABASE_URL", "default_value")
```

Ainsi ton code reste générique. Le déploiement décide des valeurs.

### Le fichier `.env`

Tu vas pas taper 15 variables à chaque fois que tu lances ton app en dev. Donc on les met dans un fichier `.env` :

```
DATABASE_URL=postgresql://localhost:5432/zion
API_KEY=mysecret123
MATRIX_MODE=development
```

La lib `python-dotenv` lit ce fichier et **injecte** les variables dans `os.environ` :

```python
from dotenv import load_dotenv
load_dotenv()   # lit .env, ajoute à os.environ
# maintenant os.environ.get("DATABASE_URL") marche
```

**Important** : par défaut, `load_dotenv` n'**écrase** PAS les variables déjà définies dans le shell. C'est volontaire. Ça permet à un déploiement de "passer par-dessus" le `.env` :

```bash
# .env contient MATRIX_MODE=development
MATRIX_MODE=production python3 oracle.py
# → la valeur du shell (production) gagne sur celle du .env
```

Ça permet d'avoir un `.env` "défaut dev" en local, et de surcharger en prod via les vraies variables d'env (gérées par Docker, Kubernetes, le système d'hébergement, etc.).

### Pourquoi `.env` doit être dans `.gitignore`

Parce que c'est là que tu mets tes **vrais secrets** en local. Si tu commits, ils partent sur GitHub, et 30 secondes après, tu as un bot qui a volé ta clé AWS et qui mine du Bitcoin sur ton compte (true story, ça coûte des milliers de dollars).

À la place, tu commits un fichier `.env.example` (ou `.env.sample`) qui contient la **structure** du `.env` mais avec des valeurs bidon. Quand un nouveau dev arrive sur le projet, il copie `.env.example` en `.env` et remplit les vraies valeurs.

```
# .env.example (committé)
DATABASE_URL=postgresql://localhost:5432/example
API_KEY=your_api_key_here
```

```
# .env (gitignored)
DATABASE_URL=postgresql://prod.zion.com:5432/real_db
API_KEY=sk_live_abc123xyz_REAL_SECRET
```

---

# PARTIE 3 — Walkthrough du projet, exo par exo

## ex0/construct.py

But pédagogique : **comprendre ce qu'est un venv et comment Python sait s'il est dedans**.

Points clés du code :

- `sys.prefix != sys.base_prefix` — méthode officielle de détection
- `os.environ.get("VIRTUAL_ENV")` — variable mise par `activate` (utile pour le nom du venv)
- `sys.executable` — chemin du Python actuellement utilisé
- Deux outputs distincts selon contexte, conformément au sujet

Test obligatoire : lancer **dans** et **hors** d'un venv, vérifier les deux outputs.

## ex1/loading.py + requirements.txt + pyproject.toml

But pédagogique : **comprendre comment Python charge des libs externes, et comment partager une liste de deps**.

Points clés du code :

- `importlib.import_module(pkg)` — import dynamique pour tester si une lib est installée sans planter
- Try/except autour de l'import — gestion gracieuse du cas "lib manquante"
- Génération d'un dataset avec `numpy.random` (le sujet l'exige : "must be the source of your dataset")
- Calcul d'une rolling mean avec pandas
- Visualisation et sauvegarde PNG avec matplotlib
- `matplotlib.use("Agg")` — backend non-interactif (pour pas ouvrir de fenêtre, juste sauvegarder)

`requirements.txt` (pour pip) liste les deps de manière flat. `pyproject.toml` (pour Poetry) déclare le projet, avec contraintes de versions plus expressives.

Le sujet autorise les erreurs flake8/mypy sur les imports — c'est normal, parce qu'on importe des libs qui peuvent être manquantes au moment de l'analyse statique.

## ex2/oracle.py + .env.example + .gitignore

But pédagogique : **gérer la config d'une app via variables d'env, sans hardcoder de secrets**.

Points clés du code :

- `load_dotenv(override=False)` — lit `.env`, mais ne touche pas aux variables shell existantes
- `os.environ.get("VAR", default)` — récupère avec fallback
- Distinction dev/prod basée sur `MATRIX_MODE`
- Security check qui affiche [OK]/[WARN] selon ce qui est trouvé

`.env.example` est committé (template). `.gitignore` contient `.env` (vrais secrets, jamais commit).

---

# PARTIE 4 — Préparation à la défense

## Q1 : C'est quoi un virtual environment ? À quoi ça sert ?

C'est un environnement Python isolé qui contient sa propre version de Python et son propre dossier `site-packages` où s'installent les libs. Ça permet d'avoir plusieurs projets sur la même machine, chacun avec ses propres versions de dépendances, sans conflit.

Sans venv, t'as un seul Python système, donc une seule version de chaque lib. Si ton projet A veut pandas 2.0 et ton projet B veut pandas 1.5, t'es coincé. Avec un venv par projet, chaque projet a sa propre version.

## Q2 : Comment ton programme détecte qu'on est dans un venv ?

Je compare `sys.prefix` et `sys.base_prefix`. `sys.prefix` est le chemin du Python qu'on est en train d'utiliser ; `sys.base_prefix` est le chemin du Python "racine" du système.

Hors venv, les deux pointent vers le même endroit. Dans un venv, `sys.prefix` pointe vers le dossier du venv, et `sys.base_prefix` reste le Python système. Donc si les deux diffèrent, on est dans un venv. C'est la méthode officielle recommandée par la doc Python.

## Q3 : Différence entre pip et Poetry ?

`pip` est l'outil de base, il installe des packages depuis PyPI. Tu donnes un fichier `requirements.txt` avec une liste plate de deps.

Poetry est un gestionnaire plus moderne qui fait trois choses en plus : il **résout l'arbre de dépendances** avant d'installer (détecte les conflits), il sépare les deps **directes** des deps **transitives** dans `pyproject.toml`, et il génère un fichier de **lock** (`poetry.lock`) qui fige toutes les versions exactes pour reproductibilité.

En gros : pip est simple mais brut ; Poetry est plus propre pour des projets sérieux et garantit que tout le monde aura exactement le même environnement.

## Q4 : Pourquoi un fichier `.env` ?

Pour stocker la configuration d'une app (URL de base de données, clés API, mode dev/prod) en dehors du code. Comme ça, le même code peut tourner avec des configs différentes selon l'environnement (dev local, staging, prod) sans qu'on modifie le code.

`python-dotenv` lit le fichier `.env` et injecte ses variables dans `os.environ` au démarrage du programme. Le code Python lit ensuite via `os.environ.get("VAR")`.

## Q5 : Pourquoi `.env` doit être dans `.gitignore` ?

Parce que le `.env` contient les **vraies valeurs sensibles** : clés API, mots de passe de base de données, tokens. Si tu commits ça sur Git, et surtout si ton repo est sur GitHub, des bots scrutent les commits publics et volent les secrets en quelques secondes — il y a des incidents publics de devs qui ont perdu des milliers d'euros à cause d'une clé AWS commit par erreur.

À la place, on commit un `.env.example` avec la même structure mais des valeurs bidon, juste pour montrer aux autres devs quelles variables sont attendues.

## Q6 : Pourquoi `load_dotenv(override=False)` et pas `override=True` ?

Pour que les variables définies dans le shell **par-dessus** le `.env` aient la priorité. C'est utile en production : ton serveur a déjà ses variables d'env définies au niveau système (par Docker, Kubernetes, etc.). Le `.env` est juste un fallback pour le dev local. Si on faisait `override=True`, le `.env` écraserait les vraies variables de prod — catastrophe.

Donc : la hiérarchie est `os.environ` (shell/système) > `.env` > valeurs par défaut hardcodées dans le code.

## Q7 : C'est quoi `pyproject.toml` ?

C'est le fichier standard moderne pour décrire un projet Python, en remplacement de `setup.py` et `setup.cfg`. Il utilise le format TOML (lisible et clair). Il déclare le nom du projet, la version, les auteurs, les dépendances, et la config des outils (build, lint, etc.).

Poetry l'utilise pour gérer les dépendances. Pip aussi sait le lire depuis quelques versions. C'est le standard recommandé par PEP 621.

## Q8 : Pourquoi ne pas commit son venv ?

Trois raisons :

1. Le venv contient des **binaires propres à ta machine et ton OS**. Quelqu'un sur Windows ne peut pas utiliser ton venv macOS.
2. Ça pèse 50-200 MB pour rien — Git n'est pas fait pour stocker des binaires aussi gros.
3. C'est inutile : on a déjà `requirements.txt` ou `pyproject.toml` qui dit comment **recréer** le venv. L'autre dev fait `python -m venv venv && pip install -r requirements.txt` chez lui, et il a le même environnement (presque) que toi.

## Q9 : Différence entre `requirements.txt` et `poetry.lock` ?

`requirements.txt` est **édité à la main** par le dev. Il contient juste les contraintes de version qu'on veut, sans forcément les figer.

`poetry.lock` est **généré automatiquement** par Poetry. Il fige les **versions exactes** de **toutes** les deps (directes + transitives) avec leur hash de fichier. C'est ce qu'on utilise pour garantir qu'un autre dev (ou un serveur CI/CD) installe **exactement** les mêmes versions, à l'octet près.

Tu commits **toujours** `poetry.lock`. Si tu le commits pas, tu perds la garantie de reproductibilité.

## Q10 : Comment ton programme gère les libs manquantes ?

J'utilise `importlib.import_module(pkg)` dans un `try/except ImportError`. Si la lib est là, je récupère sa version et j'affiche `[OK]`. Si elle manque, je note `[MISSING]` et à la fin, si quelque chose manquait, j'affiche les instructions d'install (pip et Poetry) et je quitte avec un code d'erreur.

Comme ça, le programme **ne plante pas brutalement** quand une lib manque — il explique gentiment à l'utilisateur quoi installer.

## Q11 : Que se passe-t-il quand on tape `pip install pandas` dans un venv activé ?

1. Le shell appelle `pip`, qui est celui du venv (parce que `PATH` a été modifié par `activate`).
2. `pip` télécharge le package `pandas` depuis PyPI (et toutes ses deps transitives : numpy, python-dateutil, etc.).
3. Il les installe dans `venv/lib/pythonX.Y/site-packages/`.
4. À la prochaine exécution de `python3` (toujours celui du venv), `import pandas` trouve le package dans `site-packages` et le charge.

Si tu fais `deactivate` puis `python3`, t'es de retour sur le Python système, qui ne voit **pas** ce `site-packages` du venv. Donc `import pandas` peut échouer si pandas n'est pas dans le Python système. C'est ça, l'isolation.

## Q12 : Et si tu lances `pip install` SANS venv actif ?

Tu installes la lib dans le Python **système**, dans son `site-packages` global. Conséquences :

- Tu pollues l'install Python du système avec des libs qui peuvent rentrer en conflit avec celles du système (le système d'exploitation utilise parfois Python en interne)
- Sur macOS et Linux récents, `pip` te refuse de le faire par défaut (erreur "externally-managed-environment"), pour cette raison
- Tu perds l'isolation entre projets

C'est pour ça qu'on a **toujours** un venv pour un projet sérieux.

## Q13 : Donne-moi 3 raisons d'utiliser un venv

1. **Isolation des dépendances** — chaque projet a ses propres versions, pas de conflit
2. **Reproductibilité** — un autre dev peut recréer exactement ton environnement à partir du fichier de deps
3. **Sécurité** — on ne pollue pas le Python système, qui peut être utilisé par l'OS

## Q14 : C'est quoi `os.environ` ?

C'est un dictionnaire Python qui contient toutes les variables d'environnement du processus en cours. Les clés et valeurs sont des strings. On lit avec `os.environ.get("VAR")` (avec fallback en option) ou `os.environ["VAR"]` (lève `KeyError` si absent).

`os.environ` est rempli au démarrage du programme par le shell qui l'a lancé. `python-dotenv` peut y ajouter des variables en lisant un fichier `.env`.

## Q15 : Si je supprime ton `.env`, est-ce que ton programme plante ?

Non. Mon programme utilise `load_dotenv()` qui ne plante pas si le fichier est absent — il fait juste rien. Ensuite, pour chaque variable attendue, j'utilise `os.environ.get(var, default)` avec un fallback. Donc si la variable n'est pas dans le `.env` et n'est pas dans le shell, je tombe sur la valeur par défaut.

Le security check affiche un `[WARN]` si le fichier `.env` est absent, pour que l'utilisateur sache qu'il tourne sur les defaults. Mais le programme continue de tourner proprement.

---

# Conclusion

Le module 08 est plus court conceptuellement, mais il est **plus pratique** : ces outils, tu vas les utiliser dans **tous** tes projets futurs, en Python comme dans d'autres langages (Node.js a son équivalent avec `npm` et `.env`, Rust avec `cargo`, etc.).

Les questions de défense seront probablement focalisées sur le **pourquoi** plus que sur le code. Sois prêt à expliquer :

- Pourquoi on isole les environnements
- Pourquoi Poetry est plus propre que pip seul
- Pourquoi on ne commit jamais les secrets

Si tu retiens trois phrases :

1. **Venv** = isolation des deps par projet
2. **Poetry vs pip** = Poetry résout l'arbre + locke les versions, pip est plus brut
3. **`.env`** = config externalisée, jamais committée pour les vraies valeurs

Tu peux dérouler toute la défense à partir de là. Bonne défense.