# Jupyter3DImageViewer

## Installation

``` bash
pip install -r requirements.txt
pip install .
```

## Usage

### Initialize the Viewer

``` python
from bokehView3D.bokehView3D import bokehView3D
from bokeh.io import output_notebook
viewer = bokehView3D()
output_notebook()
```

### Three different image viewers are provided in this package.

1. For a single 3D image:

``` python
viewer.imshow3d(img_full, axis=2, plot_size=0.8, img_res=(1, 1, 1))
```

![example image][image1]

[image1]:https://github.com/zhongnanf/Jupyter3DImageViewer/raw/master/imgs/1.png

2. For multiple 3D images:

``` python
viewer.compare_3d_imgs([img_full, img_brain], axis=2, plot_size=0.8, view_vertical=False, img_res=(1, 1, 1))
```

![example image][image2]

[image2]:https://github.com/zhongnanf/Jupyter3DImageViewer/raw/master/imgs/2.png

3. Overlapping two 3D images:

``` python
viewer.compare_aligned_3d(img_full, img_brain, axis=2, plot_size=0.8, img_res=(1, 1, 1))
```

![example image][image3]

[image3]:https://github.com/zhongnanf/Jupyter3DImageViewer/raw/master/imgs/3.png

To play with the examples, use "how to.ipynb". 
