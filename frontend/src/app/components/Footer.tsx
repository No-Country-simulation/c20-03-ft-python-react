import React from 'react';
import FacebookIcon from '@mui/icons-material/Facebook';
import InstagramIcon from '@mui/icons-material/Instagram';
import GitHubIcon from '@mui/icons-material/GitHub';
import YouTubeIcon from '@mui/icons-material/YouTube';
import TwitterIcon from '@mui/icons-material/Twitter';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-white py-8">
      <div className="container mx-auto flex flex-col md:flex-row justify-between items-start md:items-center space-y-8 md:space-y-0 md:space-x-16">
        
        <div className="flex flex-col md:mb-0">
          <h4 className="text-lg font-bold mb-4">Síguenos en:</h4>
          <div className="flex space-x-6">
            <a href="https://www.facebook.com" target="_blank" rel="noopener noreferrer">
              <FacebookIcon className="hover:text-blue-500" style={{ fontSize: 30 }} />
            </a>
            <a href="https://www.instagram.com" target="_blank" rel="noopener noreferrer">
              <InstagramIcon className="hover:text-pink-500" style={{ fontSize: 30 }} />
            </a>
            <a href="https://github.com" target="_blank" rel="noopener noreferrer">
              <GitHubIcon className="hover:text-gray-500" style={{ fontSize: 30 }} />
            </a>
            <a href="https://www.youtube.com" target="_blank" rel="noopener noreferrer">
              <YouTubeIcon className="hover:text-red-500" style={{ fontSize: 30 }} />
            </a>
            <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">
              <TwitterIcon className="hover:text-blue-400" style={{ fontSize: 30 }} />
            </a>
          </div>
        </div>

        
        <div className="flex flex-col md:mb-0">
          <h4 className="text-lg font-bold mb-4">Atención al Cliente</h4>
          <p>Email: atencion@ejemplo.com</p>
          <p>Horario de atención:</p>
          <p>Lunes a Viernes: 9:00 AM - 6:00 PM</p>
          <p>Sábados: 10:00 AM - 2:00 PM</p>
        </div>

       
        <div className="flex flex-col">
          <h4 className="text-lg font-bold mb-4">Sobre Nosotros</h4>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam id dolor id nibh ultricies vehicula ut id elit. Sed posuere consectetur est at lobortis.</p>
          <p className="mt-4">Suscríbete a nuestras noticias para mantenerte informado.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
