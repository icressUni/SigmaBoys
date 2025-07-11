import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import AdminDashboard from "./pages/AdminDashboard";
import Header from "./componentes/Header";
import LoadingScreen from "./componentes/LoadingScreen";
import { JSX, useEffect, useState, createContext } from "react";
import { LanguageProvider } from "./lenguage/LenguageContext";
import "./styles/index.css";

// ✅ Función helper para manejar localStorage de forma segura
const getStorageItem = (key: string): string | null => {
  try {
    if (typeof Storage !== "undefined" && window.localStorage) {
      return localStorage.getItem(key);
    }
  } catch (error) {
    console.warn('Error accessing localStorage:', error);
  }
  return null;
};

const setStorageItem = (key: string, value: string): boolean => {
  try {
    if (typeof Storage !== "undefined" && window.localStorage) {
      localStorage.setItem(key, value);
      return true;
    }
  } catch (error) {
    console.warn('Error setting localStorage:', error);
  }
  return false;
};

const removeStorageItem = (key: string): boolean => {
  try {
    if (typeof Storage !== "undefined" && window.localStorage) {
      localStorage.removeItem(key);
      return true;
    }
  } catch (error) {
    console.warn('Error removing from localStorage:', error);
  }
  return false;
};

// ✅ Context para manejar autenticación
export const AuthContext = createContext<{
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
  checkAuth: () => void;
}>({
  isAuthenticated: false,
  login: () => {},
  logout: () => {},
  checkAuth: () => {},
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isInitialized, setIsInitialized] = useState<boolean>(false);

  const checkAuth = () => {
    const token = getStorageItem("token");
    setIsAuthenticated(!!token);
    if (!isInitialized) {
      setIsInitialized(true);
    }
  };

  useEffect(() => {
    checkAuth();
    
    // Listener para cambios en localStorage desde otras pestañas
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === "token") {
        checkAuth();
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  const login = (token: string) => {
    if (setStorageItem("token", token)) {
      setIsAuthenticated(true);
    } else {
      console.error("No se pudo guardar el token");
    }
  };

  const logout = () => {
    removeStorageItem("token");
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout, checkAuth }}>
      {isInitialized ? children : <LoadingScreen />}
    </AuthContext.Provider>
  );
};

// ✅ Componente para proteger rutas mejorado
const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const [authState, setAuthState] = useState<'checking' | 'authenticated' | 'unauthenticated'>('checking');

  useEffect(() => {
    const checkAuth = () => {
      const token = getStorageItem("token");
      setAuthState(token ? 'authenticated' : 'unauthenticated');
    };

    checkAuth();
    
    // Verificar autenticación cada vez que se enfoca la ventana
    const handleFocus = () => {
      checkAuth();
    };

    window.addEventListener('focus', handleFocus);
    return () => window.removeEventListener('focus', handleFocus);
  }, []);

  if (authState === 'checking') {
    return <LoadingScreen />;
  }

  return authState === 'authenticated' ? children : <Navigate to="/" replace />;
};

function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1500);
    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return <LoadingScreen />;
  }

  return (
    <LanguageProvider>
      <AuthProvider>
        <Router>
          <div className="flex flex-col min-h-screen">
            <Header />
            <main className="flex-grow pt-16 px-4 sm:px-6 lg:px-8">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/admin" element={<Navigate to="/" replace />} />
                <Route
                  path="/admin-dashboard"
                  element={
                    <ProtectedRoute>
                      <AdminDashboard />
                    </ProtectedRoute>
                  }
                />
                {/* Ruta catch-all para manejar rutas no encontradas */}
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </main>
          </div>
        </Router>
      </AuthProvider>
    </LanguageProvider>
  );
}

export default App;