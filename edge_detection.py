from gaussian_filter import convol_fft
import numpy as np
import timeit
from PIL import Image
import cv2 as cv
np.random.seed(212312312)


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
    normalized = (np.sqrt(((horz**2 + vert**2))))
    directions = np.arctan2(vert,horz)
    #directions: convert rads to degrees and add 180
    return normalized, directions


#321 ---------- 213

'''321 - 213 / 0.1


'''
def interpolate_magnitudes(mags, direction, i, j):
    angle = direction[i, j] * (180 / np.pi)  # Convert radians to degrees
    angle = angle % 180  # Normalize angle to [0, 360)

    if (angle >= 0 and angle < 22.5) or (angle >= 157.5 and angle < 180):
        # East-West
        Y = mags[i, j + 1]  # East
        Q = mags[i, j - 1]  # West
    elif angle >= 22.5 and angle < 67.5:
        # North-East
        Y = (mags[i - 1, j + 1] * (1 - (angle - 22.5) / 45) +
             mags[i, j + 1] * ((angle - 22.5) / 45))
        Q = (mags[i + 1, j - 1] * (1 - (angle - 22.5) / 45) +
             mags[i, j - 1] * ((angle - 22.5) / 45))
    elif angle >= 67.5 and angle < 112.5:
        # North-South
        Y = mags[i - 1, j]  # North
        Q = mags[i + 1, j]  # South
    elif angle >= 112.5 and angle < 157.5:
        # North-West
        Y = (mags[i - 1, j - 1] * (1 - (angle - 112.5) / 45) +
             mags[i, j - 1] * ((angle - 112.5) / 45))
        Q = (mags[i + 1, j + 1] * (1 - (angle - 112.5) / 45) +
             mags[i, j + 1] * ((angle - 112.5) / 45))

    return Y, Q

def non_maximum_suppression(mags, direction):
    height, width = mags.shape
    output = np.zeros_like(mags)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            # Interpolate neighboring gradient magnitudes
            Y, Q = interpolate_magnitudes(mags, direction, i, j)

            # Suppress non-maxima
            if mags[i, j] >= Y and mags[i, j] >= Q:
                output[i, j] = mags[i, j]
            else:
                output[i, j] = 0

    return output




#102.92198704200564 sec for 2304x2304
def non_max_supression(mags,direction):

    x,y = mags.shape
    start = timeit.default_timer()

    output = np.zeros((x,y),dtype=np.int32)
    qy_vals = []
    for i in range(1,x-1):
        for j in range(1,y-1):
            try:
                #placeholders
                Y = 255
                Q = 255
                #Add interpolation 
                #north->south
                if direction[i,j] == 90 or direction[i,j] == 270:
                    Y = mags[i-1,j] #north
                    Q = mags[i+1,j] #south
                #east->west
                elif direction [i,j] == 0 or direction [i,j] == 180:
                    Y = mags[i,j+1] #east
                    Q = mags[i,j-1] #west
                #NE->SW

                elif   0 < direction[i,j] < 90 or 180 < direction[i,j] < 270:
    
                    #interpolation by competence or incompetence? Lets see if it works
                    Y = ((mags[i-1,j] - mags[i-1,j+1])*np.cos(np.deg2rad(direction[i,j]))) + mags[i-1,j]
                    #This might be wrong. 
                    Q = ((mags[i+1,j] - mags[i+1,j-1])*np.cos(np.deg2rad(direction[i,j]))) + mags[i+1,j-1]
                    
                #NW->SE
                elif 90 < direction[i,j] < 180 or 270 < direction[i,j] < 360:
                    #interpolation by competence or incompetence? Lets see if it works
                    Y = ((mags[i-1,j] - mags[i-1,j-1])*np.cos(np.deg2rad(direction[i,j]))) + mags[i-1,j-1]
                    #This might be wrong. 
                    Q = ((mags[i+1,j] - mags[i+1,j+1])*np.cos(np.deg2rad(direction[i,j]))) + mags[i+1,j]
                    
                qy_vals.append([Q,Y])
                if mags[i,j] >= Y and mags[i,j] >= Q:
                    output[i,j] = output[i,j]
                elif mags[i,j] < Y or mags[i,j] < Q:
                    output[i,j] = 0
            
            except IndexError as e:
                pass

    end = timeit.default_timer()
    print(end-start)
    return output