
export interface flashSaleDataInterface {
    [key: string]: any;
    imageURL: string;
    productName: string,
    productDescription: string,
    productPrice: number,
    productID: number
}

export function testFlashSaleData(numberOfItems: number) { //mockup data, delete after testing

    let testData: flashSaleDataInterface[] = []
    for (let i = 0; i< numberOfItems; i++){
        testData.push(
            {imageURL: "",
            productName: "Producto "+i,
            productDescription: "Producto "+i,
            productPrice: i,
            productID: i}
        )
    }
    return testData;
}

