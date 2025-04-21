import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def charger_donnees(chemin_fichier):
    """
    Charge les données de transactions depuis un fichier CSV.
    
    Args:
        chemin_fichier (str): Chemin vers le fichier CSV des transactions
        
    Returns:
        DataFrame: Données de transactions chargées
    """
    try:
        # Chargement des données avec pandas
        df = pd.read_csv(chemin_fichier)
        
        # Conversion de la colonne date en format datetime
        df['date'] = pd.to_datetime(df['date'], format="%B %d, %Y", errors='coerce')
        
        # Tri des données par date
        df = df.sort_values('date')
        
        return df
    except Exception as e:
        print(f"Erreur lors du chargement des données: {e}")
        return None

def identifier_type_transaction(description):
    """
    Identifie le type de transaction (prélèvement automatique ou achat ponctuel)
    basé sur la description.
    
    Args:
        description (str): Description de la transaction
        
    Returns:
        str: Type de transaction ('prelevement_auto', 'achat_ponctuel', ou 'autre')
    """
    description = str(description).lower()
    
    # Identifie les prélèvements automatiques
    if 'prlv' in description or 'prelevement' in description:
        return 'prelevement_auto'
    # Identifie les achats ponctuels (transactions par carte)
    elif 'cb' in description or 'carte' in description:
        return 'achat_ponctuel'
    # Autres types de transactions
    else:
        return 'autre'

def analyser_part_prelevements(df):
    """
    Analyse la part des prélèvements automatiques par rapport aux achats ponctuels.
    
    Args:
        df (DataFrame): Données de transactions
        
    Returns:
        dict: Résultats de l'analyse
    """
    # Copie du DataFrame pour éviter de modifier l'original
    df_analyse = df.copy()
    
    # Ajout d'une colonne pour le type de transaction
    df_analyse['type_transaction'] = df_analyse['description_fake'].apply(identifier_type_transaction)
    
    # Filtrer les dépenses (montants négatifs)
    df_depenses = df_analyse[df_analyse['net_amount'] < 0].copy()
    
    # Calculer le montant total des dépenses par type de transaction
    montants_par_type = df_depenses.groupby('type_transaction')['net_amount'].sum().abs()
    
    # Calculer les pourcentages
    total_depenses = montants_par_type.sum()
    pourcentages = (montants_par_type / total_depenses * 100).round(2)
    
    # Compter le nombre de transactions par type
    nombre_transactions = df_depenses['type_transaction'].value_counts()
    
    # Préparer les résultats
    resultats = {
        'montants': montants_par_type.to_dict(),
        'pourcentages': pourcentages.to_dict(),
        'nombre_transactions': nombre_transactions.to_dict(),
        'total_depenses': total_depenses
    }
    
    return resultats

def afficher_part_prelevements(resultats):
    """
    Affiche les résultats de l'analyse des prélèvements automatiques vs achats ponctuels.
    
    Args:
        resultats (dict): Résultats de l'analyse
    """
    print("\n=== ANALYSE DES PRÉLÈVEMENTS AUTOMATIQUES VS ACHATS PONCTUELS ===\n")
    
    # Afficher les montants et pourcentages
    print("Répartition des dépenses par type de transaction:")
    print(f"Total des dépenses: {resultats['total_depenses']:.2f} €\n")
    
    for type_transaction in ['prelevement_auto', 'achat_ponctuel', 'autre']:
        if type_transaction in resultats['montants']:
            montant = resultats['montants'][type_transaction]
            pourcentage = resultats['pourcentages'][type_transaction]
            nb_transactions = resultats['nombre_transactions'].get(type_transaction, 0)
            
            print(f"{type_transaction.replace('_', ' ').capitalize()}:")
            print(f"  - Montant total: {montant:.2f} €")
            print(f"  - Pourcentage du budget: {pourcentage}%")
            print(f"  - Nombre de transactions: {nb_transactions}")
            print()

def visualiser_part_prelevements(resultats):
    """
    Crée une visualisation graphique de la répartition des dépenses.
    
    Args:
        resultats (dict): Résultats de l'analyse
    """
    # Préparer les données pour le graphique
    labels = [k.replace('_', ' ').capitalize() for k in resultats['pourcentages'].keys()]
    sizes = list(resultats['pourcentages'].values())
    
    # Créer le graphique en camembert
    plt.figure(figsize=(10, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('Répartition des dépenses par type de transaction')
    
    # Ajouter une légende avec les montants
    montants = [f"{k}: {v:.2f} €" for k, v in resultats['montants'].items()]
    plt.legend(montants, loc="best")
    
    plt.tight_layout()
    plt.savefig('repartition_depenses.png')
    plt.show()

def analyser_categories_depenses(df):
    """
    Analyse les principales catégories de dépenses.
    
    Args:
        df (DataFrame): Données de transactions
        
    Returns:
        dict: Résultats de l'analyse des catégories
    """
    # Copie du DataFrame pour éviter de modifier l'original
    df_analyse = df.copy()
    
    # Filtrer les dépenses (montants négatifs)
    df_depenses = df_analyse[df_analyse['net_amount'] < 0].copy()
    
    # Calculer le montant total des dépenses par catégorie principale
    montants_par_categorie = df_depenses.groupby('parent_name')['net_amount'].sum().abs()
    
    # Calculer les pourcentages
    total_depenses = montants_par_categorie.sum()
    pourcentages = (montants_par_categorie / total_depenses * 100).round(2)
    
    # Trier par montant décroissant
    montants_par_categorie = montants_par_categorie.sort_values(ascending=False)
    pourcentages = pourcentages.reindex(montants_par_categorie.index)
    
    # Préparer les résultats
    resultats = {
        'montants': montants_par_categorie.to_dict(),
        'pourcentages': pourcentages.to_dict(),
        'total_depenses': total_depenses
    }
    
    return resultats

def obtenir_recommandations_budget():
    """
    Fournit des recommandations budgétaires standards par catégorie.
    
    Returns:
        dict: Recommandations budgétaires en pourcentage
    """
    # Recommandations budgétaires standards (pourcentages)
    # Source: Règle 50-30-20 et autres recommandations financières courantes
    recommandations = {
        'Logement': 25.0,  # Loyer, charges, assurances...
        'Alimentation & Restau.': 15.0,
        'Auto & Transports': 15.0,
        'Loisirs & Sorties': 10.0,
        'Achats & Shopping': 10.0,
        'Santé': 5.0,
        'Abonnements': 5.0,
        'Banque': 5.0,
        'Impôts & Taxes': 5.0,
        'Esthétique & Soins': 2.0,
        'Divers': 3.0
    }
    
    return recommandations

def comparer_avec_recommandations(resultats_analyse):
    """
    Compare les dépenses réelles avec les recommandations budgétaires.
    
    Args:
        resultats_analyse (dict): Résultats de l'analyse des catégories
        
    Returns:
        dict: Comparaison entre dépenses réelles et recommandations
    """
    # Obtenir les recommandations
    recommandations = obtenir_recommandations_budget()
    
    # Préparer la comparaison
    comparaison = {}
    
    for categorie, pourcentage_reel in resultats_analyse['pourcentages'].items():
        pourcentage_recommande = recommandations.get(categorie, 0)
        difference = pourcentage_reel - pourcentage_recommande
        
        comparaison[categorie] = {
            'pourcentage_reel': pourcentage_reel,
            'pourcentage_recommande': pourcentage_recommande,
            'difference': difference,
            'statut': 'conforme' if abs(difference) <= 3 else ('supérieur' if difference > 0 else 'inférieur')
        }
    
    return comparaison

def afficher_categories_depenses(resultats, comparaison):
    """
    Affiche les résultats de l'analyse des catégories de dépenses et la comparaison
    avec les recommandations budgétaires.
    
    Args:
        resultats (dict): Résultats de l'analyse des catégories
        comparaison (dict): Comparaison avec les recommandations
    """
    print("\n=== ANALYSE DES PRINCIPALES CATÉGORIES DE DÉPENSES ===\n")
    
    # Afficher le total des dépenses
    print(f"Total des dépenses: {resultats['total_depenses']:.2f} €\n")
    
    # Afficher les catégories principales
    print("Répartition des dépenses par catégorie principale:")
    for categorie, montant in resultats['montants'].items():
        pourcentage = resultats['pourcentages'][categorie]
        comp = comparaison.get(categorie, {})
        pourcentage_recommande = comp.get('pourcentage_recommande', 0)
        difference = comp.get('difference', 0)
        statut = comp.get('statut', 'non spécifié')
        
        print(f"\n{categorie}:")
        print(f"  - Montant total: {montant:.2f} €")
        print(f"  - Pourcentage du budget: {pourcentage}%")
        print(f"  - Recommandation standard: {pourcentage_recommande}%")
        
        # Afficher la comparaison avec les recommandations
        if statut == 'conforme':
            print(f"  - Statut: ✅ Conforme aux recommandations (différence: {difference:.2f}%)")
        elif statut == 'supérieur':
            print(f"  - Statut: ⚠️ Supérieur aux recommandations (différence: +{difference:.2f}%)")
        elif statut == 'inférieur':
            print(f"  - Statut: ℹ️ Inférieur aux recommandations (différence: {difference:.2f}%)")

def visualiser_categories_depenses(resultats, comparaison):
    """
    Crée une visualisation graphique des catégories de dépenses et leur comparaison
    avec les recommandations budgétaires.
    
    Args:
        resultats (dict): Résultats de l'analyse des catégories
        comparaison (dict): Comparaison avec les recommandations
    """
    # Préparer les données pour le graphique
    categories = list(resultats['pourcentages'].keys())
    pourcentages_reels = list(resultats['pourcentages'].values())
    pourcentages_recommandes = [comparaison.get(cat, {}).get('pourcentage_recommande', 0) for cat in categories]
    
    # Créer le graphique à barres
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Définir la largeur des barres
    bar_width = 0.35
    index = np.arange(len(categories))
    
    # Créer les barres
    rects1 = ax.bar(index, pourcentages_reels, bar_width, label='Dépenses réelles')
    rects2 = ax.bar(index + bar_width, pourcentages_recommandes, bar_width, label='Recommandations')
    
    # Ajouter les étiquettes, le titre et la légende
    ax.set_xlabel('Catégories')
    ax.set_ylabel('Pourcentage du budget (%)')
    ax.set_title('Comparaison des dépenses réelles avec les recommandations budgétaires')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.legend()
    
    # Ajouter les valeurs sur les barres
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    autolabel(rects1)
    autolabel(rects2)
    
    plt.tight_layout()
    plt.savefig('comparaison_categories.png')
    plt.show()

def identifier_depenses_inhabituelles(df, seuil_z_score=2.5, periode_recente_mois=3):
    """
    Identifie les dépenses inhabituelles dans les transactions récentes.
    
    Args:
        df (DataFrame): Données de transactions
        seuil_z_score (float): Seuil du Z-score pour considérer une dépense comme inhabituelle
        periode_recente_mois (int): Nombre de mois considérés comme "récents"
        
    Returns:
        dict: Résultats de l'analyse des dépenses inhabituelles
    """
    # Copie du DataFrame pour éviter de modifier l'original
    df_analyse = df.copy()
    
    # S'assurer que la colonne date est au format datetime
    if not pd.api.types.is_datetime64_any_dtype(df_analyse['date']):
        df_analyse['date'] = pd.to_datetime(df_analyse['date'], errors='coerce')
    
    # Filtrer les dépenses (montants négatifs)
    df_depenses = df_analyse[df_analyse['net_amount'] < 0].copy()
    
    # Calculer la date limite pour les transactions récentes
    date_max = df_depenses['date'].max()
    if pd.notna(date_max):
        date_limite = date_max - pd.DateOffset(months=periode_recente_mois)
    else:
        # Si date_max est NaT, utiliser une valeur par défaut
        date_limite = pd.NaT
    
    # Filtrer les transactions récentes
    df_recentes = df_depenses[df_depenses['date'] >= date_limite].copy() if pd.notna(date_limite) else df_depenses.copy()
    
    # Calculer les statistiques par catégorie
    stats_par_categorie = {}
    depenses_inhabituelles = []
    
    for categorie in df_depenses['category_name'].unique():
        # Transactions historiques pour cette catégorie
        df_cat_hist = df_depenses[df_depenses['category_name'] == categorie]
        
        # S'il y a suffisamment de données historiques
        if len(df_cat_hist) >= 5:
            montants = df_cat_hist['net_amount'].abs()
            moyenne = montants.mean()
            ecart_type = montants.std()
            
            # Stocker les statistiques
            stats_par_categorie[categorie] = {
                'moyenne': moyenne,
                'ecart_type': ecart_type,
                'count': len(montants)
            }
            
            # Vérifier les transactions récentes pour cette catégorie
            df_cat_recentes = df_recentes[df_recentes['category_name'] == categorie]
            
            for _, transaction in df_cat_recentes.iterrows():
                montant = abs(transaction['net_amount'])
                
                # Calculer le Z-score
                if ecart_type > 0:  # Éviter division par zéro
                    z_score = (montant - moyenne) / ecart_type
                    
                    # Si le Z-score dépasse le seuil, c'est une dépense inhabituelle
                    if z_score > seuil_z_score:
                        depenses_inhabituelles.append({
                            'date': transaction['date'],
                            'description': transaction['description_fake'],
                            'montant': montant,
                            'categorie': transaction['category_name'],
                            'parent_categorie': transaction['parent_name'],
                            'z_score': z_score,
                            'moyenne_categorie': moyenne
                        })
    
    # Trier les dépenses inhabituelles par Z-score décroissant
    depenses_inhabituelles = sorted(depenses_inhabituelles, key=lambda x: x['z_score'], reverse=True)
    
    return {
        'depenses_inhabituelles': depenses_inhabituelles,
        'stats_par_categorie': stats_par_categorie,
        'periode_recente_debut': date_limite,
        'periode_recente_fin': date_max
    }

def afficher_depenses_inhabituelles(resultats):
    """
    Affiche les résultats de l'analyse des dépenses inhabituelles.
    
    Args:
        resultats (dict): Résultats de l'analyse des dépenses inhabituelles
    """
    print("\n=== ANALYSE DES DÉPENSES INHABITUELLES ===\n")
    
    # Afficher la période analysée
    debut = resultats.get('periode_recente_debut')
    fin = resultats.get('periode_recente_fin')
    
    # Vérifier si les dates sont valides avant d'appliquer strftime
    if pd.notna(debut) and pd.notna(fin):
        debut_str = debut.strftime('%d/%m/%Y')
        fin_str = fin.strftime('%d/%m/%Y')
        print(f"Période analysée: du {debut_str} au {fin_str}\n")
    else:
        print("Période analysée: données temporelles incomplètes\n")
    
    # Afficher les dépenses inhabituelles
    depenses = resultats['depenses_inhabituelles']
    
    if depenses:
        print(f"Nombre de dépenses inhabituelles détectées: {len(depenses)}\n")
        
        # Afficher les 5 dépenses les plus inhabituelles
        for i, depense in enumerate(depenses[:5], 1):
            # Vérifier si la date est valide
            if pd.notna(depense['date']):
                date = depense['date'].strftime('%d/%m/%Y')
            else:
                date = "Date inconnue"
                
            description = depense['description']
            montant = depense['montant']
            categorie = depense['categorie']
            z_score = depense['z_score']
            moyenne = depense['moyenne_categorie']
            
            print(f"Dépense inhabituelle #{i}:")
            print(f"  - Date: {date}")
            print(f"  - Description: {description}")
            print(f"  - Montant: {montant:.2f} €")
            print(f"  - Catégorie: {categorie}")
            print(f"  - Écart: {z_score:.2f} fois l'écart-type")
            print(f"  - Moyenne habituelle pour cette catégorie: {moyenne:.2f} €")
            print()
    else:
        print("Aucune dépense inhabituelle détectée dans la période récente.")

def visualiser_depenses_inhabituelles(resultats):
    """
    Crée une visualisation graphique des dépenses inhabituelles.
    
    Args:
        resultats (dict): Résultats de l'analyse des dépenses inhabituelles
    """
    depenses = resultats['depenses_inhabituelles']
    
    if not depenses:
        print("Pas de données suffisantes pour visualiser les dépenses inhabituelles.")
        return
    
    # Limiter à 10 dépenses maximum pour la lisibilité
    depenses = depenses[:10]
    
    # Préparer les données
    categories = [d['categorie'] for d in depenses]
    montants = [d['montant'] for d in depenses]
    moyennes = [d['moyenne_categorie'] for d in depenses]
    descriptions = [f"{d['description'][:20]}..." if len(d['description']) > 20 else d['description'] for d in depenses]
    
    # Créer le graphique
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Définir la largeur des barres
    bar_width = 0.35
    index = np.arange(len(categories))
    
    # Créer les barres
    rects1 = ax.bar(index, montants, bar_width, label='Montant inhabituel')
    rects2 = ax.bar(index + bar_width, moyennes, bar_width, label='Montant moyen habituel')
    
    # Ajouter les étiquettes, le titre et la légende
    ax.set_xlabel('Transactions')
    ax.set_ylabel('Montant (€)')
    ax.set_title('Dépenses inhabituelles comparées aux moyennes habituelles')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(descriptions, rotation=45, ha='right')
    ax.legend()
    
    # Ajouter les valeurs sur les barres
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.0f}€',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    autolabel(rects1)
    autolabel(rects2)
    
    plt.tight_layout()
    plt.savefig('depenses_inhabituelles.png')
    plt.show()

def analyser_tendances_mensuelles(df, nb_mois_recents=6):
    """
    Analyse les tendances mensuelles des dépenses.
    
    Args:
        df (DataFrame): Données de transactions
        nb_mois_recents (int): Nombre de mois à analyser
        
    Returns:
        dict: Résultats de l'analyse des tendances mensuelles
    """
    # Copie du DataFrame pour éviter de modifier l'original
    df_analyse = df.copy()
    
    # S'assurer que la colonne date est au format datetime
    if not pd.api.types.is_datetime64_any_dtype(df_analyse['date']):
        df_analyse['date'] = pd.to_datetime(df_analyse['date'], errors='coerce')
    
    # Filtrer les dépenses (montants négatifs)
    df_depenses = df_analyse[df_analyse['net_amount'] < 0].copy()
    
    # Vérifier s'il y a des dates valides
    if df_depenses['date'].isna().all():
        return {
            'tendances': {},
            'depenses_totales': {},
            'mois_analyses': [],
            'periode_debut': pd.NaT,
            'periode_fin': pd.NaT
        }
    
    # Ajouter des colonnes pour le mois et l'année
    df_depenses['mois'] = df_depenses['date'].dt.strftime('%Y-%m')
    
    # Obtenir les mois uniques, triés chronologiquement
    mois_uniques = sorted(df_depenses['mois'].dropna().unique())
    
    # Si aucun mois valide n'est trouvé, retourner un dictionnaire vide
    if not mois_uniques:
        return {
            'tendances': {},
            'depenses_totales': {},
            'mois_analyses': [],
            'periode_debut': pd.NaT,
            'periode_fin': pd.NaT
        }
    
    # Limiter aux n derniers mois
    if len(mois_uniques) > nb_mois_recents:
        mois_recents = mois_uniques[-nb_mois_recents:]
    else:
        mois_recents = mois_uniques
    
    # Filtrer pour ne garder que les mois récents
    df_recents = df_depenses[df_depenses['mois'].isin(mois_recents)].copy()
    
    # Calculer les dépenses totales par mois
    depenses_totales = df_recents.groupby('mois')['net_amount'].sum().abs().to_dict()
    
    # Calculer les dépenses par catégorie et par mois
    depenses_par_categorie = {}
    
    for categorie in df_recents['parent_name'].unique():
        df_cat = df_recents[df_recents['parent_name'] == categorie]
        depenses_mensuelles = df_cat.groupby('mois')['net_amount'].sum().abs()
        
        # Calculer la variation en pourcentage entre le premier et le dernier mois
        if len(depenses_mensuelles) >= 2:
            premier_mois = depenses_mensuelles.iloc[0]
            dernier_mois = depenses_mensuelles.iloc[-1]
            
            if premier_mois > 0:  # Éviter division par zéro
                variation_pct = ((dernier_mois - premier_mois) / premier_mois) * 100
            else:
                variation_pct = 0
            
            # Déterminer le statut de la tendance
            if abs(variation_pct) < 10:
                statut = 'stable'
            elif variation_pct > 0:
                statut = 'augmentation'
            else:
                statut = 'diminution'
            
            # Stocker les résultats
            depenses_par_categorie[categorie] = {
                'valeurs': depenses_mensuelles.to_dict(),
                'variation_pct': variation_pct,
                'statut': statut
            }
    
    # Trier les catégories par amplitude de variation
    depenses_par_categorie = {k: v for k, v in sorted(
        depenses_par_categorie.items(), 
        key=lambda item: abs(item[1]['variation_pct']), 
        reverse=True
    )}
    
    # Déterminer les dates de début et de fin de la période analysée
    try:
        if mois_recents:
            debut = pd.to_datetime(str(mois_recents[0]) + '-01')
            fin = pd.to_datetime(str(mois_recents[-1]) + '-01')
        else:
            debut = pd.NaT
            fin = pd.NaT
    except (TypeError, ValueError):
        debut = pd.NaT
        fin = pd.NaT
    
    return {
        'tendances': depenses_par_categorie,
        'depenses_totales': depenses_totales,
        'mois_analyses': mois_recents,
        'periode_debut': debut,
        'periode_fin': fin
    }

def analyser_potentiel_economies(df, montant_cible=200):
    """
    Analyse les dépenses pour identifier des opportunités d'économies.
    
    Args:
        df (DataFrame): Données de transactions
        montant_cible (float): Montant d'économies visé par mois
        
    Returns:
        dict: Résultats de l'analyse des économies potentielles
    """
    # Copie du DataFrame pour éviter de modifier l'original
    df_analyse = df.copy()
    
    # Filtrer les dépenses (montants négatifs)
    df_depenses = df_analyse[df_analyse['net_amount'] < 0].copy()
    
    # Calculer les dépenses moyennes mensuelles par catégorie
    # Ajouter une colonne pour le mois
    if not pd.api.types.is_datetime64_any_dtype(df_depenses['date']):
        df_depenses['date'] = pd.to_datetime(df_depenses['date'], errors='coerce')
    
    # Compter le nombre de mois uniques dans les données
    if df_depenses['date'].isna().all():
        nb_mois = 1  # Si pas de dates valides, supposer 1 mois
    else:
        df_depenses['mois'] = df_depenses['date'].dt.strftime('%Y-%m')
        mois_uniques = df_depenses['mois'].dropna().unique()
        nb_mois = max(len(mois_uniques), 1)  # Au moins 1 mois
    
    # Calculer les dépenses totales par catégorie
    depenses_par_categorie = df_depenses.groupby('parent_name')['net_amount'].sum().abs()
    
    # Calculer les dépenses moyennes mensuelles par catégorie
    depenses_mensuelles = (depenses_par_categorie / nb_mois).round(2)
    
    # Identifier les catégories non essentielles où des économies sont possibles
    categories_non_essentielles = [
        'Loisirs & Sorties', 'Achats & Shopping', 'Voyages / Vacances', 
        'Esthétique & Soins', 'Divers', 'Restaurants'
    ]
    
    # Filtrer les catégories non essentielles
    depenses_non_essentielles = depenses_mensuelles[depenses_mensuelles.index.isin(categories_non_essentielles)]
    
    # Trier par montant décroissant
    depenses_non_essentielles = depenses_non_essentielles.sort_values(ascending=False)
    
    # Calculer le potentiel d'économies (supposons qu'on peut réduire de 30% les dépenses non essentielles)
    potentiel_reduction = {}
    total_economies = 0
    
    for categorie, montant in depenses_non_essentielles.items():
        # Calculer une réduction réaliste (30% des dépenses non essentielles)
        reduction = round(montant * 0.3, 2)
        potentiel_reduction[categorie] = {
            'depense_mensuelle': montant,
            'reduction_possible': reduction,
            'nouvelle_depense': montant - reduction
        }
        total_economies += reduction
    
    # Calculer si l'objectif est atteint
    objectif_atteint = total_economies >= montant_cible
    
    # Préparer les suggestions spécifiques par catégorie
    suggestions = {
        'Loisirs & Sorties': [
            "Réduire les sorties au restaurant/bar de 1-2 fois par mois",
            "Chercher des activités gratuites ou à prix réduit",
            "Utiliser des applications de réduction ou des offres groupées"
        ],
        'Achats & Shopping': [
            "Reporter les achats non essentiels",
            "Comparer les prix avant d'acheter",
            "Privilégier les soldes et promotions"
        ],
        'Voyages / Vacances': [
            "Planifier les voyages à l'avance pour bénéficier de meilleurs tarifs",
            "Privilégier les destinations moins coûteuses",
            "Réduire la fréquence des voyages"
        ],
        'Esthétique & Soins': [
            "Espacer certains soins non essentiels",
            "Rechercher des alternatives moins coûteuses"
        ],
        'Divers': [
            "Revoir les abonnements et services payants",
            "Annuler les services peu utilisés"
        ],
        'Restaurants': [
            "Préparer plus de repas à la maison",
            "Limiter les livraisons de repas"
        ]
    }
    
    # Suggestions pour les catégories essentielles
    suggestions_essentielles = [
        "Comparer les offres de fournisseurs d'énergie et de télécommunications",
        "Optimiser les frais bancaires en négociant avec votre banque",
        "Revoir vos contrats d'assurance pour éviter les doublons ou sur-assurances"
    ]
    
    return {
        'economies_totales': total_economies,
        'objectif_atteint': objectif_atteint,
        'montant_manquant': max(0, montant_cible - total_economies),
        'potentiel_reduction': potentiel_reduction,
        'suggestions': suggestions,
        'suggestions_essentielles': suggestions_essentielles
    }

def afficher_potentiel_economies(resultats, montant_cible=200):
    """
    Affiche les résultats de l'analyse des économies potentielles.
    
    Args:
        resultats (dict): Résultats de l'analyse des économies
        montant_cible (float): Montant d'économies visé par mois
    """
    print("\n=== ANALYSE DES ÉCONOMIES POTENTIELLES ===\n")
    
    print(f"Objectif d'économies: {montant_cible:.2f} € par mois\n")
    
    # Afficher le potentiel d'économies par catégorie
    print("Économies potentielles par catégorie de dépenses:")
    
    for categorie, details in resultats['potentiel_reduction'].items():
        print(f"\n{categorie}:")
        print(f"  - Dépense mensuelle moyenne: {details['depense_mensuelle']:.2f} €")
        print(f"  - Réduction possible (30%): {details['reduction_possible']:.2f} €")
        print(f"  - Nouvelle dépense estimée: {details['nouvelle_depense']:.2f} €")
        
        # Afficher des suggestions spécifiques pour cette catégorie
        if categorie in resultats['suggestions']:
            print("  - Suggestions:")
            for suggestion in resultats['suggestions'][categorie]:
                print(f"    • {suggestion}")
    
    # Afficher le résumé
    print("\nRésumé des économies:")
    print(f"  - Total des économies potentielles: {resultats['economies_totales']:.2f} € par mois")
    
    if resultats['objectif_atteint']:
        print(f"  - ✅ Votre objectif de {montant_cible:.2f} € d'économies mensuelles est atteignable!")
        if resultats['economies_totales'] > montant_cible:
            surplus = resultats['economies_totales'] - montant_cible
            print(f"  - Vous pourriez même économiser {surplus:.2f} € supplémentaires.")
    else:
        print(f"  - ⚠️ Votre objectif n'est pas complètement atteint. Il manque {resultats['montant_manquant']:.2f} €.")
        print("  - Suggestions supplémentaires pour les catégories essentielles:")
        for suggestion in resultats['suggestions_essentielles']:
            print(f"    • {suggestion}")

def visualiser_potentiel_economies(resultats, montant_cible=200):
    """
    Crée une visualisation graphique des économies potentielles.
    
    Args:
        resultats (dict): Résultats de l'analyse des économies
        montant_cible (float): Montant d'économies visé par mois
    """
    # Extraire les données pour le graphique
    categories = list(resultats['potentiel_reduction'].keys())
    depenses_actuelles = [resultats['potentiel_reduction'][cat]['depense_mensuelle'] for cat in categories]
    depenses_reduites = [resultats['potentiel_reduction'][cat]['nouvelle_depense'] for cat in categories]
    economies = [resultats['potentiel_reduction'][cat]['reduction_possible'] for cat in categories]
    
    # Créer le graphique
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    
    # Graphique 1: Comparaison avant/après
    x = np.arange(len(categories))
    width = 0.35
    
    rects1 = ax1.bar(x - width/2, depenses_actuelles, width, label='Dépenses actuelles')
    rects2 = ax1.bar(x + width/2, depenses_reduites, width, label='Après réduction')
    
    ax1.set_title('Comparaison des dépenses avant/après réduction')
    ax1.set_ylabel('Montant mensuel (€)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, rotation=45, ha='right')
    ax1.legend()
    
    # Ajouter les valeurs sur les barres
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax1.annotate(f'{height:.0f}€',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    autolabel(rects1)
    autolabel(rects2)
    
    # Graphique 2: Économies par catégorie (camembert)
    ax2.pie(economies, labels=categories, autopct='%1.1f%%', startangle=90, shadow=True)
    ax2.axis('equal')
    ax2.set_title(f'Répartition des économies potentielles: {sum(economies):.2f}€')
    
    # Ajouter une ligne horizontale pour l'objectif
    if ax1.get_ylim()[1] < montant_cible:
        ax1.set_ylim(top=montant_cible * 1.2)
    
    plt.tight_layout()
    plt.savefig('potentiel_economies.png')
    plt.show()

def analyser_capacite_emprunt(df, taux_interet=0.03, duree_pret=25, taux_endettement_max=0.33):
    """
    Analyse la capacité d'emprunt immobilier en fonction des revenus et dépenses.
    
    Args:
        df (DataFrame): Données de transactions
        taux_interet (float): Taux d'intérêt annuel du prêt (par défaut: 3%)
        duree_pret (int): Durée du prêt en années (par défaut: 25 ans)
        taux_endettement_max (float): Taux d'endettement maximum (par défaut: 33%)
        
    Returns:
        dict: Résultats de l'analyse de capacité d'emprunt
    """
    # Copie du DataFrame pour éviter de modifier l'original
    df_analyse = df.copy()
    
    # Identifier les revenus (montants positifs)
    df_revenus = df_analyse[df_analyse['net_amount'] > 0].copy()
    
    # Identifier les dépenses (montants négatifs)
    df_depenses = df_analyse[df_analyse['net_amount'] < 0].copy()
    
    # Calculer le nombre de mois dans les données
    if not pd.api.types.is_datetime64_any_dtype(df_analyse['date']):
        df_analyse['date'] = pd.to_datetime(df_analyse['date'], errors='coerce')
    
    # Déterminer la période couverte par les données
    dates_valides = df_analyse['date'].dropna()
    if len(dates_valides) > 0:
        date_min = dates_valides.min()
        date_max = dates_valides.max()
        
        # Calculer le nombre de mois entre les deux dates
        nb_mois = ((date_max.year - date_min.year) * 12 + 
                   date_max.month - date_min.month) + 1
    else:
        # Si pas de dates valides, supposer 12 mois
        nb_mois = 12
        date_min = None
        date_max = None
    
    # Calculer le revenu mensuel moyen
    revenu_total = df_revenus['net_amount'].sum()
    revenu_mensuel_moyen = revenu_total / nb_mois
    
    # Calculer les dépenses mensuelles moyennes
    depenses_totales = df_depenses['net_amount'].abs().sum()
    depenses_mensuelles_moyennes = depenses_totales / nb_mois
    
    # Calculer le reste à vivre mensuel
    reste_a_vivre = revenu_mensuel_moyen - depenses_mensuelles_moyennes
    
    # Calculer la capacité de remboursement mensuelle selon le taux d'endettement max
    capacite_remboursement = revenu_mensuel_moyen * taux_endettement_max
    
    # Calculer la capacité d'emprunt
    # Formule: Capacité d'emprunt = Mensualité / (taux mensuel / (1 - (1 + taux mensuel)^(-nombre de mois)))
    taux_mensuel = taux_interet / 12
    nb_mensualites = duree_pret * 12
    
    # Éviter division par zéro
    if taux_mensuel > 0:
        denominateur = taux_mensuel / (1 - (1 + taux_mensuel) ** (-nb_mensualites))
        capacite_emprunt = capacite_remboursement / denominateur
    else:
        capacite_emprunt = capacite_remboursement * nb_mensualites
    
    # Calculer l'apport personnel recommandé (10% du montant emprunté)
    apport_recommande = capacite_emprunt * 0.1
    
    # Calculer le coût total du crédit
    cout_total = (capacite_remboursement * nb_mensualites) - capacite_emprunt
    
    # Calculer le taux d'endettement actuel
    taux_endettement_actuel = depenses_mensuelles_moyennes / revenu_mensuel_moyen
    
    # Identifier les catégories de dépenses compressibles
    categories_compressibles = [
        'Loisirs & Sorties', 'Achats & Shopping', 'Voyages / Vacances', 
        'Esthétique & Soins', 'Divers', 'Restaurants'
    ]
    
    # Calculer les dépenses compressibles
    depenses_compressibles = df_depenses[df_depenses['parent_name'].isin(categories_compressibles)]
    montant_compressible = depenses_compressibles['net_amount'].abs().sum() / nb_mois
    
    # Calculer la capacité d'emprunt améliorée si on réduit les dépenses compressibles de 30%
    economie_potentielle = montant_compressible * 0.3
    capacite_remboursement_amelioree = capacite_remboursement + economie_potentielle
    
    if taux_mensuel > 0:
        capacite_emprunt_amelioree = capacite_remboursement_amelioree / denominateur
    else:
        capacite_emprunt_amelioree = capacite_remboursement_amelioree * nb_mensualites
    
    # Préparer les recommandations
    recommandations = [
        f"Réduire les dépenses non essentielles de {economie_potentielle:.2f}€ par mois pour augmenter votre capacité d'emprunt",
        "Vérifier et optimiser vos contrats d'assurance et abonnements",
        "Consolider vos dettes existantes à taux élevés",
        "Épargner pour augmenter votre apport personnel"
    ]
    
    return {
        'revenu_mensuel': revenu_mensuel_moyen,
        'depenses_mensuelles': depenses_mensuelles_moyennes,
        'reste_a_vivre': reste_a_vivre,
        'taux_endettement_actuel': taux_endettement_actuel,
        'capacite_remboursement': capacite_remboursement,
        'capacite_emprunt': capacite_emprunt,
        'capacite_emprunt_amelioree': capacite_emprunt_amelioree,
        'apport_recommande': apport_recommande,
        'cout_total': cout_total,
        'taux_interet': taux_interet,
        'duree_pret': duree_pret,
        'nb_mois_analyse': nb_mois,
        'date_debut_analyse': date_min,
        'date_fin_analyse': date_max,
        'recommandations': recommandations
    }

def afficher_capacite_emprunt(resultats):
    """
    Affiche les résultats de l'analyse de capacité d'emprunt.
    
    Args:
        resultats (dict): Résultats de l'analyse de capacité d'emprunt
    """
    print("\n=== ANALYSE DE CAPACITÉ D'EMPRUNT IMMOBILIER ===\n")
    
    # Afficher la période d'analyse
    if resultats['date_debut_analyse'] and resultats['date_fin_analyse']:
        debut = resultats['date_debut_analyse'].strftime('%d/%m/%Y')
        fin = resultats['date_fin_analyse'].strftime('%d/%m/%Y')
        print(f"Période d'analyse: du {debut} au {fin} ({resultats['nb_mois_analyse']} mois)\n")
    
    # Afficher le résumé financier
    print("RÉSUMÉ FINANCIER MENSUEL:")
    print(f"  - Revenu moyen: {resultats['revenu_mensuel']:.2f}€")
    print(f"  - Dépenses moyennes: {resultats['depenses_mensuelles']:.2f}€")
    print(f"  - Reste à vivre: {resultats['reste_a_vivre']:.2f}€")
    print(f"  - Taux d'endettement actuel: {resultats['taux_endettement_actuel']*100:.1f}%\n")
    
    # Afficher la capacité d'emprunt
    print("CAPACITÉ D'EMPRUNT:")
    print(f"  - Capacité de remboursement mensuelle: {resultats['capacite_remboursement']:.2f}€")
    print(f"  - Montant empruntable: {resultats['capacite_emprunt']:.2f}€")
    print(f"  - Apport personnel recommandé (10%): {resultats['apport_recommande']:.2f}€")
    print(f"  - Budget immobilier total: {resultats['capacite_emprunt'] + resultats['apport_recommande']:.2f}€\n")
    
    # Afficher les détails du prêt
    print("DÉTAILS DU PRÊT SIMULÉ:")
    print(f"  - Taux d'intérêt annuel: {resultats['taux_interet']*100:.2f}%")
    print(f"  - Durée du prêt: {resultats['duree_pret']} ans")
    print(f"  - Mensualité estimée: {resultats['capacite_remboursement']:.2f}€")
    print(f"  - Coût total des intérêts: {resultats['cout_total']:.2f}€\n")
    
    # Afficher le potentiel d'amélioration
    amelioration = resultats['capacite_emprunt_amelioree'] - resultats['capacite_emprunt']
    print("POTENTIEL D'AMÉLIORATION:")
    print(f"  - Capacité d'emprunt améliorée: {resultats['capacite_emprunt_amelioree']:.2f}€")
    print(f"  - Gain potentiel: {amelioration:.2f}€ (+{amelioration/resultats['capacite_emprunt']*100:.1f}%)\n")
    
    # Afficher les recommandations
    print("RECOMMANDATIONS POUR OPTIMISER VOTRE CAPACITÉ D'EMPRUNT:")
    for i, recommandation in enumerate(resultats['recommandations'], 1):
        print(f"  {i}. {recommandation}")

def visualiser_capacite_emprunt(resultats):
    """
    Crée une visualisation graphique de la capacité d'emprunt.
    
    Args:
        resultats (dict): Résultats de l'analyse de capacité d'emprunt
    """
    # Créer la figure avec 2 sous-graphiques
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    
    # Graphique 1: Répartition des revenus et dépenses
    labels = ['Dépenses', 'Capacité de remboursement', 'Reste à vivre après prêt']
    
    # Calculer le reste à vivre après remboursement du prêt
    reste_apres_pret = resultats['revenu_mensuel'] - resultats['depenses_mensuelles'] - resultats['capacite_remboursement']
    
    # Si le reste après prêt est négatif, ajuster les valeurs pour le graphique
    if reste_apres_pret < 0:
        depenses_ajustees = resultats['depenses_mensuelles'] + reste_apres_pret
        reste_apres_pret = 0
        values = [depenses_ajustees, resultats['capacite_remboursement'], reste_apres_pret]
        title = "Répartition du revenu mensuel (budget serré)"
    else:
        values = [resultats['depenses_mensuelles'], resultats['capacite_remboursement'], reste_apres_pret]
        title = "Répartition du revenu mensuel"
    
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    
    ax1.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    ax1.set_title(title)
    
    # Graphique 2: Comparaison des capacités d'emprunt
    labels = ['Capacité actuelle', 'Capacité améliorée']
    values = [resultats['capacite_emprunt'], resultats['capacite_emprunt_amelioree']]
    
    x = range(len(labels))
    width = 0.5
    
    bars = ax2.bar(x, values, width, color=['#66b3ff', '#99ff99'])
    
    # Ajouter les valeurs sur les barres
    for bar in bars:
        height = bar.get_height()
        ax2.annotate(f'{height/1000:.0f}k€',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.set_title('Capacité d\'emprunt immobilier')
    ax2.set_ylabel('Montant empruntable (€)')
    
    # Ajouter une ligne horizontale pour le prix moyen d'un appartement (exemple)
    # ax2.axhline(y=250000, color='r', linestyle='-', label='Prix moyen appartement')
    # ax2.legend()
    
    plt.tight_layout()
    plt.savefig('capacite_emprunt.png')
    plt.show()
