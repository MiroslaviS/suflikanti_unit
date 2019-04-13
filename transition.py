from __future__ import division

from moviepy.editor import *
import moviepy.video.fx.all as vfx
import os
from PIL import Image


def intro_logo_with_background(background_animation, logo):
    clip = VideoFileClip(background_animation)
    clip = clip.resize(0.5)
    # TODO resize for platform

    sub = clip.subclip(0, 16)

    clip2 = sub.speedx(final_duration=2)

    clip3 = clip2.fx(vfx.time_mirror)

    final = concatenate_videoclips([clip2, clip3])

    image_clip = ImageClip(logo, duration=final.duration)
    image_clip = image_clip.resize(0.3).set_position("center", "center")

    final_video = CompositeVideoClip([final, image_clip.resize(lambda t: 1 + 0.1 * t)])

    final_reverse = final_video.fx(vfx.time_mirror)

    return final_reverse


def product_previews(products, text_content="Realase TODAY", duration_of_product=4, font="Amiri-Bold",
                     text_color="black"):
    image_clips = [ImageClip(image, duration=duration_of_product) for image in products]

    text_clip = TextClip(text_content, color=text_color, font=font).set_duration(duration_of_product * len(products))

    clips_with_text = [
        CompositeVideoClip([image_clip, text_clip]) for image_clip in image_clips
    ]

    clips_with_text = [clipo.set_duration(4) for clipo in clips_with_text]

    final_clip = concatenate_videoclips(clips_with_text)

    return final_clip


def anim_pictures(pic1):
    image_clip = ImageClip(pic1)

    image_clip = image_clip.set_duration(4)

    new_clip = image_clip.fx(vfx.scroll, w=1280, x_speed=500)

    new_clip.set_duration(float(image_clip.w - 640 * 2) / 500)
    return new_clip


def one_on_each_other(clip_list):
    imclips = []
    for item in clip_list:
        imclips.append(ImageClip(item).set_duration(2).crossfadein(2))

    imclipsstart = []
    start = 0
    for clip in imclips:
        if start == 0:
            start += 2
            imclipsstart.append(clip)
            continue

        imclipsstart.append(clip.set_start(start))
        start += 2

    final_clip = CompositeVideoClip(imclipsstart)

    final_clip.set_duration(len(imclipsstart) * 2)

    return final_clip


def four_in_row(image):
    long_slice(image)
    imclip1 = ImageClip("/tmp/slice_1.png").set_duration(0.7)
    imclip2 = ImageClip("/tmp/slice_2.png").set_duration(0.7)
    imclip3 = ImageClip("/tmp/slice_3.png").set_duration(0.7)
    imclip4 = ImageClip("/tmp/slice_4.png").set_duration(0.7)
    imclip5 = ImageClip(image).set_duration(3)

    clip1 = [imclip1.set_start(1)], [imclip2.set_start(2)], [imclip3.set_start(3)], [imclip4.set_start(4)]
    moving_clip = clips_array(clip1)
    moving_clip.set_duration(8)
    final_clip = concatenate_videoclips([moving_clip, imclip5])
    return final_clip
    # final_clip.write_videofile("test2.mp4", fps=25)


def four_in_width(image):
    width_slice(image)
    imclip1 = ImageClip("/tmp/slice_1.png").set_duration(2.1)
    imclip2 = ImageClip("/tmp/slice_2.png").set_duration(1.4)
    imclip3 = ImageClip("/tmp/slice_3.png").set_duration(2.8)
    imclip4 = ImageClip("/tmp/slice_4.png").set_duration(0.7)
    imclip5 = ImageClip(image).set_duration(2)

    clip1 = [imclip1.set_start(1.4), imclip2.set_start(2.1), imclip3.set_start(0.7), imclip4.set_start(2.8)]
    moving_clip = clips_array([clip1])
    moving_clip.set_duration(5)
    final_clip = concatenate_videoclips([moving_clip, imclip5])
    return final_clip
    # final_clip.write_videofile("test1.mp4", fps=25)


def long_slice(image_path):
    outdir = "/tmp/"
    """slice an image into parts slice_size tall"""
    img = Image.open(image_path)
    width, height = img.size
    upper = 0
    left = 0
    slices = 4
    slice_size = height // 4

    count = 1
    for slice in range(slices):
        # if we are at the end, set the lower bound to be the bottom of the image
        if count == slices:
            lower = height
        else:
            lower = int(count * slice_size)

        bbox = (left, upper, width, lower)
        working_slice = img.crop(bbox)
        upper += slice_size
        working_slice.save(os.path.join(outdir, "slice_" + str(count) + ".png"))
        count += 1


def width_slice(image_path):
    outdir = "/tmp/"
    img = Image.open(image_path)
    width, height = img.size
    upper = 0
    left = 0
    right = 0
    slices = 4
    slice_size = width // 4

    count = 1
    for slice in range(slices):
        # if we are at the end, set the lower bound to be the bottom of the image
        if count == slices:
            right = width
        else:
            right = int(count * slice_size)

        bbox = (left, upper, right, height)
        working_slice = img.crop(bbox)
        left += slice_size
        working_slice.save(os.path.join(outdir, "slice_" + str(count) + ".png"))
        count += 1


def image_to_rotate_clip(image_path):
    clip = ImageClip(image_path)
    rotated_clip = (clip.add_mask()
                    .fx(vfx.rotate, lambda t: 4 * t, expand=False)
                    .set_duration(4)).resize(lambda t: 1 + 0.115 * t)
    final_clip = CompositeVideoClip([rotated_clip.set_pos("center")])
    reverse_clip = final_clip.fx(vfx.time_mirror)
    final_clip = final_clip.subclip(0.5, -0.5)
    reverse_clip = reverse_clip.subclip(0.5, -0.5)
    to_write = concatenate_videoclips([final_clip, reverse_clip])
    return to_write
    # to_write.write_videofile("final2.mp4", fps=25)


# def freezing(clip
#            ):


def generate_intro(logo):
    image_clip = ImageClip(logo, duration=4).crossfadein(3)

    final = CompositeVideoClip([image_clip])

    return final


def audio_to_clip(audio, clip):
    audio_clip = AudioFileClip(audio)
    clip = clip.set_audio(audio_clip.set_duration(clip.duration))
    clip = clip.audio_fadeout(clip.duration - 2)
    return clip


def concate_two(clip1, clip2):
    clip1 = clip1.resize(clip2.size)
    conc = CompositeVideoClip([clip1, clip2.set_start(clip1.duration)])

    conc = conc.set_duration(clip1.duration + clip2.duration)

    return conc


multifast = [one_on_each_other]
multislow = [one_on_each_other]
onefast = [four_in_row, four_in_width]
oneslow = [image_to_rotate_clip, anim_pictures]

if __name__ == '__main__':
    pass
