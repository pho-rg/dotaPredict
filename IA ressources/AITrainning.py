import json
import statistics

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import HistGradientBoostingClassifier

import xgboost as xgb

def openJson(path):
    with open (path) as json_file:
        data = json.load(json_file)
    return data

def transformationHeroes(row, team_col, team):
    dfOut = pd.Series([False] * 146, index=[f'picks_team_{team}_{i}' for i in range(146)])
    for hero_id in row[team_col]:
        dfOut[f'picks_team_{team}_{hero_id}'] = True
    return dfOut

def creerDataframe(datas):
    dfOut = pd.DataFrame()
    for i in range(2) :
        dfOut[f'picks_team_{i}'] = [datas[i]]
    return dfOut

def saveDataFrameToJson(matches):
    """Methode pour suvgarder les details des matches pros"""

    fileName = f"TestDfML.json"
    path = fr"C:\Users\issam\Documents\ProjetAnnuelAI\DotaMatchsData\{fileName}"

    matches.to_json(path, index=False)

def main():

    match1=[[38,103,27,94,55],[10,64,131,19,129]]
    dfTestMatch = creerDataframe(match1)

    df_testM_match_dire = dfTestMatch.apply(lambda row: transformationHeroes(row, 'picks_team_1', 'dire'), axis=1)
    df_testM_match_radiant = dfTestMatch.apply(lambda row: transformationHeroes(row, 'picks_team_0', 'radiant'), axis=1)
    dfTestMatch = pd.concat([df_testM_match_radiant, df_testM_match_dire], axis=1)


    matches = openJson(r"C:\Users\issam\Documents\ProjetAnnuelAI\DotaMatchsData\SauvgardeProMatchs2025-05-21.json")
    df = pd.DataFrame(matches)

    df_transformedDire = df.apply(lambda row: transformationHeroes(row, 'picks_id_team_1', 'dire'), axis=1)
    df_transformedRadiant = df.apply(lambda row: transformationHeroes(row, 'picks_id_team_0', 'radiant'), axis=1)
    dfTest = pd.concat([df_transformedRadiant, df_transformedDire], axis=1)

    print('debut Apprentissage')

    X=dfTest
    y=df['radiant_win']
    X_train , X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=42)
    model = xgb.XGBClassifier(
        random_state=42,
        learning_rate=0.05,
        n_estimators=500,
        max_depth=4,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric='logloss'
    )
    model.fit(X_train, y_train)
    model.save_model("dota_xgboost.json")
    y_pred = model.predict(X_test)
    print('fin apprentissage')
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    prediction=model.predict(dfTestMatch)
    prediction_pourcent=model.predict_proba(dfTestMatch)

    print(prediction)
    print(prediction_pourcent)

if __name__ == '__main__':
    main()

