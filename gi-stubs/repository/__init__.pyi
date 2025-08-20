"""
GIMP 3.0 Type Stubs for gi.repository
"""

from typing import Any, List, Tuple, Optional, Union, Callable
from gi.repository import GObject
from enum import IntEnum


class Gimp:
    """GIMP 3.0 API namespace"""

    Channel = None
    ImageBaseType = None
    ChannelOps = None

    class ImageType(IntEnum):
        """Image types"""
        RGB_IMAGE = None
        GRAY_IMAGE = None

    class LayerMode(IntEnum):
        """Layer blend modes"""
        NORMAL = None
        NORMAL_MODE = 0
        MULTIPLY_MODE = 1
        SCREEN_MODE = 2
        OVERLAY_MODE = 3

    class FillType(IntEnum):
        """Fill types"""
        BACKGROUND = None
        FOREGROUND = None
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

    class PlugIn(GObject.Object):
        """Base class for GIMP plugins"""
        def do_query_procedures(self) -> List[str]: ...
        def do_set_i18n(self, proc_name: str) -> bool: ...
        def do_create_procedure(self, name: str) -> 'Gimp.Procedure': ...
        def run(self, procedure: 'Gimp.Procedure', run_mode: 'Gimp.RunMode',
                image: 'Gimp.Image', drawable: 'Gimp.Drawable', *args, **kwargs) -> 'Gimp.PDBStatusType': ...

    class Image(GObject.Object):
        """GIMP Image object"""
        width: int
        height: int
        def get_selection(self) -> 'Gimp.Selection': ...
        def get_progress(self) -> Any: ...
        def add_layer(self, layer: 'Gimp.Layer', position: int) -> None: ...
        @staticmethod
        def new(width: int, height: int, image_type: 'Gimp.ImageType') -> 'Gimp.Image': ...

        def delete(self):
            pass

        def select_rectangle(self, REPLACE, x1, y1, param, param1):
            pass

        def get_height(self):
            pass

        def get_width(self):
            pass

        def insert_layer(self, mask_layer, param, param1):
            pass

        def select_item(self, REPLACE, selection):
            pass

        def select_item(self, REPLACE, selection):
            pass

        def get_selected_layers(self):
            pass

        def flatten(self):
            pass

    class Selection(GObject.Object):
        """GIMP Selection object"""
        @staticmethod
        def bounds(image: 'Gimp.Image') -> Tuple[bool, bool, int, int, int, int]: ...
        def get_region(self) -> Any: ...

        @classmethod
        def none(cls, mask_image):
            pass

        def save(self, image):
            pass

    class Drawable(GObject.Object):
        """GIMP Drawable object"""
        pass

        def edit_bucket_fill(self, FOREGROUND, param, param1):
            pass

    class Layer(Drawable):
        """GIMP Layer object"""
        def set_name(self, name: str) -> None: ...
        def fill(self, fill_type: 'Gimp.FillType') -> None: ...
        @staticmethod
        def new(image: 'Gimp.Image', name: str, width: int, height: int,
                layer_type: 'Gimp.ImageType', opacity: float, mode: 'Gimp.LayerMode') -> 'Gimp.Layer': ...

    class Procedure(GObject.Object):
        """GIMP Procedure object"""
        def set_image_types(self, types: str) -> None: ...
        def set_menu_label(self, label: str) -> None: ...
        def add_menu_path(self, path: str) -> None: ...
        def set_documentation(self, blurb: str, help: str, name: str) -> None: ...
        def set_attribution(self, author: str, copyright: str, date: str) -> None: ...

    class ImageProcedure(Procedure):
        """GIMP Image Procedure object"""
        @staticmethod
        def new(plugin: 'Gimp.PlugIn', name: str, proc_type: 'Gimp.PDBProcType',
                run_func: Callable, data: Any) -> 'Gimp.ImageProcedure': ...

    class RGB:
        """RGB color class"""
        def __init__(self, r: int, g: int, b: int): ...
        r: int
        g: int
        b: int

    # Static methods
    @staticmethod
    def message(message: str) -> None: ...

    @staticmethod
    def file_save(run_mode: 'Gimp.RunMode', image: 'Gimp.Image', file: 'Gio.File', options: Optional['Gimp.ExportOptions']) -> None: ...

    @staticmethod
    def file_load_layer(run_mode: 'Gimp.RunMode', image: 'Gimp.Image', file: 'Gio.File') -> 'Gimp.Layer': ...

    @staticmethod
    def progress_init(message: str) -> None: ...

    @staticmethod
    def progress_update(percentage: float) -> None: ...

    @staticmethod
    def progress_set_text(message: str) -> None: ...

    @staticmethod
    def progress_end() -> None: ...

    @staticmethod
    def main(plugin_type: Any, argv: List[str]) -> None: ...

    @classmethod
    def context_set_foreground(cls, param):
        pass

    @classmethod
    def context_push(cls):
        pass

    @classmethod
    def context_pop(cls):
        pass

    @classmethod
    def context_set_background(cls, param):
        pass


class GObject:
    """GObject base class"""
    class Object:
        """Base GObject object"""
        pass


class Gio:
    File = None


class Gegl:
    Rectangle = None
    Buffer = None
    Color = None