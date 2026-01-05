# SpamShield AI 🛡️

**Détection Intelligente de Spam Email avec Machine Learning**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3%2B-orange)](https://scikit-learn.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-GUI%20Framework-green)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-brightgreen)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

Un système avancé de détection de spam email utilisant l'apprentissage automatique (Naive Bayes) avec une interface graphique moderne et un dashboard analytique interactif.

## ✨ Fonctionnalités

### 🤖 Machine Learning
- **Classification automatique** spam/ham avec modèle Naive Bayes
- **Modèle pré-entraîné** sur dataset standardisé
- **Calcul de confiance** pour chaque prédiction
- **Vectorisation TF-IDF** des contenus textuels
- **Métriques de performance** en temps réel

### 🎨 Interface Utilisateur
- **Dashboard interactif** avec visualisations avancées
- **Design moderne** avec thème clair/sombre
- **Navigation intuitive** entre onglets
- **Animations fluides** et transitions élégantes
- **Interface responsive** adaptée à différentes résolutions

### 📊 Analytics & Monitoring
- **Statistiques en temps réel** des prédictions
- **Graphiques évolutifs** avec Matplotlib
- **Métriques clés** (précision, taux de spam, volume)
- **Historique complet** des analyses
- **Export des données** au format CSV

### 💾 Gestion des Données
- **Base de données SQLite** intégrée
- **Persistance automatique** des prédictions
- **Sauvegarde et restauration** des données
- **Gestion d'historique** avec filtres
- **Système de backup** automatisé

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.11 ou supérieur
- Git

### Installation
```bash
# 1. Cloner le dépôt
git clone https://github.com/AchrafAllali/SpamDetector-ML.git
cd SpamDetector-ML

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python main.py
```

### Structure du Projet
```
SpamShield-AI/
├── main.py                    # Point d'entrée principal
├── requirements.txt           # Dépendances Python
├── README.md                  # Documentation
│
├── config/                    # Configuration
│   ├── settings.py           # Paramètres applicatifs
│   ├── styles.py             # Système de styles CSS-like
│   └── config_manager.py     # Gestionnaire de configuration
│
├── controllers/              # Contrôleurs MVC
│   ├── app_controller.py     # Contrôleur principal
│   └── __init__.py
│
├── database/                 # Gestion de données
│   ├── db_manager.py        # Gestionnaire SQLite
│   └── __init__.py
│
├── models/                   # Modèles ML
│   ├── spam_classifier.py   # Classificateur Naive Bayes
│   ├── vectorizer.py        # Vectorisation TF-IDF
│   └── __init__.py
│
├── services/                 # Services métier
│   ├── prediction_service.py # Service de prédiction
│   ├── statistics_service.py # Service de statistiques
│   └── __init__.py
│
├── views/                    # Interface utilisateur
│   ├── main_window.py       # Fenêtre principale
│   ├── dashboard_tab.py     # Onglet Dashboard
│   ├── analysis_tab.py      # Onglet Analyse
│   ├── history_tab.py       # Onglet Historique
│   ├── components/          # Composants UI réutilisables
│   └── templates/           # Templates d'interface
│
├── utils/                    # Utilitaires
│   ├── helpers.py           # Fonctions helper
│   ├── validators.py        # Validation de données
│   └── __init__.py
│
└── data/                    # Données et ressources
    └── spam_model.pkl      # Modèle ML pré-entraîné
```

## 🛠️ Technologies Utilisées

- **Python 3.11+** - Langage principal
- **Scikit-learn 1.3+** - Machine Learning
- **Tkinter** - Interface graphique native
- **SQLite3** - Base de données embarquée
- **Matplotlib 3.7+** - Visualisation de données
- **NumPy & Pandas** - Traitement de données
- **CustomTKinter** - Composants UI modernes

## 📸 Captures d'Écran

### Dashboard Principal
![Dashboard](screenshots/dashboard.png)
*Interface moderne avec métriques en temps réel et visualisations*

### Analyse en Temps Réel
![Analysis](screenshots/analysis.png)
*Système d'analyse interactif avec classification automatique*

### Historique des Prédictions
![History](screenshots/history.png)
*Gestion complète de l'historique avec filtres et export*

## 🎯 Utilisation

### 1. Analyse d'Email
1. Ouvrez l'application
2. Naviguez vers l'onglet "Analyse"
3. Collez le contenu de l'email dans la zone de texte
4. Cliquez sur "Analyser"
5. Consultez les résultats et le niveau de confiance

### 2. Surveillance du Dashboard
- **Métriques en temps réel** : Suivez les performances du modèle
- **Graphiques évolutifs** : Visualisez les tendances
- **Alertes automatiques** : Soyez notifié des anomalies

### 3. Gestion des Données
- **Export CSV** : Exportez l'historique pour analyse externe
- **Filtres avancés** : Trouvez rapidement les données pertinentes
- **Statistiques détaillées** : Analysez les performances sur différentes périodes

## 📊 Performance du Modèle

| Métrique | Valeur | Description |
|----------|--------|-------------|
| **Précision** | 98.2% | Taux de classification correcte |
| **Rappel Spam** | 96.8% | Capacité à détecter les vrais spams |
| **F1-Score** | 97.5% | Moyenne harmonique précision/rappel |
| **Temps d'inférence** | < 100ms | Temps de prédiction par email |

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment participer :

1. **Fork** le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez sur la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une **Pull Request**

### Guide de Contribution
- Suivez les conventions PEP 8 pour le code Python
- Ajoutez des tests pour les nouvelles fonctionnalités
- Mettez à jour la documentation si nécessaire
- Assurez-vous que le code passe les vérifications existantes

## 📄 Licence

Ce projet est distribué sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

```
MIT License

Copyright (c) 2024 Achraf Allali

Permission is hereby granted...
```

## 👥 Auteurs

- **Achraf Allali** - *Développeur Principal* - [GitHub](https://github.com/AchrafAllali)

## 🙏 Remerciements

- **Scikit-learn Team** pour l'excellente bibliothèque ML
- **Python Software Foundation** pour le langage Python
- **Communauté Tkinter** pour les ressources et tutoriels
- **Contributeurs open-source** pour les datasets de spam

## 📞 Support

Pour rapporter un bug ou suggérer une amélioration :
1. Vérifiez les [issues existantes](https://github.com/AchrafAllali/SpamDetectorML-D-tecteur-de-spam-avec-apprentissage-automatique/issues)
2. Créez une nouvelle issue avec un titre descriptif
3. Fournissez des étapes pour reproduire le problème

## 🌟 Étoiles et Support

Si ce projet vous est utile, pensez à :
- ⭐ **Mettre une étoile** sur GitHub
- 🔄 **Partager** avec vos collègues
- 💬 **Contribuer** aux discussions
- 🐛 **Rapporter** les bugs rencontrés

---

**SpamShield AI** - Votre bouclier intelligent contre les spams emails 🔒

*Développé avec ❤️ en utilisant Python et Machine Learning*
