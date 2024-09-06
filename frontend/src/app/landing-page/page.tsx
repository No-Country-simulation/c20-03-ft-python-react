
import FlashSale from "./ui/flash-sale/flash-sale";
import { testFlashSaleData } from "./lib/utils";

export default function LandingPage() {

  const testData = testFlashSaleData(7);
  return (
    <div className="min-h-screen p-24">
      <FlashSale productData={testData} />
    </div>
  );
} 