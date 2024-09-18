'use client';

import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ReviewsList from '../components/Reviews';
import Footer from './Footer';

interface Product {
  id: string;
  category: string;
  name: string;
  description: string;
  price: number;
  stock: number;
  sizes: { name: string; inStock: boolean }[];
  colors: { name: string; class: string; selectedClass: string }[];
  images: string[];
  specifications: string;
}

interface ProductDetailProps {
  product: Product; 
}

const ProductDetail: React.FC<ProductDetailProps> = ({ product }) => {
  const [selectedSize, setSelectedSize] = useState(product?.sizes?.[0]?.name || '');
  const [isFavorite, setIsFavorite] = useState(false);

  const handleFavoriteClick = () => {
    setIsFavorite(!isFavorite);
  };

  if (!product || !Array.isArray(product.images) || product.images.length === 0) {
    return <p className="text-center text-red-500">Producto no disponible</p>;
  }

  return (
    <div className="bg-gray-100">
      <Navbar />
      <div className="flex flex-col items-center justify-center p-4 md:flex-row">
       
        <div className="md:w-1/4 p-4 relative flex items-center justify-center">
          <img
            src={product.images[0]} 
            alt={product.name}
            className="w-full max-w-xs h-auto object-cover rounded-lg shadow-lg"
          />
        </div>

        
        <div className="md:w-1/2 p-4">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold text-black">{product.name}</h1>
            <button onClick={handleFavoriteClick}>
              {isFavorite ? (
                <FavoriteIcon className="text-red-500 text-3xl" />
              ) : (
                <FavoriteBorderIcon className="text-gray-400 text-3xl" />
              )}
            </button>
          </div>

          <p className="text-lg font-semibold text-black mb-2">${product.price.toFixed(2)}</p>
          <p className="text-black mb-4">{product.description}</p>

          
          <div className="mb-4">
            <label className="block text-lg font-medium text-black mb-2">Talles:</label>
            <div className="grid grid-cols-4 gap-6 w-64">
              {product.sizes.map((size) => (
                <button
                  key={size.name}
                  onClick={() => setSelectedSize(size.name)}
                  disabled={!size.inStock}
                  className={`${size.inStock
                    ? 'cursor-pointer bg-white text-gray-900 shadow-sm'
                    : 'cursor-not-allowed bg-gray-50 text-gray-200'} 
                    relative flex items-center justify-center rounded-md border border-black px-8 py-3 text-lg font-medium uppercase focus:outline-none 
                    ${selectedSize === size.name ? 'ring-2 ring-indigo-500' : ''}`}
                >
                  {size.name}
                  {!size.inStock && (
                    <span className="pointer-events-none absolute inset-0 rounded-md border-2 border-gray-200">
                      <svg
                        stroke="currentColor"
                        viewBox="0 0 100 100"
                        preserveAspectRatio="none"
                        className="absolute inset-0 h-full w-full text-gray-200"
                      >
                        <line x1={0} x2={100} y1={100} y2={0} vectorEffect="non-scaling-stroke" />
                      </svg>
                    </span>
                  )}
                </button>
              ))}
            </div>
          </div>

          
          <button className="bg-blue-500 text-white px-4 py-2 w-full md:w-80 rounded-lg hover:bg-blue-600">
            Agregar al Carrito
          </button>
        </div>
      </div>

      
      <div className="p-4">
        <h2 className="text-2xl font-bold text-black mb-4 text-center">Reseñas</h2>
        <div className="p-4 bg-gray-100 rounded-lg shadow-md">
          <ReviewsList />
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default ProductDetail;
