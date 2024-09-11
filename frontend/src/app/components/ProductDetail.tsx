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
  product?: Product; 
}

const ProductDetail: React.FC<ProductDetailProps> = ({ product }) => {
  const [selectedSize, setSelectedSize] = useState(product?.sizes[0]?.name || '');
  const [selectedColor, setSelectedColor] = useState(product?.colors[0]?.name || '');
  const [isFavorite, setIsFavorite] = useState(false);

  const handleFavoriteClick = () => {
    setIsFavorite(!isFavorite);
  };

 
  const NoProductAvailable = () => (
    <div className='bg-gray-100'>
      <Navbar />
      <div className="flex md:flex-row p-4 justify-center">
        <div className="md:w-1/4 p-4 relative flex items-center justify-center content-center">
          <div className="w-full max-w-xs h-auto bg-gray-300 rounded-lg shadow-lg flex items-center justify-center">
            <span className="text-gray-500">Imagen no disponible</span>
          </div>
        </div>

        <div className="md:w-1/2 p-4 item-center">
          <div className="flex items-center mb-4">
            <h1 className="text-2xl font-bold mr-4 text-black">Producto no disponible</h1>
            <button className="ml-60" disabled>
              <FavoriteBorderIcon className="text-gray-400 text-3xl" />
            </button>
          </div>
          <p className="text-lg font-semibold mb-2 text-black">$0.00</p>
          <p className="mb-4 text-black">Descripción no disponible</p>

          <div className="mb-4">
            <fieldset aria-label="Choose a color">
              <legend className="text-lg font-medium mb-2 text-black">Color:</legend>
              <div className="flex items-center space-x-3">
                <select
                  value={selectedColor}
                  onChange={(e) => setSelectedColor(e.target.value)}
                  className="p-2 border border-black rounded-md focus:ring-2 focus:ring-indigo-500 text-black"
                >
                  <option value="" disabled>Selecciona un color</option>
                </select>
              </div>
            </fieldset>
          </div>

          <div className="mb-4">
            <label className="block text-lg font-medium mb-2 text-black">Talles:</label>
            <div className="grid grid-cols-4 gap-6 w-64">
              <button
                disabled
                className="cursor-not-allowed bg-gray-50 text-gray-200 border border-black px-8 py-3 text-lg font-medium uppercase"
              >
                Talla no disponible
              </button>
            </div>
          </div>

          <button className="bg-blue-500 text-white px-4 py-2 w-80 rounded-lg hover:bg-blue-600" disabled>
            Agregar al Carrito
          </button>
        </div>
      </div>

      <h2 className="text-2xl text-black font-bold mb-2 flex md:flex-row md:w-1/3 p-4 relative flex items-center justify-center text-center">Reseñas</h2>
      <div className="p-4 bg-gray-100 rounded-lg shadow-md flex flex-col md:flex-row relative flex items-center justify-center">
        <ReviewsList />
      </div>
      <Footer />
    </div>
  );

  
  const ProductAvailable = () => (
    <div className='bg-gray-100'>
      <Navbar />
      <br />
      <div className="flex md:flex-row p-4 justify-center">
        <div className="md:w-1/4 p-4 relative flex items-center justify-center content-center">
          <img
            src={product.images[0]}
            alt={product.name}
            className="w-full max-w-xs h-auto object-cover rounded-lg shadow-lg"
          />
        </div>

        <div className="md:w-1/2 p-4 item-center">
          <div className="flex items-center mb-4">
            <h1 className="text-2xl font-bold mr-4 text-black">{product.name}</h1>
            <button className="ml-60" onClick={handleFavoriteClick}>
              {isFavorite ? (
                <FavoriteIcon className="text-red-500 text-3xl" />
              ) : (
                <FavoriteBorderIcon className="text-gray-400 text-3xl" />
              )}
            </button>
          </div>
          <p className="text-lg font-semibold mb-2 text-black">${product.price.toFixed(2)}</p>
          <p className="mb-4 text-black">{product.description}</p>

          <div className="mb-4">
            <fieldset aria-label="Choose a color">
              <legend className="text-lg font-medium mb-2 text-black">Color:</legend>
              <div className="flex items-center space-x-3">
                <select
                  value={selectedColor}
                  onChange={(e) => setSelectedColor(e.target.value)}
                  className="p-2 border border-black rounded-md focus:ring-2 focus:ring-indigo-500 text-black"
                >
                  {product.colors.map((color) => (
                    <option
                      key={color.name}
                      value={color.name}
                      className="text-black"
                    >
                      {color.name}
                    </option>
                  ))}
                </select>
              </div>
            </fieldset>
          </div>

          <div className="mb-4">
            <label className="block text-lg font-medium mb-2 text-black">Talles:</label>
            <div className="grid grid-cols-4 gap-6 w-64">
              {product.sizes.map((size) => (
                <button
                  key={size.name}
                  onClick={() => setSelectedSize(size.name)}
                  disabled={!size.inStock}
                  className={`${size.inStock
                    ? 'cursor-pointer bg-white text-gray-900 shadow-sm'
                    : 'cursor-not-allowed bg-gray-50 text-gray-200'} 
                    group relative flex items-center justify-center rounded-md border border-black px-8 py-3 text-lg font-medium uppercase focus:outline-none 
                    ${selectedSize === size.name ? 'ring-2 ring-indigo-500' : ''}`}

                >
                  {size.name}
                  {size.inStock ? (
                    <span
                      aria-hidden="true"
                      className="pointer-events-none absolute -inset-px rounded-md border-2 border-transparent group-focus:border-indigo-500"
                    />
                  ) : (
                    <span
                      aria-hidden="true"
                      className="pointer-events-none absolute -inset-px rounded-md border-2 border-gray-200"
                    >
                      <svg
                        stroke="currentColor"
                        viewBox="0 0 100 100"
                        preserveAspectRatio="none"
                        className="absolute inset-0 h-full w-50 stroke-2 text-gray-200"
                      >
                        <line x1={0} x2={100} y1={100} y2={0} vectorEffect="non-scaling-stroke" />
                      </svg>
                    </span>
                  )}
                </button>
              ))}
            </div>
          </div>

          <button className="bg-blue-500 text-white px-4 py-2 w-80 rounded-lg hover:bg-blue-600">
            Agregar al Carrito
          </button>
        </div>
      </div>

      <h2 className="text-2xl text-black font-bold mb-2 flex md:flex-row md:w-1/3 p-4 relative flex items-center justify-center text-center">Reseñas</h2>
      <div className="p-4 bg-gray-100 rounded-lg shadow-md flex flex-col md:flex-row relative flex items-center justify-center">
        <ReviewsList />
      </div>
      <Footer />
    </div>
  );

  
  return product ? <ProductAvailable /> : <NoProductAvailable />;
};

export default ProductDetail;
