import os
import json
import shutil
from PIL import Image, ImageFile
import glob

train_dir = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/train"
val_dir = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/valid"
test_dir = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/test"

train_annotations = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/train/_annotations.coco.json"
val_annotations = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/valid/_annotations.coco.json"
test_annotations = "/home/mixup/Documentos/Emociones Dataset/Emociones.v4-80x80.coco/test/_annotations.coco.json"

def is_image_corrupted(file_path):
    """
    Verifica si una imagen está corrupta intentando abrirla y cargarla completamente.
    """
    try:
        with Image.open(file_path) as img:
            # Intentar cargar la imagen completamente
            img.verify()
        
        # Verificar una segunda vez abriendo y convirtiendo
        with Image.open(file_path) as img:
            img.load()
            # Intentar obtener información básica
            _ = img.size
            _ = img.mode
        
        return False  # No está corrupta
    except Exception as e:
        print(f"Imagen corrupta detectada {os.path.basename(file_path)}: {str(e)}")
        return True  # Está corrupta

def fix_corrupted_jpg(file_path):
    """
    Intenta reparar una imagen JPG corrupta usando diferentes métodos.
    """
    print(f"Intentando reparar imagen corrupta: {os.path.basename(file_path)}")
    
    backup_path = file_path + ".backup"
    
    try:
        # Hacer backup del archivo original
        import shutil
        shutil.copy2(file_path, backup_path)
        
        # Método 1: Intentar abrir con PIL y guardar de nuevo
        try:
            with Image.open(file_path) as img:
                img.load()
                # Si llegamos aquí, la imagen se puede cargar parcialmente
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                img.save(file_path, 'JPEG', quality=95)
                print(f"Reparada exitosamente: {os.path.basename(file_path)}")
                
                # Eliminar backup si la reparación fue exitosa
                os.remove(backup_path)
                return True
        except Exception:
            pass
        
        # Método 2: Usar ImageFile para permitir imágenes truncadas
        from PIL import ImageFile
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        
        try:
            with Image.open(file_path) as img:
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                img.save(file_path, 'JPEG', quality=95)
                print(f"Reparada con método truncado: {os.path.basename(file_path)}")
                
                # Eliminar backup si la reparación fue exitosa
                os.remove(backup_path)
                return True
        except Exception:
            pass
        
        # Si no se pudo reparar, restaurar el backup y reportar error
        shutil.move(backup_path, file_path)
        print(f"No se pudo reparar: {os.path.basename(file_path)}")
        return False
        
    except Exception as e:
        print(f"Error al intentar reparar {file_path}: {str(e)}")
        # Restaurar backup si existe
        if os.path.exists(backup_path):
            try:
                shutil.move(backup_path, file_path)
            except:
                pass
        return False

def convert_images_to_jpg(directory):
    """
    Convierte todas las imágenes en el directorio especificado a formato JPG,
    elimina los archivos originales si no son JPG, y repara JPG corruptos.
    Si no se puede reparar una imagen corrupta, la elimina.
    """
    print(f"Procesando directorio: {directory}")
    
    # Primero, verificar y reparar archivos JPG existentes
    jpg_files = glob.glob(os.path.join(directory, "*.jpg"))
    jpg_files.extend(glob.glob(os.path.join(directory, "*.JPG")))
    jpg_files.extend(glob.glob(os.path.join(directory, "*.jpeg")))
    jpg_files.extend(glob.glob(os.path.join(directory, "*.JPEG")))
    
    corrupted_count = 0
    repaired_count = 0
    deleted_files = []  # Lista de archivos eliminados por corrupción
    
    print(f"Verificando {len(jpg_files)} archivos JPG existentes...")
    for jpg_file in jpg_files:
        if is_image_corrupted(jpg_file):
            corrupted_count += 1
            if fix_corrupted_jpg(jpg_file):
                repaired_count += 1
            else:
                # Si no se pudo reparar, eliminar el archivo
                try:
                    os.remove(jpg_file)
                    deleted_files.append(os.path.basename(jpg_file))
                    print(f"Imagen corrupta eliminada: {os.path.basename(jpg_file)}")
                except Exception as e:
                    print(f"Error al eliminar imagen corrupta {jpg_file}: {str(e)}")
    
    if corrupted_count > 0:
        print(f"Encontradas {corrupted_count} imágenes JPG corruptas, reparadas: {repaired_count}, eliminadas: {len(deleted_files)}")
    
    # Buscar todos los archivos de imagen (excluyendo archivos JSON y JPG ya procesados)
    image_extensions = ['*.png', '*.bmp', '*.tiff', '*.tif', '*.webp', '*.gif']
    
    converted_count = 0
    
    for extension in image_extensions:
        # Buscar archivos con esta extensión
        files = glob.glob(os.path.join(directory, extension))
        files.extend(glob.glob(os.path.join(directory, extension.upper())))
        
        for file_path in files:
            try:
                # Obtener el nombre del archivo sin extensión
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                new_file_path = os.path.join(directory, f"{base_name}.jpg")
                
                # Si ya existe un archivo JPG con el mismo nombre, saltar
                if os.path.exists(new_file_path) and file_path != new_file_path:
                    print(f"Ya existe {new_file_path}, saltando...")
                    continue
                
                # Abrir y convertir la imagen
                with Image.open(file_path) as img:
                    # Convertir a RGB si es necesario (para PNG con transparencia, etc.)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        # Crear fondo blanco para imágenes con transparencia
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Guardar como JPG
                    img.save(new_file_path, 'JPEG', quality=95)
                    
                    print(f"Convertido: {os.path.basename(file_path)} -> {os.path.basename(new_file_path)}")
                    
                    # Eliminar el archivo original si es diferente del nuevo
                    if file_path != new_file_path:
                        os.remove(file_path)
                        print(f"Eliminado archivo original: {os.path.basename(file_path)}")
                    
                    converted_count += 1
                    
            except Exception as e:
                print(f"Error al convertir {file_path}: {str(e)}")
    
    print(f"Convertidas {converted_count} imágenes en {directory}")
    return converted_count, corrupted_count, repaired_count, deleted_files

def remove_annotations_for_deleted_images(annotations_file, deleted_files):
    """
    Elimina las anotaciones correspondientes a las imágenes que fueron eliminadas por corrupción.
    """
    if not deleted_files or not os.path.exists(annotations_file):
        return 0
    
    print(f"Eliminando anotaciones para {len(deleted_files)} imágenes eliminadas en: {annotations_file}")
    
    try:
        # Leer el archivo de anotaciones
        with open(annotations_file, 'r') as f:
            annotations = json.load(f)
        
        # Crear conjuntos para búsqueda rápida
        deleted_set = set(deleted_files)
        
        # Encontrar IDs de imágenes a eliminar
        images_to_remove = []
        image_ids_to_remove = set()
        
        for i, image in enumerate(annotations.get('images', [])):
            filename = image.get('file_name', '')
            if filename in deleted_set:
                images_to_remove.append(i)
                image_ids_to_remove.add(image.get('id'))
        
        # Eliminar imágenes de la lista (en orden inverso para no afectar índices)
        for i in reversed(images_to_remove):
            annotations['images'].pop(i)
        
        # Eliminar anotaciones asociadas a esas imágenes
        annotations_to_remove = []
        for i, annotation in enumerate(annotations.get('annotations', [])):
            if annotation.get('image_id') in image_ids_to_remove:
                annotations_to_remove.append(i)
        
        # Eliminar anotaciones (en orden inverso)
        for i in reversed(annotations_to_remove):
            annotations['annotations'].pop(i)
        
        # Guardar las anotaciones actualizadas
        with open(annotations_file, 'w') as f:
            json.dump(annotations, f, indent=2)
        
        removed_count = len(images_to_remove)
        print(f"Eliminadas {removed_count} imágenes y {len(annotations_to_remove)} anotaciones del archivo COCO")
        return removed_count
        
    except Exception as e:
        print(f"Error al eliminar anotaciones en {annotations_file}: {str(e)}")
        return 0

def update_annotations_file_extensions(annotations_file):
    """
    Actualiza las referencias de archivos en las anotaciones COCO para usar extensión .jpg
    """
    if not os.path.exists(annotations_file):
        print(f"Archivo de anotaciones no encontrado: {annotations_file}")
        return
    
    print(f"Actualizando anotaciones: {annotations_file}")
    
    try:
        # Leer el archivo de anotaciones
        with open(annotations_file, 'r') as f:
            annotations = json.load(f)
        
        # Actualizar las referencias de archivos de imagen
        updated_count = 0
        for image in annotations.get('images', []):
            original_filename = image.get('file_name', '')
            if original_filename:
                # Cambiar la extensión a .jpg
                base_name = os.path.splitext(original_filename)[0]
                new_filename = f"{base_name}.jpg"
                
                if original_filename != new_filename:
                    image['file_name'] = new_filename
                    updated_count += 1
        
        # Guardar las anotaciones actualizadas
        with open(annotations_file, 'w') as f:
            json.dump(annotations, f, indent=2)
        
        print(f"Actualizadas {updated_count} referencias de archivos en las anotaciones")
        
    except Exception as e:
        print(f"Error al actualizar anotaciones {annotations_file}: {str(e)}")

def main():
    """
    Función principal que convierte todas las imágenes a JPG, repara archivos corruptos
    y elimina imágenes irrecuperables junto con sus anotaciones.
    """
    directories = [train_dir, val_dir, test_dir]
    annotation_files = [train_annotations, val_annotations, test_annotations]
    
    total_converted = 0
    total_corrupted = 0
    total_repaired = 0
    all_deleted_files = []
    
    # Convertir imágenes en cada directorio
    directory_deleted_files = {}
    for i, directory in enumerate(directories):
        if os.path.exists(directory):
            converted, corrupted, repaired, deleted_files = convert_images_to_jpg(directory)
            total_converted += converted
            total_corrupted += corrupted
            total_repaired += repaired
            directory_deleted_files[annotation_files[i]] = deleted_files
            all_deleted_files.extend(deleted_files)
        else:
            print(f"Directorio no encontrado: {directory}")
            directory_deleted_files[annotation_files[i]] = []
    
    print(f"\n=== RESUMEN ===")
    print(f"Total de imágenes convertidas: {total_converted}")
    print(f"Total de imágenes JPG corruptas encontradas: {total_corrupted}")
    print(f"Total de imágenes JPG reparadas: {total_repaired}")
    print(f"Total de imágenes eliminadas por corrupción: {len(all_deleted_files)}")
    
    # Actualizar archivos de anotaciones
    print("\nActualizando archivos de anotaciones...")
    total_annotations_removed = 0
    
    for annotation_file in annotation_files:
        # Primero eliminar anotaciones de imágenes eliminadas
        deleted_files_for_this_annotation = directory_deleted_files.get(annotation_file, [])
        removed_count = remove_annotations_for_deleted_images(annotation_file, deleted_files_for_this_annotation)
        total_annotations_removed += removed_count
        
        # Luego actualizar extensiones de archivos
        update_annotations_file_extensions(annotation_file)
    
    if total_annotations_removed > 0:
        print(f"\nTotal de anotaciones eliminadas: {total_annotations_removed}")
    
    print("\n¡Conversión, reparación y limpieza completada!")

if __name__ == "__main__":
    main()