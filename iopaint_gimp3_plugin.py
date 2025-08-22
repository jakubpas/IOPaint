#!/usr/bin/env python3
# GIMP 3.0 Plugin

import os
import sys
import tempfile
import subprocess
import gi

gi.require_version('Gimp', '3.0')
from gi.repository import Gimp, Gio, Gegl

class IopaintErase(Gimp.PlugIn):
    DEBUG_LOG_FILE = os.path.join(tempfile.gettempdir(), "iopaint_gimp_debug.log")
    IOPAINT_EXECUTABLE = "/Library/Frameworks/Python.framework/Versions/3.10/bin/iopaint"
    MODEL = "lama" # Change to "sd" for Stable Diffusion
    DEVICE = "cpu"  # Change to "cuda" if you have a compatible GPU

    def do_query_procedures(self):
        return ['python-fu-iopaint-erase']

    def do_set_i18n(self, proc_name):
        return False

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(
            self,
            name,
            Gimp.PDBProcType.PLUGIN,
            self.run,
            None
        )
        procedure.set_image_types("*")
        procedure.set_menu_label("IOPaint Erase")
        procedure.add_menu_path("<Image>/Tools")  # Corrected menu path
        procedure.set_documentation(
            "Use IOPaint to erase objects from the image.",
            "Make sure IOPaint is installed and configured correctly.",
            name
        )
        procedure.set_attribution("Gemini", "Google", "2025")
        return procedure

    def run(self, procedure, run_mode, image, drawable, *args, **kwargs):
        try:
            Gimp.progress_init("Running IOPaint Erase...")
            Gimp.progress_update(0.1)
            Gimp.context_set_foreground(Gegl.Color.new("#FFFFFF"))
            Gimp.context_set_background(Gegl.Color.new("#000000"))
            image_path = IopaintErase.get_temp_path(".png")
            mask_path = IopaintErase.get_temp_path("_mask.png")
            output_dir = tempfile.gettempdir()
            Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, image, Gio.File.new_for_path(image_path), None)
            self.debug_log("Creating mask from selection...")
            self.debug_log("Created mask from selection...")
            Gimp.progress_update(0.2)
            successful, non_empty, x1, y1, x2, y2 = Gimp.Selection.bounds(image)
            if not successful or not non_empty:
                message = "Unable to get selection bounds."
                Gimp.message(message)
                self.debug_log(message)
                return Gimp.PDBStatusType.CALLING_ERROR

            # Calculate the center point of selection for bucket fill
            center_x = x1 + (x2 - x1) // 2
            center_y = y1 + (y2 - y1) // 2

            result_layer = Gimp.Layer.new(
                image,
                "Black/White Result",
                image.get_width(),
                image.get_height(),
                Gimp.ImageType.RGB_IMAGE,
                100.0,
                Gimp.LayerMode.NORMAL
            )
            image.insert_layer(result_layer, None, 0)
            Gimp.context_push()
            result_layer.fill(Gimp.FillType.BACKGROUND)
            Gimp.Drawable.edit_bucket_fill(
                result_layer,
                Gimp.FillType.FOREGROUND,
                center_x,
                center_y
            )
            Gimp.context_pop()
            Gimp.Image.flatten(image)
            Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, image, Gio.File.new_for_path(mask_path), None)
            Gimp.progress_update(0.4)

            # Run IOPaint command in separate process
            Gimp.progress_set_text(f"Running IOPaint with {self.MODEL} model...")
            command = [
                self.IOPAINT_EXECUTABLE,
                "run",
                "--model", self.MODEL,
                "--device", self.DEVICE,
                "--image", image_path,
                "--mask", mask_path,
                "--output", output_dir,
            ]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                message = f"IOPaint command failed. Error: {stderr}"
                Gimp.message(message)
                self.debug_log(message)
                return Gimp.PDBStatusType.CALLING_ERROR

            Gimp.progress_update(0.8)

            # Load result back into GIMP
            Gimp.progress_set_text("Loading result...")

            base_name = os.path.splitext(os.path.basename(image_path))[0]
            final_output_path = os.path.join(output_dir, f"{base_name}.png")

            if not os.path.exists(final_output_path):
                message = f"Output file not found. Expected: {final_output_path}"
                Gimp.message(message)
                self.debug_log(message)
                return Gimp.PDBStatusType.CALLING_ERROR

            self.debug_log(f"Output file found. Loading into GIMP...")
            image_file = Gio.File.new_for_path(final_output_path)
            result_layer = Gimp.file_load_layer(Gimp.RunMode.NONINTERACTIVE, image, image_file)
            self.debug_log(f"Result layer loaded from {final_output_path}")
            image.insert_layer(result_layer, None, 0)
            self.debug_log("Result layer added to image.")
            result_layer.set_name(f"IOPaint {self.MODEL} Result")
            self.debug_log("Result layer loaded and added to image.")

            # Delete temporary files
            for path in [image_path, mask_path, final_output_path]:
                if os.path.exists(path):
                    os.remove(path)
                    self.debug_log(f"Cleaned up: {path}")

            Gimp.progress_update(1.0)

        except Exception as e:
            message = "An unexpected error occurred."
            Gimp.message(f"{message}: {e}")
            self.debug_log(f"{message}: {e}")
            return Gimp.PDBStatusType.CALLING_ERROR

        finally:
            Gimp.progress_end()
            self.debug_log("--- IOPaint Plugin Finished ---")

        return (Gimp.PDBStatusType.SUCCESS,)

    @staticmethod
    def get_temp_path(extension):
        return os.path.join(tempfile.gettempdir(), f"gimp_iopaint_{os.urandom(4).hex()}{extension}")

    @staticmethod
    def debug_log(message):
        try:
            with open(IopaintErase.DEBUG_LOG_FILE, "a") as f:
                f.write(message + "\n")
        except Exception as e:
            # If logging fails, try to use Gimp.message as a fallback
            Gimp.message(f"Failed to write to log: {e}")


# --- Plugin Registration ---
Gimp.main(IopaintErase.__gtype__, sys.argv)
