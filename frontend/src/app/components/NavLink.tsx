'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import DropdownMenu from './DropdownMenu';

interface NavLinkProps {
  title: string;
}

const NavLink: React.FC<NavLinkProps> = ({ title }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div
      className="relative"
      onMouseEnter={() => setIsOpen(true)}
      onMouseLeave={() => setIsOpen(false)}
    >
      <Link href={`/${title.toLowerCase()}`}>
        {/* Aquí eliminamos la etiqueta <a> */}
        <span className="text-lg font-medium hover:text-gray-700">{title}</span>
      </Link>

      {isOpen && (
        <div className="absolute left-0 top-full mt-2 bg-white shadow-lg py-4 px-6 z-50">
          <DropdownMenu category={title} />
        </div>
      )}
    </div>
  );
};

export default NavLink;
