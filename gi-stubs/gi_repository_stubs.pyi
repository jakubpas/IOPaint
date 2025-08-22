# GIMP 3.0 Type Stubs for better IDE support
from typing import Any, List, Tuple, Callable
from gi.repository import GObject


class Gimp:
    """GIMP 3.0 API namespace"""

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

    class Selection(GObject.Object):
        """GIMP Selection object"""
        def bounds(self) -> Tuple[bool, int, int, int, int]: ...
        def get_region(self) -> Any: ...

    class Layer(GObject.Object):
        """GIMP Layer object"""
        def set_name(self, name: str) -> None: ...
        def fill(self, fill_type: 'Gimp.FillType') -> None: ...
        @staticmethod
        def new(image: 'Gimp.Image', name: str, width: int, height: int,
                layer_type: 'Gimp.ImageType', opacity: float, mode: 'Gimp.LayerMode') -> 'Gimp.Layer': ...

    class Drawable(GObject.Object):
        """GIMP Drawable object"""
        pass

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

    class PDBProcType:
        """Procedure database procedure types"""
        PLUGIN: int = 1
        EXTENSION: int = 2
        TEMPORARY: int = 3

    class PDBStatusType:
        """Procedure database status types"""
        SUCCESS: int = 0
        CALLING_ERROR: int = 1
        EXECUTION_ERROR: int = 2
        CANCEL: int = 3

    class RunMode:
        """Plugin run modes"""
        INTERACTIVE: int = 0
        NONINTERACTIVE: int = 1
        WITH_LAST_VALS: int = 2

    class ImageType:
        """Image types"""
        RGB: int = 0
        GRAY: int = 1
        INDEXED: int = 2

    class LayerMode:
        """Layer blend modes"""
        NORMAL_MODE: int = 0
        MULTIPLY_MODE: int = 1
        SCREEN_MODE: int = 2
        OVERLAY_MODE: int = 3

    class FillType:
        """Fill types"""
        WHITE_FILL: int = 0
        BLACK_FILL: int = 1
        TRANSPARENT_FILL: int = 2
        FOREGROUND_FILL: int = 3
        BACKGROUND_FILL: int = 4

    class RGB:
        """RGB color class"""
        def __init__(self, r: int, g: int, b: int): ...
        r: int
        g: int
        b: int

    # Static methods
    @staticmethod
    def message(message: str) -> None:
        """Display a message to the user"""
        ...

    @staticmethod
    def file_save(image: 'Gimp.Image', drawables: List['Gimp.Drawable'],
                  filename: str, raw_filename: str) -> None:
        """Save an image to file"""
        ...

    @staticmethod
    def file_load_layer(image: 'Gimp.Image', filename: str) -> 'Gimp.Layer':
        """Load a layer from file"""
        ...

    @staticmethod
    def progress_init(progress: Any, message: str) -> None:
        """Initialize progress bar"""
        ...

    @staticmethod
    def progress_update(progress: Any, percentage: float) -> None:
        """Update progress bar"""
        ...

    @staticmethod
    def progress_set_text(progress: Any, message: str) -> None:
        """Set progress bar text"""
        ...

    @staticmethod
    def progress_end(progress: Any) -> None:
        """End progress bar"""
        ...

    @staticmethod
    def main(plugin_type: Any, argv: List[str]) -> None:
        """Main plugin entry point"""
        ...


# Make Gimp available at module level for direct import
__all__ = ['Gimp']
