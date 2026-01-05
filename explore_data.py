import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger le dataset
df = pd.read_csv('data/spam.csv', encoding='latin-1')

# Afficher les premières lignes
print("=== Aperçu du dataset ===")
print(df.head())

# Informations générales
print("\n=== Informations ===")
print(df.info())

# Vérifier les valeurs manquantes
print("\n=== Valeurs manquantes ===")
print(df.isnull().sum())

# Renommer les colonnes (si nécessaire)
df = df[['v1', 'v2']]  # Garder seulement les 2 colonnes utiles
df.columns = ['label', 'message']

# Distribution des classes
print("\n=== Distribution des classes ===")
print(df['label'].value_counts())

# Visualisation
plt.figure(figsize=(8, 5))
sns.countplot(x='label', data=df)
plt.title('Distribution Spam vs Ham')
plt.xlabel('Classe')
plt.ylabel('Nombre de messages')
plt.show()

# Exemples de messages
print("\n=== Exemple de SPAM ===")
print(df[df['label'] == 'spam']['message'].head(2))

print("\n=== Exemple de HAM (non-spam) ===")
print(df[df['label'] == 'ham']['message'].head(2))