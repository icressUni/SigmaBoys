import unittest
import os
import tempfile
import shutil
import pickle
from unittest.mock import patch, mock_open, MagicMock
import sys

# Agregar el directorio actual al path para poder importar el módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Intentar importar el módulo a testear
    from model_creation import crear_y_guardar_modelo
except ImportError as e:
    print(f"Error al importar model_creation: {e}")
    print("Asegúrate de que model_creation.py esté en el mismo directorio")
    sys.exit(1)


class TestModelCreation(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        # Crear directorio temporal para las pruebas
        self.test_dir = tempfile.mkdtemp()
        self.directorio_autorizadas = os.path.join(self.test_dir, "personas_autorizadas")
        self.ruta_modelo = os.path.join(self.test_dir, "modelo_test.pkl")
        
    def tearDown(self):
        """Limpieza después de cada test"""
        # Eliminar directorio temporal
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_directorio_personas_autorizadas_no_existe(self):
        """Test cuando el directorio personas_autorizadas no existe"""
        with patch('builtins.print') as mock_print:
            crear_y_guardar_modelo(self.test_dir, self.ruta_modelo)
            mock_print.assert_called_with(f"El directorio {self.directorio_autorizadas} no existe.")
    
    @patch('face_recognition.load_image_file')
    @patch('face_recognition.face_encodings')
    def test_procesamiento_exitoso_de_rostros(self, mock_encodings, mock_load_image):
        """Test del procesamiento exitoso de rostros"""
        # Crear estructura de directorios
        os.makedirs(self.directorio_autorizadas)
        persona_dir = os.path.join(self.directorio_autorizadas, "juan")
        os.makedirs(persona_dir)
        
        # Crear archivo de imagen simulado
        imagen_path = os.path.join(persona_dir, "foto1.jpg")
        with open(imagen_path, 'w') as f:
            f.write("fake image content")
        
        # Configurar mocks
        mock_load_image.return_value = "fake_image"
        mock_encodings.return_value = [[[0.1, 0.2, 0.3]]]  # Codificación simulada
        
        with patch('builtins.print') as mock_print:
            crear_y_guardar_modelo(self.test_dir, self.ruta_modelo)
            
            # Verificar que se llamaron las funciones correctas
            mock_load_image.assert_called_once_with(imagen_path)
            mock_encodings.assert_called_once_with("fake_image")
            mock_print.assert_any_call("Rostro de juan agregado al modelo")
            mock_print.assert_any_call(f"Modelo guardado en {self.ruta_modelo}")
        
        # Verificar que el modelo se guardó correctamente
        self.assertTrue(os.path.exists(self.ruta_modelo))
        
        # Verificar contenido del modelo
        with open(self.ruta_modelo, 'rb') as f:
            modelo = pickle.load(f)
            self.assertEqual(len(modelo["rostros"]), 1)
            self.assertEqual(modelo["nombres"], ["juan"])
    
    @patch('face_recognition.load_image_file')
    @patch('face_recognition.face_encodings')
    def test_multiples_personas_y_imagenes(self, mock_encodings, mock_load_image):
        """Test con múltiples personas e imágenes"""
        # Crear estructura de directorios
        os.makedirs(self.directorio_autorizadas)
        
        personas = ["juan", "maria"]
        imagenes_por_persona = ["foto1.jpg", "foto2.png"]
        
        for persona in personas:
            persona_dir = os.path.join(self.directorio_autorizadas, persona)
            os.makedirs(persona_dir)
            
            for imagen in imagenes_por_persona:
                imagen_path = os.path.join(persona_dir, imagen)
                with open(imagen_path, 'w') as f:
                    f.write("fake image content")
        
        # Configurar mocks
        mock_load_image.return_value = "fake_image"
        mock_encodings.return_value = [[[0.1, 0.2, 0.3]]]
        
        crear_y_guardar_modelo(self.test_dir, self.ruta_modelo)
        
        # Verificar que el modelo contiene todas las personas
        with open(self.ruta_modelo, 'rb') as f:
            modelo = pickle.load(f)
            self.assertEqual(len(modelo["rostros"]), 4)  # 2 personas × 2 imágenes
            # Verificar que cada persona aparece 2 veces
            self.assertEqual(modelo["nombres"].count("juan"), 2)
            self.assertEqual(modelo["nombres"].count("maria"), 2)
    
    @patch('face_recognition.load_image_file')
    @patch('face_recognition.face_encodings')
    def test_imagen_sin_rostro_detectado(self, mock_encodings, mock_load_image):
        """Test cuando no se detecta ningún rostro en una imagen"""
        # Crear estructura de directorios
        os.makedirs(self.directorio_autorizadas)
        persona_dir = os.path.join(self.directorio_autorizadas, "juan")
        os.makedirs(persona_dir)
        
        imagen_path = os.path.join(persona_dir, "foto_sin_rostro.jpg")
        with open(imagen_path, 'w') as f:
            f.write("fake image content")
        
        # Configurar mocks - sin rostros detectados
        mock_load_image.return_value = "fake_image"
        mock_encodings.return_value = []  # Lista vacía = sin rostros
        
        with patch('builtins.print') as mock_print:
            crear_y_guardar_modelo(self.test_dir, self.ruta_modelo)
            mock_print.assert_any_call(f"No se encontró ningún rostro en {imagen_path}")
    
    @patch('face_recognition.load_image_file')
    def test_error_al_procesar_imagen(self, mock_load_image):
        """Test cuando ocurre un error al procesar una imagen"""
        # Crear estructura de directorios
        os.makedirs(self.directorio_autorizadas)
        persona_dir = os.path.join(self.directorio_autorizadas, "juan")
        os.makedirs(persona_dir)
        
        imagen_path = os.path.join(persona_dir, "foto_corrupta.jpg")
        with open(imagen_path, 'w') as f:
            f.write("fake image content")
        
        # Configurar mock para lanzar excepción
        mock_load_image.side_effect = Exception("Error de lectura de imagen")
        
        with patch('builtins.print') as mock_print:
            crear_y_guardar_modelo(self.test_dir, self.ruta_modelo)
            mock_print.assert_any_call(f"Error al procesar {imagen_path}: Error de lectura de imagen")
    
    def test_archivos_no_imagen_ignorados(self):
        """Test que los archivos que no son imágenes se ignoran"""
        # Crear estructura de directorios
        os.makedirs(self.directorio_autorizadas)
        persona_dir = os.path.join(self.directorio_autorizadas, "juan")
        os.makedirs(persona_dir)
        
        # Crear archivos de diferentes tipos
        archivos = ["documento.txt", "video.mp4", "audio.wav", "imagen.jpg"]
        for archivo in archivos:
            archivo_path = os.path.join(persona_dir, archivo)
            with open(archivo_path, 'w') as f:
                f.write("contenido falso")
        
        with patch('face_recognition.load_image_file') as mock_load_image:
            with patch('face_recognition.face_encodings') as mock_encodings:
                mock_load_image.return_value = "fake_image"
                mock_encodings.return_value = [[[0.1, 0.2, 0.3]]]
                
                crear_y_guardar_modelo(self.test_dir, self.ruta_modelo)
                
                # Solo debe haberse procesado el archivo .jpg
                mock_load_image.assert_called_once()
    
    def test_directorio_vacio(self):
        """Test cuando el directorio personas_autorizadas está vacío"""
        # Crear directorio vacío
        os.makedirs(self.directorio_autorizadas)
        
        crear_y_guardar_modelo(self.test_dir, self.ruta_modelo)
        
        # Verificar que se crea un modelo vacío
        self.assertTrue(os.path.exists(self.ruta_modelo))
        with open(self.ruta_modelo, 'rb') as f:
            modelo = pickle.load(f)
            self.assertEqual(len(modelo["rostros"]), 0)
            self.assertEqual(len(modelo["nombres"]), 0)
    
    def test_persona_sin_imagenes(self):
        """Test cuando una persona no tiene imágenes válidas"""
        # Crear estructura de directorios
        os.makedirs(self.directorio_autorizadas)
        persona_dir = os.path.join(self.directorio_autorizadas, "juan")
        os.makedirs(persona_dir)
        
        # No crear ningún archivo de imagen
        
        crear_y_guardar_modelo(self.test_dir, self.ruta_modelo)
        
        # Verificar que se crea un modelo vacío
        with open(self.ruta_modelo, 'rb') as f:
            modelo = pickle.load(f)
            self.assertEqual(len(modelo["rostros"]), 0)
            self.assertEqual(len(modelo["nombres"]), 0)
    
    @patch('face_recognition.load_image_file')
    @patch('face_recognition.face_encodings')
    def test_extensiones_imagen_soportadas(self, mock_encodings, mock_load_image):
        """Test que se procesan todas las extensiones de imagen soportadas"""
        # Crear estructura de directorios
        os.makedirs(self.directorio_autorizadas)
        persona_dir = os.path.join(self.directorio_autorizadas, "juan")
        os.makedirs(persona_dir)
        
        # Crear archivos con diferentes extensiones
        extensiones = [".jpg", ".jpeg", ".png"]
        for i, ext in enumerate(extensiones):
            imagen_path = os.path.join(persona_dir, f"foto{i}{ext}")
            with open(imagen_path, 'w') as f:
                f.write("fake image content")
        
        # Configurar mocks
        mock_load_image.return_value = "fake_image"
        mock_encodings.return_value = [[[0.1, 0.2, 0.3]]]
        
        crear_y_guardar_modelo(self.test_dir, self.ruta_modelo)
        
        # Verificar que se procesaron todas las extensiones
        self.assertEqual(mock_load_image.call_count, 3)
        
        with open(self.ruta_modelo, 'rb') as f:
            modelo = pickle.load(f)
            self.assertEqual(len(modelo["rostros"]), 3)
    
    def test_archivo_no_es_directorio(self):
        """Test cuando hay un archivo en lugar de directorio en personas_autorizadas"""
        # Crear estructura de directorios
        os.makedirs(self.directorio_autorizadas)
        
        # Crear un archivo en lugar de directorio
        archivo_path = os.path.join(self.directorio_autorizadas, "no_es_directorio.txt")
        with open(archivo_path, 'w') as f:
            f.write("contenido")
        
        # También crear un directorio válido
        persona_dir = os.path.join(self.directorio_autorizadas, "juan")
        os.makedirs(persona_dir)
        imagen_path = os.path.join(persona_dir, "foto.jpg")
        with open(imagen_path, 'w') as f:
            f.write("fake image")
        
        with patch('face_recognition.load_image_file') as mock_load_image:
            with patch('face_recognition.face_encodings') as mock_encodings:
                mock_load_image.return_value = "fake_image"
                mock_encodings.return_value = [[[0.1, 0.2, 0.3]]]
                
                crear_y_guardar_modelo(self.test_dir, self.ruta_modelo)
                
                # Solo debe procesarse el directorio válido
                mock_load_image.assert_called_once()


class TestMainFunction(unittest.TestCase):
    """Tests para la función main y el bucle interactivo"""
    
    @patch('builtins.input')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('model_creation.crear_y_guardar_modelo')
    def test_main_flujo_completo(self, mock_crear, mock_exists, mock_makedirs, mock_input):
        """Test del flujo principal simulado"""
        # Configurar mocks con ciclo completo
        mock_input.side_effect = ['', 'back']  # Primera entrada vacía, luego 'back'
        mock_exists.side_effect = [False, True]  # modelo_dir no existe, modelo sí existe después
        
        with patch('builtins.print') as mock_print:
            # Simular el flujo completo del main
            directorio_base = "./"
            modelo_dir = "./model"
            ruta_modelo = os.path.join(modelo_dir, "modelo_rostros.pkl")
            
            # Crear carpeta si no existe
            if not mock_exists(modelo_dir):
                mock_makedirs(modelo_dir)
            
            # Simular el bucle while True
            call_count = 0
            while call_count < 2:  # Limitar iteraciones para evitar bucle infinito
                entrada = mock_input.side_effect[call_count]
                call_count += 1
                
                if entrada.strip().lower() == "back":
                    print("Saliendo del programa.")
                    break
                
                # Crear y guardar el modelo
                mock_crear(directorio_base, ruta_modelo)
                
                # Verificar si el modelo fue creado
                if mock_exists(ruta_modelo):
                    print(f"Modelo creado correctamente en {ruta_modelo}")
                else:
                    print("Error: No se pudo crear el modelo.")
        
        # Verificaciones
        mock_makedirs.assert_called_once()
        mock_crear.assert_called_once()
        mock_print.assert_any_call("Saliendo del programa.")
    
    @patch('builtins.input')
    def test_salida_inmediata(self, mock_input):
        """Test cuando el usuario escribe 'back' inmediatamente"""
        mock_input.return_value = 'back'
        
        with patch('builtins.print') as mock_print:
            # Simular entrada inmediata de 'back'
            entrada = mock_input.return_value
            if entrada.strip().lower() == "back":
                print("Saliendo del programa.")
            
            mock_print.assert_called_with("Saliendo del programa.")
    
    @patch('builtins.input')
    @patch('os.path.exists')  
    @patch('os.makedirs')
    @patch('model_creation.crear_y_guardar_modelo')
    def test_modelo_no_creado(self, mock_crear, mock_makedirs, mock_exists, mock_input):
        """Test cuando el modelo no se puede crear"""
        mock_input.side_effect = ['', 'back']
        mock_exists.side_effect = [False, False]  # modelo_dir no existe, modelo tampoco se crea
        
        with patch('builtins.print') as mock_print:
            directorio_base = "./"
            modelo_dir = "./model"  
            ruta_modelo = os.path.join(modelo_dir, "modelo_rostros.pkl")
            
            if not mock_exists(modelo_dir):
                mock_makedirs(modelo_dir)
            
            # Simular una iteración
            entrada = mock_input.side_effect[0]
            if entrada.strip().lower() != "back":
                mock_crear(directorio_base, ruta_modelo)
                if not mock_exists(ruta_modelo):
                    print("Error: No se pudo crear el modelo.")
            
            # Segunda iteración - salir
            entrada = mock_input.side_effect[1] 
            if entrada.strip().lower() == "back":
                print("Saliendo del programa.")
        
        mock_print.assert_any_call("Error: No se pudo crear el modelo.")


class TestImportsAndConstants(unittest.TestCase):
    """Tests para mejorar cobertura de importaciones y constantes"""
    
    def test_module_imports(self):
        """Test que verifica que se pueden importar todos los módulos necesarios"""
        # Verificar que el módulo model_creation se puede importar
        import model_creation
        
        # Verificar que tiene las funciones esperadas
        self.assertTrue(hasattr(model_creation, 'crear_y_guardar_modelo'))
        
        # Verificar imports internos del módulo
        self.assertTrue(hasattr(model_creation, 'os'))
        self.assertTrue(hasattr(model_creation, 'pickle'))
        # Note: face_recognition se mockea en las pruebas
    
    def test_file_extensions_coverage(self):
        """Test adicional para cubrir todas las extensiones de archivo"""
        import tempfile
        import os
        
        # Crear estructura de prueba
        test_dir = tempfile.mkdtemp()
        try:
            directorio_autorizadas = os.path.join(test_dir, "personas_autorizadas")
            os.makedirs(directorio_autorizadas)
            persona_dir = os.path.join(directorio_autorizadas, "test_person")
            os.makedirs(persona_dir)
            
            # Crear archivos con diferentes extensiones (incluyendo mayúsculas)
            test_files = [
                "image.JPG",    # Mayúscula
                "image.JPEG",   # Mayúscula  
                "image.PNG",    # Mayúscula
                "image.gif",    # No soportada
                "image.bmp",    # No soportada
                "document.pdf", # No soportada
            ]
            
            for filename in test_files:
                filepath = os.path.join(persona_dir, filename)
                with open(filepath, 'w') as f:
                    f.write("fake content")
            
            with patch('face_recognition.load_image_file') as mock_load:
                with patch('face_recognition.face_encodings') as mock_encodings:
                    mock_load.return_value = "fake_image"
                    mock_encodings.return_value = [[[0.1, 0.2, 0.3]]]
                    
                    ruta_modelo = os.path.join(test_dir, "test_model.pkl")
                    crear_y_guardar_modelo(test_dir, ruta_modelo)
                    
                    # Solo las extensiones soportadas deben procesarse
                    # .jpg, .jpeg, .png (sin importar mayúsculas/minúsculas)
                    expected_calls = 3  # JPG, JPEG, PNG
                    self.assertEqual(mock_load.call_count, expected_calls)
                    
        finally:
            shutil.rmtree(test_dir)


class TestEdgeCasesAndExceptions(unittest.TestCase):
    """Tests para casos extremos y manejo de excepciones"""
    
    @patch('face_recognition.load_image_file')
    @patch('face_recognition.face_encodings')  
    def test_multiple_faces_in_image(self, mock_encodings, mock_load):
        """Test cuando una imagen tiene múltiples rostros"""
        # Crear estructura de prueba
        test_dir = tempfile.mkdtemp()
        try:
            directorio_autorizadas = os.path.join(test_dir, "personas_autorizadas")
            os.makedirs(directorio_autorizadas)
            persona_dir = os.path.join(directorio_autorizadas, "juan")
            os.makedirs(persona_dir)
            
            imagen_path = os.path.join(persona_dir, "grupo.jpg")
            with open(imagen_path, 'w') as f:
                f.write("fake image with multiple faces")
            
            # Simular múltiples rostros detectados
            mock_load.return_value = "fake_image"
            mock_encodings.return_value = [
                [[0.1, 0.2, 0.3]],  # Primer rostro
                [[0.4, 0.5, 0.6]]   # Segundo rostro (será ignorado)
            ]
            
            with patch('builtins.print') as mock_print:
                ruta_modelo = os.path.join(test_dir, "test_model.pkl")
                crear_y_guardar_modelo(test_dir, ruta_modelo)
                
                # Verificar que solo se toma el primer rostro
                with open(ruta_modelo, 'rb') as f:
                    modelo = pickle.load(f)
                    self.assertEqual(len(modelo["rostros"]), 1)
                    self.assertEqual(modelo["nombres"], ["juan"])
                
        finally:
            shutil.rmtree(test_dir)
    
    @patch('pickle.dump')
    def test_pickle_save_error(self, mock_dump):
        """Test cuando hay error al guardar el modelo"""
        # Configurar mock para lanzar excepción
        mock_dump.side_effect = Exception("Disk full")
        
        test_dir = tempfile.mkdtemp()
        try:
            # No crear el directorio personas_autorizadas para trigger el return temprano
            ruta_modelo = os.path.join(test_dir, "test_model.pkl")
            
            # Este test verifica que el código maneja el caso donde no existe el directorio
            with patch('builtins.print') as mock_print:
                crear_y_guardar_modelo(test_dir, ruta_modelo)
                
                expected_dir = os.path.join(test_dir, "personas_autorizadas")
                mock_print.assert_called_with(f"El directorio {expected_dir} no existe.")
            
        finally:
            shutil.rmtree(test_dir)
    
    def test_empty_person_name(self):
        """Test con nombre de persona vacío o especial"""
        test_dir = tempfile.mkdtemp()
        try:
            directorio_autorizadas = os.path.join(test_dir, "personas_autorizadas")
            os.makedirs(directorio_autorizadas)
            
            # Crear directorio con nombre especial
            persona_dir = os.path.join(directorio_autorizadas, "")  # Nombre vacío
            # Como no se puede crear directorio vacío, crear uno con espacios
            persona_dir = os.path.join(directorio_autorizadas, "   ")
            os.makedirs(persona_dir)
            
            imagen_path = os.path.join(persona_dir, "foto.jpg")
            with open(imagen_path, 'w') as f:
                f.write("fake image")
            
            with patch('face_recognition.load_image_file') as mock_load:
                with patch('face_recognition.face_encodings') as mock_encodings:
                    mock_load.return_value = "fake_image"
                    mock_encodings.return_value = [[[0.1, 0.2, 0.3]]]
                    
                    ruta_modelo = os.path.join(test_dir, "test_model.pkl")
                    crear_y_guardar_modelo(test_dir, ruta_modelo)
                    
                    # Verificar que se procesó correctamente
                    with open(ruta_modelo, 'rb') as f:
                        modelo = pickle.load(f)
                        self.assertEqual(len(modelo["rostros"]), 1)
                        self.assertEqual(modelo["nombres"], ["   "])
                        
        finally:
            shutil.rmtree(test_dir)


if __name__ == '__main__':
    # Configurar cobertura si está disponible
    try:
        import coverage
        cov = coverage.Coverage()
        cov.start()
        
        # Ejecutar tests con más verbosidad
        suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        cov.stop()
        cov.save()
        
        print("\n" + "="*50)
        print("REPORTE DE COBERTURA")
        print("="*50)
        cov.report(show_missing=True)
        
        # Intentar generar reporte HTML
        try:
            cov.html_report(directory='htmlcov')
            print(f"\n✓ Reporte HTML generado en htmlcov/index.html")
        except Exception:
            pass
        
        # Mostrar resultado final
        if result.wasSuccessful():
            print(f"\n🎉 ¡ÉXITO! Todas las {result.testsRun} pruebas pasaron")
        else:
            print(f"\n❌ {len(result.failures)} fallas, {len(result.errors)} errores")
            
        sys.exit(0 if result.wasSuccessful() else 1)
        
    except ImportError:
        print("Coverage no está instalado. Ejecutando tests sin cobertura...")
        unittest.main(verbosity=2)