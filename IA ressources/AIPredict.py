import pandas as pd
import xgboost as xgb
from tensorflow.keras.models import load_model

def transformation_heroes(row, team_col, team):
    dfOut = pd.Series([False] * 146, index=[f'picks_team_{team}_{i}' for i in range(146)])
    for hero_id in row[team_col]:
        dfOut[f'picks_team_{team}_{hero_id}'] = True
    return dfOut

def data_frame(datas):
    return pd.DataFrame({
        'picks_team_0': [datas[0]],
        'picks_team_1': [datas[1]]
    })

def predict_dota_XGBoost(match):

    df_match = data_frame(match)

    radiant = df_match.apply(lambda row: transformation_heroes(row, 'picks_team_0', 'radiant'), axis=1)
    dire = df_match.apply(lambda row: transformation_heroes(row, 'picks_team_1', 'dire'), axis=1)
    df_match_predict = pd.concat([radiant, dire], axis=1)

    model=xgb.XGBClassifier()
    model.load_model("dota_xgboost.json")

    return {"Gagnant":model.predict(df_match_predict), "Probabilité":model.predict_proba(df_match_predict)}




def predict_dota_ANN(match):

    df_match = data_frame(match)

    radiant = df_match.apply(lambda row: transformation_heroes(row, 'picks_team_0', 'radiant'), axis=1)
    dire = df_match.apply(lambda row: transformation_heroes(row, 'picks_team_1', 'dire'), axis=1)
    df_match_predict = pd.concat([radiant, dire], axis=1)

    model = load_model("dota_ann.h5")
    y_pred_proba = model.predict(df_match_predict)
    y_pred = (y_pred_proba > 0.5).astype(int)

    return {"Gagnant":y_pred,"Probabilité":(y_pred_proba,1-y_pred_proba)}
