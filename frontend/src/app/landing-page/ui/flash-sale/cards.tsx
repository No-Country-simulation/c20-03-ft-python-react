import * as React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { flashSaleDataInterface } from '../../lib/utils';

export default function ProductCard({
    productData
}:{
    productData: flashSaleDataInterface
}){
  return (
    <Card sx={{ maxWidth: 384, mx: 1, borderRadius: "16px"} } variant="outlined">
      <CardMedia
        sx={{ height: 512, bgcolor: 'text.disabled'}}
      />
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          {productData.productName ? productData.productName : "Product Name"}
        </Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary' }}>
            {productData.productDescription ? productData.productDescription : "Product description"}
        </Typography>
      </CardContent>
      <CardActions sx={{p: 2, justifyContent: 'space-between'}}>
        <Typography variant="body2">
            {productData.productPrice ? productData.productPrice : "Product price"}
        </Typography>
        <Button size="small" variant="outlined" color="secondary">Comprar</Button>
      </CardActions>
    </Card>
  );
}