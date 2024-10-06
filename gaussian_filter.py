import numpy as np
import timeit



#Create the gaussian kernal. This will be used to smooth the image. 
#https://en.wikipedia.org/wiki/Kernel_(image_processing)
#https://en.wikipedia.org/wiki/Gaussian_function#:~:text=.-,Two%2Ddimensional%20Gaussian%20function,-%5Bedit%5D
def gaussian_kernal(size,std):
    kernel = np.fromfunction(
        lambda x,y: np.divide(1,2*np.pi* std**2) * 
        np.exp(
            -((x-(size-1)/2)**2 + (y-(size-1)/2)**2) / (2* std**2)
               ),
        (size,size)

    )
    return np.array(kernel/np.sum(kernel))


#https://en.wikipedia.org/wiki/Kernel_(image_processing)#:~:text=the%20center%20element.-,Convolution,-%5Bedit%5D
def convolution(image,kernel_size,kernel_std):
    kernel = gaussian_kernal(kernel_size,kernel_std)
    x,y = image.shape
    #padding the image to ensure convolution hits every pixel of original image
    image_pad = np.pad(image,((kernel_size,kernel_size),(kernel_size,kernel_size)), mode='reflect')
    #created empty image to store output
    convolved_image = np.zeros((x,y), dtype=np.float32)
    print(np.average(image))
    start = timeit.default_timer()
    for i in range(x):
        for j in range(y):
            convolved_image[i,j] = np.sum(np.multiply(image_pad[i:i+kernel_size,j:j+kernel_size],kernel))
    end = timeit.default_timer()
    print(end-start)
    print(np.average(convolved_image))
    return convolved_image


def gaussian_filter(image_array,kernal):
    #calculate standard deviations along the x and y axii
    x_std = np.std(image_array, axis=1)
    y_std = np.std(image_array, axis=0)

    #define the 2d gaussian function. 

    first_half = np.divide(1/2*np.pi*x_std*y_std)
    exponent_fraction = -(image_array)