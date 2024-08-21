# crud/views.py
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import NotFound
from surprise import SVD, Dataset, Reader
from surprise.model_selection import cross_validate
import pandas as pd
from .serializers import PredictionSerializer

# Carregar dados e modelo
ratings = pd.read_csv('data/ratings_small.csv')
reader = Reader()
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

svd = SVD()
cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

trainset = data.build_full_trainset()
svd.fit(trainset)

@api_view(['POST'])
def recomendar_filmes(request):
    serializer = PredictionSerializer(data=request.data)
    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        movie_id = serializer.validated_data['movie_id']

        # Verifica se user_id e movie_id são válidos
        if user_id not in ratings['userId'].values:
            return Response({'error': 'User ID not found'}, status=status.HTTP_400_BAD_REQUEST)
        if movie_id not in ratings['movieId'].values:
            return Response({'error': 'Movie ID not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Fazer a predição
        prediction = svd.predict(uid=user_id, iid=movie_id)
        return Response({
            'user_id': user_id,
            'movie_id': movie_id,
            'predicted_rating': prediction.est
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
