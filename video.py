import main
from moviepy.editor import *
import moviepy.video.fx.all as vfx

list = []
list.append('/home/filipcaladi/Desktop/suflikanti_unit/images/newyork.jpg')
list.append('/home/filipcaladi/Desktop/suflikanti_unit/images/stars.jpg')
list.append('/home/filipcaladi/Desktop/suflikanti_unit/images/tma.jpg')

video1 = main.one_on_each_other(list)#intro_logo_with_background('/home/filipcaladi/Desktop/suflikanti_unit/Dense_fog_ahead_of_Forest.mp4','/home/filipcaladi/Desktop/suflikanti_unit/logo6.png')
video1.write_videofile("test.mp4", fps=24)