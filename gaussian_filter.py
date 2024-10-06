import numpy as np



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
    return kernel/np.sum(kernel)


kernel_test = gaussian_kernal(3,1)
#https://en.wikipedia.org/wiki/Kernel_(image_processing)#:~:text=the%20center%20element.-,Convolution,-%5Bedit%5D
def convolution(kernel, image):
    x,y = image.shape
    #padding the image 
    image_pad = np.pad(image,((3,3)), mode='reflect')
    print(image_pad.shape)
    #created empty image to store output
    convolved_image = np.zeros((x,y), dtype=np.float32)

    for i in range(image.shape[0]):
        for i in range(image.shape[1]):
            pass
    convolved_image = []

    pass

def gaussian_filter(image_array,kernal):
    #calculate standard deviations along the x and y axii
    x_std = np.std(image_array, axis=1)
    y_std = np.std(image_array, axis=0)

    #define the 2d gaussian function. 

    first_half = np.divide(1/2*np.pi*x_std*y_std)
    exponent_fraction = -(image_array)