#!/usr/bin/env python3
"""
Sceau de la Pureté Doctrinale – Guardian V9
Analyse statique doctrinale pour la Dualité, la Trinité Cognitive et la Résilience.
Usage : python seal_of_purity.py [racine_du_repo]
Gloire à la Résilience Souveraine.
"""

import os
import ast
import re
import sys
import json
from pathlib import Path

# -- Constantes sacrées pour la Hiérarchie des Hérésies --
GRAVITE_CRITIQUE = "CRITIQUE"
GRAVITE_MAJEURE = "MAJEURE"
GRAVITE_AVERTISSEMENT = "AVERTISSEMENT"

# -- Chargement de la Loi sacrée --
CONFIG_PATH = Path(__file__).parent / ".seal_config.json"
if not CONFIG_PATH.exists():
    print("⚠️  Loi doctrinale absente (.seal_config.json introuvable). La forge ne peut opérer sans la Loi.")
    sys.exit(1)
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    SEAL_CONFIG = json.load(f)

FORBIDDEN_SYMBOLS = set(SEAL_CONFIG.get("forbidden_symbols_python", []))
STRATEGY_KEYWORDS_C = set(SEAL_CONFIG.get("forbidden_keywords_c", []))
DUALITY_IMPORTS_PY = set(SEAL_CONFIG.get("duality_imports_python", []))
TRINITY_HEURISTICS = SEAL_CONFIG.get("trinity_heuristics", [])

# --- Définition des hérésies ---
class Heresie:
    def __init__(self, type_, fichier, ligne, gravite, texte, verset):
        self.type = type_
        self.fichier = fichier
        self.ligne = ligne
        self.gravite = gravite
        self.texte = texte
        self.verset = verset

    def to_markdown(self):
        return (f"- **Type**: {self.type}\n"
                f"  - **Fichier**: `{{self.fichier}}` (ligne {{self.ligne}})\n"
                f"  - **Gravité**: `{{self.gravite}}`\n"
                f"  - **Hérésie**: {{self.texte}}\n"
                f"  - **Verset violé**: {{self.verset}}\n")

# --- Sceau de la Dualité : analyse Python ---
def scan_python_duality(python_file):
    heresies = []
    with open(python_file, "r", encoding="utf-8") as f:
        source = f.read()
    try:
        tree = ast.parse(source, filename=python_file)
    except Exception as e:
        heresies.append(Heresie(
            "Dualité", python_file, 1, GRAVITE_MAJEURE,
            "Sanctuaire Python non parsable (erreur syntaxe) : " + str(e),
            "II. L'ARCHITECTURE SACRÉE"))
        return heresies

    # Recherche d'opérations mathématiques sacrées (Sʀ, Iφ, etc.) hors FFI
    class MathSacreeVisitor(ast.NodeVisitor):
        def visit_Name(self, node):
            if node.id in FORBIDDEN_SYMBOLS:
                heresies.append(Heresie(
                    "Dualité", python_file, node.lineno, GRAVITE_MAJEURE,
                    f"Usage profane de la Mathématique Sacrée '{{node.id}}' dans l'Esprit Python.",
                    "II. L'ARCHITECTURE SACRÉE"))
        def visit_Import(self, node):
            for alias in node.names:
                if alias.name in DUALITY_IMPORTS_PY:
                    heresies.append(Heresie(
                        "Dualité", python_file, node.lineno, GRAVITE_AVERTISSEMENT,
                        f"Import direct du Corps Natif ('{{alias.name}}') dans l'Esprit Python.",
                        "II. L'ARCHITECTURE SACRÉE"))
        def visit_ImportFrom(self, node):
            if node.module and node.module in DUALITY_IMPORTS_PY:
                heresies.append(Heresie(
                    "Dualité", python_file, node.lineno, GRAVITE_AVERTISSEMENT,
                    f"Import direct du Corps Natif ('{{node.module}}') dans l'Esprit Python.",
                    "II. L'ARCHITECTURE SACRÉE"))
    MathSacreeVisitor().visit(tree)
    return heresies

# --- Sceau de la Dualité : analyse C/C++ ---
def scan_c_duality(c_file):
    heresies = []
    with open(c_file, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    for idx, line in enumerate(lines, 1):
        for keyword in STRATEGY_KEYWORDS_C:
            if re.search(rf"\b{{re.escape(keyword)}}\b", line, re.IGNORECASE):
                heresies.append(Heresie(
                    "Dualité", c_file, idx, GRAVITE_MAJEURE,
                    f"Trace d'une logique stratégique/consciente ('{{keyword}}') dans le Corps natif.",
                    "II. L'ARCHITECTURE SACRÉE"))
    return heresies

# --- Sceau de la Trinité Cognitive ---
def scan_python_trinite(python_file):
    heresies = []
    with open(python_file, "r", encoding="utf-8") as f:
        source = f.read()
    for rule in TRINITY_HEURISTICS:
        if all(kw in source for kw in rule.get("must_contain", [])):
            heresies.append(Heresie(
                "Trinité", python_file, 1, rule.get("gravite", GRAVITE_MAJEURE),
                rule.get("message", "Fusion profane des organes dans un même sanctuaire."),
                "III. LA TRINITÉ COGNITIVE"))
    return heresies

# --- Sceau de la Résilience ---
def scan_python_resilience(python_file):
    heresies = []
    with open(python_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for idx, line in enumerate(lines, 1):
        # Détection des rituels critiques sans try/except
        if re.search(r"(open\(|os\.remove|os\.rename|ctypes\.|requests\.|socket\.)", line):
            contexte = "".join(lines[max(0,idx-4): min(len(lines), idx+3)])
            if "try:" not in contexte:
                heresies.append(Heresie(
                    "Résilience", python_file, idx, GRAVITE_CRITIQUE,
                    f"Rituel critique sans garde sacrée (try/except) : {{line.strip()}}",
                    "IV. LA PURETÉ AVANT LA FACILITÉ"))
    return heresies

# --- Explorateur de la cathédrale ---
def explorer_cathedrale(racine):
    heresies = []
    for root, dirs, files in os.walk(racine):
        for file in files:
            path = os.path.join(root, file)
            if file.endswith(".py"):
                heresies += scan_python_duality(path)
                heresies += scan_python_trinite(path)
                heresies += scan_python_resilience(path)
            elif file.endswith(('.c', '.h')):
                heresies += scan_c_duality(path)
    return heresies

def rapport_markdown(heresies, sortie):
    with open(sortie, "w", encoding="utf-8") as f:
        f.write("# Rapport de Pureté Doctrinale\n\n")
        if not heresies:
            f.write("Aucune hérésie détectée. Gloire à la Résilience Souveraine.\n")
        else:
            for h in heresies:
                f.write(h.to_markdown() + "\n")

def main():
    racine = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"Analyse doctrinale en cours sur : {{racine}}")
    heresies = explorer_cathedrale(racine)
    rapport_markdown(heresies, "rapport_purete.md")
    print(f"Analyse terminée. Rapport généré : rapport_purete.md")
    if heresies:
        print(f"{{len(heresies)}} hérésies détectées. Voir le rapport pour le détail.")
    else:
        print("Aucune hérésie détectée. Le Vaisseau est pur.")

if __name__ == "__main__":
    main()