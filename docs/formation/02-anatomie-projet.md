# 02 - Anatomie du projet

## Vue globale

Fichiers principaux :

- `client.py` : agent CLI et logique de décision
- `server.py` : exposition MCP des tools utilisés par le client
- `mcp_client.py` : connexion MCP locale entre le client et le serveur
- `intent_router.py` : détection d'intention météo/heure
- `tool_services.py` : logique métier partagée des tools
- `settings.py` : configuration commune via `.env`
- `requirements.txt` : dépendances Python
- `.env` : configuration locale (clé API, DEBUG)

## `client.py` : ce qui se passe

Blocs principaux :

1. chargement de la configuration (`.env`)
2. connexion à `server.py` via `mcp_client.py`
3. détection d'intention via `intent_router.py`
4. appel des tools via MCP si nécessaire
5. boucle de conversation (`main`)

## `server.py` : pourquoi ce fichier existe

Ce fichier porte la surface MCP du projet.

Il est utile pour :

- brancher ces tools dans `client.py`
- brancher ces mêmes tools dans un autre agent
- séparer la logique tool de la logique chat
- apprendre la structure standard d'un serveur MCP

Quand on le lance directement :

- quand un client MCP externe doit utiliser ces tools
- quand on teste l'intégration MCP de bout en bout

Pourquoi il n'est plus optionnel ici :

- le mode principal du projet passe maintenant par MCP
- `client.py` démarre une session MCP locale vers `server.py`
- la logique métier des tools est centralisée côté serveur

## `requirements.txt` : dépendances utiles

- `groq` : client API LLM
- `python-dotenv` : lecture de `.env`
- `requests` : appels HTTP
- `pytz` : gestion des fuseaux horaires
- `mcp` : primitives serveur MCP

## `.env` : bonnes pratiques

Variables typiques :

- `GROQ_API_KEY`
- `DEBUG`

Règle d'or :

- ne jamais commiter `.env`
- partager un `.env.template` si nécessaire
