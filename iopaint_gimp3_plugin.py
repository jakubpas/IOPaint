#!/usr/bin/env python3
# GIMP 3.0 Plugin

import os
import sys
import tempfile
import subprocess
import gi

gi.require_version('Gimp', '3.0')
from gi.repository import Gimp, Gio, Gegl

# --- Debug Log Function ---
DEBUG_LOG_FILE = os.path.join(tempfile.gettempdir(), "iopaint_gimp_debug.log")


def debug_log(message):
    try:
        with open(DEBUG_LOG_FILE, "a") as f:
            f.write(message + "\n")
    except Exception as e:
        # If logging fails, try to use Gimp.message as a fallback
        Gimp.message(f"Failed to write to log: {e}")


# --- Main Plugin Class for GIMP 3.0 ---
class IopaintErase(Gimp.PlugIn):
    # --- Configuration ---
    IOPAINT_EXECUTABLE = "/Library/Frameworks/Python.framework/Versions/3.10/bin/iopaint"
    MODEL = "lama"
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
            "Erases the selected part of the image using the IOPaint tool.",
            name
        )
        procedure.set_attribution("Gemini", "Google", "2025")
        return procedure

    # Corrected run method signature to accept procedure as first argument
    def run(self, procedure, run_mode, image, drawable, *args, **kwargs):
        debug_log("--- IOPaint Plugin Started ---")
        debug_log(f"Procedure: {procedure}, Run Mode: {run_mode}, Image: {image}, Drawable: {drawable}")
        debug_log(f"Extra args: {args}, Extra kwargs: {kwargs}")

        Gimp.progress_init("Running IOPaint Erase...")
        debug_log("Progress bar initialized.")

        Gimp.context_set_foreground(Gegl.Color.new("#FFFFFF"))
        Gimp.context_set_background(Gegl.Color.new("#000000"))
        try:
            # 2. Prepare temporary files
            image_path = self.get_temp_path(".png")
            mask_path = self.get_temp_path("_mask.png")
            output_dir = tempfile.gettempdir()
            debug_log(f"Temp image path: {image_path}")
            debug_log(f"Temp mask path: {mask_path}")
            debug_log(f"Output directory: {output_dir}")

            # Save the original image using GIMP 3.0 API
            debug_log("save image")
            Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, image, Gio.File.new_for_path(image_path), None)
            debug_log(f"Image saved to {image_path}")

            # Create mask from selection using GIMP 3.0 API
            debug_log("Creating mask from selection...")
            debug_log("Created mask from selection...")


            successful, non_empty, x1, y1, x2, y2 = Gimp.Selection.bounds(image)
            if not successful or not non_empty:
                Gimp.message("Unable to get selection bounds.")
                debug_log("Unable to get selection bounds")
                return Gimp.PDBStatusType.CALLING_ERROR

            # Calculate center point of selection for bucket fill
            center_x = x1 + (x2 - x1) // 2
            center_y = y1 + (y2 - y1) // 2

            #------
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
            debug_log("Created new result layer")
            Gimp.context_push()
            Gimp.context_set_foreground(Gegl.Color.new("#FFFFFF"))  # White
            Gimp.context_set_background(Gegl.Color.new("#000000"))  # Black
            result_layer.fill(Gimp.FillType.BACKGROUND)
            Gimp.Drawable.edit_bucket_fill(
                result_layer,
                Gimp.FillType.FOREGROUND,
                center_x,
                center_y
            )
            Gimp.context_pop()
            Gimp.Image.flatten(image)

            # Save the mask using GIMP 3.0 API
            debug_log("save mask")
            Gimp.file_save(Gimp.RunMode.NONINTERACTIVE, image, Gio.File.new_for_path(mask_path), None)
            debug_log(f"Mask saved to {mask_path}")

            Gimp.progress_update(0.2)

            # 3. Run IOPaint command
            Gimp.progress_set_text(f"Running {self.MODEL} model...")
            command = [
                self.IOPAINT_EXECUTABLE,
                "run",
                "--model", self.MODEL,
                "--device", self.DEVICE,
                "--image", image_path,
                "--mask", mask_path,
                "--output", output_dir,
            ]
            debug_log(f"Running command: {' '.join(command)}")

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            debug_log(f"Command finished. Return code: {process.returncode}")
            debug_log(f"Stdout: {stdout}")
            debug_log(f"Stderr: {stderr}")

            if process.returncode != 0:
                Gimp.message(f"IOPaint Error:\n\n{stderr}")
                debug_log(f"IOPaint command failed. Error: {stderr}")
                return Gimp.PDBStatusType.CALLING_ERROR

            Gimp.progress_update(0.8)

            # 4. Load result back into GIMP
            Gimp.progress_set_text("Loading result...")

            base_name = os.path.splitext(os.path.basename(image_path))[0]
            final_output_path = os.path.join(output_dir, f"{base_name}.png")
            debug_log(f"Expected output path: {final_output_path}")

            if not os.path.exists(final_output_path):
                Gimp.message(
                    f"IOPaint Error: Output file not found!\n{final_output_path}\n\nStdout:\n{stdout}\n\nStderr:\n{stderr}")
                debug_log(f"Output file not found. Expected: {final_output_path}")
                return Gimp.PDBStatusType.CALLING_ERROR

            debug_log(f"Output file found. Loading into GIMP...")
            image_file = Gio.File.new_for_path(final_output_path)
            result_layer = Gimp.file_load_layer(Gimp.RunMode.NONINTERACTIVE, image, image_file)
            debug_log(f"Result layer loaded from {final_output_path}")
            image.insert_layer(result_layer, None, 0)
            debug_log("Result layer added to image.")
            result_layer.set_name(f"IOPaint {self.MODEL} Result")
            debug_log("Result layer loaded and added to image.")

            #Clean up
            for path in [image_path, mask_path, final_output_path, mask_image]:
                if os.path.exists(path):
                    os.remove(path)
                    debug_log(f"Cleaned up: {path}")

            Gimp.progress_update(1.0)

        except Exception as e:
            Gimp.message(f"An unexpected error occurred: {e}")
            debug_log(f"An unexpected error occurred: {e}")
            return Gimp.PDBStatusType.CALLING_ERROR

        finally:
            Gimp.progress_end()
            debug_log("--- IOPaint Plugin Finished ---")

        return (Gimp.PDBStatusType.SUCCESS,)

    def get_temp_path(self, extension):
        # A helper function to create temporary file paths
        return os.path.join(tempfile.gettempdir(), f"gimp_iopaint_{os.urandom(4).hex()}{extension}")


# --- Plugin Registration ---
Gimp.main(IopaintErase.__gtype__, sys.argv)
