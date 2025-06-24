#!/usr/bin/env python3
"""
Script para ejecutar las pruebas unitarias con reporte de cobertura
"""

import subprocess
import sys
import os

def check_files():
    """Verifica que los archivos necesarios existan"""
    required_files = ['model_creation.py', 'test_model_creation.py']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        return False
    
    print("✓ Todos los archivos necesarios están presentes")
    return True

def run_tests_with_coverage():
    """Ejecuta las pruebas con reporte de cobertura"""
    print("="*60)
    print("EJECUTANDO PRUEBAS UNITARIAS CON COBERTURA")
    print("="*60)
    
    commands = [
        # Limpiar datos de cobertura anteriores
        [sys.executable, '-m', 'coverage', 'erase'],
        # Ejecutar pruebas con coverage
        [sys.executable, '-m', 'coverage', 'run', '--source=.', '--omit=test_*,run_tests.py,test_simple.py', '-m', 'unittest', 'test_model_creation', '-v'],
        # Generar reporte
        [sys.executable, '-m', 'coverage', 'report', '-m', '--include=model_creation.py']
    ]
    
    try:
        for i, cmd in enumerate(commands):
            print(f"\nEjecutando paso {i+1}/3: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd='.')
            
            if result.returncode != 0:
                print(f"❌ Error en paso {i+1}:")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                if i == 1:  # Si falla la ejecución de tests, intentar sin coverage
                    print("\n⚠ Intentando ejecutar sin coverage...")
                    return run_simple_tests()
                return False
            
            if i == 1:  # Mostrar salida de los tests
                print("✓ Pruebas ejecutadas:")
                print(result.stdout)
                if result.stderr:
                    print("Warnings:", result.stderr)
            
            if i == 2:  # Mostrar reporte de cobertura
                print("\n" + "="*60)
                print("REPORTE DE COBERTURA")
                print("="*60)
                print(result.stdout)
                
                # Extraer porcentaje de cobertura
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'model_creation.py' in line:
                        parts = line.split()
                        if len(parts) >= 4:
                            try:
                                coverage_percent = parts[3].replace('%', '')
                                coverage_num = int(coverage_percent)
                                if coverage_num >= 80:
                                    print(f"\n🎉 ¡ÉXITO! Cobertura: {coverage_percent}% (objetivo: 80%)")
                                else:
                                    print(f"\n⚠ Cobertura: {coverage_percent}% (objetivo: 80%)")
                                    print("Para mejorar la cobertura, revisa las líneas Missing en el reporte")
                            except (ValueError, IndexError):
                                pass
                        break
        
        # Generar reporte HTML
        try:
            html_result = subprocess.run([sys.executable, '-m', 'coverage', 'html'], 
                         capture_output=True, check=False)
            if html_result.returncode == 0:
                print("\n✓ Reporte HTML generado en htmlcov/index.html")
            else:
                print("\n⚠ No se pudo generar reporte HTML")
        except:
            print("\n⚠ Error generando reporte HTML")
        
        return True
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return run_simple_tests()

def run_simple_tests():
    """Ejecuta las pruebas sin coverage si no está disponible"""
    print("\n" + "="*60)
    print("EJECUTANDO PRUEBAS UNITARIAS (SIN COBERTURA)")
    print("="*60)
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'unittest', 'test_model_creation', '-v'
        ], capture_output=True, text=True, cwd='.')
        
        print("Resultado de las pruebas:")
        print(result.stdout)
        if result.stderr:
            print("Errores/Warnings:", result.stderr)
        
        if result.returncode == 0:
            print("\n✅ Todas las pruebas pasaron")
        else:
            print("\n❌ Algunas pruebas fallaron")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("Verificando archivos...")
    
    if not check_files():
        sys.exit(1)
    
    print("\nVerificando dependencias...")
    
    # Verificar coverage
    try:
        import coverage
        print("✓ coverage está disponible")
        use_coverage = True
    except ImportError:
        print("⚠ coverage no está disponible")
        use_coverage = False
    
    # Verificar face_recognition (mock en tests)
    try:
        import face_recognition
        print("✓ face_recognition está disponible")
    except ImportError:
        print("⚠ face_recognition no está disponible (se usarán mocks)")
    
    if use_coverage:
        success = run_tests_with_coverage()
    else:
        success = run_simple_tests()
    
    if success:
        print("\n🎉 ¡Pruebas completadas exitosamente!")
    else:
        print("\n💥 Hubo problemas con las pruebas")
        sys.exit(1)

if __name__ == '__main__':
    main()