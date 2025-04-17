import tkinter as tk
from tkinter import filedialog
import threading
import queue
import os
import time

class FileExplorer:
    """Maneja diálogos de archivo en un hilo separado para evitar conflictos con Pygame"""
    
    @staticmethod
    def save_file_dialog(initial_dir=None, callback=None):
        """
        Muestra un diálogo para guardar archivo en un hilo separado
        
        Args:
            initial_dir: Directorio inicial
            callback: Función a llamar con la ruta del archivo seleccionado
        """
        if initial_dir is None:
            initial_dir = os.getcwd()
            
        # Cola para comunicar el resultado entre hilos
        result_queue = queue.Queue()
        
        # Función que se ejecutará en el hilo separado
        def show_dialog():
            try:
                # Inicializar tkinter
                root = tk.Tk()
                root.withdraw()
                
                # Hacer que el diálogo esté en primer plano
                root.attributes('-topmost', True)
                
                # Pequeña pausa para estabilizar
                time.sleep(0.1)
                
                # Mostrar diálogo para guardar
                file_path = filedialog.asksaveasfilename(
                    parent=root,
                    initialdir=initial_dir,
                    title="Save File",
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                )
                
                # Poner el resultado en la cola
                result_queue.put(file_path)
                
                # Limpiar tkinter
                root.destroy()
            except Exception as e:
                # En caso de error, poner None en la cola
                print(f"Error en diálogo de guardar: {e}")
                result_queue.put(None)
        
        # Crear y ejecutar el hilo
        dialog_thread = threading.Thread(target=show_dialog)
        dialog_thread.daemon = True  # El hilo se cerrará cuando el programa principal termine
        dialog_thread.start()
        
        # Si se proporcionó un callback, configurar un verificador periódico
        if callback:
            def check_result():
                try:
                    # Verificar si hay resultado disponible (no bloqueante)
                    file_path = result_queue.get_nowait()
                    # Llamar al callback con el resultado
                    callback(file_path)
                except queue.Empty:
                    # Si la cola está vacía, verificar nuevamente en 100ms
                    root = tk.Tk()
                    root.withdraw()
                    root.after(100, check_result)
                    root.mainloop()
            
            # Iniciar verificación
            check_thread = threading.Thread(target=check_result)
            check_thread.daemon = True
            check_thread.start()
            
            return None
        else:
            # Si no hay callback, esperar y devolver el resultado (bloqueante)
            dialog_thread.join()
            return result_queue.get()
    
    @staticmethod
    def open_file_dialog(initial_dir=None, callback=None):
        """
        Muestra un diálogo para abrir archivo en un hilo separado
        
        Args:
            initial_dir: Directorio inicial
            callback: Función a llamar con la ruta del archivo seleccionado
        """
        if initial_dir is None:
            initial_dir = os.getcwd()
            
        # Cola para comunicar el resultado entre hilos
        result_queue = queue.Queue()
        
        # Función que se ejecutará en el hilo separado
        def show_dialog():
            try:
                # Inicializar tkinter
                root = tk.Tk()
                root.withdraw()
                
                # Hacer que el diálogo esté en primer plano
                root.attributes('-topmost', True)
                
                # Pequeña pausa para estabilizar
                time.sleep(0.1)
                
                # Mostrar diálogo para abrir
                file_path = filedialog.askopenfilename(
                    parent=root,
                    initialdir=initial_dir,
                    title="Open File",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                )
                
                # Poner el resultado en la cola
                result_queue.put(file_path)
                
                # Limpiar tkinter
                root.destroy()
            except Exception as e:
                # En caso de error, poner None en la cola
                print(f"Error en diálogo de abrir: {e}")
                result_queue.put(None)
        
        # Crear y ejecutar el hilo
        dialog_thread = threading.Thread(target=show_dialog)
        dialog_thread.daemon = True  # El hilo se cerrará cuando el programa principal termine
        dialog_thread.start()
        
        # Si se proporcionó un callback, configurar un verificador periódico
        if callback:
            def check_result():
                try:
                    # Verificar si hay resultado disponible (no bloqueante)
                    file_path = result_queue.get_nowait()
                    # Llamar al callback con el resultado
                    callback(file_path)
                except queue.Empty:
                    # Si la cola está vacía, verificar nuevamente en 100ms
                    root = tk.Tk()
                    root.withdraw()
                    root.after(100, check_result)
                    root.mainloop()
            
            # Iniciar verificación
            check_thread = threading.Thread(target=check_result)
            check_thread.daemon = True
            check_thread.start()
            
            return None
        else:
            # Si no hay callback, esperar y devolver el resultado (bloqueante)
            dialog_thread.join()
            return result_queue.get()