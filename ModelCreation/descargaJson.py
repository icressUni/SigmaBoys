import psycopg2
import json
from psycopg2.extras import RealDictCursor
import pandas as pd
from datetime import datetime, date

# Configuración de la base de datos
DATABASE_URL = "postgresql://alumnos_db_owner:npg_S7BvNrnaRLy5@ep-rapid-glitter-aaxbrr0d-pooler.westus3.azure.neon.tech/alumnos_db?sslmode=require&channel_binding=require"

def conectar_db():
    """Establece conexión con la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def obtener_datos_alumnos():
    """Obtiene todos los datos de la tabla alumnos"""
    conn = conectar_db()
    if not conn:
        return None
    
    try:
        # Usar RealDictCursor para obtener resultados como diccionarios
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM alumnos")
            datos = cursor.fetchall()
            return datos
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return None
    finally:
        conn.close()

def convertir_a_json_serializable(obj):
    """Convierte objetos no serializables a JSON"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: convertir_a_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convertir_a_json_serializable(item) for item in obj]
    else:
        return obj

def visualizar_json_bonito(datos):
    """Visualiza los datos en formato JSON bonito"""
    if not datos:
        print("No se encontraron datos")
        return
    
    # Convertir a formato serializable
    datos_serializables = convertir_a_json_serializable(datos)
    
    # Convertir a JSON con formato bonito
    json_bonito = json.dumps(datos_serializables, indent=2, ensure_ascii=False)
    
    print("=== DATOS DE LA TABLA ALUMNOS ===")
    print(json_bonito)
    
    # También mostrar estadísticas básicas
    print(f"\n=== ESTADÍSTICAS ===")
    print(f"Total de registros: {len(datos)}")
    
    if datos:
        print(f"Campos disponibles: {list(datos[0].keys())}")

def obtener_estructura_tabla():
    """Obtiene la estructura de la tabla alumnos"""
    conn = conectar_db()
    if not conn:
        return None
    
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = 'alumnos'
                ORDER BY ordinal_position
            """)
            estructura = cursor.fetchall()
            return estructura
    except Exception as e:
        print(f"Error al obtener estructura: {e}")
        return None
    finally:
        conn.close()

def visualizar_estructura():
    """Visualiza la estructura de la tabla"""
    estructura = obtener_estructura_tabla()
    if estructura:
        print("\n=== ESTRUCTURA DE LA TABLA ALUMNOS ===")
        for columna in estructura:
            print(f"- {columna['column_name']}: {columna['data_type']} "
                  f"(Nullable: {columna['is_nullable']}, Default: {columna['column_default']})")

def guardar_json_archivo(datos, nombre_archivo="alumnos_data.json"):
    """Guarda los datos en un archivo JSON"""
    if not datos:
        print("No hay datos para guardar")
        return
    
    try:
        datos_serializables = convertir_a_json_serializable(datos)
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos_serializables, f, indent=2, ensure_ascii=False)
        print(f"\nDatos guardados en: {nombre_archivo}")
    except Exception as e:
        print(f"Error al guardar archivo: {e}")

def main():
    """Función principal"""
    print("Conectando a la base de datos...")
    
    # Obtener y visualizar estructura
    visualizar_estructura()
    
    # Obtener datos
    datos = obtener_datos_alumnos()
    
    if datos:
        # Visualizar JSON
        visualizar_json_bonito(datos)
        
        # Guardar en archivo
        guardar_json_archivo(datos)
        
        # Opción adicional: convertir a DataFrame de pandas para análisis
        try:
            df = pd.DataFrame(datos)
            print("\n=== VISTA PREVIA CON PANDAS ===")
            print(df.head())
            print(f"\nForma del DataFrame: {df.shape}")
        except Exception as e:
            print(f"Error al crear DataFrame: {e}")
    else:
        print("No se pudieron obtener los datos")

if __name__ == "__main__":
    main()