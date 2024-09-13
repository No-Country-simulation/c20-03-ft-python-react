import axios from 'axios';



const BASE_URL = 'https://back-dev.avillalba.com.ar/api/v1';

interface Product {
  id: number;
  category: string;
  name: string;
  description: string;
  price: number;
  stock: number;
  sizes: string[];
  colors: string[];
  images: string[];
  specifications: string;
}

const getProductData = async (id: string): Promise<Product | null> => {
  try {
    const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2MTg5MjI0LCJpYXQiOjE3MjYxODg5MjQsImp0aSI6ImRhZjEwOTE5MTkzYTRlODY5OGE0YjM1M2FiMmI1OWFkIiwidXNlcl9pZCI6N30.tbSTGAlaA-CfdoM7ktOvmN7BNvWqFrUqJoZN9pU___I'; // Reemplaza con tu token real
    const response = await axios.get<Product>(`${BASE_URL}/products/${id}/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching product data', error);
    return null;
  }
};

const ProductPage = async ({ params }: { params: { id: string } }) => {
  const product = await getProductData(params.id);

  if (!product) {
    return (
      <div>
        <h2>Producto no encontrado</h2>
      </div>
    );
  }

  return (
    <div>
      <ProductDetail product={product} />
    </div>
  );
};

export default ProductPage;
