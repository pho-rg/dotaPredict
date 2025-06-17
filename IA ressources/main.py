from AIPredict import predict_dota_XGBoost , predict_dota_ANN

data = [[38,103,27,94,55],[1,2,3,4,5]]
#data = [[38,103,27,94,55],[10,64,131,19,129]]
#data = [[10,64,131,19,129],[38,103,27,94,55]]

#Prediction du match par le model IA
#prediction = predict_dota_XGBoost(data)

#print("Résultats de la prédiction :", prediction["Gagnant"],prediction["Probabilité"])

prediction = predict_dota_ANN(data)

print("Résultats de la prédiction :", prediction["Gagnant"],prediction["Probabilité"])