# GIMP 3.0 Type Stubs for better IDE support
from typing import Any, List, Tuple, Optional, Union
from gi.repository import GObject

class Gimp:
    class PlugIn(GObject.Object):
        def do_query_procedures(self) -> List[str]: ...
        def do_set_i18n(self, proc_name: str) -> bool: ...
        def do_create_procedure(self, name: str) -> 'Gimp.Procedure': ...
        def run(self, procedure: 'Gimp.Procedure', run_mode: 'Gimp.RunMode',
                image: 'Gimp.Image', drawable: 'Gimp.Drawable', *args, **kwargs) -> 'Gimp.PDBStatusType': ...

    class Image(GObject.Object):
        width: int
        height: int
        def get_selection(self) -> 'Gimp.Selection': ...
        def get_progress(self) -> Any: ...
        def add_layer(self, layer: 'Gimp.Layer', position: int) -> None: ...
        @staticmethod
        def new(width: int, height: int, image_type: 'Gimp.ImageType') -> 'Gimp.Image': ...

    class Selection(GObject.Object):
        def bounds(self) -> Tuple[bool, int, int, int, int]: ...
        def get_region(self) -> Any: ...

    class Layer(GObject.Object):
        def set_name(self, name: str) -> None: ...
        def fill(self, fill_type: 'Gimp.FillType') -> None: ...
        @staticmethod
        def new(image: 'Gimp.Image', name: str, width: int, height: int,
                layer_type: 'Gimp.ImageType', opacity: float, mode: 'Gimp.LayerMode') -> 'Gimp.Layer': ...

    class Drawable(GObject.Object): ...

    class Procedure(GObject.Object):
        def set_image_types(self, types: str) -> None: ...
        def set_menu_label(self, label: str) -> None: ...
        def add_menu_path(self, path: str) -> None: ...
        def set_documentation(self, blurb: str, help: str, name: str) -> None: ...
        def set_attribution(self, author: str, copyright: str, date: str) -> None: ...

    class ImageProcedure(Procedure):
        @staticmethod
        def new(plugin: 'Gimp.PlugIn', name: str, proc_type: 'Gimp.PDBProcType',
                run_func: Any, data: Any) -> 'Gimp.ImageProcedure': ...

    class PDBProcType:
        PLUGIN: int

    class PDBStatusType:
        SUCCESS: int
        CALLING_ERROR: int
        EXECUTION_ERROR: int
        CANCEL: int

    class RunMode:
        INTERACTIVE: int
        NONINTERACTIVE: int
        WITH_LAST_VALS: int

    class ImageType:
        RGB: int
        GRAY: int
        INDEXED: int

    class LayerMode:
        NORMAL_MODE: int

    class FillType:
        WHITE_FILL: int
        BLACK_FILL: int
        TRANSPARENT_FILL: int

    class RGB:
        def __init__(self, r: int, g: int, b: int): ...

    @staticmethod
    def message(message: str) -> None: ...

    @staticmethod
    def file_save(image: 'Gimp.Image', drawables: List['Gimp.Drawable'],
                  filename: str, raw_filename: str) -> None: ...

    @staticmethod
    def file_load_layer(image: 'Gimp.Image', filename: str) -> 'Gimp.Layer': ...

    @staticmethod
    def progress_init(progress: Any, message: str) -> None: ...

    @staticmethod
    def progress_update(progress: Any, percentage: float) -> None: ...

    @staticmethod
    def progress_set_text(progress: Any, message: str) -> None: ...

    @staticmethod
    def progress_end(progress: Any) -> None: ...

    @staticmethod
    def main(plugin_type: Any, argv: List[str]) -> None: ...
