// src/app/components/Review.tsx
import React from 'react';
import { Rating, Typography, Card, CardContent, CardHeader } from '@mui/material';

interface ReviewProps {
  name: string;
  rating: number;
  text: string;
}

const Review: React.FC<ReviewProps> = ({ name, rating, text }) => {
  return (
    <Card sx={{ maxWidth: 345, minWidth: 200 }}>
      <CardHeader
        title={name}
        subheader={<Rating name="read-only" value={rating} readOnly />}
      />
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          {text}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default Review;
