import os.path
import random
import gradio as gr

from modules import rng, scripts
from modules.processing import StableDiffusionProcessingTxt2Img, opt_f
from modules.ui_components import ToolButton

ext = os.path.dirname(os.path.dirname(__file__))
config = os.path.join(ext, "res.txt")

_classic = str(gr.__version__).startswith("3")
js = {"_js" if _classic else "js": "onToggleRandomRes"}


class RandomResolution(scripts.Script):
    resolutions: list[tuple[int, int]] = []

    def title(self):
        return "Random Resolution"

    def show(self, is_img2img):
        return None if is_img2img else scripts.AlwaysVisible

    def ui(self, is_img2img):
        if is_img2img:
            return

        self.load_configs()

        randomize = gr.Checkbox(value=False, visible=False)
        randomize.do_not_save_to_config = True

        toggle = ToolButton(value="\U0001f3b2", elem_id="random_resolution_toggle")
        toggle.do_not_save_to_config = True

        toggle.click(
            fn=lambda val: gr.update(value=(not val)),
            inputs=[randomize],
            outputs=[randomize],
        ).success(
            fn=None,
            inputs=[randomize],
            **js,
        )

        return [randomize]

    @classmethod
    def load_configs(cls):
        with open(config, "r") as f:
            data = f.read()

        cls.resolutions.clear()
        for line in data.split("\n"):
            if not line.strip():
                continue
            w, h = line.split("x")
            cls.resolutions.append((int(w), int(h)))

        print(f"[Rand. Res] Loaded {len(cls.resolutions)} Resolutions")

    def before_process_batch(
        self,
        p: StableDiffusionProcessingTxt2Img,
        randomize: bool,
        batch_number: int,
        prompts: list[str],
        seeds: list[int],
        subseeds: list[int],
    ):
        if not randomize or not self.resolutions:
            return

        random.seed(seeds[0])
        i = random.randint(1, len(self.resolutions))
        w, h = self.resolutions[i - 1]

        p.width = w
        p.height = h
        p.calculate_target_resolution()
        print(f"[Rand. Res] Set to {w} x {h}")

        _c, *_ = p.rng.shape

        p.rng = rng.ImageRNG(
            (_c, p.height // opt_f, p.width // opt_f),
            p.seeds,
            subseeds=p.subseeds,
            subseed_strength=p.subseed_strength,
            seed_resize_from_h=p.seed_resize_from_h,
            seed_resize_from_w=p.seed_resize_from_w,
        )
