import ProductCard from "../flash-sale/cards"
import { flashSaleDataInterface } from "../../lib/utils";

export default function MasVendidos ({productData}:{productData: flashSaleDataInterface[]}){

    let filteredProductData: flashSaleDataInterface[] = productData; //min width of 384px supports at most 4 cards on the page
    if (filteredProductData.length > 4){
        filteredProductData = productData.slice(0,4)
    }

    return(
        <>
        <div className="flex justify-center mb-12 text-6xl font-bold">
          <p>Mas vendidos</p>
        </div>
        <div className={`grid gap-2 grid-cols-${filteredProductData.length}`}>
            {filteredProductData.map((item) => (
                <ProductCard productData={item} width={"auto"}/>
            ))}
        </div>
      </>
    )
}