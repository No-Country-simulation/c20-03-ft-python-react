import Link from 'next/link';
import { PersonOutline, ShoppingBag } from '@mui/icons-material';

const UserActions = () => {
  return (
    <div className="flex items-center space-x-4">
      <Link href="/login" className="flex items-center hover:text-gray-700">
        <PersonOutline className="text-2xl" />
        <span className="ml-2">Iniciar sesión</span>
      </Link>
      
      <Link href="/cart" className="flex items-center hover:text-gray-700">
        <ShoppingBag className="text-2xl" />
        <span className="ml-2">Carrito</span>
      </Link>
    </div>
  );
};

export default UserActions;
