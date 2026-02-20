# 🐜 Simulation de Fourmis - Version Débutant

## 📁 Structure du Projet

```
NEW/
├── main.py          👈 LANCER CE FICHIER
├── config.py        📋 Tous les paramètres
├── ant.py           🐜 La classe Fourmi
├── simulation.py    🌍 La classe Monde/Simulation
├── gui.py           🖥️ L'interface graphique
└── README.md        📖 Ce fichier
```

## 🎯 Comment ça marche?

### 1️⃣ **config.py** - Les paramètres
Contient TOUS les nombres à changer:
- Taille de la fenêtre
- Nombre de fourmis
- Positions des nids
- Positions de la nourriture
- Couleurs
- etc...

### 2️⃣ **ant.py** - Une fourmi seule
La classe `Ant` représente UNE fourmi:
- Elle a une position (x, y)
- Elle a une direction (angle)
- Elle peut se déplacer
- Elle peut chercher de la nourriture
- Elle peut retourner au nid

### 3️⃣ **simulation.py** - Le monde
La classe `Simulation` gère TOUT:
- Toutes les fourmis ensemble
- La nourriture
- Les obstacles
- Remise à jour chaque image (30 fois/seconde)

### 4️⃣ **gui.py** - Le dessin à l'écran
- `Canvas`: Dessine les fourmis, la nourriture, les nids
- `MainWindow`: Les boutons et la fenêtre

### 5️⃣ **main.py** - Le point de départ
Lance simplement l'application!

## 🚀 Comment lancer?

```bash
python main.py
```

Ou avec le chemin complet:
```bash
python "NEW\main.py"
```

## 🎮 Contrôles

- **▶ DÉMARRER** - Lance la simulation
- **⏸ STOP** - Met en pause
- **🔄 RÉINITIALISER** - Recommence à zéro

## 📊 Qu'est-ce que tu vois?

- 🔴 **Carrés rouges** = Les nids (maisons des fourmis)
- ⬛ **Petits carrés noirs** = Les fourmis qui explorent
- 🟨 **Petits carrés jaunes** = Les fourmis qui ont trouvé de la nourriture
- 🟩 **Carrés verts** = La nourriture
- ⬜ **Gris** = Les obstacles

## 💡 Comment modifier?

**Tout est dans `config.py`** !

Par exemple, pour ajouter plus de fourmis:
```python
ANTS_PER_NEST = 10  # Au lieu de 5
```

Pour ajouter de la nourriture:
```python
FOODS = [
    (150, 350),
    (850, 350),
    (500, 200),  # ← Nouvelle nourriture!
]
```

## 📚 Pour apprendre le code

1. Lis **config.py** - comprends les paramètres
2. Lis **ant.py** - comprends comment une fourmi fonctionne
3. Lis **simulation.py** - vois comment tout fonctionne ensemble
4. Lis **gui.py** - découvre comment dessiner à l'écran
5. Modifie **config.py** - expérimente!

## 🔬 Idées d'expériences

- Change `ANTS_PER_NEST` pour plus/moins de fourmis
- Change `ANT_SPEED` pour plus/moins rapide
- Ajoute un nouvel obstacle dans `OBSTACLES`
- Ajoute plus de nids dans `NESTS`
- Change les couleurs (RGB)

---

**Bon apprentissage!** 🎉
