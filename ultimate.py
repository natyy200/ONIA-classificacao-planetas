# instalar catboost (Colab-google)
# biblioteca externa
!pip install catboost

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, StratifiedKFold, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from imblearn.over_sampling import ADASYN
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier

# Carregar os dados
dados = pd.read_csv("treino.csv")
dados = dados.drop(columns=["id"])  # Removendo ID para treinamento

dados.columns = [
    "TempMédia", "Gravidade", "PressãoAtm", "Radiação", "ComposiçãoAr", "Hidratação",
    "Vegetação", "Fauna", "SoloFértil", "Ventos", "Luas", "Magnetismo", "ClimaEstável", "target"
]

# Criar novas features
def criar_features(df):
    df["TempPressão"] = df["TempMédia"] * df["PressãoAtm"]
    df["GravidadeRadiação"] = df["Gravidade"] * df["Radiação"]
    df["MédiaSoloVegetação"] = (df["SoloFértil"] + df["Vegetação"]) / 2
    df["InteraçãoFaunaClima"] = df["Fauna"] * df["ClimaEstável"]
    df["InteraçãoMagnetismoGravidade"] = df["Magnetismo"] * df["Gravidade"]

    # Clusterização para capturar padrões ocultos
    kmeans = KMeans(n_clusters=5, random_state=42)
    df['Cluster'] = kmeans.fit_predict(df.drop(columns=["target"]))

    return df

dados = criar_features(dados)

# Tratamento de outliers
from scipy.stats import zscore
z_scores = np.abs(zscore(dados.drop(columns=["target"])))
dados = dados[(z_scores < 3).all(axis=1)]

# Balanceamento de classes
X = dados.drop(columns=['target'])
y = dados['target']
adasyn = ADASYN(random_state=42)
X_res, y_res = adasyn.fit_resample(X, y)

# Padronização
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_res)

# Redução de dimensionalidade
pca = PCA(n_components=0.95)
X_pca = pca.fit_transform(X_scaled)

# Cross-validation estratificada
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Modelos e hiperparâmetros
models = {
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42),
    "LightGBM": LGBMClassifier(random_state=42),
    "CatBoost": CatBoostClassifier(verbose=0, random_state=42)
}

tuned_params = {
    "XGBoost": {'n_estimators': [200], 'max_depth': [10], 'learning_rate': [0.2]},
    "LightGBM": {'n_estimators': [200], 'max_depth': [10], 'learning_rate': [0.1]},
    "CatBoost": {'iterations': [200], 'depth': [10], 'learning_rate': [0.1]}
}

best_models = {}
for name, model in models.items():
    search = RandomizedSearchCV(model, tuned_params[name], n_iter=4, cv=cv, scoring='f1_weighted', random_state=42, n_jobs=-1)
    search.fit(X_pca, y_res)
    best_models[name] = search.best_estimator_
    print(f"{name} - Melhor configuração: {search.best_params_}")

# Criar Voting Classifier
eclf = VotingClassifier(
    estimators=[
        ("LightGBM", best_models["LightGBM"]),
        ("CatBoost", best_models["CatBoost"]),
        ("XGBoost", best_models["XGBoost"])
    ],
    voting="soft",
    weights=[2, 3, 1]  # Ajuste do peso do CatBoost
)

eclf.fit(X_pca, y_res)

# Salvar o modelo treinado
joblib.dump(eclf, "modelo_voting.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(pca, "pca.pkl")

print("\nModelo salvo com sucesso!")

# Avaliação do modelo
y_pred = eclf.predict(X_pca)
y_pred_proba = eclf.predict_proba(X_pca)

print("\nVoting Classifier:")
print("Acurácia:", accuracy_score(y_res, y_pred))
print("AUC-ROC:", roc_auc_score(y_res, y_pred_proba, multi_class='ovr'))
print("F1-Score:", f1_score(y_res, y_pred, average='weighted'))
print(classification_report(y_res, y_pred))
cm = confusion_matrix(y_res, y_pred)
ConfusionMatrixDisplay(cm).plot()
plt.title("Matriz de Confusão - Voting Classifier")
plt.show()

"""Script com a saída dos resultados em csv"""

# Carregar modelo, scaler e PCA
eclf = joblib.load("modelo_voting.pkl")
scaler = joblib.load("scaler.pkl")
pca = joblib.load("pca.pkl")

# Carregar a base de teste
teste = pd.read_csv("teste.csv")

# Salvar o ID para o arquivo final
ids = teste["id"]

# Remover a coluna ID para predição
teste = teste.drop(columns=["id"])

teste.columns = [
    "TempMédia", "Gravidade", "PressãoAtm", "Radiação", "ComposiçãoAr", "Hidratação",
    "Vegetação", "Fauna", "SoloFértil", "Ventos", "Luas", "Magnetismo", "ClimaEstável"
]

# Aplicar as mesmas features engineering usadas no treino
def criar_features(df):
    df["TempPressão"] = df["TempMédia"] * df["PressãoAtm"]
    df["GravidadeRadiação"] = df["Gravidade"] * df["Radiação"]
    df["MédiaSoloVegetação"] = (df["SoloFértil"] + df["Vegetação"]) / 2
    df["InteraçãoFaunaClima"] = df["Fauna"] * df["ClimaEstável"]
    df["InteraçãoMagnetismoGravidade"] = df["Magnetismo"] * df["Gravidade"]

    # Cluster foi gerado no treino, precisamos recriá-lo aqui:
    df["Cluster"] = (df["Gravidade"] * df["Radiação"] + df["Fauna"] * df["SoloFértil"]).round(1)

    return df


teste = criar_features(teste)

# Padronizar os dados
X_scaled = scaler.transform(teste)

# Aplicar a redução de dimensionalidade com PCA
X_pca = pca.transform(X_scaled)

# Realizar a predição
y_pred = eclf.predict(X_pca)

# Criar o DataFrame final
resultado = pd.DataFrame({
    "id": ids,
    "target": y_pred
})

# Salvar o arquivo CSV
resultado.to_csv("previsoes.csv", index=False)

print("Arquivo de predição salvo com sucesso: previsoes.csv")
