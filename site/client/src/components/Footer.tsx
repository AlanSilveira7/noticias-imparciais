import { Link } from "wouter";
import { Scale, Mail, Instagram } from "lucide-react";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-white">
      {/* Main footer content */}
      <div className="container py-10">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <Link href="/" className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <Scale className="w-4 h-4 text-white" />
              </div>
              <span className="text-lg font-bold">
                Notícias<span className="text-blue-400">Imparciais</span>
              </span>
            </Link>
            <p className="text-gray-400 text-sm leading-relaxed max-w-md">
              Analisamos diferentes fontes de notícias, identificamos vieses editoriais 
              e apresentamos os fatos de forma neutra. Você decide, nós informamos.
            </p>
          </div>

          {/* Navigation */}
          <div>
            <h4 className="font-bold text-sm uppercase tracking-wider text-gray-400 mb-4">
              Navegação
            </h4>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="text-gray-300 hover:text-white text-sm transition-colors">
                  Início
                </Link>
              </li>
              <li>
                <Link href="/politica" className="text-gray-300 hover:text-white text-sm transition-colors">
                  Política
                </Link>
              </li>
              <li>
                <Link href="/economia" className="text-gray-300 hover:text-white text-sm transition-colors">
                  Economia
                </Link>
              </li>
              <li>
                <Link href="/sobre" className="text-gray-300 hover:text-white text-sm transition-colors">
                  Sobre Nós
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-bold text-sm uppercase tracking-wider text-gray-400 mb-4">
              Contato
            </h4>
            <ul className="space-y-3">
              <li>
                <a 
                  href="mailto:contato@noticiasimparciais.com.br" 
                  className="text-gray-300 hover:text-white text-sm transition-colors flex items-center gap-2"
                >
                  <Mail className="w-4 h-4" />
                  contato@noticiasimparciais.com.br
                </a>
              </li>
              <li>
                <a 
                  href="https://instagram.com/noticiasimparciais" 
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-300 hover:text-white text-sm transition-colors flex items-center gap-2"
                >
                  <Instagram className="w-4 h-4" />
                  @noticiasimparciais
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Bottom bar */}
      <div className="border-t border-gray-800">
        <div className="container py-4 flex flex-col sm:flex-row justify-between items-center gap-2 text-xs text-gray-500">
          <p>© {currentYear} Notícias Imparciais. Todos os direitos reservados.</p>
          <p>Os fatos, sem filtro.</p>
        </div>
      </div>
    </footer>
  );
}
