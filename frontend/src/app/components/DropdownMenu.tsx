import Link from 'next/link';

interface DropdownMenuProps {
  category: string;
}

const DropdownMenu: React.FC<DropdownMenuProps> = ({ category }) => {
  const items = getDropdownItems(category); // Función ficticia que retorna los elementos por categoría

  return (
    <div className="absolute  left-0 top-full mt-2 bg-white shadow-lg py-4 px-6 z-50 insert-0">
      <ul className="space-y-2 w-screen">
        {items.map((item) => (
          <li key={item} className="hover:bg-gray-100">
            <Link href={`/${category.toLowerCase()}/${item.toLowerCase()}`} className="block px-4 py-2 text-black hover:text-gray-700">
              {item}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

const getDropdownItems = (category: string) => {
  switch (category) {
    case 'Hombre':
      return ['Poleras', 'Camisas', 'Chaquetas', 'Pantalones'];
    case 'Mujer':
      return ['Tops', 'Leggings', 'Chaquetas', 'Accesorios'];
    case 'Niño/a':
      return ['Zapatillas', 'Ropa Deportiva', 'Accesorios'];
    default:
      return ['Zapatillas', 'Ropa', 'Accesorios'];
  }
};

export default DropdownMenu;
