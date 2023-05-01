
import numpy as np 
from osgeo import gdal
import gc
import os

def Corrector(inSolar, path, outPath):
    print ('its Working')

    coeff=np.array([1.007951631,1.003136498,1.012137177,0.983221552,0.982301846,0.980570808,0.974865433,0.97640194,0.992019454,1.007100398,1.004167929,0.986444903,1.005016461,1.013553818,1.009490688,1.003308071,1.011969658,1.0141375,1.006193945,1.015513554,1.020218579,1.016652203,1.023330972,1.020211072,1.015149832,1.00860599,1.000767149,0.994761146,1.067891991,1.044841918,0.972851837,0.9762951,0.979046208,0.97102683,0.982455709,0.987001059,0.988436954,0.979160136,0.9986847,0.997752521,0.998447812,1.016854934,0.997900542,0.983831379,0.969376425,0.979670198,0.973878228,0.996289037,1.014184498,1.01477613,1.001481496,0.975778394,0.997684295,0.984763646,0.983395789,0.98823384,0.988012215,0.952374697,0.937581808,1.013480796,1.014063354,1.022099753,1.03204087,1.035484491,1.041175268,1.036634478,1.034566162,1.03809732,1.046558655,1.021576737,1.028588801,1.007904219,0.972531419,0.956629793,0.955287872,0.979925337,1.002466257,1.014420813,1.008463966,1.00003099,1.008471522,0.99282371,0.99980302,0.987547313,0.984068212,0.992388063,0.988139868,1.012650312,1.052139241,1.012472306,0.965437548,0.939243701,0.967441753,0.963544372,0.990952989,0.973117569,1.013248635,1.020203633,1.029157186,1.020485688,1.020579985,1.006238104,1.014835128,1.006275303,1.010898129,1.00045314,1.008028897,1.012421421,1.027533403,1.031189861,1.029572772,0.998242,0.988472694,0.964883574,0.965888213,0.949632716,0.959468989,0.953967103,0.97185828,0.975099523,0.99858193,0.998573727,1.021937907,1.019142949,1.038073792,1.031876174,1.041953094,1.029414494,1.031461328,1.008333598,1.0158236,0.997626672,0.997772942,0.951297807,0.98848544,0.983055255,0.973287938,1.020004362,1.007683124,1.002357289,1.009943767,0.967795252,0.999227534,0.97305723,0.984516543,0.996874775,1.05340332,1.037099582,1.015145219,1.02252679,0.987330432,0.896931034,0.854160633,1.141899078,1.108682789,1.023030659,0.939513645,0.914993685,0.994857247,1.264567511,0.759581027,1.008047196,1.012150301,0.962843991,1.019548525,0.989332932,1.049050719,0.980318607,1.018721793,0.965286873,1.027176253,0.963709485,1.010598964,0.971110269,1.076940686,1.020255436,0.929940419,0.996612177,0.958811048,1.059205186,1.002448358,0.973559634,1.002937935,1.013683258,1.0474072,1.000925241,0.985500261,0.982660401,0.938587583,1.046900212,0.952743318,1.026649622,1.115011575,0.887761742,1.005459078,0.95483364,0.967275555,1.13852458,0.986343909,0.965651948,1.101161236,0.988116073,0.853138055,0.974375472,1.177442497,0.927739407,0.932486397,0.962300997,0.985181241,0.829206405,1.493934047,1.059590538,0.71322689,0.875132631,1.121072252,0.938541303,1.139668914,0.897165185,1.117762208,0.961511703,0.528956345,1.711570255,1.20749058,1.024243553,0.713165588,1.06875679,0.570841199,0.932178556,2.546499369,2.664596812,1.224978705,0.567434034,0.726464718,0.745085856,1.21801428,1.140071493,0.828417838,1.063662997,0.953993832,1.084346492,0.826805177,1.166156321,0.873581953,0.906603941,1.403382254,0.898905495,1.006518779])
    coeff=np.reshape(coeff,(coeff.shape[0],1,1))


    gdal.AllRegister()
    driver=gdal.GetDriverByName('ENVI')
    c=3e8
    h=6.626e-34
    k=1.38e-23



    res=1 # resize factor


    def outWrite(nm):


        sL=800  #starting lmb
        eL=5000  #ending lmb

        sIdx=np.argmin(abs(L[:,0]*1e9-sL))
        eIdx=np.argmin(abs(L[:,0]*1e9-eL))+1

        outRefR=outRef[sIdx:eIdx,:,:]
        L1=L[sIdx:eIdx,0]*1e9
        L1=np.round(L1,5)

        os.chdir(outPath)
        outN=path.split('.')[0].split('/')[-1]+nm#'_Corr_Ref'
        outDS= driver.Create(outN,outRefR.shape[2],outRefR.shape[1],outRefR.shape[0],gdal.GDT_Float32)

        for i in range(outRefR.shape[0]):
            bnd=outDS.GetRasterBand(i+1)
            bnd.WriteArray(outRefR[i,:,:])
        outDS=None

        with open(outN+'.hdr','a') as f:
            f.write('\n')
            f.write('wavelength={')
            rg=np.arange(0,outRefR.shape[0],5)
            for i in rg:
                if i+5>outRefR.shape[0]:
                    ed=outRefR.shape[0]
                else:
                    ed=i+5
                f.write('\n')
                f.write(str(list(L1[i:ed]))[1:-1])
                if i!=rg[-1]:
                    f.write(',')

            f.write('}')
        f.close()


    # In[8]:
    # Dark corrected image

    ### read radiance ds
    path1=path 

    inDS=gdal.Open(path1)
    XSize=inDS.RasterXSize
    YSize=inDS.RasterYSize


    # In[26]:


    rad=inDS.ReadAsArray(0,0,XSize,YSize)
    print(rad.shape)
    rad=rad[7:-2,:,:]*0.01



    XSize=rad.shape[2]
    YSize=rad.shape[1]
    L=np.loadtxt(inSolar)[7:-2,:]
    L[:,1]=np.round(L[:,1],4)
    L[:,1]=L[:,1]*10
    RT=np.zeros_like(rad)
    outRef=np.zeros_like(rad)
    Temp=np.zeros((YSize,XSize))
    em=np.zeros((YSize,XSize))
    L[:,0]=L[:,0]*1e-9
    lmb=L[:,0]



    # In[27]:


    lmbL=4500 ## select subset range from the bands
    lmbU=4874

    lmbidxL=np.argmin(abs(L[:,0]*1e9-lmbL))
    lmbidxU=np.argmin(abs(L[:,0]*1e9-lmbU))


    # In[28]:


    Llambda=np.reshape(L[:,1],(outRef.shape[0],1,1))
    e=0.95
    mT=370


    for i in range(YSize):
        for j in range(XSize):
            
            T=[]        
            ra=rad[lmbidxL:lmbidxU,i,j]#/3.14
            lmbS=L[lmbidxL:lmbidxU,0]
            for lm,B in zip(lmbS,ra):
                q=np.log(e*2*h*c*c*1e-6/(B*(lm)**5)+1)
                T.append(h*c/(lm*k*q))
            mT=np.mean(T)        
            B=(1e-6)*(2*h*c*c/lmb**5)*1/(np.exp(h*c/(lmb*k*mT))-1)
            Temp[i,j]=mT # Temperature
            em[i,j]=e
            RT[:,i,j]=B #Thermal Radiance

    outRef=3.14*(rad-e*RT)/Llambda
    outRef[np.where(outRef<0)]=0


    # In[29]:
    del rad
    del RT
    gc.collect()


    outRef=outRef/coeff
    os.chdir(outPath)
    angDS=gdal.Open(path.split('.')[0].split('/')[-1]+'_angle')
    angle=angDS.ReadAsArray()
    outRef=outRef/np.cos(angle*np.pi/180)

    ### moving average 

    row,col=outRef.shape[1],outRef.shape[2]
    for i in range(row):
        for j in range(col):
            datMV=outRef[:,i,j]
            a1=np.hstack((datMV,0,0))
            a2=np.hstack((0,datMV,0))
            a3=np.hstack((0,0,datMV))
            outRef[:,i,j]=np.hstack(((datMV[1]+datMV[2])/2,((a1+a2+a3)/3)[2:-2],(datMV[-1]+datMV[-2])/2))


    outWrite('_inc_corrRef')
    os.chdir(outPath)
    outN=path.split('.')[0].split('/')[-1]+'_Temp'
    outDST=driver.Create(outN,outRef.shape[2],outRef.shape[1],1,gdal.GDT_Float32)
    bnd=outDST.GetRasterBand(1)
    bnd.WriteArray(Temp[:,:])
    outDST=None

    del outRef
    gc.collect()