import os
import sys
from abc import ABC
from packaging.version import Version

import gradio as gr
import spandrel

from backend import memory_management
from modules import modelloader, upscaler_utils
from modules.options import OptionInfo
from modules.script_callbacks import on_ui_settings
from modules.shared import opts
from modules.upscaler import Upscaler, UpscalerData
from modules_forge.utils import prepare_free_memory


spandrel_ver: str = spandrel.__version__

MOSR_SUPPORTED = Version(spandrel_ver) >= Version("0.4.0")
MOESR_RCAN_SUPPORTED = Version(spandrel_ver) >= Version("0.4.1")


class BaseUpscaler(ABC):
    """
    Base class for Spandrel upscalers.
    """

    name = None
    model_path = None
    model_name = None
    model_url = None
    enable = True
    ex_filter = [".pt", ".pth", ".safetensors"]
    model = None
    user_path = None
    scalers: list
    tile = True
    scalers: list = []  # Define scalers as a class attribute

    def __init__(self, dirname):
        self.scalers = []
        self.user_path = dirname

        super().__init__()

        for file in self.find_models(ext_filter=self.ex_filter):
            name = modelloader.friendly_name(file)
            scale = 4  # TODO: scale might not be 4, but we can't know without loading the model
            scaler_data = UpscalerData(name, file, upscaler=self, scale=scale)
            self.scalers.append(scaler_data)

    def do_upscale(self, img, selected_model):
        prepare_free_memory()

        try:
            model = self.load_model(selected_model)
        except Exception as e:
            print(
                f"Unable to load {self.model_name} model {selected_model}: {e}",
                file=sys.stderr,
            )
            return img

        model.to(memory_management.get_torch_device())

        tile_size = getattr(
            opts, f"{self.name}_tile", getattr(opts, "ESRGAN_tile", 192)
        )
        tile_overlap = getattr(
            opts, f"{self.name}_tile_overlap", getattr(opts, "ESRGAN_tile_overlap", 8)
        )
        return upscaler_utils.upscale_with_model(
            model,
            img,
            tile_size=tile_size,
            tile_overlap=tile_overlap,
        )

    def load_model(self, path: str):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Model file {path} not found")
        return modelloader.load_spandrel_model(
            path,
            device=memory_management.get_torch_device(),
            expected_architecture=self.model_name,
        )


# Multiple inheritance lets us override `Upscaler` methods without
# `BaseUpscaler` being deteced as a subclass of `Upscaler`


class UpscalerATD(BaseUpscaler, Upscaler):
    def __init__(self, dirname):
        self.name = "ATD"
        self.model_name = "ATD"
        super().__init__(dirname)


class UpscalerPLKSR(BaseUpscaler, Upscaler):
    def __init__(self, dirname):
        self.name = "PLKSR"
        self.model_name = "PLKSR"
        super().__init__(dirname)


class UpscalerRealPLKSR(BaseUpscaler, Upscaler):
    def __init__(self, dirname):
        self.name = "RealPLKSR"
        self.model_name = "RealPLKSR"
        super().__init__(dirname)


class UpscalerDRCT(BaseUpscaler, Upscaler):
    def __init__(self, dirname):
        self.name = "DRCT"
        self.model_name = "DRCT"
        super().__init__(dirname)


if MOSR_SUPPORTED:

    class UpscalerMoSR(BaseUpscaler, Upscaler):
        def __init__(self, dirname):
            self.name = "MoSR"
            self.model_name = "MoSR"
            super().__init__(dirname)
else:
    print(
        "MoSR upscaler not supported in this version of Spandrel. Please update to 0.4.0 or later."
    )

if MOESR_RCAN_SUPPORTED:

    class UpscalerMoESR(BaseUpscaler, Upscaler):
        def __init__(self, dirname):
            self.name = "MoESR"
            self.model_name = "MoESR"
            super().__init__(dirname)

    class UpscalerRCAN(BaseUpscaler, Upscaler):
        def __init__(self, dirname):
            self.name = "RCAN"
            self.model_name = "RCAN"
            super().__init__(dirname)
else:
    print(
        "MoESR & RCAN upscalers not supported in this version of Spandrel. Please update to 0.4.1 or later."
    )

loaded_upscaler_classes = [
    cls.__name__
    for cls in [
        UpscalerATD,
        UpscalerPLKSR,
        UpscalerRealPLKSR,
        UpscalerDRCT,
        *([UpscalerMoSR] if MOSR_SUPPORTED else []),
        *([UpscalerMoESR, UpscalerRCAN] if MOESR_RCAN_SUPPORTED else []),
    ]
]
print("Loaded extra upscaler classes:", loaded_upscaler_classes)

section = ("upscaling", "Upscaling")


def on_settings():
    for cls_name in loaded_upscaler_classes:
        name = cls_name.replace("Upscaler", "")

        opts.add_option(
            f"{name}_tile",
            OptionInfo(
                192,
                f"Tile size for {name} upscaler.",
                component=gr.Slider,
                component_args={"minimum": 0, "maximum": 512, "step": 16},
                section=section,
            ).info("0 = no tiling"),
        )
        opts.add_option(
            f"{name}_tile_overlap",
            OptionInfo(
                8,
                f"Tile overlap for {name} upscaler.",
                component=gr.Slider,
                component_args={"minimum": 0, "maximum": 48, "step": 1},
                section=section,
            ).info("Low values = visible seam"),
        )


on_ui_settings(on_settings)
