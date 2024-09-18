import React, { useState } from 'react';
import { Search } from '@mui/icons-material';

const SearchBar = () => {
  const [query, setQuery] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // Aquí puedes manejar la lógica de búsqueda
    console.log('Searching for:', query);
  };

  return (
    <form onSubmit={handleSearch} className="flex items-center bg-gray-100 rounded-full px-4 py-2">
      <input
        type="text"
        className="bg-transparent focus:outline-none text-black px-2"
        placeholder="Buscar..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button type="submit">
        <Search className="text-gray-600" />
      </button>
    </form>
  );
};

export default SearchBar;
