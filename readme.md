## Software / Bibliotecas Utilizado:
Utilizei o Google Colab para desenvolver o código e minhas referências foram **Coding with Josh** e **FreeCodeCamp no Youtube**, além dos famosos **Chatgpt** e **DeepSeek** para apoio. 
As principais bibliotecas que utilizei foram:

- **Pandas** e **NumPy**: Para manipulação e análise de dados.
- **Scikit-learn**: Para tarefas de aprendizado de máquina, como divisão de dados, padronização, redução de dimensionalidade (PCA), e avaliação de modelos.
- **LightGBM**, **CatBoost**, **XGBoost** e **RandomForest**: Para criar modelos de classificação.
- **Imbalanced-learn (ADASYN)**: Para balancear as classes do conjunto de dados.
- **Matplotlib** e **Seaborn**: Para visualização de dados e gráficos.
- **Joblib**: Para salvar e carregar modelos treinados.

## Passos da Resolução da Prova:

1. **Carregar os dados de treinamento**:
   - Utilizei a função `pd.read_csv()` para carregar o arquivo `treino.csv`, que contém os dados de treinamento. Em seguida, renomeei as colunas para facilitar a visualização e removi a coluna `id`, que não era relevante para o modelo. Além de utilizar .info(), .head() e .describe() do Pandas e matplotlibe seaborn para visualizar os dados. Por fim separei os dados de treino em 10 partes e testei cada uma individualmente.

2. **Tratamento dos dados**:
   - Criei novas features combinando algumas colunas existentes, como `TempPressão` (multiplicação de temperatura e pressão) e `GravidadeRadiação` (multiplicação de gravidade e radiação). Isso ajuda o modelo a capturar relações mais complexas entre as variáveis.
   - Tratei outliers usando o método Z-Score, que remove valores que estão muito distantes da média.
   - Separei os dados em variáveis independentes (`X`) e a variável dependente (`y`), que é o `target`.

3. **Balanceamento das classes**:
   - Como o conjunto de dados estava desbalanceado, usei a técnica **ADASYN** para gerar amostras sintéticas das classes minoritárias, garantindo que o modelo não fosse tendencioso.

4. **Padronização e redução de dimensionalidade**:
   - Padronizei os dados usando `StandardScaler`, que transforma os dados para ter média zero e desvio padrão um. Isso é importante para modelos que dependem de distâncias, como PCA.
   - Apliquei **PCA** (Análise de Componentes Principais) para reduzir a dimensionalidade dos dados, mantendo 95% da variância original. Isso ajuda a reduzir o tempo de treinamento e a evitar overfitting.

5. **Divisão dos dados em treino e teste**:
   - Dividi os dados em conjuntos de treino (80%) e teste (20%), garantindo que a proporção das classes fosse mantida em ambos os conjuntos.

6. **Treinamento dos modelos**:
   - Testei quatro modelos diferentes: **XGBoost**, **LightGBM**, **CatBoost** e **RandomForest**. Para cada um, usei **RandomizedSearchCV** para ajustar os hiperparâmetros e encontrar a melhor configuração.
   - Após o ajuste, criei um **Voting Classifier**, que combina as previsões dos três melhores modelos (LightGBM, CatBoost e XGBoost) usando uma média ponderada das probabilidades.

7. **Avaliação do modelo**:
   - Avaliei o modelo final usando métricas como acurácia, AUC-ROC e F1-Score. Também plotei a matriz de confusão para visualizar o desempenho do modelo em cada classe.

8. **Salvar o modelo treinado**:
   - Salvei o modelo treinado, o scaler e o PCA usando a biblioteca `joblib`, para que pudessem ser reutilizados posteriormente.

9. **Teste do modelo em novos dados**:
   - Carreguei um novo conjunto de dados (`teste.csv`), apliquei as mesmas transformações (criação de features, padronização e PCA) e usei o modelo treinado para fazer previsões. As previsões foram salvas em um arquivo CSV (`previsoes.csv`).

### Explicação da Escolha do Algoritmo de Aprendizado de Máquina:

Escolhi usar um **Voting Classifier** que combina três algoritmos diferentes: **LightGBM**, **CatBoost** e **XGBoost**. Esses algoritmos são baseados em árvores de decisão, mas cada um tem suas próprias vantagens. O **LightGBM** é rápido e eficiente em grandes conjuntos de dados, o **CatBoost** lida bem com dados categóricos e o **XGBoost** é conhecido por sua alta precisão. Ao combinar esses modelos, o **Voting Classifier** aproveita as forças de cada um, resultando em um modelo mais robusto e preciso.

Além disso, usei técnicas como **PCA** para reduzir a complexidade dos dados e **ADASYN** para lidar com o desbalanceamento das classes. Essas etapas foram essenciais para garantir que o modelo fosse capaz de generalizar bem e não enviesado para uma classe específica.

No final, o modelo foi capaz de prever com boa precisão a classificação dos planetas, como mostrado pelas métricas de avaliação e pela matriz de confusão.

## Tropeços no caminho
Como nem tudo são flores comecei com um modelo básico sem nenhum tratamento dos dados utilizando árvore de decisões, mas os resultados esperados foram péssimos em torno de 0.70 e com risco de overfitting. Testei vários modelos como GridSearchCV, SMOTE e vários outros. A variação nos resultados são impressionantes chegando a 0.92 em alguns casos e outros 0.65... isso devido as particularidades de cada modelo e mudanças nos hiperparâmetros.
No final não sabia da autenticidade dos resultados. Alguns modelos geravam resultados rápidos variando de 2 minutos até 30 minutos.

## Solução temporária
Após treinar mais de 30 modelos variando entre as escolhas resolvi dividir minha base de dados em 10 partes iguais,craindo um pequeno script em python para me ajudar nesta tarefa.
Testei cada arquivo individualmente e depois comparei os resultados e percebi que havia poucas variações entre eles.

## Resultado final
Resolvi testar com uma biblioteca externa e outro modelo ao invés do SMOTE e foi onde obtive os melhores resultados(0.92). Obtive resultados melhores com GridSearch mas demorava muito para treinar o modelo e corria um sério risco de decorar os dados além de ser muito custoso computacionalmente. Preferi utilizar um modelo equilibrado entre tempo e analise. A parte que mais demorou para carregar no código era no .fit()(treinamento).
