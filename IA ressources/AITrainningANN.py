import json
import pandas as pd
from keras.src.callbacks import EarlyStopping
from keras.src.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense , Dropout



def openJson(path):
    with open (path) as json_file:
        data = json.load(json_file)
    return data

def transformationHeroes(row, team_col, team):
    dfOut = pd.Series([False] * 146, index=[f'picks_team_{team}_{i}' for i in range(146)])
    for hero_id in row[team_col]:
        dfOut[f'picks_team_{team}_{hero_id}'] = True
    return dfOut

def data_frame(datas):
    return pd.DataFrame({
        'picks_team_0': [datas[0]],
        'picks_team_1': [datas[1]]
    })

def saveDataFrameToJson(matches):
    """Methode pour suvgarder les details des matches pros"""

    fileName = f"TestDfML.json"
    path = fr"C:\Users\issam\Documents\ProjetAnnuelAI\DotaMatchsData\{fileName}"

    matches.to_json(path, index=False)

def main():

    match1=[[38,103,27,94,55],[10,64,131,19,129]]
    dfTestMatch = data_frame(match1)

    df_testM_match_dire = dfTestMatch.apply(lambda row: transformationHeroes(row, 'picks_team_1', 'dire'), axis=1)
    df_testM_match_radiant = dfTestMatch.apply(lambda row: transformationHeroes(row, 'picks_team_0', 'radiant'), axis=1)
    dfTestMatch = pd.concat([df_testM_match_radiant, df_testM_match_dire], axis=1)


    #matches = openJson(r"C:\Users\issam\Documents\ProjetAnnuelAI\DotaMatchsData\SauvgardeProMatchs2025-05-21.json")
    matches = openJson(r"C:\Users\issam\Documents\ProjetAnnuelAI\DotaMatchsData\processed_matches.json")
    df = pd.DataFrame(matches)

    df_transformedRadiant = df.apply(lambda row: transformationHeroes(row, 'picks_id_team_0', 'radiant'), axis=1)
    df_transformedDire = df.apply(lambda row: transformationHeroes(row, 'picks_id_team_1', 'dire'), axis=1)
    dfTest = pd.concat([df_transformedRadiant, df_transformedDire], axis=1)

    print('debut Apprentissage')

    X=dfTest
    y=df['radiant_win']
    X_train , X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=42)

    model = Sequential()

    model.add(Dense(64, activation='relu', input_shape=(292,)))
    model.add(Dropout(0.3))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    model.fit(X_train, y_train,
              validation_data=(X_test, y_test),
              epochs=20, batch_size=16,
              callbacks=[early_stop], verbose=1)

    model.save("dota_ann.h5")

    y_pred_proba = model.predict(X_test)
    y_pred = (y_pred_proba > 0.5).astype(int)
    print('fin apprentissage')
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

if __name__ == '__main__':
    main()

