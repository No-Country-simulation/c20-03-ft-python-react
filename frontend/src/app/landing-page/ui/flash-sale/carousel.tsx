'use client'

import React from "react";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import Slider from "react-slick";
import ProductCard from "./cards";
import { flashSaleDataInterface } from "../../lib/utils";

export default function SimpleSlider({productData}:{productData: flashSaleDataInterface[]}) {
  var settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 3,
    slidesToScroll: 1
  };
  return (
    <Slider {...settings}>
      {productData.map((item) => (
        <ProductCard productData={item} />
      ))}
    </Slider>
  );
}