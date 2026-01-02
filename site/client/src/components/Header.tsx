/*
 * HEADER COMPONENT - Axia News
 * Design: Fiel ao modelo original do outro agente
 * 
 * Estrutura:
 * - Logo "Axia News" centralizado em vermelho/laranja (gradiente)
 * - Menu hamburguer à esquerda
 * - Ícone de usuário e busca à direita
 * - Barra de navegação com links coloridos: Política, Economia, Tecnologia, Sobre Nós
 */

import { Menu, Search, User, X } from 'lucide-react';
import { useState } from 'react';
import { Link, useLocation } from 'wouter';

const navLinks = [
  { name: 'Início', href: '/', color: '#FF0000' },
  { name: 'Política', href: '/politica', color: '#FF0000' },
  { name: 'Economia', href: '/economia', color: '#FF6B00' },
  { name: 'Tecnologia', href: '/tecnologia', color: '#00A859' },
  { name: 'Sobre Nós', href: '/sobre', color: '#333333' },
];

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [location, setLocation] = useLocation();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setLocation(`/busca?q=${encodeURIComponent(searchQuery.trim())}`);
      setSearchOpen(false);
      setSearchQuery('');
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-white shadow-sm">
      {/* Top bar */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-100">
        {/* Left - Menu */}
        <button 
          onClick={() => setMenuOpen(!menuOpen)}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
          aria-label="Menu"
        >
          <Menu size={24} />
        </button>

        {/* Center - Logo */}
        <div className="flex-1 flex justify-center">
          <Link href="/" className="flex items-center">
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
              Axia News
            </span>
          </Link>
        </div>

        {/* Right - User & Search */}
        <div className="flex items-center gap-2">
          <button 
            className="text-gray-600 hover:text-gray-900 transition-colors p-2"
            aria-label="Conta"
          >
            <User size={20} />
          </button>
          <button 
            onClick={() => setSearchOpen(!searchOpen)}
            className="text-gray-600 hover:text-gray-900 transition-colors p-2"
            aria-label="Buscar"
          >
            {searchOpen ? <X size={20} /> : <Search size={20} />}
          </button>
        </div>
      </div>

      {/* Search bar (expandable) */}
      {searchOpen && (
        <div className="bg-gray-50 border-b border-gray-200 px-4 py-3">
          <form onSubmit={handleSearch} className="flex items-center gap-2 max-w-2xl mx-auto">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Buscar notícias..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
              autoFocus
            />
            <button
              type="submit"
              className="px-4 py-2 bg-gradient-to-r from-red-600 to-orange-500 text-white rounded-lg hover:opacity-90 transition-opacity font-semibold"
            >
              Buscar
            </button>
          </form>
        </div>
      )}

      {/* Navigation bar with colored links */}
      <nav className="overflow-x-auto scrollbar-hide bg-white border-b border-gray-100">
        <div className="flex items-center justify-start gap-4 sm:gap-6 px-4 py-2">
          {navLinks.map((link) => (
            <Link
              key={link.name}
              href={link.href}
              className="text-sm sm:text-base font-semibold whitespace-nowrap hover:opacity-70 transition-opacity"
              style={{ color: link.color }}
            >
              {link.name}
            </Link>
          ))}
        </div>
      </nav>

      {/* Mobile menu overlay */}
      {menuOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40"
          onClick={() => setMenuOpen(false)}
        >
          <div 
            className="absolute left-0 top-0 h-full w-72 bg-white shadow-xl p-6"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-center mb-6">
              <span 
                className="text-xl font-bold"
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
              <button onClick={() => setMenuOpen(false)} className="text-gray-500 hover:text-gray-700">
                <X size={24} />
              </button>
            </div>
            <nav className="space-y-1">
              <Link
                href="/"
                className="block py-3 px-2 font-semibold border-b border-gray-100 text-gray-700 hover:bg-gray-50 rounded"
                onClick={() => setMenuOpen(false)}
              >
                Início
              </Link>
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  href={link.href}
                  className="block py-3 px-2 font-semibold border-b border-gray-100 hover:bg-gray-50 rounded"
                  style={{ color: link.color }}
                  onClick={() => setMenuOpen(false)}
                >
                  {link.name}
                </Link>
              ))}
            </nav>
            
            {/* Slogan */}
            <div className="mt-8 pt-6 border-t border-gray-200">
              <p className="text-sm text-gray-500 italic">
                Nós informamos, você decide.
              </p>
              <p className="text-xs text-gray-400 mt-2">
                Análise imparcial de notícias com indicadores de viés editorial.
              </p>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
