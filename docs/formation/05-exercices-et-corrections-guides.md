# 05 - Exercices et corrections guidées

## Exercice 1

Question :

Pourquoi la météo n'est-elle pas fournie directement par le modèle ?

Correction guidée :

- Un LLM n'est pas une base de données temps réel.
- Pour des données à jour, il faut un tool/API externe.
- Ici, c'est wttr.in qui fournit la météo.

## Exercice 2

Question :

À quoi sert l'historique de conversation ?

Correction guidée :

- garder le contexte des tours précédents
- permettre des réponses plus cohérentes
- fournir au LLM les informations déjà produites

## Exercice 3

Question :

Quel est le risque principal si `DEBUG=true` en production ?

Correction guidée :

- logs trop verbeux et potentiellement sensibles
- bruit inutile pour l'utilisateur final
- bonne pratique : debug OFF en usage normal

## Exercice 4

Question :

Quelle stratégie simple permet d'ajouter une source météo de secours ?

Correction guidée :

1. Garder wttr.in en source principale.
2. Ajouter une seconde fonction d'appel API.
3. Sur exception/timeout, basculer automatiquement.
4. Afficher la source utilisée dans la réponse.
