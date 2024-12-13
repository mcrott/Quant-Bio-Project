import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import skimage.io as io
from scipy.spatial.distance import cdist
from sklearn.linear_model import LinearRegression
import matplotlib.animation as animation
def msd_fft(r):
                """This is function that calculates the MSD. This was copied from the stack exchange link below, so all credit goes to that post
                
                https://stackoverflow.com/questions/34222272/computing-mean-square-displacement-using-python-and-fft
                Args:
                    r (array): input array in x,y(,z) 

                Returns:
                    array: Returns the MSD values for that track. 
                """
                def autocorrFFT(x):
                        N=len(x)
                        F = np.fft.fft(x, n=2*N)  #2*N because of zero-padding
                        PSD = F * F.conjugate()
                        res = np.fft.ifft(PSD)
                        res= (res[:N]).real   #now we have the autocorrelation in convention B
                        n=N*np.ones(N)-np.arange(0,N) #divide res(m) by (N-m)
                        return res/n #this is the autocorrelation in convention A
                N=len(r)
                D=np.square(r).sum(axis=1) 
                D=np.append(D,0) 
                S2=sum([autocorrFFT(r[:, i]) for i in range(r.shape[1])])
                Q=2*D.sum()
                S1=np.zeros(N)
                for m in range(N):
                        Q=Q-D[m-1]-D[N-m]
                        S1[m]=Q/(N-m)
                return S1-2*S2  
class Objects:
    def __msd_fft(self,r):
                """This is function that calculates the MSD. This was copied from the stack exchange link below, so all credit goes to that post
                
                https://stackoverflow.com/questions/34222272/computing-mean-square-displacement-using-python-and-fft
                Args:
                    r (array): input array in x,y(,z) 

                Returns:
                    array: Returns the MSD values for that track. 
                """
                def autocorrFFT(x):
                        N=len(x)
                        F = np.fft.fft(x, n=2*N)  #2*N because of zero-padding
                        PSD = F * F.conjugate()
                        res = np.fft.ifft(PSD)
                        res= (res[:N]).real   #now we have the autocorrelation in convention B
                        n=N*np.ones(N)-np.arange(0,N) #divide res(m) by (N-m)
                        return res/n #this is the autocorrelation in convention A
                N=len(r)
                D=np.square(r).sum(axis=1) 
                D=np.append(D,0) 
                S2=sum([autocorrFFT(r[:, i]) for i in range(r.shape[1])])
                Q=2*D.sum()
                S1=np.zeros(N)
                for m in range(N):
                        Q=Q-D[m-1]-D[N-m]
                        S1[m]=Q/(N-m)
                return S1-2*S2
    def flatten_coords(self,list_of_lists):
        return [sublist[1] for sublist in list_of_lists if len(sublist) > 1]
    def initial_blobs(self):
        list_frames = list(frame_dict.keys())
        first_frame = self.frames[list_frames[0]]
        for i in range(len(first_frame)):
            self.blobs[f"Blob {self.num_blobs + 1}"] = [first_frame[i]]
            self.num_blobs = len(self.blobs.keys())
        self.current_blobs.append(list(self.blobs.keys()))
        return  
    def __init__(self,frame_dict):
        #this will contain all the blobs
        self.frames = frame_dict
        num_frames = len(frame_dict.keys())
        self.blobs: dict = {}
        self.num_blobs = len(self.blobs.keys())
        self.current_blobs = []
        self.msd = []
        self.msd_weights = []
        self.diff_coef = []
        self.diff_r2 = []
        self.removal_report = {}
        self.pdf = False
        self.name = "Quant Bio Project"
        
        self.initial_blobs()
    #new input is going to add blobs based on the cost matrix
    def elucidian_distance(self,n_coords,n1_coords):
        # based on 2d distance formula of sqrt((x2-x1)**2 + (y2-y1)**2))
        x1 = n_coords[0]
        y1 = n_coords[1]
        x2 = n1_coords[0]
        y2 = n1_coords[1]
        distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        return distance
    def distance_thresholding(self,distance,threshold):
        if distance > threshold:
            return False
        else:
            return True
    def pairing(self,matrix,coords_n,coords_n1):
        rows = matrix.min(axis=1).argsort()
        cols = matrix.argmin(axis=1)[rows]
        usedRows = set()
        usedCols = set()
        unpaired_rows = set()
        unpaired_cols = set()
        pairs = []
        unpaired = []
        for row,col in zip(rows,cols):
            #skips previously used rows/columns
            if row in usedRows or col in usedCols:
                continue
            n= coords_n[row]
            n1 = coords_n1[col]
            distance = self.elucidian_distance(n,n1)
            if self.distance_thresholding(distance,15) == True:
                    pairs.append([n,n1])
                    usedRows.add(row)
                    usedCols.add(col)
            if row in unpaired_rows or col in unpaired_cols:
                continue
            if self.distance_thresholding(distance,15) != True:
                    unpaired.append([n,n1])
                    unpaired_rows.add(row)
                    unpaired_cols.add(col)
            
                
                

        return pairs,unpaired
    def add_blob(self,add):
        self.blobs[f"Blob {self.num_blobs + 1}"] = [add]
        self.num_blobs += 1
    def find_contours_in_frame(self,val,frame = True):
        #current = true
        if frame == True:
            n = self.current_frame
            list_to_enum = self.flatten_coords(self.frames[n])
            for index, sublist in enumerate(list_to_enum):
                if sublist == val:
                    #returns the index of self.frames[current]
                    return index
        if frame == False:
            n1 = self.next_frame
            list_to_enum = self.flatten_coords(self.frames[n1])
            for index, sublist in enumerate(list_to_enum):
                if sublist == val:
                    #returns the index of self.frames[current]
                    return index
    def praying_for_blobs(self,pairs,unpairs,n,n1):
        list_of_keys = list(self.blobs.keys())
        count = 0
        peared = set()
        for p_index,p_sublist in enumerate(pairs):
            for j in self.blobs:
                val = self.blobs[j]
                if p_sublist[0] == val[-1][1]:
                    for index, sublist in enumerate(n1):
                         if sublist == p_sublist[1]:
                             self.blobs[j].append(self.frames[self.next_frame][index])
                             peared.add(p_index)
        for p_index,p_sublist in enumerate(pairs):
            if p_index in peared:
                continue
            for index, sublist in enumerate(n):
                    if sublist == p_sublist[0]:
                        self.add_blob(self.frames[self.current_frame][index])
        for up_index,up_sublist in enumerate(unpairs):
            for index, sublist in enumerate(n):
                if sublist == up_sublist[0]:
                    self.add_blob(self.frames[self.current_frame][index])

        #shameless chatgpt
        for indices in range(len(pairs)):
            if indices in peared:
                continue   
    def new_input(self,n,n1):
        self.current_frame = n
        self.next_frame = n1
        coords_n = flatten_coords(self.frames[n]) #current
        coords_n1 = flatten_coords(self.frames[n1]) #next frame
        cost_matrix = cdist(coords_n,coords_n1)
        pairs,unpairs = self.pairing(cost_matrix,coords_n,coords_n1)
        self.praying_for_blobs(pairs,unpairs,coords_n,coords_n1)
    def updateblobs(self,threshold):
        #remove low track num blobs
        placeholder_dict: dict = {}
        max = 0
        for blob in self.blobs:
            if len(self.blobs[blob]) > threshold:

                placeholder_dict[blob] = self.blobs[blob]
            if len(self.blobs[blob]) > max:
                 max = len(self.blobs[blob])
        self.blobs = placeholder_dict
        self.num_blobs = len(self.blobs.keys())
        self.max_spots = max
    def msd_compute(self):
                """MSD Computation based on msdanalyzer computeMSD function.  msd.fft calculation is pulled from stack exchange(see that function for the link)
                """
                coords_list = []
                for blobs in self.blobs:
                    coords_list.append(self.flatten_coords(self.blobs[blobs]))
                
                frameint = 20 #ms
                     

                msd_fast = {}
                tolerance = 12
                max_spots = self.max_spots
                self.timepoints = np.arange(0,max_spots)*frameint
                         
                #update coords list
                for i in range(self.num_blobs):
                        weights = np.arange(1,len(coords_list[i])+1)
                        reversed_weights = weights[::-1]
                        results = (self.__msd_fft(np.array(coords_list[i])))
                        #setting t0 to 0 do 
                        results[0] = 0
                        prenan = np.empty((max_spots - len(coords_list[i])))
                        prenan[:] = np.nan
                        zers = np.zeros((max_spots - len(coords_list[i])))
                        # c is for weights
                        #b is results 
                        c = np.concatenate([reversed_weights,zers])
                        b = np.concatenate([results,prenan])
                        msd_fast[i] = [self.timepoints,b,c]
                        #updating self
                        self.msd.append(b)
                        self.msd_weights.append(c)     
            
                return
    def pull_out_xy_vals(self):
        x = []
        y = []
        frames = []
        for j in self.blobs:
                x_values, y_values = zip(*self.flatten_coords(self.blobs[j]))
                x.append(x_values)
                y.append(y_values)
                first_elements = [sublist[0] for sublist in self.blobs[j]]
                frames.append(first_elements)
        self.x = x
        self.y = y
        self.unique_frames = frames           
    def calc_diffusion(self, dimension = None, clipfactor = None,filter = False,filter_r2 = None):
                num_filtered = 0
                self.ntracks = len(self.msd)
                removed_indices = []
                if clipfactor == None:
                        clip = 0.25
                else: 
                        if clipfactor > 1:
                                clip = 1
                        if clipfactor < 0:
                                clip = 0
                        if clipfactor <= 1 or clipfactor >= 0:
                                clip = clipfactor
                if filter == True and filter_r2 != None: 
                        filter_val_r2 = filter_r2
                if filter == True and filter_r2 == None:
                        filter_val_r2 = 0.8
                if dimension == None:
                        n = 2
                if dimension != None:
                        n = dimension
                # MSD = 2nDt
                time = self.timepoints
               
                coef = []
                inter = []
                #same idea for loglog, just dont take the log of the values
                print("Calculating diffusion coeffcient in uM^2/s through the weighted linear fit of " + str(self.num_blobs) + " MSD curves.")
                print("Only taking the first " + str(int(clip*100)) + " percent of each MSD curve. ") 
                if filter_r2 == True:
                        print("Filtering out tracks that have an r2 value below " + str(filter_val_r2))
                for i in range(len(self.msd)):
                        #REMOVE LATER   
                        msds= self.msd[i]
                        valid = ~np.isnan(msds)
                        y = self.msd[i][valid]
                        x = time[valid].reshape((-1,1))
                        weights = self.msd_weights[i][valid]
                        length = int(np.round(len(y)*clip))
                        x_axis = x[:length]
                        y_axis = y[:length]
                        # if x_axis.shape == (0,) or y_axis.shape == (0,) or len(x_axis) < 5:
                        #         num_filtered += 1
                        #         removed_indices.append(False)
                        #         continue
                        model = LinearRegression().fit(x_axis,y_axis,sample_weight=weights[:length])
                        # Diffusion_Coefficient = MSD/2n
                        r2 = model.score(x_axis,y_axis)

                        # if filter == True and (r2 < filter_val_r2 or r2 == np.nan) :
                        #         removed_indices.append(False)
                        #         num_filtered += 1
                        #         continue
                        coef.append(model.coef_)
                        inter.append(model.intercept_)
                        diff = np.divide(model.coef_, 2*n)
                        removed_indices.append(True)
                        self.diff_coef.append(float(diff[0]))
                        self.diff_r2.append(r2)
                self.intercept = inter
                self.coef = coef
    def post_filter_plot_tracks(self):
                self.space_units = 'uM'
                fig,ax = plt.subplots()
                for i in range(self.num_blobs):
                        ax.plot(self.x[i], self.y[i],linewidth =0.25)
                ax.set_xlabel("X " + self.space_units)
                ax.set_ylabel("Y " + self.space_units)
                self.name = "Quant Bio Project"
                self.min_max = {'X-Max': 256, 'X-Min': 0,'Y-Max': 256, 'Y-Min': 0,  }
                ax.set(xlim=(self.min_max['X-Min']-3, self.min_max['X-Max']+3), ylim=(self.min_max['Y-Min']-3, self.min_max['Y-Max']+3))


                plt.title(f'Tracks of {self.name}')
                plt.axis('equal')
                if self.pdf == True:
                        plt.savefig(self.path + '\\' +self.name +"_tracks_post.pdf",dpi=300,format='pdf')
                else:
                        plt.savefig(r"tracks_plot.png" ,dpi=300)
    def plot_mean_msd_diffusion(self):
                fig, ax = plt.subplots()

                vals = self.msd_average[self.msd_average > 0]
                # 
                self.mean_std = np.nan_to_num(self.mean_std,0)
                ax.plot(self.timepoints[:len(vals)],vals)

                ax.errorbar(self.timepoints[:len(vals)],vals,yerr = self.mean_std[:len(vals)],alpha = 0.25)

                m_len = int(len(vals)*0.25)

                m = self.timepoints[:len(vals)].reshape(-1, 1)

                model = LinearRegression().fit(m[:m_len],vals[:m_len])
                d_r2 = model.score(m[:m_len],vals[:m_len])

                y= (model.coef_)
                b = np.average(model.intercept_)
                funct = y*m+b

                ax.set_xlabel(r"(Δt)(s)")
                ax.set_ylabel(r'(MSD)($µm^{2}$)')
                ax.plot(m,funct,color='black')
                plt.title(f"Mean MSD Plot with Diffusion Slope of {self.name}", wrap=True )
                diff_value = y/(2*self.dimensions)
                plt.text(0.55,0.9,f"D = {diff_value[0]:.2e} $µm^{2}/s$",wrap=True,transform=ax.transAxes)
                plt.text(.55, 0.85,f"$R^{2}$ = {round(d_r2,3)}",wrap=True,transform=ax.transAxes)
                plt.ylim(0,max(self.msd_average)+0.15)

                if self.pdf == True:
                        plt.savefig(self.path + '\\' +self.name +"_msd-plot.pdf",dpi=300,format='pdf')
                else:
                        plt.savefig("/Users/cmdb/Quant_Bio_Project/Quant-Bio-Project/mean_diffusion_msd.png",dpi=300)   
    def plot_msd(self):
            fig,ax = plt.subplots()
            ax.set_xlabel(r"(Δt)(s)")
            ax.set_ylabel(r'(MSD)($µm^{2}$)')
            plt.title(f" MSD Plot of {self.name}", wrap=True )
            for a in range(0,len(self.msd)):
                    ax.plot(self.timepoints,self.msd[a])
            if self.pdf == True:
                    plt.savefig(self.path + '\\' +self.name +"_msd-plot.pdf",dpi=300,format='pdf')
            else:
                    plt.savefig(r"msd_plot.png" ,dpi=300)    
    def calc_mean_msd(self):
        """Calculates the mean MSD among remaining tracks post diffusion/loglog removal. 
        
        This can be called before removal. Function call order in spt_workflow.py should be updated.

        Returns:
            self.msd_average is updated with the values
        """
        #updating timepoints incase there was a track removal
        msd_data = np.copy(self.msd)
        #checking to see if the msd computation has been completed
        if self.num_blobs == None:
                return print("You have not calculated any MSDs with msd_compute()")
        time = self.timepoints
        sum_weights = np.zeros(len(time))
        for i in self.msd_weights:
                sum_weights = sum_weights + i 
        sum_msd_weights = np.zeros(len(time))
        for i in range(0,len(msd_data)):                    
                msd_w = self.msd_weights
                #boolean indexing to determine what to keep
                valid = ~np.isnan(msd_data[i])
                msd_valid = msd_data[i][valid]
                sum_msd_weights[valid] += np.multiply(msd_valid,msd_w[i][valid])      
                
        mean_msd = np.divide(sum_msd_weights,sum_weights)       
        self.msd_average = mean_msd
        
        #weighted varience 
        sum_weighted_varience = np.zeros(len(time))
        sum_sq_weight = np.zeros(len(time))
        
        for i in range(0,len(msd_data)):
                val = ~np.isnan(msd_data[i])
                alpha = msd_data[i][val]
                msd_weights = self.msd_weights
                nums = msd_weights[i][val]   
                sum_weighted_varience[val] += np.multiply(nums,((alpha - mean_msd[val])**2))
                sum_sq_weight[val] += nums**2
        
        std_calc_first_bot =  (sum_weights**2 - sum_sq_weight)      
        std_calc_first = sum_weights / std_calc_first_bot
        std_calc = np.sqrt(np.multiply(std_calc_first,sum_weighted_varience))
        nfreedom = (np.divide(sum_weights**2, sum_sq_weight))
        
        
        self.mean_degree_freedom = nfreedom
        self.mean_std = std_calc
        return   
    def plot_mean_msd_diffusion(self):
                fig, ax = plt.subplots()
                self.dimensions = 2

                vals = self.msd_average[self.msd_average > 0]
                # 
                self.mean_std = np.nan_to_num(self.mean_std,0)
                ax.plot(self.timepoints[:len(vals)],vals)

                ax.errorbar(self.timepoints[:len(vals)],vals,yerr = self.mean_std[:len(vals)],alpha = 0.25)

                m_len = int(len(vals)*0.25)

                m = self.timepoints[:len(vals)].reshape(-1, 1)

                model = LinearRegression().fit(m[:m_len],vals[:m_len])
                d_r2 = model.score(m[:m_len],vals[:m_len])

                y= (model.coef_)
                b = np.average(model.intercept_)
                funct = y*m+b

                ax.set_xlabel(r"(Δt)(s)")
                ax.set_ylabel(r'(MSD)($µm^{2}$)')
                ax.plot(m,funct,color='black')
                plt.title(f"Mean MSD Plot with Diffusion Slope of {self.name}", wrap=True )
                diff_value = y/(2*self.dimensions)
                plt.text(0.55,0.9,f"D = {diff_value[0]:.2e} $µm^{2}/s$",wrap=True,transform=ax.transAxes)
                plt.text(.55, 0.85,f"$R^{2}$ = {round(d_r2,3)}",wrap=True,transform=ax.transAxes)
                plt.ylim(0,max(self.msd_average)+0.15)
                if self.pdf == True:
                        plt.savefig(self.path + '\\' +self.name +"_msd-plot.pdf",dpi=300,format='pdf')
                else:
                        plt.savefig(r"mean_msd_plot.png",dpi=300) 
  
def gaussian_kernal(size,std):
    kernel = np.fromfunction(
        lambda x,y: np.divide(1,2*np.pi* std**2) * 
        np.exp(
            -((x-(size-1)/2)**2 + (y-(size-1)/2)**2) / (2* std**2)
               ),
        (size,size)
    )
    return np.array(kernel/np.sum(kernel))
def find(frame,mask,contour,pixelSize):

    """
    This function takes in an image and draws the given contours.  It returns an inverted boolean array
    where true = pixel within a contour. This gives the number of pixels within a given contour to calculate area, as well as the 
    starting point for blob labeling and tracking.
    """
    #dont want to edit the original image
    filled_mask = np.copy(mask)
    #draw the contour
    filled_mask = cv.drawContours(filled_mask,[contour], 0,(0, 255, 0),thickness=cv.FILLED)
    #boolean mask and returning it, ensuring true = 0, false = 1. The sum of this is pixel size. 
    image_mask = filled_mask > 0
    total_pixels = np.sum(~image_mask.astype(int))
    image_mask = ~image_mask
    total_pixels = np.sum(image_mask.astype(int))
    #output [frame, x,y, Area, TotalIntensity]
    total_intensity = np.sum(mask*(image_mask.astype(int)))
    ##Find X,Y center of mass based on contours. 
    #https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html
    M = cv.moments(contour)
    x = int(M['m10']/M['m00'])
    y = int(M['m01']/M['m00'])
    #in units of pixelSize(micron squared)
    total_area = total_pixels*(pixelSize**2)
    return [frame,[x,y],total_area,total_intensity]
def flatten_coords(list_of_lists):
    return [sublist[1] for sublist in list_of_lists if len(sublist) > 1]
kernel = gaussian_kernal(3,np.sqrt(3))
low_thresh: int = 13
high_thresh: int = 50
#contour filtering
# we want anything equal to or greater than 5
filter_val:int = 10
##Pixel Size. This is used for area calculations. Where the area of a pixel is pixelSize**2
pixel_size: float = 0.159

tiff_stack = io.imread("/Users/cmdb/Quant_Bio_Project/Quant-Bio-Project/cell2.tif",plugin='tifffile')
tiff_stack = (tiff_stack/256).astype(np.uint8)
copied = np.copy(tiff_stack)
frame_dict = {}
for i in range(len(tiff_stack)):
    tiff_stack[i,:,:] = cv.filter2D(tiff_stack[i,:,:],-1,kernel)
    ret,thresh = cv.threshold(tiff_stack[i,:,:],low_thresh,high_thresh,cv.THRESH_BINARY)
    contours,hierarchy = cv.findContours(thresh, 1, 2)
    #filtering out contours less than 10
    contours = [lst for lst in contours if len(lst) >= filter_val]
    frame_dict[f"Timepoint {i}"] = []
    for j in contours:
        #thresholding step needed to skip bad areas. Area == 0 is nothing. 
        area = cv.moments(j)["m00"]
        if area > 0:
            centroid_output = find(i,copied[i,:,:],j,pixel_size)
            frame_dict[f"Timepoint {i}"].append(centroid_output)

list_of_keys = sorted(frame_dict.keys())
blobs = Objects(frame_dict)
keys = list(blobs.frames.keys())
#len(keys) -1
for i in range(len(keys)-1):
    blobs.new_input(n=keys[i],n1=keys[i+1])
#filtering blobs based on length. Blobs with len < 15 are removed
blobs.pull_out_xy_vals()
blobs.post_filter_plot_tracks()
blobs.updateblobs(15)
#computing the MSD for each blob
blobs.msd_compute()
#computing the mean MSD for the image
blobs.calc_mean_msd()
#calculating diffusion based on the mean MSD
blobs.calc_diffusion()
#extracting x,y coords for each blob for plotting
#plotting tracks post filtering
# blobs.post_filter_plot_tracks()
blobs.plot_mean_msd_diffusion()
blobs.plot_msd()

##ethans code
key_list = list(blobs.blobs.keys())

for i in range(len(list(blobs.blobs.keys()))):
    time_list = []
    area_list = []
    intensity_list = []
    for j in range(len(blobs.blobs[key_list[i]])):
        time_list.append(blobs.blobs[key_list[i]][j][0])
        area = float(blobs.blobs[key_list[i]][j][2])
        area_list.append(area)
        intensity = float(blobs.blobs[key_list[i]][j][3])
        intensity_list.append(intensity)
    plt.plot(time_list, intensity_list, label = key_list[i])
plt.title('Granule intensity over time')  # Title of the plot
plt.xlabel('Time')  # x-axis label
plt.ylabel('Intensity')  # y-axis label
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Moves the legend outside the plot to the right
plt.show()
