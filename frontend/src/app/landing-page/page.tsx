import FlashSale from "./ui/flash-sale/flash-sale";
import LandingPageCategories from "./ui/categorias/categories";
import { testFlashSaleData } from "./lib/utils";

export default function LandingPage() {

  const testData = testFlashSaleData(7); //se generan 7 items de prueba
  return (
    <div className="min-h-screen p-24">
      <div className="mb-52">
        <FlashSale productData={testData} />
      </div>
      <LandingPageCategories />
    </div>
  );
} 