## Software: Google Colab.

## Bibliotecas utilizadas: 
- Pandas e NumPy: Para manipulação e análise de dados.
- Scikit-learn: Aprendizado de máquina, como divisão de dados, padronização, redução de dimensionalidade (PCA), e avaliação de modelos.
- LightGBM, CatBoost, XGBoost e RandomForest: Para criar modelos de classificação.
- Imbalanced-learn (ADASYN): Para balancear as classes do conjunto de dados.
- Matplotlib e Seaborn: Para visualização de dados e gráficos.
- Joblib: Para salvar e carregar modelos treinados.

## Passos da resolução da Prova:
1. Carregar os dados: primeiro carreguei os dados da planilha de treinamento. Em seguida, renomeei as colunas para facilitar a visualização e removi a coluna `id`, que não era relevante para o modelo. Além de utilizar .info(), .head() e .describe() do Pandas, matplotlib e seaborn para visualizar os dados. Por fim separei os dados de treino em partes e testei cada uma individualmente. Depois criei um script simples onde testei os seguintes modelos de Machine Learning: LogisticRegression, Árvore De Decisão, Random Forest, XBClassifier, LGBM, GradientBoosting, SVC, KNeighbors e MLP, onde Random Forest, XB e LGBM tiveram o melhor resultado (0.75). A partir disso, comecei uma ánalise dos dados, para ver a importância de cada variável no resultado do target. E comecei excluindo colunas uma a uma e observando os resultados. Resolvi criar novas colunas, com base em seus nomes e influência deles na classificação do planeta. Ex: Temperatura tem relação com a Pressão Atmosférica.
2. Tratamento dos dados: Criei novas colunas combinando algumas colunas existentes para obter melhores resultados. Separei os dados em variáveis X e y, sendo o y o target.
3. Balanceamento das classes: Testei o SMOTE e o ADASYN. Com o ADASYN obtive melhores resultados.
4. Padronização e redução de dimensionalidade: Testei MinMaxScaler, StandardScaler, e com o StandardScaler tive melhor resultado.
5. Divisão dos dados: Dividi os dados em conjuntos de treino (80%) e teste (20%), e testei também outros valores (50-50), (70-30), onde não tive bons resultados. E também testei a validação cruzada (StratifiedKfold), que não alterou os resultados.
6. Treinamento dos modelos: Testei cada modelo separadamente (DecisionTree, RandomForest, etc) e comparei os resultados, que davam em média 0.56. Então optei por usar quatro modelos diferentes no mesmo código, modificando os hiperparâmetros a cada teste. Optei por utilizar o RandomizedSearchCV, que busca valores aleatórios ao invés do GridSearchCV, que testa todos.
7. Avaliação do modelo: Avaliei o modelo final usando métricas como acurácia, AUC-ROC e F1-Score. Também plotei a matriz de confusão para visualizar o desempenho do modelo em cada classe.
8. Salvar o modelo treinado: Salvei o modelo treinado, o scaler e o PCA usando a biblioteca `joblib`, para que pudessem ser reutilizados posteriormente.
9. Teste do modelo em novos dados: Carreguei um novo conjunto de dados (`teste.csv`), apliquei as mesmas transformações e usei o modelo treinado para fazer previsões. As previsões foram salvas em um arquivo CSV (`previsoes.csv`).

## Explicação da escolha do algoritmo de Aprendizado de Máquina: 

Depois de muita pesquisa e testes, combinando valores, vendo vídeos e tutoriais, escolhi usar Voting Classifier combinando três algoritmos diferentes (LightGBM, CatBoost e XGBoost). Todos são baseados em árvores de decisão, mas cada um tem suas próprias vantagens. Ao combinar esses modelos, o Voting Classifier aproveita as forças de cada um, resultando em um modelo mais preciso e com menos variações nos resultados.

Além disso, usei técnicas como PCA para reduzir a complexidade dos dados e ADASYN para lidar com o desbalanceamento das classes. Essas etapas foram essenciais para garantir que o modelo fosse capaz de generalizar bem e não puxado apenas para uma classe.
Resumindo, foi o melhor resultado que obtive com esses parâmetros. Também observei que alguns modelos levavam muito tempo para carregar os resultados, e optei pelo modelo que tinha um equilibrio da performance e precisão.

## Referências: 
https://www.youtube.com/watch?v=bgvjq-JPzZY (Eduardo | Ciência dos Dados), 

https://www.youtube.com/watch?v=39HBlzFV9vk (Programação Dinâmica), 

https://www.youtube.com/watch?v=SW0YGA9d8y8 (Code with Josh).
