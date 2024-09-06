'use client'
import SimpleSlider from "./carousel";
import Box from '@mui/material/Box';
import { useState } from "react";
import { flashSaleDataInterface } from "../../lib/utils";

export default function FlashSale({productData}: {productData: flashSaleDataInterface[]}) {

  const [selectedCategory, setSelectedCategory] = useState(0)
  const categories = ["Hombre", "Mujer", "Niños", "Accesorios"]
  const handleCategory = (id: number) => {
    setSelectedCategory(id);
  }

    return (
      <>
        <div className="flex justify-center mb-8 text-6xl font-bold">
          <p>FLASH SALE</p>
        </div>
        <div className="flex justify-center">
          {categories.map((category, id) =>(
            <h2 onClick={() => handleCategory(id)} className={`p-1 mx-5 mb-8 border-b-2 cursor-pointer ${selectedCategory === id ? "text-fuchsia-400 border-fuchsia-400" : "hover:bg-slate-600/[0.1] border-black"}`}>{category}</h2>
          ))}
        </div>
        <div className="flex justify-center">
          <Box sx={{width: 1200}}>
            <SimpleSlider productData={productData}/>
          </Box>
        </div>
      </>
    );
  } 