import json
import os
import numpy as np
import pandas as pd
import xgboost as xgb
from tensorflow.keras.models import load_model

# Path to the directory containing AI models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AI_MODELS_PATH = os.path.join(BASE_DIR, "ai_models/")
DATA_PATH = os.path.join(BASE_DIR, "data/")

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

# Get the default AI model ID
def get_default_model():
    all_models = get_ai_models_list()
    default_model = next((x for x in all_models if x.get('default')), None)
    return default_model

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
        case "multiScale":
            prediction = predict_dota_multiscale(hero_picks, model_path)
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

    model = xgb.XGBClassifier()
    model.load_model(model_path)
    prediction = model.predict_proba(df_match_predict)

    return float(prediction[0][1])

def predict_dota_ANN(match, model_path):
    df_match = data_frame(match)

    radiant = df_match.apply(lambda row: transformation_heroes(row, 'picks_team_0', 'radiant'), axis=1)
    dire = df_match.apply(lambda row: transformation_heroes(row, 'picks_team_1', 'dire'), axis=1)
    df_match_predict = pd.concat([radiant, dire], axis=1)

    model = load_model(model_path)
    y_pred_proba = model.predict(df_match_predict)

    return float(y_pred_proba[0][0])

def predict_dota_multiscale(hero_picks, model_path):
    full_heroes_array = create_picks_vector(hero_picks)
    print("full_heroes_array: ", full_heroes_array)
    heroes_characteristics = create_hero_characteristics_vector(hero_picks)
    print("heroes_characteristics: ", heroes_characteristics)

    predict_data = [full_heroes_array, heroes_characteristics]
    print("predict_data: ", predict_data)

    print("model path", model_path)
    model = load_model(model_path, compile=False)
    print("model loaded")
    y_pred_proba = model.predict([full_heroes_array, heroes_characteristics])

    print("pred_proba", float(y_pred_proba[0][0]))
    return float(y_pred_proba[0][0])

def create_picks_vector(team_picks):
    # Load the heroes data to get all possible hero IDs
    df_heroes_processed = pd.read_csv(DATA_PATH + 'processed_heroes.csv')
    all_hero_ids = sorted(df_heroes_processed['id'].tolist())

    # Create binary vector: [radiant_picks + dire_picks]
    total_heroes = len(all_hero_ids)
    picks_vector = np.zeros(total_heroes * 2)  # *2 for radiant + dire

    # Create hero_id to index mapping
    hero_id_to_index = {hero_id: idx for idx, hero_id in enumerate(all_hero_ids)}

    # Set radiant team picks (first half of vector)
    radiant_heroes = team_picks[0][:5]  # Ensure only 5 heroes
    for hero_id in radiant_heroes:
        if hero_id in hero_id_to_index:
            picks_vector[hero_id_to_index[hero_id]] = 1

    # Set dire team picks (second half of vector)
    dire_heroes = team_picks[1][:5]  # Ensure only 5 heroes
    for hero_id in dire_heroes:
        if hero_id in hero_id_to_index:
            picks_vector[total_heroes + hero_id_to_index[hero_id]] = 1

    return picks_vector.reshape(1, -1)

def create_hero_characteristics_vector(team_picks):
    import numpy as np
    import pandas as pd

    # Load the static heroes dataframe
    df_heroes_processed = pd.read_csv(DATA_PATH + 'processed_heroes.csv')

    # Get feature columns (excluding 'id')
    feature_cols = [col for col in df_heroes_processed.columns if col != 'id']
    n_features = len(feature_cols)

    # Create hero lookup dictionary
    hero_dict = df_heroes_processed.set_index('id').to_dict('index')

    # Initialize hero characteristics vector
    # 5 heroes per team * 2 teams * n_features per hero
    hero_chars_vector = np.zeros(5 * 2 * n_features)

    # Process radiant team (first 5 positions)
    radiant_heroes = team_picks[0][:5]  # Ensure only 5 heroes
    for i, hero_id in enumerate(radiant_heroes):
        if hero_id in hero_dict:
            for j, feat in enumerate(feature_cols):
                hero_chars_vector[i * n_features + j] = hero_dict[hero_id][feat]

    # Process dire team (next 5 positions)
    dire_heroes = team_picks[1][:5]  # Ensure only 5 heroes
    for i, hero_id in enumerate(dire_heroes):
        if hero_id in hero_dict:
            for j, feat in enumerate(feature_cols):
                hero_chars_vector[(5 + i) * n_features + j] = hero_dict[hero_id][feat]

    return hero_chars_vector.reshape(1, -1)