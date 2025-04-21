# Assistant-intelligent-financier


## Présentation

Ce projet implémente un assistant financier intelligent capable d'analyser des données de transactions bancaires et de répondre à des questions en langage naturel. L'assistant combine des analyses financières déterministes avec l'intelligence artificielle de ChatGPT pour offrir une expérience conversationnelle intuitive et des insights financiers pertinents.

## Fonctionnalités

L'assistant peut répondre à 5 types de questions financières :

1. **Analyse des prélèvements automatiques vs achats ponctuels**
   - Répartition des dépenses par type de transaction
   - Visualisation de la distribution

2. **Analyse des principales catégories de dépenses**
   - Identification des postes de dépenses principaux
   - Comparaison avec des recommandations budgétaires

3. **Identification des dépenses inhabituelles**
   - Détection des anomalies par analyse statistique
   - Visualisation des tendances de dépenses

4. **Analyse du potentiel d'économies mensuelles**
   - Recommandations pour atteindre un objectif d'économies
   - Simulation d'impact sur le budget

5. **Analyse de la capacité d'emprunt immobilier**
   - Calcul de la capacité d'emprunt basé sur les revenus et dépenses
   - Recommandations pour optimiser cette capacité

## Architecture technique

### Structure du projet

- `fonctions.py` : Contient toutes les fonctions d'analyse financière
- `assistant.py` : Gère l'interaction avec l'API ChatGPT et la génération de réponses
- `main.py` : Interface utilisateur en ligne de commande

### Choix techniques

#### Points forts

1. **Architecture modulaire bien structurée**
   - Séparation claire entre les fonctions d'analyse et l'interface utilisateur
   - Utilisation d'un module dédié pour l'assistant IA
   - Cette modularité facilite la maintenance et l'évolution du code

2. **Analyses financières complètes et pertinentes**
   - Couverture de 5 domaines d'analyse financière essentiels
   - Fonctions d'analyse sophistiquées avec des calculs statistiques pertinents (z-scores, tendances, etc.)
   - Visualisations graphiques pour chaque type d'analyse

3. **Intégration efficace de l'IA**
   - Utilisation de ChatGPT pour classifier les questions et générer des réponses en langage naturel
   - Approche hybride combinant des analyses déterministes avec l'IA générative
   - Séparation entre classification (faible température) et génération de réponses (température plus élevée)

4. **Interface utilisateur conversationnelle**
   - Expérience utilisateur naturelle via une interface en ligne de commande
   - Possibilité d'approfondir l'analyse avec l'option "voir les détails"
   - Exemples de questions pour guider l'utilisateur

5. **Gestion des erreurs**
   - Try/except pour gérer les erreurs d'API et de traitement des données
   - Validation des données d'entrée (dates, montants, etc.)

#### Axes d'amélioration potentiels

1. **Optimisation des appels API**
   - Les appels à l'API OpenAI pourraient être optimisés pour réduire les coûts
   - Possibilité de mettre en cache certaines classifications fréquentes

2. **Extraction de paramètres**
   - Le système pourrait extraire automatiquement des paramètres des questions
   - Utilisation des fonctions OpenAI pour structurer les réponses

3. **Persistance du contexte**
   - L'assistant ne maintient pas le contexte entre les questions
   - Une gestion de session permettrait des conversations plus naturelles

4. **Sécurité des données**
   - La clé API devrait être placée dans une variable d'environnement
   - Protection des données financières sensibles

## Installation et utilisation

### Prérequis

- Python 3.8+
- Packages requis : pandas, matplotlib, numpy, openai

### Installation

# Cloner le dépôt
git clone https://github.com/votre-username/assistant-financier.git
cd assistant-financier

# Créer un environnement virtuel
python -m venv env
source env/bin/activate  # Sur Windows : env\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configuration
1. Obtenez une clé API OpenAI sur https://platform.openai.com
2. Modifiez le fichier assistant.py pour y ajouter votre clé API ou utilisez une variable d'environnement


# Utilisation
python main.py
