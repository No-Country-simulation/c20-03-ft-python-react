// src/app/product/[id]/page.tsx
import  ProductDetail  from '../../components/ProductDetail';
import products from '../../data/products.json'; // Ajusta la ruta según la ubicación del archivo

interface Product {
  id: string;
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

const getProductData = (id: string): Product | null => {
  return products.find((product: Product) => product.id === id) || null;
};

const ProductPage = async ({ params }: { params: { id: string } }) => {
  const product = getProductData(params.id);

  if (!product) {
    return <p>Producto no encontrado</p>;
  }

  return (
    <div>
      <ProductDetail product={product} />
    </div>
  );
};

export default ProductPage;
