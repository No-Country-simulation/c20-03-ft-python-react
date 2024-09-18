import FlashSale from "./landing-page/ui/flash-sale/flash-sale";
import LandingPageCategories from "./landing-page/ui/categorias/categories";
import MasVendidos from "./landing-page/ui/mas-vendidos/mas-vendidos";
import Navbar from './landing-page/ui/navbar/Navbar';

import { testProductData } from "./landing-page/lib/utils";


const HomePage = () => {

  const testFlashSaleData = testProductData(7); //se generan 7 items de prueba
  const testMasVendidosData = testProductData(4);
  
  return (
    <div className="min-h-screen p-24">
      <Navbar />
      {/* Contenido de la página */}
      <div className="container mx-auto p-8">
        <h1 className="text-4xl font-bold text-center mb-8">Bienvenido a Nuestro E-commerce</h1>
        <p className="text-center text-lg mb-4">
          Explora nuestra colección de productos de alta calidad para Hombres, Mujeres y Niños/as.
        </p>
        {/* Aquí puedes agregar más contenido, como una galería de productos, ofertas, etc. */}
      </div>
      <div className="mb-32">
        <FlashSale productData={testFlashSaleData} /> 
      </div>
      <div className="mb-32">
        <LandingPageCategories />
      </div>
      <div className="mb-32">
        <MasVendidos productData={testMasVendidosData}/>
      </div>
    </div>
  );
};

export default HomePage;
