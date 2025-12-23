import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import { Route, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import Home from "./pages/Home";
import Article from "./pages/Article";
import About from "./pages/About";
import Search from "./pages/Search";
import Politica from "./pages/Politica";
import Economia from "./pages/Economia";

function Router() {
  return (
    <Switch>
      <Route path="/" component={Home} />
      <Route path="/noticia/:id" component={Article} />
      <Route path="/sobre" component={About} />
      <Route path="/busca" component={Search} />
      <Route path="/politica" component={Politica} />
      <Route path="/economia" component={Economia} />
      <Route path="/404" component={NotFound} />
      {/* Final fallback route */}
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider defaultTheme="light">
        <TooltipProvider>
          <Toaster position="bottom-center" />
          <Router />
        </TooltipProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
