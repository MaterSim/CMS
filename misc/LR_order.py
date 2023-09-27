from ase import Atoms
from ase import io
import pyxtal
import numpy as np
import copy
from scipy.signal import savgol_filter
import scipy.signal as sig
import matplotlib.pyplot as plt
import pandas as pd
import json


class LR_order:
    def __init__(self,poscars,ele,plane_density=5,load=None):
        """
        Compares long range order preservation for all crystallographic planes in a series of structures 
        connecting a crystal to its amorphous phase.
        
        Args:
        
        poscars: list of filenames to poscar files
        ele: element used to track order
        plane_density: calculates order for all planes with indicies less than value
        load: dictionary object created from previous LR_order calculation using save_p function.
        """
        
        self.structures=[]
        for x in poscars:
            s=pyxtal.pyxtal()
            s.from_seed(x)
            self.structures.append(s)
        
        if load is not None:
            self.planes=np.array(load['planes'])
            self.struc_projections=np.array(load['struc_projections'])
            self.projection_bins=np.array(load['projection_bins'])
            print(len(self.planes))
        
        else:
        #finds all planes for order calculation
            sample=io.read(poscars[0])
            self.planes=[x for x in pyxtal.XRD(sample).hkl_list if np.all(np.abs(x)<=plane_density)]
            self.point_projections(ele=ele)
        
        
        #q is order. Lower value is more order. Index is same as planes index.
        self.q=[]
        scatter=[]
        for p in self.projection_bins:
            r,zz=self.quantify_order(p)
            self.q.append(np.round(r,10))
            scatter.append(zz)
        
        
            

        # argsortedq=np.argsort(self.q)
        # for j,i in enumerate(argsortedq[1:]):
        #     if self.q[argsortedq[j]]==self.q[argsortedq[j-1]]:
        #         continue  
            # fig,ax=plt.subplots(nrows=1,ncols=2,figsize=(13,5))
            # ax[0].hist(self.projection_bins[i],50)
            # ax[0].set_title(str(self.planes[i])+'        '+str(self.q[i])+'       '+str(i))
            # ax[1].scatter(scatter[i][0],scatter[i][1],color='red')
            # ax[1].plot(scatter[i][2][:-1],scatter[i][3])
            # plt.show()
            
        
        
        
        
        
        
    def point_projections(self,ele):
        """
        Projects the location of atoms of ele in the structure onto the planes in self.planes.
        
        Returns:
            self.struc_projection: the atom projections distances for each structure, seperated by structure
            self.projection_bins: the atom projections distances for every structure, seperated by planes.
        """
        points=[]
        for struc in self.structures:
            points_=[]
            for i,plane in enumerate(self.planes):
                points_.append(sorted(self.projector(struc,plane,ele)))
            points.append(points_)
        
        zss=[]
        for i,y in enumerate(self.planes):
            zss.append([x[i] for x in points])
        
        ###Broken poscarfile correct?
        for i,x in enumerate(zss):
            for j,y in enumerate(zss[i]):
                if len(y)==1:
                    zss[i].pop(j)

        for i,p in enumerate(zss):
            zss[i]=self.shifted_c(p)

        pss=[]
        for v in zss:
            pzz=[]
            for w in v:
                pzz.extend(w)
            pss.append(pzz)
            
        self.struc_projections=zss
        self.projection_bins=pss
            
    def shifted_c(self,points):
        """
        Shifts all the projected points to be centered at the middle of the average range. Helps with comparisons.
        """
        a=np.average([x[0] for x in points])
        b=np.average([x[-1] for x in points])
        c=(a+b)/2
        for i in range(1,len(points)):
            shift=((points[i][-1]+points[i][0])/2)-c
            points[i]=points[i]-shift
        return points

    def projector(self,struc,plane,specie):
        """
        Finds distances of atoms projected along crystal plane
        """
        
        total=[]
        mat=struc.lattice.matrix
        unit=np.array(plane)/np.linalg.norm(plane) #create unit vector for projection.
        r=[np.linalg.norm(np.dot(np.dot(site.position,unit),mat)) for site in struc.atom_sites if site.specie==specie]
        return r
    
    def quantify_order(self,p):
        """
        Quantifies the order of particular plane. Uses a histogram of the projected points. Peak finder and peak width
        calculator is used to quantify relative atom distance consistency between all the structures.
        
        Returns:
            width of maximum width peak
            x,y coordinates of found peaks
            x,y coordinates of smoothing function
        """
        
        y,x=np.histogram(p,bins=50,density=True)
        yhat=savgol_filter(y,19,12)#can tune this value
        zz,props=sig.find_peaks(yhat,width=2.4)
        yy=[yhat[v] for v in list(zz)]
        xx=[x[v] for v in list(zz)]
        return max(props['widths']),[xx,yy,x,yhat]
    
    def plotting_data(self,filename='plot_data.csv'):
        """
        Prints data to be used in plotting function
        """
        d={'h':[x[0] for x in self.planes],
           'k':[x[1] for x in self.planes],
           'l':[x[2] for x in self.planes],
           'I':[x for x in self.q]}
        df=pd.DataFrame.from_dict(d)
        df.to_csv(filename)
        
        
    # def save_p(self,filename='load_data.csv'):
    #     weith open(
    #     d={'planes': self.planes,
    #        'struc_projections': self.struc_projections,
    #        'projection_bins': self.projection_bins}
    #     df=pd.DataFrame.from_dict(d)
    #     df.to_csv(filename)                              
            

    


    
    
    
    
    
       
    
if __name__ == "__main__":
    filenames=['S812/POSCAR.'+str(x) for x in range(1,813)]
    # df=read.csv('data.csv')
    o=LR_order(filenames,ele='Al',load=None)
    o.plotting_data(filename='plot_data.csv')
    # o.save_p()
    
    