# TD Ransomware

## 1. Description

Ce projet a pour but de créer un ransomware qui chiffre les fichiers d'un ordinateur et qui envoie une clé de déchiffrement à un serveur distant.


*<span style="color:red">Pour des raisons de sécurité, le ransomware est exécutable uniquement dans un environnement Docker. </span>*

*<span style="color:red">Les deux conteneurs Docker doivent être lancés sur la même machine.</span>*

## 2.Installation

### 2.1. Prérequis

Pour exécuter Docker, il faut installer sudo afin de pouvoir lancer les commandes en tant que root.

En tant que root, il faut exécuter la commande suivante:

Pour debian :

```bash
apt install sudo
```

Pour archlinux :

```bash
pacman -S sudo
```

Pour fedora :

```bash
dnf install sudo
```

Pour installer le ransomware, il faut d'abord installer Docker sur votre machine. Pour cela, vous pouvez suivre les instructions suivantes : [cliquez ici](https://docs.docker.com/engine/install/)


### 2.2. Création des conteneurs

Pour créer les conteneurs, il faut se placer dans le dossier du projet puis exécuter la commande suivante :
```bash
sudo chmod +x build.sh && sudo ./build.sh
```

### 2.3. lancement du serveur CNC

Avant le lancer le ransomware, il faut lancer le serveur CNC. Pour cela, il faut se placer dans le dossier du projet puis exécuter la commande suivante :
```bash
sudo chmod +x run_cnc.sh && sudo ./run_cnc.sh
```

> **Note:** Le serveur CNC est accessible sur le port 6666.

### 2.4. Client

Enfin, pour lancer le ransomware, il faut se placer dans le dossier du projet et exécuter la commande suivante :
```bash
sudo chmod +x run_ransomware.sh && sudo ./run_ransomware.sh
```

> **Note:** Si vous voulez seulement lancer l'environnement Docker (sans lancer le ransomware), vous pouvez exécuter la commande suivante :
> ```bash
> sudo chmod +x exec_target.sh && sudo ./exec_target.sh
> ```
> Cela vous permettra d'entrer dans l'environnement Docker et d'exécuter le ransomware à la main en exécutant la commande suivante :
> ```bash
> cd /root/ransomware && python3 ransomware.py
> ```

## 3. Utilisation

### 3.1. Lancement du ransomware

Lorsque le ransomware est lancé, il va chiffrer les fichiers txt du dossier `/root`. Il va ensuite envoyer la clé de déchiffrement au serveur CNC et enregistrer le salt et le token sous forme binaire dans le dossier `token_data` sur votre machine.

Une fois le chiffrement terminé, le ransomware va afficher un message sur le terminal avec le token.

Exemple de message :
```bash
INFO:Ransomware:
________                        ____   ____    .__   __    ._. ._. ._.
\______ \   ____  __ __  ______ \   \ /   /_ __|  |_/  |_  | | | | | |
 |    |  \_/ __ \|  |  \/  ___/  \   Y   /  |  \  |\   __\ | | | | | |
 |    `   \  ___/|  |  /\___ \    \     /|  |  /  |_|  |    \|  \|  \|
/_______  /\___  >____//____  >    \___/ |____/|____/__|    __  __  __
        \/     \/           \/                              \/  \/  \/

Your precious and useful txt files have been locked. Send an email to evil@hell.com with title 'd448529985da7eaad9265e901469ce54' to unlock your data.
```

### 3.2. Récupération des fichiers

#### 3.2.1. Récupération de la clé de déchiffrement

Pour récupérer les fichiers, il faut récupérer la clé. Pour cela, il faut aller du côté du serveur CNC.

**Solution 1:**

Vous récupérez la clé directement depuis les logs du serveur CNC.

Exemple de logs :
```bash
69.69.69.69 - - [11/Sep/2001 16:01:69] New victim : {'token': '1EhSmYXafqrZJl6QFGnOVA==', 'salt': 'BQnVrEo8dPX0xke+QoTj2Q==', 'key': 'yHehSkojK6Wxr9YUgcq7nw=='}
```
Vous pouvez alors copier la clé sous forme base64.

**Solution 2:**

Vous récupérez la clé sous forme binaire depuis le dossier `cnc_data` sur votre machine.

Pour cela, une fois dans le dossier `cnc_data`, il faut se placer dans le dossier qui a pour nom le token de la victime. Dans ce dossier, il y a un fichier `key.bin` qui contient la clé de déchiffrement.

Vous convertissez ensuite la clé de déchiffrement en base64.

#### 3.2.2. Déchiffrement des fichiers

Imaginons que pour simuler le client, vous ayez lancé le script `exec_target.sh` et que vous ayez récupéré la clé de déchiffrement sous forme base64 sur le CNC.

Pour déchiffrer les fichiers, il faut se placer dans le dossier `/root/ransomware` et exécuter la commande suivante :
```bash
python3 ransomware.py --decrypt
```

Un formulaire va alors s'afficher. Il faut alors entrer la clé de déchiffrement en base64 récupérée sur le CNC et appuyer sur la touche `Entrée`.

## 4. Réponses aux questions

### 4.1. Quel est le nom de l'algorithme de chiffrement ? Est-il robuste et Pourquoi ?

> Il s'agit d'un chiffrement de flux via un XOR avec une clé. Il n'est pas robuste car il est possible de faire une attaque par fréquence.


### 4.2. Pourquoi ne pas hasher directement la clé et le salt ?

> On utilise une fonction de dérivation de clé au lieu d'une fonction de hachage car on veut que la clé dérivée soit plus longue que la clé de base.


### 4.3. Pourquoi il est préférable de vérifier qu'un fichier token.bin n'est pas déjà présent ?

> Pour éviter de réinitialiser (et donc perdre) le token à chaque fois qu'on lance le programme et d'éviter de chiffrer un fichier déjà chiffré.


### 4.4. Comment vérifier que la clef est la bonne ?

> Nous pouvons vérifier que la clef est la bonne en dérivant la clé et le salt (que l'on récupère dans le fichier salt.bin) pour obtenir un token. Ce token va être comparé au token du fichier token.bin (on va utiliser la fonction `do_derivation`). Si les deux tokens sont identiques, alors la clef est la bonne.


