import Link from 'next/link';
import { Search, Person } from '@mui/icons-material';


const Navbar = () => {
    return (
      <nav className="p-4" style={{ backgroundColor: '#FAF3E0' }}>
        <div className="container mx-auto flex justify-between items-center">
          {/* Logo */}
          <Link href="/">
            <span className="font-bold text-black text-xl">SinEtiquetas</span>
          </Link>
  
          {/* Links centrados */}
          <div className="flex space-x-6">
            <Link href="/hombre">
              <span className="hover:text-gray-500 text-black text-lg">hombre</span>
            </Link>
            <Link href="/mujer">
              <span className="hover:text-gray-500 text-black text-lg">mujer</span>
            </Link>
            <Link href="/nino">
              <span className="hover:text-gray-500 text-black text-lg">niño/a</span>
            </Link>
            <Link href="/new">
              <span className="hover:text-gray-500 text-black text-lg">NewArrivals</span>
            </Link>
          </div>
          {/*INICIAR SESION REGISTRARSE */}
          <div className="flex items-center space-x-2">
              <Link href="/login">
                <span className="text-black text-lg">
                <Person style={{ fontSize: '24px', marginRight: '4px' }} />
                  Iniciar Sesión
                  </span>
              </Link>
              <Link href="/signup">
                <span className="text-black text-lg">Registrarse</span>
              </Link>
          </div>
        </div>
      </nav>
    );
  };
  
  export default Navbar; 