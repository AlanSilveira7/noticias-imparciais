import { Link, useLocation } from "wouter";
import { Menu, Search, X, Scale } from "lucide-react";
import { useState } from "react";

interface HeaderProps {
  onSearch?: (query: string) => void;
}

export default function Header({ onSearch }: HeaderProps) {
  const [location, setLocation] = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  
  const navItems = [
    { href: "/", label: "Início" },
    { href: "/politica", label: "Política" },
    { href: "/economia", label: "Economia" },
    { href: "/sobre", label: "Sobre" },
  ];

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setLocation(`/busca?q=${encodeURIComponent(searchQuery.trim())}`);
      setSearchOpen(false);
    }
  };

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      {/* Top bar with date */}
      <div className="border-b border-gray-100">
        <div className="container flex items-center justify-between py-2 text-xs text-gray-500">
          <span>
            {new Date().toLocaleDateString('pt-BR', { 
              weekday: 'long', 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            }).replace(/^\w/, c => c.toUpperCase())}
          </span>
          <span className="hidden sm:block">Os fatos, sem filtro.</span>
        </div>
      </div>
      
      {/* Main header */}
      <div className="container">
        <div className="flex items-center justify-between py-3">
          {/* Mobile menu button */}
          <button 
            className="lg:hidden p-2 -ml-2 text-gray-600 hover:text-gray-900"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Menu"
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
          
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <div className="w-9 h-9 bg-blue-600 rounded-lg flex items-center justify-center">
              <Scale className="w-5 h-5 text-white" />
            </div>
            <div className="hidden sm:block">
              <span className="text-xl font-bold text-gray-900">
                Notícias<span className="text-blue-600">Imparciais</span>
              </span>
            </div>
          </Link>
          
          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`px-4 py-2 text-sm font-medium rounded transition-colors ${
                  location === item.href || (item.href !== "/" && location.startsWith(item.href))
                    ? "text-blue-600 bg-blue-50"
                    : "text-gray-700 hover:text-blue-600 hover:bg-gray-50"
                }`}
              >
                {item.label}
              </Link>
            ))}
          </nav>
          
          {/* Search button */}
          <button 
            className="p-2 text-gray-600 hover:text-gray-900" 
            aria-label="Buscar"
            onClick={() => setSearchOpen(!searchOpen)}
          >
            {searchOpen ? <X size={20} /> : <Search size={20} />}
          </button>
        </div>
        
        {/* Search bar */}
        {searchOpen && (
          <div className="pb-3">
            <form onSubmit={handleSearch} className="flex gap-2">
              <input
                type="text"
                placeholder="Buscar notícias..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                autoFocus
              />
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Buscar
              </button>
            </form>
          </div>
        )}
      </div>
      
      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-t border-gray-200 bg-white">
          <nav className="container py-2">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setMobileMenuOpen(false)}
                className={`block px-4 py-3 text-sm font-medium border-b border-gray-100 last:border-0 ${
                  location === item.href || (item.href !== "/" && location.startsWith(item.href))
                    ? "text-blue-600 bg-blue-50"
                    : "text-gray-700 hover:text-blue-600 hover:bg-gray-50"
                }`}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      )}
    </header>
  );
}
