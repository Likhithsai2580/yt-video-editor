from moviepy.editor import VideoFileClip, CompositeVideoClip, vfx
import numpy as np

class VideoEffects:
    @staticmethod
    def apply_effect(clip, effect_name, **kwargs):
        effect_method = getattr(VideoEffects, effect_name, None)
        if not effect_method:
            raise ValueError(f"Unknown effect: {effect_name}")
        return effect_method(clip, **kwargs)

    @staticmethod
    def fadein(clip, duration=1):
        return clip.fx(vfx.fadein, duration)

    @staticmethod
    def fadeout(clip, duration=1):
        return clip.fx(vfx.fadeout, duration)

    @staticmethod
    def invert_colors(clip):
        return clip.fx(vfx.invert_colors)

    @staticmethod
    def colorx(clip, factor=1.5):
        return clip.fx(vfx.colorx, factor)

    @staticmethod
    def lum_contrast(clip, lum=0, contrast=0.5):
        return clip.fx(vfx.lum_contrast, lum, contrast)

    @staticmethod
    def brightness(clip, factor=1.2):
        return clip.fx(vfx.colorx, factor)

    @staticmethod
    def blackwhite(clip):
        return clip.fx(vfx.blackwhite)

    @staticmethod
    def rotate(clip, angle=45):
        return clip.fx(vfx.rotate, angle)

    @staticmethod
    def resize(clip, new_size=(640, 480)):
        return clip.resize(new_size)

    @staticmethod
    def scroll(clip, speed=10):
        return clip.fx(vfx.scroll, y_speed=speed)

    @staticmethod
    def crop(clip, x1=0, x2=640, y1=0, y2=480):
        return clip.fx(vfx.crop, x1=x1, x2=x2, y1=y1, y2=y2)

    @staticmethod
    def mirror_x(clip):
        return clip.fx(vfx.mirror_x)

    @staticmethod
    def mirror_y(clip):
        return clip.fx(vfx.mirror_y)

    @staticmethod
    def speedx(clip, factor=2):
        return clip.fx(vfx.speedx, factor)

    @staticmethod
    def fadeinout(clip, duration=1):
        return clip.fx(vfx.fadein, duration).fx(vfx.fadeout, duration)

    @staticmethod
    def clip_duration(clip, duration=10):
        return clip.set_duration(duration)

    @staticmethod
    def crop_center(clip, x_center=0.5, y_center=0.5, width=640, height=480):
        return clip.fx(vfx.crop, x_center=x_center, y_center=y_center, width=width, height=height)

    @staticmethod
    def add_text(clip, text="Sample Text"):
        from moviepy.video.tools.drawing import TextClip
        text = TextClip(text, fontsize=70, color='white')
        text = text.set_position('center').set_duration(clip.duration)
        return CompositeVideoClip([clip, text])

    @staticmethod
    def vignette(clip, radius=0.5):
        from moviepy.video.fx import vignette
        return clip.fx(vignette, radius)

    @staticmethod
    def color_filter(clip, factor=0.5):
        return clip.fx(vfx.colorx, factor)

    @staticmethod
    def clip_speed(clip, factor=1):
        return clip.fx(vfx.speedx, factor)

    @staticmethod
    def resize_aspect_ratio(clip, width=640):
        return clip.resize(width=width)

    @staticmethod
    def edge_detection(clip):
        from moviepy.video.fx import edge_detect
        return clip.fx(edge_detect)

    @staticmethod
    def zoom(clip):
        return clip.fx(vfx.resize, lambda t: 1 + 0.1 * t)

    @staticmethod
    def saturation(clip, factor=1.5):
        return clip.fx(vfx.colorx, factor)

    @staticmethod
    def apply_effects_to_clip(input_path, output_path, effects):
        clip = VideoFileClip(input_path)
        
        for effect in effects:
            effect_name = effect.get("name")
            kwargs = effect.get("kwargs", {})
            clip = VideoEffects.apply_effect(clip, effect_name, **kwargs)
        
        clip.write_videofile(output_path, codec="libx264")