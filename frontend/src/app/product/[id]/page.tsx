import ProductDetail from '../../components/ProductDetail';
import axios from 'axios';

const BASE_URL = 'https://back-dev.avillalba.com.ar/api/v1';

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

const getProductData = async (id: string): Promise<Product | null> => {
  try {
    const response = await axios.get(`${BASE_URL}/products/${id}`);
    const product = response.data;
    return product;
  } catch (error) {
    console.error('Error fetching product data', error);
    return null;
  }
};

const ProductPage = async ({ params }: { params: { id: string } }) => {
  const product = await getProductData(params.id);

  if (!product) {
    return <div>Error obteniendo los datos del producto.</div>;
  }

  return (
    <div>
      <ProductDetail product={product} />
    </div>
  );
};

export default ProductPage;
