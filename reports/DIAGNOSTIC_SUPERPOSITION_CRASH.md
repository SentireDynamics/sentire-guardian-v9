# 🔍 DIAGNOSTIC - Superposition Crash

**Problème** : L'application Superposition crash immédiatement après le lancement

---

## 📊 AMÉLIORATION AJOUTÉE

J'ai modifié le Chroniqueur pour **capturer le message d'erreur** de l'application quand elle crash.

**Changements** :
- Capture de `stderr` au lieu de le jeter
- Vérification immédiate (0.5s) si l'app crash
- Affichage du message d'erreur complet

---

## 🚀 TESTER MAINTENANT

```powershell
cd C:\sentire-guardian-v9

python tools/forge_chronicle.py "C:\Program Files\Unigine\Superposition Benchmark\bin\superposition.exe" --duration 30
```

**Cette fois, si l'app crash, vous verrez** :
```
❌ Application crashée immédiatement (code: -1073741515)
   Message d'erreur: [Le vrai message d'erreur de Superposition]
```

---

## 🔍 CAUSES POSSIBLES

### 1. DLL Manquantes

**Symptôme** : Code d'erreur -1073741515 (0xC0000135)
**Cause** : L'app cherche une DLL qui n'existe pas
**Solution** : 
- Vérifier que Superposition est correctement installé
- Essayer de lancer `superposition.exe` MANUELLEMENT depuis l'Explorateur
- Voir si des DLLs Visual C++ sont manquantes

### 2. DirectX/Vulkan Non Disponibles

**Symptôme** : Erreur liée à graphics/rendering
**Cause** : Drivers GPU ou API graphique manquants
**Solution** :
- Mettre à jour drivers NVIDIA
- Installer DirectX Runtime : https://www.microsoft.com/en-us/download/details.aspx?id=35

### 3. Permissions Insuffisantes

**Symptôme** : Access denied
**Cause** : Certains benchmarks nécessitent droits admin
**Solution** :
```powershell
# Lancer PowerShell en tant qu'Administrateur
cd C:\sentire-guardian-v9
python tools/forge_chronicle.py "..." --duration 30
```

### 4. Arguments Requis

**Symptôme** : Crash immédiat sans erreur claire
**Cause** : L'app attend des arguments en ligne de commande
**Solution** : Certains benchmarks ont un mode headless/console

---

## 🧪 TESTS ALTERNATIFS

### Test 1 : Application Simple

```powershell
# Tester avec une app qui marche à coup sûr
python tools/forge_chronicle.py "C:\Windows\System32\notepad.exe" --duration 10
```

**Résultat attendu** : Devrait collecter ~50 échantillons

### Test 2 : Lancement Manuel

```powershell
# 1. Ouvrir un terminal dans le répertoire de Superposition
cd "C:\Program Files\Unigine\Superposition Benchmark\bin"

# 2. Lancer manuellement
.\superposition.exe
```

**Si ça marche** : Le problème vient du Chroniqueur
**Si ça crash** : Le problème vient de Superposition lui-même

### Test 3 : Diagnostic Windows

```powershell
# Vérifier les DLLs requises
dumpbin /dependents "C:\Program Files\Unigine\Superposition Benchmark\bin\superposition.exe"
```

---

## 📋 INFORMATIONS À COLLECTER

**Relancer le Chroniqueur avec le nouveau code et copier** :
1. Le code d'erreur : `(code: XXXXX)`
2. Le message d'erreur complet
3. La version de Superposition installée
4. Si le lancement manuel (double-clic) fonctionne

---

## 🎯 PROCHAINES ÉTAPES

**Une fois le message d'erreur obtenu**, je pourrai :
1. Identifier la cause exacte
2. Proposer une solution spécifique
3. Éventuellement ajouter des arguments en ligne de commande si nécessaire

---

**Relancez le test et partagez le message d'erreur complet !** 🔍

