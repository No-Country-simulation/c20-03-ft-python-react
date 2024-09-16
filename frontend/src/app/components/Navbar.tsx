'use client';
import React from 'react';
import Link from 'next/link';
import NavLink from './NavLink';
import SearchBar from './SearchBar';
import UserActions from './UserActions';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto flex justify-between items-center py-4">
        {/* Logo */}
        <Link href="/">
          {/* Se elimina el uso innecesario de <a> */}
          <span className="w-28"> NAiK</span>
        </Link>

        {/* Links Centrales */}
        <div className="flex space-x-6">
          <NavLink title="Hombre" />
          <NavLink title="Mujer" />
          <NavLink title="Niño/a" />
          <NavLink title="Accesorios" />
          <NavLink title="New Arrivals" />
        </div>

        {/* Search Bar */}
        <SearchBar />

        {/* User Actions */}
        <UserActions />
      </div>
    </nav>
  );
};

export default Navbar;
