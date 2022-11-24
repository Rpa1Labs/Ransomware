# TD Ransomware

## Description


## Installation

### CNC Server


### Client


### For Developers


## Réponses

### 1. Quel est le nom de l'algorithme de chiffrement ? Est-il robuste et Pourquoi ?

> Il s'agit d'un chiffrement de flux via un XOR avec une clé. Il n'est pas robuste car il est possible de faire une attaque par fréquence.


### 2. Pourquoi ne pas hasher directement la clé et le salt ?

> On utilise une fonction de dérivation de clé au lieu d'une fonction de hachage car on veut que la clé dérivée soit plus longue que la clé de base. On utilise une fonction de hachage pour le salt car on veut que le salt soit de taille fixe.


### 3. Pourquoi il est préférable de vérifier qu'un fichier token.bin n'est pas déjà présent ?

> Pour éviter de réinitialiser (et donc perdre) le token à chaque fois qu'on lance le programme.


### 4. Comment vérifier que la clef est la bonne ?

> Nous pouvons vérifier que la clef est la bonne en dérivant la clé et le salt pour obtenir un token que l'on compare au token du fichier token.bin. (on va utiliser la fonction `do_derivation`)


