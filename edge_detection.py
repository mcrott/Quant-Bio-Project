from gaussian_filter import convol_fft
import numpy as np
import timeit




# Slow method for finding edges, 180secs for 2304x2304 image
def find_edges(image):
    kernel_size = 3
    vertical = np.array([[0.25, 0.00, -0.25],
                          [0.5,0.0,-0.5],
                          [0.25,0.0,-0.25]],dtype=np.float32)
    horizontal = np.array([
                            [0.25, 0.50, 0.25],
                            [0.0, 0.0, 0.0],
                            [-0.25, -0.5, -0.25]
                        ], dtype=np.float32)
    x,y = image.shape
    image_pad = np.pad(image,((kernel_size,kernel_size),(kernel_size,kernel_size)), mode='reflect')
    image_vert = np.zeros((x,y), dtype=np.float32)
    image_horz = np.zeros((x,y), dtype=np.float32)
    start = timeit.default_timer()
    for i in range(x):
        for j in range(y):
            image_vert[i,j] = np.sum(np.multiply(image_pad[i:i+kernel_size,j:j+kernel_size],vertical))
            image_horz[i,j] = np.sum(np.multiply(image_pad[i:i+kernel_size,j:j+kernel_size],horizontal))
    end = timeit.default_timer()
    print(end-start)
    return image_vert, image_horz
#0.8 seconnds for a 2304x2304 image

#https://en.wikipedia.org/wiki/Sobel_operator

# turns out I already implemented the Sobel Operator
def find_edges_fft(image,sobel_scaling):
    start = timeit.default_timer()
    kernel_size = 3
    pad_size = kernel_size // 2
    

    #sobel_scaling changes the sharpness of the edge detection. at 1, it is based on
    # the edge detection showing in 3brown1blue video, 4 is from wikipedia
    vertical = np.array([[0.25*sobel_scaling, 0.00, -0.25*sobel_scaling],
                          [0.5*sobel_scaling,0.0,-0.5*sobel_scaling],
                          [0.25*sobel_scaling,0.0,-0.25*sobel_scaling]],dtype=np.float32)
    horizontal = np.array([
                            [0.25*sobel_scaling, 0.50*sobel_scaling, 0.25*sobel_scaling],
                            [0.0, 0.0, 0.0],
                            [-0.25*sobel_scaling, -0.5*sobel_scaling, -0.25*sobel_scaling]
                        ], dtype=np.float32)
    x,y = image.shape
    image_pad = np.pad(image,((kernel_size,kernel_size),(kernel_size,kernel_size)), mode='reflect')
    
    pad_shape = (x + kernel_size - 1, y + kernel_size - 1)
    vert_pad = np.pad(vertical, 
                           ((0, image_pad.shape[0] - vertical.shape[0]), 
                            (0, image_pad.shape[1] - vertical.shape[1])), 
                           mode='constant')
    horz_pad = np.pad(horizontal, 
                           ((0, image_pad.shape[0] - horizontal.shape[0]), 
                            (0, image_pad.shape[1] - horizontal.shape[1])), 
                           mode='constant')
    vertical_edges = convol_fft(x,y,pad_shape,image_pad,vert_pad,pad_size)
    horizontal_edges = convol_fft(x,y,pad_shape,image_pad,horz_pad,pad_size)
    end = timeit.default_timer()
    print(end-start)
    return vertical_edges, horizontal_edges

#gradient magnitude
def grad_mag(horz,vert):
    return np.sqrt(((horz**2 + vert**2)))


