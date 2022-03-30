# View 3D images in Jupyter with Bokeh library
# Author: Zhongnan Fang
# zhongnanf@gmail.com

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, GlyphRenderer, Range1d
from bokeh.io import push_notebook, output_notebook
import ipywidgets
from IPython.display import display
import numpy as np


class bokehView3D:

    def __init__(self):
        output_notebook()

    def imshow3d(self, img, axis=0, plot_size=1, img_res=(1, 1, 1)):

        img = self.format_view(img, axis)
        nslices = img.shape[2]
        img_slc = img[:, :, 0]

        size_x = img_slc.shape[0]
        size_y = img_slc.shape[1]
        phys_scale = 10 / np.max([size_x, size_y])

        phys_scale_x = 1.0
        if axis == 0:
            phys_scale_y = img_res[0] / img_res[1]
        elif axis == 1:
            phys_scale_y = img_res[1] / img_res[2]
        else:
            phys_scale_y = img_res[0] / img_res[2]

        if phys_scale_y < 1.0:
            ratio = 1.0 / phys_scale_y
            phys_scale_x *= ratio
            phys_scale_y *= ratio

        phys_size_x = size_x * phys_scale * phys_scale_x
        phys_size_y = size_y * phys_scale * phys_scale_y
        plot_width = int(phys_size_y * 50 * plot_size)
        plot_height = int(phys_size_x * 50 * plot_size)

        palette = ['#%02x%02x%02x' % (i, i, i) for i in range(256)]
        fig_t = figure(x_range=(0, phys_size_x),
                       y_range=(0, phys_size_y),
                       plot_width=plot_width,
                       plot_height=plot_height)
        fig_t.axis.visible = False
        img_t = fig_t.image(image=[img_slc],
                            x=[0],
                            y=[0],
                            dw=phys_size_x,
                            dh=phys_size_y,
                            palette=palette,
                            name='img3d')
        bk_t = show(fig_t, notebook_handle=True)

        layout = ipywidgets.Layout(width='%dpx' % plot_width)
        sld = ipywidgets.IntSlider(min=0,
                                   max=nslices - 1,
                                   step=1,
                                   value=0,
                                   layout=layout)
        sld_tool = ipywidgets.HBox([ipywidgets.Label('Slice'), sld])

        def slider_value_changed(change):
            img_slc = img[:, :, sld.value]
            renderer = fig_t.select(dict(name='img3d', type=GlyphRenderer))
            img_t.data_source.data['image'] = [img_slc]
            push_notebook(handle=bk_t)

        sld.observe(slider_value_changed)
        display(sld_tool)

    def compare_3d_imgs(self,
                        imgs,
                        axis=0,
                        plot_size=1,
                        view_vertical=True,
                        img_res=(1, 1, 1)):

        nimgs = len(imgs)
        imgs2 = []
        for cnt1 in range(nimgs):
            imgs[cnt1] = self.normalize_img(imgs[cnt1])
            self.format_view(imgs[cnt1], axis)
            imgs2.append(self.format_view(imgs[cnt1], axis))

        size_x = imgs2[0].shape[0]
        size_y = imgs2[0].shape[1]
        nslices = imgs2[0].shape[2]

        phys_scale = 10 / np.max([size_x, size_y])

        phys_scale_x = 1.0
        if axis == 0:
            phys_scale_y = img_res[0] / img_res[1]
        elif axis == 1:
            phys_scale_y = img_res[1] / img_res[2]
        else:
            phys_scale_y = img_res[0] / img_res[2]

        if phys_scale_y < 1.0:
            ratio = 1.0 / phys_scale_y
            phys_scale_x *= ratio
            phys_scale_y *= ratio

        phys_size_x = int(size_x * phys_scale * phys_scale_x)
        phys_size_y = int(size_y * phys_scale * phys_scale_y)

        if view_vertical:
            plot_width = int(phys_size_y * 50 * plot_size)
            plot_height = int(phys_size_x * 50 * plot_size * nimgs)
        else:
            plot_width = int(phys_size_y * 50 * plot_size * nimgs)
            plot_height = int(phys_size_x * 50 * plot_size)

        fig_t = figure(x_range=(0, phys_size_x),
                       y_range=(0, phys_size_y),
                       match_aspect=True,
                       plot_width=plot_width,
                       plot_height=plot_height)
        fig_t.axis.visible = False

        if view_vertical:
            fig_t.x_range = Range1d(0, phys_size_x)
            fig_t.y_range = Range1d(0, phys_size_y * nimgs)
        else:
            fig_t.x_range = Range1d(0, phys_size_x * nimgs)
            fig_t.y_range = Range1d(0, phys_size_y)

        palette = ['#%02x%02x%02x' % (i, i, i) for i in range(256)]
        img_t = []

        for cnt1 in range(nimgs):
            if view_vertical:
                xloc = 0
                yloc = phys_size_y * (nimgs - cnt1 - 1)
            else:
                xloc = phys_size_x * cnt1
                yloc = 0

            tmp = fig_t.image(image=[imgs2[cnt1][:, :, 0]],
                              x=[xloc],
                              y=[yloc],
                              dw=phys_size_x,
                              dh=phys_size_y,
                              palette=palette,
                              name='img3d%d' % cnt1)
            img_t.append(tmp)

        bk_t = show(fig_t, notebook_handle=True)

        layout = ipywidgets.Layout(width='%dpx' % plot_width)
        sld = ipywidgets.IntSlider(min=0,
                                   max=nslices - 1,
                                   step=1,
                                   value=0,
                                   layout=layout)
        sld_tool = ipywidgets.HBox([ipywidgets.Label('Slice'), sld])

        def slider_value_changed(change):
            for cnt1 in range(nimgs):
                renderer = fig_t.select(
                    dict(name='img3d%d' % cnt1, type=GlyphRenderer))
                img_t[cnt1].data_source.data['image'] = [
                    imgs2[cnt1][:, :, sld.value]
                ]
            push_notebook(handle=bk_t)

        sld.observe(slider_value_changed)
        display(sld_tool)

    def compare_aligned_3d(self,
                           img1,
                           img2,
                           axis=0,
                           plot_size=1,
                           img_res=(1, 1, 1)):

        img1 = self.normalize_img(self.format_view(img1, axis)) * 255
        img2 = self.normalize_img(self.format_view(img2, axis)) * 255
        img1 = np.expand_dims(img1.astype(np.uint8), axis=3)
        img2 = np.expand_dims(img2.astype(np.uint8), axis=3)
        ch3 = np.zeros(img1.shape, dtype=np.uint8)
        alpha = np.ones(img1.shape, dtype=np.uint8) * 255
        img = np.concatenate([img1, img2, ch3, alpha], axis=3)

        nslices = img.shape[2]

        size_x = img.shape[0]
        size_y = img.shape[1]
        phys_scale = 10 / np.max([size_x, size_y])
        phys_scale_x = 1.0
        if axis == 0:
            phys_scale_y = img_res[0] / img_res[1]
        elif axis == 1:
            phys_scale_y = img_res[1] / img_res[2]
        else:
            phys_scale_y = img_res[0] / img_res[2]

        if phys_scale_y < 1.0:
            ratio = 1.0 / phys_scale_y
            phys_scale_x *= ratio
            phys_scale_y *= ratio
        phys_size_x = size_x * phys_scale * phys_scale_x
        phys_size_y = size_y * phys_scale * phys_scale_y

        plot_width = int(phys_size_y * 50 * plot_size)
        plot_height = int(phys_size_x * 50 * plot_size)

        fig_t = figure(x_range=(0, phys_size_x),
                       y_range=(0, phys_size_y),
                       plot_width=plot_width,
                       plot_height=plot_height)

        img_slc = np.empty((size_x, size_y), dtype=np.uint32)
        view = img_slc.view(dtype=np.uint8).reshape((size_x, size_y, 4))
        view[...] = img[:, :, 0, :]

        fig_t.axis.visible = False
        img_t = fig_t.image_rgba(image=[img_slc],
                                 x=[0],
                                 y=[0],
                                 dw=phys_size_x,
                                 dh=phys_size_y,
                                 name='img_aligned_3d')
        bk_t = show(fig_t, notebook_handle=True)

        layout = ipywidgets.Layout(width='%dpx' % plot_width)
        sld = ipywidgets.IntSlider(min=0,
                                   max=nslices - 1,
                                   step=1,
                                   value=0,
                                   layout=layout)
        sld_tool = ipywidgets.HBox([ipywidgets.Label('Slice'), sld])

        def slider_value_changed(change):
            view[...] = img[:, :, sld.value, :]
            renderer = fig_t.select(dict(name='img3d', type=GlyphRenderer))
            img_t.data_source.data['image'] = [img_slc]
            push_notebook(handle=bk_t)

        sld.observe(slider_value_changed)
        display(sld_tool)

    def format_view(self, img, view):
        """ format raw nifti data into conventional views
            Inputs:
                img: the raw nifti data 3D matrix
                view: the view wanted
                      0. Axial
                      1. Sagittal
                      2. Coronal
            Output:
                img: the formated image
        """
        if (view == 1):
            img = np.transpose(img, (2, 1, 0))
            img = img[:, ::-1, :]
        elif (view == 2):
            img = np.transpose(img, (2, 0, 1))
            img = img[:, :, ::-1]
        else:
            img = np.transpose(img, (1, 0, 2))
            img = img[:, :, ::-1]
        return img

    def normalize_img(self, img):
        imgmax = np.max(img)
        imgmin = np.min(img)
        img2 = (img - imgmin) / (imgmax - imgmin)
        return img2