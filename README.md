# Brute

Brute est un petit script python qui permet de repérer le type de mot de passe et d'essayer de le cracker.

Il va simplement essayer de repérer le type de mot de passe avec une expression régulière, et si un match est trouvé, tous les mots de passes contenus dans les fichiers qui sont dans le repertoire `wordlists` seront essayés.

## Chiffrements supportés

- MD5
- SHA1
- SHA256
- SHA512
- BCRYPT


## Installation

Pour l'installer, il suffit de cloner le dépôt git et d'installer les dépendances.

```bash
git clone https://github.com/davidtchilian/brute.git
cd brute
pip3 install -r requirements.txt
```

## Utilisation

Il existe plusieurs utilisations possibles : 

### Hash en ligne de commande

```bash
python3 brute.py 48a10d9b69ab6d80b814443d266ca190
```

Attention, si le hash contient des caractères spéciaux, vous devez les escape avec un backslash ou mettre le hash dans un fichier.

### Hash(s) dans un fichier

Il est possible de donner plusieurs hash par fichier, chaque hash doit être sur une ligne.

```bash
python3 brute.py -f hash.txt
```

### Hash unique en ligne de commande

```bash
python3 brute.py -H password
```

### hash.txt

Si vous ne donnez ni de hash en ligne de commande, ni de fichier, le script va chercher un fichier `hash.txt` dans le dossier courant.

```bash
python3 brute.py
```

## Ajouter des wordlists

Pour ajouter des wordlists, il suffit de les mettre dans le dossier `wordlists` et de les nommer comme vous le souhaitez.


## License

[MIT](https://choosealicense.com/licenses/mit/)


## TODO

- [ ] Ajouter plus de chiffrements
- [ ] Implémenter un système de threads pour accélérer le processus
- [ ] Ajouter un système de verbose
- [ ] Ajouter un système de logs
- [ ] Ajouter un système de sauvegarde pour permettre d'intérompre le processus et de le reprendre plus tard 