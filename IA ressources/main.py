from AIPredict import predict_dota

data = [[38,103,27,94,55], [1,4,3,8,5]]

#Prediction du match par le model IA
prediction = predict_dota(data)

print("Résultats de la prédiction :", prediction["Gagnant"],prediction["Probabilité"])