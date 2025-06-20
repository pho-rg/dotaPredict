import json
import os
import pandas as pd
import xgboost as xgb
from tensorflow.keras.models import load_model

# Path to the directory containing AI models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AI_MODELS_PATH = os.path.join(BASE_DIR, "ai_models/")

# List active AI models
def get_ai_models_list(all_data=False):
    with open(AI_MODELS_PATH + "list.json", 'r') as file:
        raw_data = json.load(file)
        result = []
        default_found = False
        for model in raw_data:
            model_path = os.path.join(AI_MODELS_PATH, model['filename'])
            if model['default'] and not default_found:
                default_found = True
                default = True
            else:
                default = False
            if os.path.exists(model_path) and model['active']:
                if all_data:
                    result.append(model)
                else:  # only return id, name, version and default status for the users
                    result.append({
                        "id": model['id'],
                        "name": model['name'],
                        "version": model['version'],
                        "default": default
                    })
        return result
    
# Predict match using the selected AI model and the provided hero picks
def predict_match(hero_picks, ai_model_id):
    # get all available AI models
    ai_models = get_ai_models_list(True)

    # find the requested AI model by ID
    requested_model = next((model for model in ai_models if model['id'] == ai_model_id), None)
    if not requested_model:
        return {"error": "Model not found."}
    
    # check if the model file exists
    model_path = os.path.join(AI_MODELS_PATH, requested_model['filename'])
    if not os.path.exists(model_path):
        return {"error": "Model file not found."}
    
    # predict according to the model type
    prediction = 0
    match requested_model['type']:
        case "xgboost":
            prediction = predict_dota_XGBoost(hero_picks, model_path)
        case "ann":
            prediction = predict_dota_ANN(hero_picks, model_path)
        case _:
            return {"error": "Model not found or not implemented."}
        
    # return the prediction result
    return {
        "radiantWinChance": prediction,
    }

# model usage methods
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
def predict_dota_XGBoost(match, model_path):
    df_match = data_frame(match)

    radiant = df_match.apply(lambda row: transformation_heroes(row, 'picks_team_0', 'radiant'), axis=1)
    dire = df_match.apply(lambda row: transformation_heroes(row, 'picks_team_1', 'dire'), axis=1)
    df_match_predict = pd.concat([radiant, dire], axis=1)

    model=xgb.XGBClassifier()
    model.load_model(model_path)

    return model.predict_proba(df_match_predict)[1]
def predict_dota_ANN(match, model_path):
    df_match = data_frame(match)

    radiant = df_match.apply(lambda row: transformation_heroes(row, 'picks_team_0', 'radiant'), axis=1)
    dire = df_match.apply(lambda row: transformation_heroes(row, 'picks_team_1', 'dire'), axis=1)
    df_match_predict = pd.concat([radiant, dire], axis=1)

    model = load_model(model_path)
    y_pred_proba = model.predict(df_match_predict)

    return y_pred_proba