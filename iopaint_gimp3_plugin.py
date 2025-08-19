#!/usr/bin/env python3
# GIMP 3.0 Plugin

import os
import sys
import tempfile
import subprocess
import gi

gi.require_version('Gimp', '3.0')
from gi.repository import Gimp, GObject

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
        procedure.set_menu_label("IOPaint Erase...")
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

        # 1. Check for a selection
        debug_log("Checking for selection...")
        try:
            # Capture all returned values from bounds() to see what's actually returned
            has_selection, non_empty, x1, y1, x2, y2 = Gimp.Selection.bounds(image)
            debug_log(
                f"Selection.bounds() returned: has_selection={has_selection}, non_empty={non_empty}, x1={x1}, y1={y1}, x2={x2}, y2={y2}")

            if not has_selection:
                Gimp.message("IOPaint Plugin: Please make a selection to erase.")
                debug_log("No selection found (has_selection is False). Exiting.")
                return Gimp.PDBStatusType.CALLING_ERROR
            debug_log("Selection found. Proceeding.")
        except Exception as e:
            debug_log(f"Error during selection check: {e}")
            Gimp.message(f"IOPaint Plugin Error during selection check: {e}")
            return Gimp.PDBStatusType.CALLING_ERROR

        Gimp.progress_init("Running IOPaint Erase...")
        debug_log("Progress bar initialized.")

        try:
            # 2. Prepare temporary files
            image_path = self.get_temp_path(".png")
            mask_path = self.get_temp_path("_mask.png")
            output_dir = tempfile.gettempdir()
            debug_log(f"Temp image path: {image_path}")
            debug_log(f"Temp mask path: {mask_path}")
            debug_log(f"Output directory: {output_dir}")

            # Save the original image
            Gimp.file_save(image, [drawable], image_path, image_path)
            debug_log(f"Image saved to {image_path}")

            # Create and save the mask from the selection
            debug_log("Creating mask from selection...")
            mask_drawable = Gimp.Layer.new_from_selection(image)
            if not mask_drawable:
                debug_log("Failed to create layer from selection.")
                Gimp.message("IOPaint Error: Could not create mask from selection.")
                return Gimp.PDBStatusType.CALLING_ERROR

            mask_image = Gimp.Image.new(image.width, image.height, Gimp.ImageType.GRAY)
            mask_image.add_layer(mask_drawable, 0)
            debug_log("Inverting mask colors (selection is black)")
            mask_drawable.invert(False)  # Invert so the selection is white on a black background

            Gimp.file_save(mask_image, [mask_drawable], mask_path, mask_path)
            debug_log(f"Mask saved to {mask_path}")

            # Clean up temporary mask image
            Gimp.Image.delete(mask_image)

            Gimp.progress_update(image.get_progress(), 0.2)

            # 3. Run IOPaint command
            Gimp.progress_set_text(image.get_progress(), f"Running {self.MODEL} model...")
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

            Gimp.progress_update(image.get_progress(), 0.8)

            # 4. Load result back into GIMP
            Gimp.progress_set_text(image.get_progress(), "Loading result...")

            base_name = os.path.splitext(os.path.basename(image_path))[0]
            final_output_path = os.path.join(output_dir, f"{base_name}_IOPaint.png")
            debug_log(f"Expected output path: {final_output_path}")

            if not os.path.exists(final_output_path):
                Gimp.message(
                    f"IOPaint Error: Output file not found!\n{final_output_path}\n\nStdout:\n{stdout}\n\nStderr:\n{stderr}")
                debug_log(f"Output file not found. Expected: {final_output_path}")
                return Gimp.PDBStatusType.CALLING_ERROR

            result_layer = Gimp.file_load_layer(image, final_output_path)
            image.add_layer(result_layer, 0)
            result_layer.set_name(f"IOPaint {self.MODEL} Result")
            debug_log("Result layer loaded and added to image.")

            # Clean up
            for path in [image_path, mask_path, final_output_path]:
                if os.path.exists(path):
                    os.remove(path)
                    debug_log(f"Cleaned up: {path}")

            Gimp.progress_update(image.get_progress(), 1.0)

        except Exception as e:
            Gimp.message(f"An unexpected error occurred: {e}")
            debug_log(f"An unexpected error occurred: {e}")
            return Gimp.PDBStatusType.CALLING_ERROR

        finally:
            Gimp.progress_end(image.get_progress())
            debug_log("--- IOPaint Plugin Finished ---")

        return Gimp.PDBStatusType.SUCCESS

    def get_temp_path(self, extension):
        # A helper function to create temporary file paths
        return os.path.join(tempfile.gettempdir(), f"gimp_iopaint_{os.urandom(4).hex()}{extension}")


# --- Plugin Registration ---
Gimp.main(IopaintErase.__gtype__, sys.argv)
