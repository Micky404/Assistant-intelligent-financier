# Description du Dataset transactions_fake.csv

## Aperçu général
Le fichier `transactions_fake.csv` contient un ensemble de transactions bancaires anonymisées représentant l'activité financière d'un utilisateur sur une période donnée. Ce jeu de données est représentatif des données réelles traitées par l'application Bankin' mais a été anonymisé pour protéger la vie privée des utilisateurs.

## Structure du fichier
Format : CSV (Comma Separated Values)
Encodage : UTF-8
Nombre de lignes : 2 459
Nombre de colonnes : 5

## Description des colonnes

| Colonne | Type | Description |
|---------|------|-------------|
| date | Chaîne de caractères | Date de la transaction au format "mois jour, année" (ex: "janvier 2, 2024") |
| description_fake | Chaîne de caractères | Libellé de la transaction tel qu'il apparaît sur le relevé bancaire. Ce champ a été anonymisé mais reste représentatif des libellés bancaires réels |
| net_amount | Numérique | Montant de la transaction en euros. Les valeurs négatives représentent des dépenses, les valeurs positives des revenus |
| category_name | Chaîne de caractères | Catégorie détaillée de la transaction (ex: "Supermarché / Epicerie", "Restaurants", "Loyer") |
| parent_name | Chaîne de caractères | Catégorie principale à laquelle appartient la transaction (ex: "Alimentation & Restau.", "Logement") |

## Particularités à noter

1. **Catégorisation hiérarchique** : Le système de catégorisation est organisé en deux niveaux - catégorie principale (`parent_name`) et sous-catégorie (`category_name`).

2. **Format des descriptions** : Les descriptions des transactions sont en minuscules et peuvent contenir différents formats typiques des relevés bancaires :
   - Transactions par carte bancaire (préfixées par "cb")
   - Prélèvements automatiques (préfixés par "prlv")
   - Virements (préfixés par "vir")
   - Références diverses (numéros, dates, lieux)

3. **Diversité des catégories** : Le dataset contient environ 100 sous-catégories réparties en 15 catégories principales, couvrant l'ensemble des types de transactions qu'un utilisateur peut rencontrer dans sa vie quotidienne.

## Utilisation prévue
Ce dataset est destiné à être utilisé pour développer et tester des fonctionnalités d'analyse et de coaching financier pour l'application Bankin'. Il peut servir à entraîner des modèles de catégorisation, d'analyse de tendances, de détection d'anomalies, ou à alimenter des systèmes de recommandation personnalisée.
