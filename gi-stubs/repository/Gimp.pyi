"""
GIMP 3.0 Module Stub
"""

from typing import Any, List, Tuple, Optional, Union, Callable
from enum import IntEnum


class ImageType(IntEnum):
    """Image types"""
    RGB = 0
    GRAY = 1
    INDEXED = 2

class LayerMode(IntEnum):
    """Layer blend modes"""
    NORMAL_MODE = 0
    MULTIPLY_MODE = 1
    SCREEN_MODE = 2
    OVERLAY_MODE = 3

class FillType(IntEnum):
    """Fill types"""
    WHITE_FILL = 0
    BLACK_FILL = 1
    TRANSPARENT_FILL = 2
    FOREGROUND_FILL = 3
    BACKGROUND_FILL = 4

class PDBProcType(IntEnum):
    """Procedure database procedure types"""
    PLUGIN = 1
    EXTENSION = 2
    TEMPORARY = 3

class PDBStatusType(IntEnum):
    """Procedure database status types"""
    SUCCESS = 0
    CALLING_ERROR = 1
    EXECUTION_ERROR = 2
    CANCEL = 3

class RunMode(IntEnum):
    """Plugin run modes"""
    INTERACTIVE = 0
    NONINTERACTIVE = 1
    WITH_LAST_VALS = 2

class PlugIn:
    """Base class for GIMP plugins"""
    def do_query_procedures(self) -> List[str]: ...
    def do_set_i18n(self, proc_name: str) -> bool: ...
    def do_create_procedure(self, name: str) -> 'Procedure': ...
    def run(self, procedure: 'Procedure', run_mode: RunMode, 
            image: 'Image', drawable: 'Drawable', *args, **kwargs) -> PDBStatusType: ...

class Image:
    """GIMP Image object"""
    width: int
    height: int
    def get_selection(self) -> 'Selection': ...
    def get_progress(self) -> Any: ...
    def add_layer(self, layer: 'Layer', position: int) -> None: ...
    @staticmethod
    def new(width: int, height: int, image_type: ImageType) -> 'Image': ...

class Selection:
    """GIMP Selection object"""
    def bounds(self) -> Tuple[bool, int, int, int, int]: ...
    def get_region(self) -> Any: ...

class Drawable:
    """GIMP Drawable object"""
    pass

class Layer(Drawable):
    """GIMP Layer object"""
    def set_name(self, name: str) -> None: ...
    def fill(self, fill_type: FillType) -> None: ...
    @staticmethod
    def new(image: 'Image', name: str, width: int, height: int, 
            layer_type: ImageType, opacity: float, mode: LayerMode) -> 'Layer': ...

class Procedure:
    """GIMP Procedure object"""
    def set_image_types(self, types: str) -> None: ...
    def set_menu_label(self, label: str) -> None: ...
    def add_menu_path(self, path: str) -> None: ...
    def set_documentation(self, blurb: str, help: str, name: str) -> None: ...
    def set_attribution(self, author: str, copyright: str, date: str) -> None: ...

class ImageProcedure(Procedure):
    """GIMP Image Procedure object"""
    @staticmethod
    def new(plugin: 'PlugIn', name: str, proc_type: PDBProcType, 
            run_func: Callable, data: Any) -> 'ImageProcedure': ...

class RGB:
    """RGB color class"""
    def __init__(self, r: int, g: int, b: int): ...

# Static functions
def message(message: str) -> None: ...
def file_save(image: Image, drawables: List[Drawable], filename: str, raw_filename: str) -> None: ...
def file_load_layer(image: Image, filename: str) -> Layer: ...
def progress_init(progress: Any, message: str) -> None: ...
def progress_update(progress: Any, percentage: float) -> None: ...
def progress_set_text(progress: Any, message: str) -> None: ...
def progress_end(progress: Any) -> None: ...
def main(plugin_type: Any, argv: List[str]) -> None: ...
