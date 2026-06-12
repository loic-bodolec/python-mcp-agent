# 01 - Fondamentaux MCP et IA

## Objectif de cette page

Cette page sert à comprendre trois idées de base avant de lire le reste du projet :

- ce qu'est un agent IA
- à quoi sert MCP
- qui fait quoi entre le modèle, les tools et le code Python

## 1) Les rôles dans un agent

Un agent moderne combine au moins 3 éléments :

- un modèle de langage (LLM) : comprend une consigne et produit du texte
- des tools : exécutent des actions concrètes sur le monde extérieur
- un orchestrateur : décide quand appeler un tool et comment réutiliser le résultat

Dans ce projet :

- LLM = Groq
- Tool météo = wttr.in
- Tool heure = pytz
- Orchestrateur = logique dans `client.py`, qui dialogue avec `server.py` via MCP

Point important : le modèle ne remplace pas les tools. Il raisonne sur le texte et formule la réponse finale, mais il a besoin d'une source externe pour obtenir une météo à jour ou une heure locale précise.

## 2) MCP en une phrase

MCP (Model Context Protocol) est une manière standard de connecter une application IA à des tools, à des données et à des services externes.

Ressource utile : [What is the Model Context Protocol (MCP)? - Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)

Résumé du site :

- MCP est un standard open source qui connecte une application IA à des systèmes externes
- il permet de brancher des sources de données, des outils et des workflows de façon standardisée
- l'idée est comparable à un port USB-C pour l'IA : une seule interface pour se connecter à des services variés
- MCP simplifie l'intégration pour les développeurs et rend les agents plus capables pour les utilisateurs
- l'écosystème est large : des assistants comme Claude ou ChatGPT et des outils comme VS Code peuvent s'y connecter

Concrètement, un serveur MCP :

- déclare la liste des tools disponibles
- décrit les entrées attendues pour chaque tool
- reçoit les appels venant d'un client MCP
- exécute le tool demandé
- renvoie le résultat au client

Dans ce dépôt, `server.py` n'est plus seulement une démo : il fait partie du flux principal et expose les tools utilisés par `client.py`.

## 3) Comment cela se traduit dans ce projet

Le flux le plus simple est le suivant :

1. l'utilisateur pose une question
2. `client.py` détecte si un tool est nécessaire
3. si besoin, `client.py` appelle `server.py` via MCP
4. `server.py` exécute le tool concerné
5. le résultat est ajouté au contexte
6. Groq produit une réponse naturelle à afficher

Exemple météo :

- question utilisateur : "Quelle est la météo à Nantes ?"
- `client.py` détecte une intention météo
- `client.py` appelle `server.py` via MCP
- `server.py` interroge wttr.in
- le résultat brut est renvoyé au modèle
- Groq reformule la réponse en langage naturel

Exemple heure :

- question utilisateur : "Quelle heure est-il à Tokyo ?"
- `client.py` détecte une intention heure
- `client.py` appelle `server.py` via MCP
- `server.py` utilise `pytz` avec `Asia/Tokyo`
- le résultat est intégré dans la réponse finale

## 4) Ce que le LLM fait et ne fait pas

Le LLM fait bien :

- comprendre la demande utilisateur
- reformuler une information technique en réponse naturelle
- tenir compte de l'historique de conversation

Le LLM ne fait pas directement :

- appeler une API sans qu'on lui fournisse un mécanisme d'appel
- garantir qu'une donnée externe est à jour sans source fiable
- exécuter du code Python local par lui-même

Règle pratique : quand une réponse dépend du monde réel ou d'un système externe, il faut en général un tool.

## 5) Point de clarté important

Il est utile de bien séparer les responsabilités :

- wttr.in fournit les données météo
- pytz calcule l'heure locale à partir d'un fuseau
- Groq transforme ces informations en réponse lisible
- `client.py` décide quand utiliser chaque composant et passe par MCP pour invoquer les tools

Autrement dit, l'intelligence conversationnelle et l'accès aux données sont deux choses différentes mais complémentaires.

## 6) Pourquoi MCP est utile

Sans MCP, chaque application doit inventer sa propre façon d'exposer ses tools.

Avec MCP :

- les tools sont plus faciles à brancher dans plusieurs clients
- l'architecture est plus claire entre client et serveur
- on peut réutiliser les mêmes tools dans d'autres agents plus tard

Dans ce projet, le mode principal passe maintenant par `client.py` puis `server.py`, ce qui rend l'architecture à la fois modulaire et directement interopérable.

## 7) Lexique rapide

- intent detection : détection de l'intention utilisateur
- tool call : appel d'une fonction externe
- orchestration : logique qui choisit quoi faire et dans quel ordre
- fallback : solution de secours quand le cas attendu échoue
- prompt : message envoyé au modèle
- context window : historique pris en compte par le modèle
