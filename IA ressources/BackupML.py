import json

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import HistGradientBoostingClassifier

import xgboost as xgb
import ast

def openJson(path):

    with open (path) as json_file:
        data = json.load(json_file)

    return data

def transformationHeroes(row, team_col, team):
    dfOut = pd.Series([False] * 146, index=[f'picks_team_{team}_{i}' for i in range(146)])
    for hero_id in row[team_col]:
        dfOut[f'picks_team_{team}_{hero_id}'] = True
    return dfOut

def saveDataFrameToJson(matches):
    """Methode pour suvgarder les details des matches pros"""

    fileName = f"TestDfML.json"
    path = fr"C:\Users\issam\Documents\ProjetAnnuelAI\DotaMatchsData\{fileName}"

    matches.to_json(path, index=False)

def main():
    matches = openJson(r"C:\Users\issam\Documents\ProjetAnnuelAI\DotaMatchsData\SauvgardeProMatchs2025-05-21.json")
    df = pd.DataFrame(matches)

    df_transformedRadiant = df.apply(lambda row: transformationHeroes(row, 'picks_id_team_0', 'radiant'), axis=1)

    df_transformedDire = df.apply(lambda row: transformationHeroes(row, 'picks_id_team_1', 'dire'), axis=1)
    dfTrain = pd.concat([df_transformedRadiant, df_transformedDire], axis=1)


    # Transformer la colonne en plusieurs colonnes
    #df_vectors_picks_team0 = df['picks_id_team_0'].apply(pd.Series)
    #df_vectors_picks_team0 = df_vectors_picks_team0.fillna(0).astype(int)
    #df_vectors_picks_team1 = df['picks_id_team_1'].apply(pd.Series)
    #df_vectors_picks_team1 = df_vectors_picks_team1.fillna(0).astype(int)
    #df_vectors_ban_team0 = df['bans_id_team_0'].apply(pd.Series)
    #df_vectors_ban_team0 = df_vectors_ban_team0.fillna(0).astype(int)
    #df_vectors_ban_team1 = df['bans_id_team_1'].apply(pd.Series)
    #df_vectors_ban_team1 = df_vectors_ban_team1.fillna(0).astype(int)

    #df = pd.concat([df_vectors_picks_team0, df], axis=1)
    #df = pd.concat([df_vectors_ban_team0, df], axis=1)
    #df = pd.concat([df_vectors_picks_team1, df], axis=1)
    #df = pd.concat([df_vectors_ban_team1, df], axis=1)
    #df = df.drop(columns=['picks_id_team_1'])
    #df = df.drop(columns=['picks_id_team_0'])
    #df = df.drop(columns=['bans_id_team_0'])
    #df = df.drop(columns=['bans_id_team_1'])


    saveDataFrameToJson(df)

    df.columns = df.columns.astype(str)
    X=dfTrain
    y=df['radiant_win']
    X_train , X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=42)
    model = xgb.XGBClassifier(
        n_estimators=300,  # Nombre d'arbres (plus = mieux, mais plus lent)
        max_depth=6,  # Profondeur max des arbres
        learning_rate=0.05,  # Apprentissage lent mais stable
        subsample=0.8,  # 80% des lignes utilisées à chaque arbre
        colsample_bytree=0.8,  # 80% des colonnes utilisées à chaque arbre
        scale_pos_weight=1,  # À ajuster si dataset déséquilibré
        eval_metric='logloss',
        random_state=42
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(len(df))
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

if __name__ == '__main__':
    main()

