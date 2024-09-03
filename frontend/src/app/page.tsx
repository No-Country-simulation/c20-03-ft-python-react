// src/app/page.tsx
import Navbar from './components/Navbar';

const HomePage = () => {
  return (
    <div>
      {/* Incluir el Navbar */}
      <Navbar />

      {/* Contenido de la página */}
      <div className="container mx-auto p-8">
        <h1 className="text-4xl font-bold text-center mb-8">Bienvenido a Nuestro E-commerce</h1>
        <p className="text-center text-lg mb-4">
          Explora nuestra colección de productos de alta calidad para Hombres, Mujeres y Niños/as.
        </p>
        {/* Aquí puedes agregar más contenido, como una galería de productos, ofertas, etc. */}
      </div>
    </div>
  );
};

export default HomePage;
