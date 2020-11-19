# -*- coding: utf-8 -*-
# @Time    : 2018/11/6 16:45
# @Author  : tanlei0
# @FileName: Viewer.py
import pyglet
import numpy as np

class Viewer(pyglet.window.Window):
    # sheep and sheepdog use the global coords, only need parameter reward circle
    def __init__(self, sheepGroup_coords, sheepDog_coords, target, WIN_WIGHT, WIN_HEIGHT):
        super(Viewer, self).__init__(width=WIN_WIGHT, height=WIN_HEIGHT, resizable=False, caption='Sheepdog',
                                     vsync=False)
        pyglet.gl.glClearColor(1, 1, 1, 1)
        # load image
        self.sheep_image = pyglet.image.load('./image/point_b.png')
        sheepdog_image = pyglet.image.load('./image/point_k.png')
        red_image = pyglet.image.load('./image/point_red.png')
        green_image = pyglet.image.load('./image/point_green.png')
        target_image = pyglet.image.load('./image/circle-green.png')

        self.batch = pyglet.graphics.Batch()
        self.sprite_sheepGroup = []
        self.sprite_sheepDogGroup = []

        self.setSheepGroup(sheepGroup_coords)
        self.mouseCoords = np.zeros([1, 2])

        assert (sheepDog_coords.shape[1] == 2)

        for i in range(sheepDog_coords.shape[0]):
            self.sprite_sheepDogGroup.append(
                pyglet.sprite.Sprite(sheepdog_image, sheepDog_coords[i][0], sheepDog_coords[i][1],
                                     batch=self.batch))
            self.sprite_sheepDogGroup[i].scale = 0.8

        self.sprite_target = pyglet.sprite.Sprite(target_image, x=target[0], y=target[1], batch=self.batch)
        self.sprite_target.scale = 0.6

        self.label = pyglet.text.Label('', x=0, y=0, font_name='Times New Roman', font_size=20,
                                       color=[0, 0, 0, 255], batch=self.batch)

        self.sprite_red = pyglet.sprite.Sprite(red_image, 0, 0, batch=self.batch)
        self.sprite_red.scale = 0.3
        self.sprite_green = pyglet.sprite.Sprite(green_image, 0, 0, batch=self.batch)
        self.sprite_green.scale = 0.3

        # reward circle , maybe it can be removed ?
        # self.batch.add(circle.shape[0], pyglet.gl.GL_LINE_LOOP, None,
        #                ('v2f', circle.reshape(-1)), ('c3B', (0, 0, 0) * circle.shape[0]))

    def render(self, sheepGroup_coords, sheepDog_coords, kwargs={}):
        self._update(sheepGroup_coords, sheepDog_coords, kwargs)
        self.switch_to()
        self.dispatch_events()
        self.dispatch_event('on_draw')
        self.flip()

    def on_draw(self):
        self.clear()  # 清屏
        self.batch.draw()  # 画上 batch 里面的内容

    def _update(self, sheepGroup_coords, sheepDog_coords, kwargs):
        for i in range(sheepGroup_coords.shape[0]):
            self.sprite_sheepGroup[i].update(x=int(sheepGroup_coords[i][0]), y=int(sheepGroup_coords[i][1]))
        for i in range(sheepDog_coords.shape[0]):
            self.sprite_sheepDogGroup[i].update(x=int(sheepDog_coords[i][0]), y=int(sheepDog_coords[i][1]))
        if kwargs != {}:
            P_an = kwargs['P_an']
            P_GCM = kwargs['P_GCM']
            TaskLabel = kwargs['TaskLabel']
            self.sprite_red.update(x=int(P_an[0]), y=int(P_an[1]))
            self.sprite_green.update(x=int(P_GCM[0]), y=int(P_GCM[1]))
            self.label.text = TaskLabel

    def setSheepGroup(self, sheepGroup_coords):
        self.sprite_sheepGroup = []
        for i in range(sheepGroup_coords.shape[0]):
            self.sprite_sheepGroup.append(
                pyglet.sprite.Sprite(self.sheep_image, sheepGroup_coords[i][0], sheepGroup_coords[i][1], batch=self.batch))
            self.sprite_sheepGroup[i].scale = 0.7

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouseCoords = np.array([[x, y]])

