#!/usr/bin/env python3
"""
Script simple para probar las pruebas unitarias paso a paso
"""

import sys
import os

def test_imports():
    """Prueba las importaciones básicas"""
    print("🔍 Probando importaciones...")
    
    try:
        import unittest
        print("✓ unittest importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando unittest: {e}")
        return False
    
    try:
        import tempfile
        import shutil
        import pickle
        from unittest.mock import patch, MagicMock
        print("✓ Dependencias estándar importadas correctamente")
    except ImportError as e:
        print(f"❌ Error importando dependencias estándar: {e}")
        return False
    
    try:
        # Verificar que model_creation.py existe
        if not os.path.exists('model_creation.py'):
            print("❌ model_creation.py no encontrado en el directorio actual")
            return False
        print("✓ model_creation.py encontrado")
        
        # Intentar importar
        sys.path.insert(0, '.')
        from model_creation import crear_y_guardar_modelo
        print("✓ model_creation importado correctamente")
        
    except ImportError as e:
        print(f"❌ Error importando model_creation: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    
    return True

def run_single_test():
    """Ejecuta una sola prueba simple"""
    print("\n🧪 Ejecutando prueba simple...")
    
    try:
        import unittest
        from unittest.mock import patch
        import os
        import tempfile
        import shutil
        
        # Importar función
        from model_creation import crear_y_guardar_modelo
        
        # Crear test simple
        class SimpleTest(unittest.TestCase):
            def test_directorio_no_existe(self):
                """Test básico: directorio no existe"""
                test_dir = tempfile.mkdtemp()
                try:
                    with patch('builtins.print') as mock_print:
                        crear_y_guardar_modelo(test_dir, "test_model.pkl")
                        # Verificar que se imprimió el mensaje de error
                        expected_dir = os.path.join(test_dir, "personas_autorizadas")
                        mock_print.assert_called_with(f"El directorio {expected_dir} no existe.")
                    print("✓ Test básico pasó correctamente")
                    return True
                finally:
                    shutil.rmtree(test_dir)
        
        # Ejecutar test
        suite = unittest.TestLoader().loadTestsFromTestCase(SimpleTest)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
        
    except Exception as e:
        print(f"❌ Error en test simple: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal de diagnóstico"""
    print("🚀 DIAGNÓSTICO DE PRUEBAS UNITARIAS")
    print("=" * 50)
    
    # Verificar directorio actual
    print(f"📁 Directorio actual: {os.getcwd()}")
    print(f"📄 Archivos en directorio: {os.listdir('.')}")
    
    # Probar importaciones
    if not test_imports():
        print("\n❌ Falla en importaciones. Revisa las dependencias.")
        return False
    
    # Ejecutar test simple
    if not run_single_test():
        print("\n❌ Falla en test simple.")
        return False
    
    print("\n🎉 ¡Diagnóstico exitoso! Las pruebas deberían funcionar.")
    print("\nAhora puedes ejecutar:")
    print("  python -m unittest test_model_creation -v")
    print("  o")
    print("  python run_tests.py")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
