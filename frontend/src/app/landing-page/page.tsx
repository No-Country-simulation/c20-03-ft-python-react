import FlashSale from "./ui/flash-sale/flash-sale";
import LandingPageCategories from "./ui/categorias/categories";
import MasVendidos from "./ui/mas-vendidos/mas-vendidos";

import { testProductData } from "./lib/utils";

export default function LandingPage() {

  const testFlashSaleData = testProductData(7); //se generan 7 items de prueba
  const testMasVendidosData = testProductData(2);
  return (
    <div className="min-h-screen p-24">
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
} 