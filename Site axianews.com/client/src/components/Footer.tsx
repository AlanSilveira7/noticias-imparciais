/*
 * FOOTER COMPONENT - Portal de Notícias
 * Design: Minimalista e limpo
 * 
 * Estrutura:
 * - 4 links: Política, Economia, Tecnologia, Sobre Nós
 * - Logo e copyright
 */

const footerLinks = [
  { name: 'Política', color: '#FF0000' },
  { name: 'Economia', color: '#FF6B00' },
  { name: 'Tecnologia', color: '#00A859' },
  { name: 'Sobre Nós', color: '#FFFFFF' },
];

export default function Footer() {
  return (
    <footer className="bg-[#0A1F44] text-white">
      {/* Navigation links */}
      <div className="container py-8">
        <nav className="flex flex-wrap items-center justify-center gap-6 sm:gap-10">
          {footerLinks.map((link) => (
            <a
              key={link.name}
              href="#"
              className="text-base sm:text-lg font-semibold hover:opacity-80 transition-opacity"
              style={{ color: link.color }}
            >
              {link.name}
            </a>
          ))}
        </nav>
      </div>

      {/* Bottom bar */}
      <div className="border-t border-white/10">
        <div className="container py-6">
          <div className="flex flex-col items-center gap-4">
            {/* Logo */}
            <a href="/" className="flex items-center">
              <span 
                className="text-2xl font-extrabold tracking-tight text-white"
                style={{ fontFamily: "'Encode Sans Semi Condensed', sans-serif" }}
              >
                axianews.com
              </span>
            </a>

            {/* Copyright */}
            <p className="text-center text-sm text-white/60">
              © Copyright 2025 Axia News. Todos os direitos reservados.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
