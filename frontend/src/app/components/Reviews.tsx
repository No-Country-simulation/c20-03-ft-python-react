import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Rating, Typography, Card, CardContent, CardHeader } from '@mui/material';

interface ReviewProps {
  rating: number;
  text: string;
  name: string;
}

const URL_DE_RESEÑAS = 'https://tu-url-para-reseñas.com';  

const Review: React.FC<ReviewProps> = ({ name, rating, text }) => {
  return (
    <Card sx={{ maxWidth: 345, minWidth: 200 }}>
      <CardHeader
        subheader={<Rating name="read-only" value={rating} readOnly />}
        title={name}
      />
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          {text}
        </Typography>
      </CardContent>
    </Card>
  );
};

const ReviewsList: React.FC = () => {
  const [reviews, setReviews] = useState<ReviewProps[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  
  const getReviews = async () => {
    try {
      const response = await axios.get(`${URL_DE_RESEÑAS}/reviews`);
      setReviews(response.data);  
      setLoading(false);
    } catch (err) {
      setError('Error al cargar las reseñas');
      setLoading(false);
    }
  };

  useEffect(() => {
    getReviews(); 
  }, []);

  if (loading) return <p>Cargando reseñas...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {reviews.length > 0 ? (
        reviews.map((review, index) => (
          <Review key={index} name={review.name} rating={review.rating} text={review.text} />
        ))
      ) : (
        <p className="text-gray-500">No hay reseñas para este producto.</p>
      )}
    </div>
  );
};

export default ReviewsList;
