import openai
import json
from fonctions import *

# Configuration de l'API OpenAI
client = openai.OpenAI(api_key="OPENAI_API_KEY")

def classifier_question(question):
    """
    Utilise ChatGPT pour classifier la question de l'utilisateur
    et déterminer quelle analyse financière effectuer.
    
    Args:
        question (str): Question posée par l'utilisateur
        
    Returns:
        str: Type d'analyse à effectuer
    """
    prompt = f"""
    Classifie la question suivante dans l'une des catégories d'analyse financière:
    
    Question: "{question}"
    
    Catégories possibles:
    1. prelevements_automatiques - Analyse des prélèvements automatiques vs achats ponctuels
    2. categories_depenses - Analyse des principales catégories de dépenses
    3. depenses_inhabituelles - Analyse des dépenses inhabituelles
    4. potentiel_economies - Analyse du potentiel d'économies mensuelles (objectif 200€)
    5. capacite_emprunt - Analyse de la capacité d'emprunt immobilier
    
    Réponds uniquement avec le nom de la catégorie.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un assistant financier qui aide à classifier les questions des utilisateurs."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=50
    )
    
    # Extraire la catégorie identifiée
    categorie = response.choices[0].message.content.strip().lower()
    
    # Normaliser la réponse
    if "prelevements" in categorie:
        return "prelevements_automatiques"
    elif "categories" in categorie or "dépenses" in categorie:
        return "categories_depenses"
    elif "inhabituelles" in categorie:
        return "depenses_inhabituelles"
    elif "economies" in categorie or "économies" in categorie:
        return "potentiel_economies"
    elif "emprunt" in categorie or "crédit" in categorie:
        return "capacite_emprunt"
    else:
        return "inconnu"

def generer_reponse(categorie, resultats):
    """
    Utilise ChatGPT pour générer une réponse en langage naturel
    basée sur les résultats de l'analyse.
    
    Args:
        categorie (str): Type d'analyse effectuée
        resultats (dict): Résultats de l'analyse
        
    Returns:
        str: Réponse en langage naturel
    """
    # Convertir les résultats en JSON pour les inclure dans le prompt
    resultats_json = json.dumps(resultats, default=str)
    
    prompt = f"""
    Tu es un conseiller financier expert. Voici les résultats d'une analyse financière de type "{categorie}".
    Génère une réponse claire, informative et personnalisée qui explique ces résultats à l'utilisateur.
    
    Résultats de l'analyse: {resultats_json}
    
    Quelques conseils pour ta réponse:
    - Commence par un résumé des points clés
    - Explique les chiffres importants de manière simple
    - Donne des conseils pratiques et personnalisés
    - Utilise un ton professionnel mais accessible
    - Limite ta réponse à 250 mots maximum
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un conseiller financier expert qui explique des analyses financières de façon claire et utile."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content

def assistant_financier(question, transactions):
    """
    Fonction principale qui gère l'interaction avec l'utilisateur.
    
    Args:
        question (str): Question posée par l'utilisateur
        transactions (DataFrame): Données de transactions
        
    Returns:
        str: Réponse à la question
    """
    try:
        # Classifier la question
        categorie = classifier_question(question)
        
        # Effectuer l'analyse appropriée
        if categorie == "prelevements_automatiques":
            resultats = analyser_part_prelevements(transactions)
            # Générer une visualisation
            visualiser_part_prelevements(resultats)
            
        elif categorie == "categories_depenses":
            resultats = analyser_categories_depenses(transactions)
            comparaison = comparer_avec_recommandations(resultats)
            # Fusionner les résultats pour la génération de réponse
            resultats_complets = {
                "categories": resultats,
                "comparaison": comparaison
            }
            # Générer une visualisation
            visualiser_categories_depenses(resultats, comparaison)
            return generer_reponse(categorie, resultats_complets)
            
        elif categorie == "depenses_inhabituelles":
            resultats = identifier_depenses_inhabituelles(transactions)
            # Générer une visualisation
            visualiser_depenses_inhabituelles(resultats)
            
        elif categorie == "potentiel_economies":
            montant_cible = 200  # Par défaut 200€
            resultats = analyser_potentiel_economies(transactions, montant_cible)
            # Générer une visualisation
            visualiser_potentiel_economies(resultats, montant_cible)
            
        elif categorie == "capacite_emprunt":
            resultats = analyser_capacite_emprunt(transactions)
            # Générer une visualisation
            visualiser_capacite_emprunt(resultats)
            
        else:
            return "Je ne comprends pas votre question. Pourriez-vous la reformuler en lien avec l'une de ces analyses : prélèvements automatiques, catégories de dépenses, dépenses inhabituelles, potentiel d'économies ou capacité d'emprunt."
        
        # Générer une réponse en langage naturel
        return generer_reponse(categorie, resultats)
    
    except Exception as e:
        return f"Désolé, une erreur s'est produite lors du traitement de votre demande: {str(e)}"