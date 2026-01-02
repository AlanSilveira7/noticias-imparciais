/*
 * FOOTER COMPONENT - Axia News
 * Design: Minimalista e limpo com cores das editorias
 * 
 * Estrutura:
 * - Links de navegação com cores das editorias
 * - Seção de contato
 * - Logo e copyright
 */

import { Link } from 'wouter';
import { Mail, Instagram } from 'lucide-react';

const footerLinks = [
  { name: 'Política', href: '/politica', color: '#FF0000' },
  { name: 'Economia', href: '/economia', color: '#FF6B00' },
  { name: 'Tecnologia', href: '/tecnologia', color: '#00A859' },
  { name: 'Sobre Nós', href: '/sobre', color: '#FFFFFF' },
];

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-[#0A1F44] text-white">
      {/* Main footer content */}
      <div className="container py-10">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <Link href="/" className="flex items-center mb-4">
              <span 
                className="text-2xl font-extrabold tracking-tight"
                style={{ 
                  fontFamily: "'Encode Sans Semi Condensed', sans-serif",
                  background: 'linear-gradient(135deg, #FF0000 0%, #FF6B00 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text'
                }}
              >
                Axia News
              </span>
            </Link>
            <p className="text-white/70 text-sm leading-relaxed max-w-md">
              Analisamos diferentes fontes de notícias, identificamos vieses editoriais 
              e apresentamos os fatos de forma neutra. Nós informamos, você decide.
            </p>
            <p className="text-white/50 text-sm italic mt-3">
              Os fatos, sem filtro.
            </p>
          </div>

          {/* Navigation */}
          <div>
            <h4 className="font-bold text-sm uppercase tracking-wider text-white/60 mb-4">
              Navegação
            </h4>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="text-white/80 hover:text-white text-sm transition-colors">
                  Início
                </Link>
              </li>
              {footerLinks.map((link) => (
                <li key={link.name}>
                  <Link 
                    href={link.href} 
                    className="text-sm transition-colors hover:opacity-80"
                    style={{ color: link.color }}
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-bold text-sm uppercase tracking-wider text-white/60 mb-4">
              Contato
            </h4>
            <ul className="space-y-3">
              <li>
                <a 
                  href="mailto:contato@axianews.com" 
                  className="text-white/80 hover:text-white text-sm transition-colors flex items-center gap-2"
                >
                  <Mail className="w-4 h-4" />
                  contato@axianews.com
                </a>
              </li>
              <li>
                <a 
                  href="https://instagram.com/axianews" 
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-white/80 hover:text-white text-sm transition-colors flex items-center gap-2"
                >
                  <Instagram className="w-4 h-4" />
                  @axianews
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Bottom bar */}
      <div className="border-t border-white/10">
        <div className="container py-4 flex flex-col sm:flex-row justify-between items-center gap-2 text-xs text-white/40">
          <p>© {currentYear} Axia News. Todos os direitos reservados.</p>
          <p className="italic">Os fatos, sem filtro.</p>
        </div>
      </div>
    </footer>
  );
}
