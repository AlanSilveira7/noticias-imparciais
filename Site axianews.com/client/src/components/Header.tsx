/*
 * HEADER COMPONENT - Portal de Notícias
 * Design: Fidelidade Editorial Clássica
 * 
 * Estrutura:
 * - Logo centralizado em vermelho/laranja
 * - Menu hamburguer à esquerda
 * - Botão Conta à direita
 * - Barra de navegação com 4 links: Política, Economia, Tecnologia, Sobre Nós
 */

import { Menu, Search, User } from 'lucide-react';
import { useState } from 'react';

const navLinks = [
  { name: 'Política', color: '#FF0000' },
  { name: 'Economia', color: '#FF6B00' },
  { name: 'Tecnologia', color: '#00A859' },
  { name: 'Sobre Nós', color: '#0A1F44' },
];

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-white shadow-sm">
      {/* Top bar */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-100">
        {/* Left - Menu */}
        <button 
          onClick={() => setMenuOpen(!menuOpen)}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
          aria-label="Menu"
        >
          <Menu size={24} />
          <span className="text-sm font-medium hidden sm:inline">Menu</span>
        </button>

        {/* Center - Logo */}
        <div className="flex-1 flex justify-center">
          <a href="/" className="flex items-center">
            <span 
              className="text-2xl sm:text-3xl font-extrabold tracking-tight"
              style={{ 
                fontFamily: "'Encode Sans Semi Condensed', sans-serif",
                background: 'linear-gradient(135deg, #FF0000 0%, #FF6B00 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text'
              }}
            >
              axia
              <span 
                style={{ 
                  background: 'linear-gradient(135deg, #FF6B00 0%, #FF0000 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text'
                }}
              >
                news.com
              </span>
            </span>
          </a>
        </div>

        {/* Right - Account & Search */}
        <div className="flex items-center gap-3">
          <a 
            href="#" 
            className="flex items-center gap-1 text-gray-600 hover:text-gray-900 transition-colors"
          >
            <User size={20} />
            <span className="text-sm font-medium hidden sm:inline">Conta</span>
          </a>
          <button 
            className="text-gray-600 hover:text-gray-900 transition-colors"
            aria-label="Buscar"
          >
            <Search size={20} />
          </button>
        </div>
      </div>

      {/* Navigation bar with 4 links */}
      <nav className="overflow-x-auto scrollbar-hide">
        <div className="flex items-center justify-center gap-2 sm:gap-6 px-4 py-2">
          {navLinks.map((link) => (
            <a
              key={link.name}
              href="#"
              className="px-3 py-1.5 rounded text-sm sm:text-base font-semibold whitespace-nowrap hover:bg-gray-100 transition-colors"
              style={{ color: link.color }}
            >
              {link.name}
            </a>
          ))}
        </div>
      </nav>

      {/* Mobile menu overlay */}
      {menuOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setMenuOpen(false)}
        >
          <div 
            className="absolute left-0 top-0 h-full w-72 bg-white shadow-xl p-6"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-center mb-6">
              <span className="text-xl font-bold" style={{ fontFamily: "'Encode Sans Semi Condensed', sans-serif" }}>
                Menu
              </span>
              <button onClick={() => setMenuOpen(false)} className="text-gray-500">
                ✕
              </button>
            </div>
            <nav className="space-y-4">
              {navLinks.map((link) => (
                <a
                  key={link.name}
                  href="#"
                  className="block py-2 font-semibold border-b border-gray-100"
                  style={{ color: link.color }}
                >
                  {link.name}
                </a>
              ))}
            </nav>
          </div>
        </div>
      )}
    </header>
  );
}
