# 04 - Ateliers pratiques

## Atelier 1 : activer/désactiver le debug

Objectif :

- comprendre ce qui est journalisé en mode diagnostic

Étapes :

1. Mettre `DEBUG=true` dans `.env`.
2. Lancer `python client.py`.
3. Poser une question météo.
4. Observer les logs `[DEBUG ...]`.
5. Repasser `DEBUG=false`.

Résultat attendu :

- mode ON : logs visibles
- mode OFF : sortie utilisateur propre

## Atelier 2 : enrichir la détection d'intention

Objectif :

- gérer plus de variantes linguistiques

Étapes :

1. Ouvrir `should_use_tool` dans `client.py`.
2. Ajouter de nouveaux mots-clés météo.
3. Tester 5 formulations différentes.

Idées de tests :

- "faire un point météo"
- "température à Lille"
- "il pleut à Paris ?"

## Atelier 3 : ajouter un 3e tool

Objectif :

- ajouter une nouvelle capacité à l'agent

Suggestion :

- `get_day_of_week(city_or_timezone)`

Étapes :

1. Créer la fonction tool.
2. Intégrer `process_tool_call`.
3. Étendre `should_use_tool`.
4. Ajouter un test manuel.

## Atelier 4 : robustesse réseau

Objectif :

- mieux gérer les erreurs API

Étapes :

1. Simuler une erreur réseau.
2. Vérifier le message utilisateur.
3. Ajouter un timeout explicite si besoin.
4. Vérifier que l'application ne plante pas.
