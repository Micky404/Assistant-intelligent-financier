from fonctions import *
from assistant import assistant_financier, classifier_question

def main():
    # Charger les données
    transactions = charger_donnees('transactions.csv')
    
    if transactions is not None:
        print("\n--- ASSISTANT FINANCIER INTELLIGENT ---\n")
        print("Bonjour ! Je suis votre assistant financier personnel.")
        print("Vous pouvez me poser des questions sur vos finances, par exemple :")
        print("1. Quelle est la part de mes prélèvements automatiques par rapport à mes achats ponctuels ?")
        print("2. Quelles sont mes principales catégories de dépenses ?")
        print("3. Ai-je des dépenses inhabituelles récemment ?")
        print("4. Comment puis-je économiser 200€ par mois ?")
        print("5. J'envisage de prendre un crédit immobilier. Quelle serait ma capacité d'emprunt ?")
        
        while True:
            print("\n" + "-"*50)
            question = input("\nVotre question (ou 'quitter' pour sortir) : ")
            
            if question.lower() in ['quitter', 'exit', 'q', 'quit']:
                print("Merci d'avoir utilisé l'assistant financier. À bientôt !")
                break
            
            # Classifier la question
            categorie = classifier_question(question)
            
            # Effectuer l'analyse appropriée
            if categorie == "prelevements_automatiques":
                resultats = analyser_part_prelevements(transactions)
                visualiser_part_prelevements(resultats)
                
            elif categorie == "categories_depenses":
                resultats = analyser_categories_depenses(transactions)
                comparaison = comparer_avec_recommandations(resultats)
                resultats_complets = {"categories": resultats, "comparaison": comparaison}
                visualiser_categories_depenses(resultats, comparaison)
                
            elif categorie == "depenses_inhabituelles":
                resultats = identifier_depenses_inhabituelles(transactions)
                visualiser_depenses_inhabituelles(resultats)
                
            elif categorie == "potentiel_economies":
                montant_cible = 200
                resultats = analyser_potentiel_economies(transactions, montant_cible)
                visualiser_potentiel_economies(resultats, montant_cible)
                
            elif categorie == "capacite_emprunt":
                resultats = analyser_capacite_emprunt(transactions)
                visualiser_capacite_emprunt(resultats)
                
            else:
                print("\nJe ne comprends pas votre question. Pourriez-vous la reformuler ? Pour rappel, je peux vous guider sur les prélèvements automatiques, les catégories de dépenses, les dépenses inhabituelles, les économies potentielles et la capacité d'emprunt.")
                continue
            
            # Générer une réponse en langage naturel avec l'assistant
            from assistant import generer_reponse
            reponse = generer_reponse(categorie, resultats if categorie != "categories_depenses" else resultats_complets)
            
            print("\nRÉPONSE DE L'ASSISTANT :")
            print(reponse)
            
            # Demander si l'utilisateur souhaite voir les détails
            voir_details = input("\nSouhaitez-vous voir les détails de l'analyse ? (oui/non) : ")
            if voir_details.lower() in ['oui', 'o', 'yes', 'y']:
                if categorie == "prelevements_automatiques":
                    afficher_part_prelevements(resultats)
                    
                elif categorie == "categories_depenses":
                    afficher_categories_depenses(resultats, comparaison)
                    
                elif categorie == "depenses_inhabituelles":
                    afficher_depenses_inhabituelles(resultats)
                    
                elif categorie == "potentiel_economies":
                    afficher_potentiel_economies(resultats, montant_cible)
                    
                elif categorie == "capacite_emprunt":
                    afficher_capacite_emprunt(resultats)
    else:
        print("Impossible de procéder à l'analyse: données non disponibles.")

if __name__ == "__main__":
    main()