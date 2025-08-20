# IOPaint Erase - GIMP 3.0 Plugin

**AI-Powered Object Removal Plugin for GIMP 3.0**

A GIMP plugin that creates black and white masks from user selections and uses IOPaint's advanced AI models to intelligently remove objects from images.

![Plugin Demo](assets/demo.gif)

## What It Does

This plugin transforms your GIMP selection workflow by:

1. **Selection to Mask**: Converts any GIMP selection into a binary mask (white selected area, black background)
2. **AI Inpainting**: Uses IOPaint's LAMA model to intelligently fill the selected area
3. **Seamless Integration**: Returns the result as a new layer in your GIMP image

Perfect for removing unwanted objects, people, text, watermarks, or any other elements from your photos.

## Features

- ✨ **One-Click Object Removal**: Simply select and remove
- 🎯 **Precise Selection Support**: Works with any GIMP selection tool
- 🤖 **AI-Powered**: Uses state-of-the-art LAMA (Large Mask Inpainting) model
- 📊 **Progress Tracking**: Real-time progress updates
- 🔧 **Configurable**: Support for multiple AI models and devices
- 🧹 **Auto Cleanup**: Handles temporary files automatically
- 📝 **Debug Logging**: Comprehensive error reporting

## Before & After Examples

| Original | After IOPaint Erase |
|----------|-------------------|
| ![Unwanted Object](assets/unwant_object.jpg) | ![Clean Result](assets/unwant_object_clean.jpg) |
| ![Unwanted Person](assets/unwant_person.jpg) | ![Clean Result](assets/unwant_person_clean.jpg) |
| ![Watermark](assets/watermark.jpg) | ![Clean Result](assets/watermark_cleanup.jpg) |

## Quick Start

### Prerequisites

- GIMP 3.0+
- Python 3.10+
- IOPaint installed: `pip install iopaint`

### Installation

1. **Download the Plugin**
   ```bash
   wget https://raw.githubusercontent.com/your-repo/iopaint_gimp3_plugin.py
   ```

2. **Copy to GIMP Plugin Directory**
   ```bash
   # macOS
   cp iopaint_gimp3_plugin.py ~/Library/Application\ Support/GIMP/3.0/plug-ins/
   
   # Linux
   cp iopaint_gimp3_plugin.py ~/.config/GIMP/3.0/plug-ins/
   
   # Windows
   copy iopaint_gimp3_plugin.py %APPDATA%\GIMP\3.0\plug-ins\
   ```

3. **Make Executable** (Unix-like systems)
   ```bash
   chmod +x ~/Library/Application\ Support/GIMP/3.0/plug-ins/iopaint_gimp3_plugin.py
   ```

4. **Configure Plugin**
   
   Edit the plugin file to set your IOPaint path:
   ```python
   IOPAINT_EXECUTABLE = "/usr/local/bin/iopaint"  # Update this path
   ```
   
   Find your IOPaint path with: `which iopaint`

### Usage

1. **Open Image** in GIMP 3.0
2. **Select Area** to remove using any selection tool
3. **Run Plugin**: `Tools` → `IOPaint Erase`
4. **Wait** for AI processing (progress bar shown)
5. **Review Result** in new layer

## Configuration

### Available Models

Edit the plugin to change the AI model:

```python
MODEL = "lama"    # Default - best for most cases
# MODEL = "ldm"   # Latent Diffusion Model
# MODEL = "zits"  # ZITS inpainting
# MODEL = "mat"   # Mask-Aware Transformer
# MODEL = "fcf"   # Foreground-aware Content Fill
```

### Device Settings

```python
DEVICE = "cpu"    # CPU processing (slower, compatible)
# DEVICE = "cuda" # GPU acceleration (faster, requires NVIDIA GPU)
```

## Workflow Tips

### Best Practices

- **Precise Selections**: Use the Free Select tool for irregular objects
- **Feathered Edges**: Add slight feather to selections for smoother results
- **Multiple Passes**: For complex removals, work in smaller sections
- **Layer Management**: Keep original layer intact, work with copies

### Selection Tools Recommended

- **Free Select Tool**: Best for irregular objects
- **Fuzzy Select**: Good for areas with similar colors
- **By Color Select**: Effective for backgrounds
- **Rectangle/Ellipse**: Perfect for geometric objects

## Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| Plugin not in menu | Restart GIMP, check file permissions |
| "IOPaint not found" | Update `IOPAINT_EXECUTABLE` path |
| "No selection" error | Make sure area is selected before running |
| Slow processing | Switch to GPU mode or use smaller images |
| Out of memory | Use CPU mode, close other applications |

### Debug Information

Check the debug log for detailed error information:
```bash
tail -f /tmp/iopaint_gimp_debug.log
```

### Performance Tips

- **Image Size**: Smaller images process faster
- **GPU vs CPU**: GPU is 5-10x faster if available
- **Model Choice**: LAMA is fastest, LDM is most accurate
- **Selection Size**: Smaller selections process quicker

## Technical Details

### Plugin Architecture

```
User Selection → Binary Mask → IOPaint AI → Result Layer
```

1. **Mask Creation**: Selection converted to black/white PNG
2. **AI Processing**: IOPaint command-line tool processes image
3. **Result Import**: Processed image loaded as new GIMP layer
4. **Cleanup**: Temporary files automatically removed

### File Locations

- **Plugin**: `~/.config/GIMP/3.0/plug-ins/iopaint_gimp3_plugin.py`
- **Debug Log**: `/tmp/iopaint_gimp_debug.log`
- **Temp Files**: System temp directory (auto-cleaned)

### Dependencies

```python
# Core GIMP 3.0 API
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp, Gio, Gegl

# System libraries
import os, sys, tempfile, subprocess
```

## Advanced Usage

### Batch Processing

For multiple images, consider using IOPaint directly:
```bash
iopaint run --model lama --device cpu --image input.jpg --mask mask.png --output results/
```

### Custom Models

To use custom trained models, modify the plugin:
```python
MODEL = "path/to/your/custom/model"
```

### Integration with Other Plugins

This plugin works well with:
- **G'MIC**: For advanced selections
- **Resynthesizer**: For texture synthesis
- **Layer Effects**: For post-processing

## Contributing

### Development Setup

1. Clone the repository
2. Install development dependencies
3. Set up GIMP 3.0 development environment
4. Test with sample images in `assets/`

### Reporting Issues

Please include:
- GIMP version
- Python version
- IOPaint version
- Debug log contents
- Sample image (if possible)

## License

This plugin is released under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- **IOPaint Team**: For the amazing AI inpainting library
- **GIMP Developers**: For the powerful image editing platform
- **LAMA Authors**: For the state-of-the-art inpainting model
- **Community**: For testing and feedback

## Related Projects

- [IOPaint](https://github.com/Sanster/IOPaint) - The AI inpainting library
- [GIMP](https://www.gimp.org/) - GNU Image Manipulation Program
- [LAMA](https://github.com/saic-mdal/lama) - Large Mask Inpainting model

---

**Made with ❤️ for the GIMP community**

> Need help? Open an issue or check the [troubleshooting guide](#troubleshooting) above.
