import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [userId, setUserId] = useState('');
  const [movieId, setMovieId] = useState('');
  const [prediction, setPrediction] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await axios.post('http://localhost:8000/recomendar/', {
      user_id: userId,
      movie_id: movieId
    });
    setPrediction(response.data.predicted_rating);
  };

  return (
    <div>
      <h1>Recomendação de Filmes</h1>
      <form onSubmit={handleSubmit}>
        <label>
          User ID:
          <input type="number" value={userId} onChange={(e) => setUserId(e.target.value)} />
        </label>
        <label>
          Movie ID:
          <input type="number" value={movieId} onChange={(e) => setMovieId(e.target.value)} />
        </label>
        <button type="submit">Recomendar</button>
      </form>
      {prediction && <p>Nota do usuário para o filme: {prediction}</p>}
    </div>
  );
}

export default App;
