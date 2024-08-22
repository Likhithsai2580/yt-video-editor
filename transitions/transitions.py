from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips, vfx, clips_array
from moviepy.video.fx import scroll, fadein, fadeout, mask_color
import numpy as np

class TransitionEffects:
    @staticmethod
    def apply_transition(clip1_path, clip2_path, transition_name, **kwargs):
        clip1 = VideoFileClip(clip1_path).resize(height=720)
        clip2 = VideoFileClip(clip2_path).resize(height=720)
        
        transition_method = getattr(TransitionEffects, transition_name, None)
        if not transition_method:
            raise ValueError(f"Unknown transition: {transition_name}")
        
        final_clip = transition_method(clip1, clip2, **kwargs)
        
        output_file = f"{transition_name}.mp4"
        final_clip.write_videofile(output_file, codec="libx264")
        return output_file

    @staticmethod
    def a_roll_transition(clip1, clip2, duration=1):
        transition = clip1.fx(vfx.scroll, y_speed=-(clip1.size[1] / duration))
        return concatenate_videoclips([clip1, transition, clip2], method="compose")

    @staticmethod
    def b_roll_transition(clip1, clip2, start_time=5, duration=2):
        b_roll_clip = clip2.subclip(start_time, start_time + duration)
        b_roll_clip = b_roll_clip.set_position(("center", "center")).resize(clip1.size)
        return CompositeVideoClip([clip1, b_roll_clip])

    @staticmethod
    def crossfade_transition(clip1, clip2, duration=1):
        clip1 = clip1.crossfadeout(duration)
        clip2 = clip2.crossfadein(duration)
        return concatenate_videoclips([clip1, clip2], method="compose")

    @staticmethod
    def fade_transition(clip1, clip2, fade_duration=1):
        clip1 = clip1.fx(vfx.fadeout, fade_duration)
        clip2 = clip2.fx(vfx.fadein, fade_duration)
        return concatenate_videoclips([clip1, clip2], method="compose")

    @staticmethod
    def slide_transition(clip1, clip2, duration=1):
        clip1 = clip1.fx(scroll, x_speed=-clip1.size[0] / duration).set_duration(clip1.duration)
        clip2 = clip2.fx(scroll, x_speed=clip2.size[0] / duration).set_duration(clip2.duration)
        return CompositeVideoClip([clip1, clip2.set_start(clip1.duration - duration)])

    @staticmethod
    def wipe_transition(clip1, clip2, duration=1):
        transition = clip1.fx(vfx.slide_in, duration=duration).set_duration(clip1.duration)
        return concatenate_videoclips([clip1, transition, clip2], method="compose")

    @staticmethod
    def zoom_transition(clip1, clip2, zoom_duration=1):
        zoom_in = vfx.resize(clip1, lambda t: 1 + 0.1 * (t / zoom_duration)).set_duration(zoom_duration)
        zoom_out = vfx.resize(clip2, lambda t: 1 + 0.1 * ((zoom_duration - t) / zoom_duration)).set_duration(zoom_duration)
        return concatenate_videoclips([zoom_in, zoom_out], method="compose")

    @staticmethod
    def split_transition(clip1, clip2, duration=1):
        def make_split_transition(clip1, clip2, duration):
            w, h = clip1.size
            num_splits = 4
            clips = []
            for i in range(num_splits):
                start_pos = int(i * (w / num_splits))
                end_pos = int((i + 1) * (w / num_splits))
                part1 = clip1.crop(x1=start_pos, x2=end_pos).set_position((start_pos, 0))
                part2 = clip2.crop(x1=start_pos, x2=end_pos).set_position((start_pos, 0))
                clips.append(part1)
                clips.append(part2.set_start(duration / 2))
            return clips_array([clips])
        return make_split_transition(clip1, clip2, duration)

    @staticmethod
    def circle_reveal_transition(clip1, clip2, radius=200, duration=1):
        def circle_mask(clip, radius, t):
            return clip.fx(vfx.mask_color, color=(0, 0, 0), thr=0.3).fx(vfx.circle_mask, radius=radius * t / duration)
        mask1 = clip1.fx(circle_mask, radius=radius, t=0).set_duration(duration)
        mask2 = clip2.fx(circle_mask, radius=radius, t=duration).set_duration(duration)
        return CompositeVideoClip([mask1, mask2.set_start(duration / 2)], size=clip1.size)

    @staticmethod
    def page_turn_transition(clip1, clip2, duration=1):
        def page_turn_effect(t):
            return vfx.mosaic(clip1, t / duration).set_duration(duration)
        page_turn = page_turn_effect(duration - duration / 2)
        return CompositeVideoClip([page_turn, clip2.set_start(duration / 2)], size=clip1.size)

    @staticmethod
    def light_leak_transition(clip1, clip2, leak_duration=1):
        light_leak = VideoFileClip("light_leak.mp4").resize(clip1.size).set_duration(leak_duration)
        return concatenate_videoclips([clip1, light_leak, clip2], method="compose")

    @staticmethod
    def inverted_colors_transition(clip1, clip2, duration=1):
        inverted = clip1.fx(vfx.invert_colors).set_duration(duration)
        return concatenate_videoclips([clip1, inverted, clip2], method="compose")

    @staticmethod
    def dissolve_transition(clip1, clip2, duration=1):
        fade_clip1 = fadeout(clip1, duration)
        fade_clip2 = fadein(clip2, duration)
        return CompositeVideoClip([fade_clip1.set_duration(duration),
                                   fade_clip2.set_start(duration - fade_clip2.duration)])

    @staticmethod
    def rotate_transition(clip1, clip2, rotation_duration=1):
        def rotate_effect(t):
            return clip1.fx(vfx.rotate, angle=360 * (t / rotation_duration)).set_duration(rotation_duration)
        rotating_clip = rotate_effect(rotation_duration)
        return CompositeVideoClip([rotating_clip, clip2.set_start(rotation_duration / 2)], size=clip1.size)

    @staticmethod
    def diagonal_wipe_transition(clip1, clip2, wipe_duration=1):
        def diagonal_wipe(t):
            return vfx.crop(clip1, x1=0, x2=clip1.size[0] * t / wipe_duration,
                            y1=0, y2=clip1.size[1] * t / wipe_duration).set_duration(wipe_duration)
        wipe_clip = diagonal_wipe(wipe_duration)
        return CompositeVideoClip([wipe_clip, clip2.set_start(wipe_duration / 2)], size=clip1.size)

    @staticmethod
    def heart_shape_transition(clip1, clip2, duration=1):
        from moviepy.video.tools.drawing import color_gradient
        
        def heart_shape(size, t):
            mask = np.zeros(size)
            x = np.linspace(-1, 1, size[1])
            y = np.linspace(-1, 1, size[0])
            X, Y = np.meshgrid(x, y)
            equation = (X**2 + (Y - np.sqrt(abs(X)))**2 - 1)**3 - X**2 * (Y**2)**3
            mask[equation < 0] = 1
            return mask
        
        mask_clip = color_gradient(clip1.size, p1=(0, 0), p2=(1, 1), color1=(0, 0, 0), color2=(1, 0, 0))
        mask_clip = mask_clip.fx(mask_color, color=(0, 0, 0)).fx(lambda clip: clip.set_duration(duration))
        
        heart_mask = heart_shape(clip1.size, duration)
        heart_mask_clip = VideoFileClip.from_array(heart_mask).set_duration(duration)
        
        return CompositeVideoClip([clip1.set_opacity(heart_mask_clip.fx(vfx.colorx, 0.5)), 
                                   clip2.set_start(duration / 2).set_opacity(heart_mask_clip)], 
                                  size=clip1.size)

    @staticmethod
    def film_roll_transition(clip1, clip2, roll_duration=1):
        def roll_effect(t):
            return vfx.scroll(clip1, y_speed=-clip1.size[1] * (t / roll_duration)).set_duration(roll_duration)
        rolling_clip = roll_effect(roll_duration)
        return CompositeVideoClip([rolling_clip, clip2.set_start(roll_duration / 2)], size=clip1.size)

    @staticmethod
    def ripple_transition(clip1, clip2, ripple_duration=1):
        def ripple_effect(t):
            return vfx.ripple(clip1, frequency=10, amplitude=20 * (t / ripple_duration)).set_duration(ripple_duration)
        ripple_clip = ripple_effect(ripple_duration)
        return CompositeVideoClip([ripple_clip, clip2.set_start(ripple_duration / 2)], size=clip1.size)

    @staticmethod
    def starfield_transition(clip1, clip2, starfield_duration=1):
        def starfield_effect(t):
            stars = np.random.rand(clip1.size[1], clip1.size[0]) * 255
            starfield = VideoFileClip.from_array(stars.astype(np.uint8)).set_duration(starfield_duration)
            return CompositeVideoClip([starfield, clip1.set_opacity(0.5)])
        final_clip = starfield_effect(starfield_duration)
        return CompositeVideoClip([final_clip, clip2.set_start(starfield_duration / 2)], size=clip1.size)

