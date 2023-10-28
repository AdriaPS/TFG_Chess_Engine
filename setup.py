# setup.py
import sys
from cx_Freeze import setup, Executable

# Ruta del archivo principal de tu juego
main_file = 'chess_engine.py'


# Otras opciones de configuración
options = {
    'build_exe': {
        'includes': ['pygame',  'random', 'chess', 'sys', 'tkinter', 'game_controller', 'button', 'tkinter.messagebox',
                     'pygetwindow'],  # Incluir todas las dependencias de PyGame
        'include_files': ['images']  # Incluir otros archivos o carpetas necesarios
    }
}

base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name='Chess Engine',
    version='1.0',
    description='This is a Chess Game',
    options=options,
    executables=[Executable("chess_engine.py", base=base)],
)
