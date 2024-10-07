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



# # scipy 1.18 seconds
# def convolution(image,kernel_size,kernel_std):
#     start = timeit.default_timer()

#     kernel = gaussian_kernal(kernel_size,kernel_std)

#     # convolved_image = sci.signal.fftconvolve(image,kernel)
#     convolved_image = np.convolve(image,kernel)
#     print(convolved_image)
#     end = timeit.default_timer()
#     print(end-start)

#original approach, 2.12 seconds
#fft*fft method: 0.01 seconds


#originial approach - slow, however correct
# def convolution(image,kernel_size,kernel_std):
#     kernel = gaussian_kernal(kernel_size,kernel_std)
#     x,y = image.shape
#     #padding the image to ensure convolution hits every pixel of original image
#     image_pad = np.pad(image,((kernel_size,kernel_size),(kernel_size,kernel_size)), mode='reflect')
#     #created empty image to store output
#     convolved_image = np.zeros((x,y), dtype=np.float32)
#     start = timeit.default_timer()
#     for i in range(x):
#         for j in range(y):
#             convolved_image[i,j] = np.sum(np.multiply(image_pad[i:i+kernel_size,j:j+kernel_size],kernel))
#     end = timeit.default_timer()
#     print(end-start)
#     return convolved_image

#fft to make things fast 
#https://en.wikipedia.org/wiki/Kernel_(image_processing)#:~:text=the%20center%20element.-,Convolution,-%5Bedit%5D
def convolution(image,kernel_size,kernel_std):
    kernel = gaussian_kernal(kernel_size,kernel_std)
    x,y = image.shape
    #padding the image to ensure convolution hits every pixel of original image
    # Padding size based on kernel size
    pad_size = kernel_size // 2
    # pad to ensure adequate coverage
    image_pad = np.pad(image, ((pad_size, pad_size), (pad_size, pad_size)), mode='reflect')
    # Pad the kernel to match the size of the padded image
    kernel_padded = np.pad(kernel, 
                           ((0, image_pad.shape[0] - kernel.shape[0]), 
                            (0, image_pad.shape[1] - kernel.shape[1])), 
                           mode='constant')
    #created empty image to store output
    pad_shape = (x + kernel_size - 1, y + kernel_size - 1)
    convolved_image = np.zeros(pad_shape, dtype=np.float32)
    convolved = np.fft.fft2(image_pad)
    raw = convolved * np.fft.fft2(kernel_padded,s=image_pad.shape)
    convolved_image = np.fft.ifft2(raw)
    convolved_image = np.real(convolved_image)[pad_size:pad_size+x, pad_size:pad_size+y]
   
    return convolved_image
def convol_fft(x,y,pad_shape,padded_image, padded_kernel,pad_size):
    convolv_image = np.zeros(pad_shape,dtype=np.float32)
    convolv = np.fft.fft2(padded_image)
    raw_convol = convolv * np.fft.fft2(padded_kernel,s=padded_image.shape)
    convolv_image = np.fft.ifft2(raw_convol)
    convolv_image = np.real(convolv_image)[pad_size:pad_size+x, pad_size:pad_size+y]
    
    return convolv_image

# def convolution(image,kernel_size,kernel_std):
#     kernel = gaussian_kernal(kernel_size,kernel_std)
#     x,y = image.shape
#     #padding the image to ensure convolution hits every pixel of original image
#     image_pad = np.pad(image,((kernel_size,kernel_size),(kernel_size,kernel_size)), mode='reflect')
#     #created empty image to store output
#     convolved_image = np.zeros((x,y), dtype=np.float32)
#     print(np.average(image))
#     start = timeit.default_timer()
#     for i in range(x):
#         for j in range(y):
#             convolved_image[i,j] = np.sum(np.multiply(image_pad[i:i+kernel_size,j:j+kernel_size],kernel))
#     end = timeit.default_timer()
#     print(end-start)
#     print(np.average(convolved_image))
#     return convolved_image


def gaussian_filter(image_array,kernel):
    #calculate standard deviations along the x and y axii
    x_std = np.std(image_array, axis=1)
    y_std = np.std(image_array, axis=0)

    #define the 2d gaussian function. 

    first_half = np.divide(1/2*np.pi*x_std*y_std)
    exponent_fraction = -(image_array)