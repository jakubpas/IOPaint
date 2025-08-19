#!/usr/bin/env python3
# GIMP 3.0 Minimal Plugin (Tutorial-Based)

import sys
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp, GObject

class HelloGimpTutorial(Gimp.PlugIn):
    def do_query_procedures(self):
        return ['python-fu-hello-gimp-tutorial']

    def do_set_i18n(self, proc_name):
        # As per tutorial, return False to disable i18n for simplicity
        return False

    def do_create_procedure(self, name):
        # Use Gimp.ImageProcedure for plugins that operate on images
        procedure = Gimp.ImageProcedure.new(
            self,
            name,
            Gimp.PDBProcType.PLUGIN,
            self.run,
            None
        )
        procedure.set_image_types("*") # Works on any image type
        procedure.set_menu_label("Hello Tutorial...")
        procedure.add_menu_path("<Image>/Tools")
        procedure.set_documentation("A minimal tutorial-based test plugin.", "", name)
        procedure.set_attribution("Gemini", "Google", "2025")
        return procedure

    # Correct run method signature for Gimp.ImageProcedure
    def run(self, run_mode, image, drawable):
        Gimp.message("Hello Tutorial plugin is running!")
        return Gimp.PDBStatusType.SUCCESS

Gimp.main(HelloGimpTutorial.__gtype__, sys.argv)