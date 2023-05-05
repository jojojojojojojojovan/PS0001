import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def change_brightness(image, value):
    img=image.copy()
    for i in range(len(img)):
        for j in range(len(img[0])):
            for k in range(3):
                if img[i][j][k] + value <0:
                    img[i][j][k] = 0
                elif img[i][j][k] + value >255:
                    img[i][j][k] = 255
                else:
                    img[i][j][k] += value
    return img
        
  
def change_contrast(image, value):
    img=image.copy()
    F = (259 * (value+255)) / (255 * (259-value))
    for i in range(len(img)):
        for j in range(len(img[0])):
            for k in range(3):
                if (F * (img[i][j][k]-128)+128) <0:
                    img[i][j][k] = 0
                elif (F * (img[i][j][k]-128)+128) >255:
                    img[i][j][k] = 255
                else:
                    img[i][j][k] = F * (img[i][j][k]-128)+128
    return img
        
    
def grayscale(image):
    img=image.copy()
    for i in range(len(img)):
        for j in range(len(img[0])):
            grey = 0.3 * img[i][j][0] + 0.59 * img[i][j][1] + 0.11 * img[i][j][2]
            for k in range(3):
                img[i][j][k] = grey    
    return img

    
def blur_effect(image):
    img=image.copy()
    newimg = img.copy()
    for i in range(1,len(img)-1):
        for j in range(1,len(img[0])-1):
            for k in range(3):
                newimg[i][j][k]=0.0625 * (img[i-1][j-1][k] + img[i-1][j+1][k] + img[i+1][j-1][k] + img[i+1][j+1][k])+\
                                0.125 * (img[i-1][j][k] + img[i][j-1][k] + img[i][j+1][k] + img[i+1][j][k])+\
                                0.25 * (img[i][j][k])
    return newimg


def edge_detection(image):
    img=image.copy()
    newimg = img.copy()
    for i in range(1,len(img)-1):
        for j in range(1,len(img[0])-1):
            for k in range(3):
                newimg[i][j][k]= -1 * (img[i-1][j-1][k] + img[i-1][j+1][k] + img[i+1][j-1][k] + img[i+1][j+1][k]+\
                                img[i-1][j][k] + img[i][j-1][k] + img[i][j+1][k] + img[i+1][j][k])+\
                                8 * (img[i][j][k]) + 128
                if newimg[i][j][k] <0:
                    newimg[i][j][k] = 0
                elif newimg[i][j][k] >255:
                    newimg[i][j][k] = 255
    return newimg


def embossed(image):
    img=image.copy()
    newimg = img.copy()
    for i in range(1,len(img)-1):
        for j in range(1,len(img[0])-1):
            for k in range(3):
                newimg[i][j][k]= -1 * (img[i-1][j-1][k] + img[i-1][j][k] + img[i][j-1][k]) +\
                                 0 * (img[i-1][j+1][k] + img[i][j][k] + img[i+1][j-1][k]) +\
                                 1 * (img[i][j+1][k] + img[i+1][j][k] + img[i+1][j+1][k]) + 128
                if newimg[i][j][k] <0:
                    newimg[i][j][k] = 0
                elif newimg[i][j][k] >255:
                    newimg[i][j][k] = 255
    return newimg


def rectangle_select(image, x, y):
    mask = np.zeros((len(image),len(image[0]))) # create a mask full of "0" of the same size of the laoded image    
    for i in range(x[0], y[0]+1):
        for j in range(x[1],y[1]+1):
            mask[i][j] = 1
        
    return mask # to be removed when filling this function

def magic_wand_select(image, x, thres):  
    row = len(image)
    col = len(image[0])
    mask = np.zeros((row,col))
    mask[x[0],x[1]] = 1
    check = np.zeros((row,col))
    check[x[0],x[1]] = 1
    stack = []
    pixel = x
    
    while True:
        pixelrow = pixel[0]
        pixelcol = pixel[1]
        if pixelrow!= 0: #can check top
            i = pixelrow - 1
            j = pixelcol
            if check[i,j] != 1:
                check[i,j] = 1
                r = (image[x[0],x[1],0] + image[i,j,0]) / 2
                diffr = image[x[0],x[1],0] - image[i,j,0]
                diffg = image[x[0],x[1],1] - image[i,j,1]
                diffb = image[x[0],x[1],2] - image[i,j,2]
                dist = ((2+r/256)*(diffr**2)+4*(diffg**2)+(2+(255-r)/256)*(diffb**2))**0.5
                if dist<=thres:
                    stack.append((i,j))
                    mask[i,j] = 1
        if pixelrow!=row-1: #can check bottom
            i = pixelrow + 1
            j = pixelcol
            if check[i,j] != 1:
                check[i,j] = 1
                r = (image[x[0],x[1],0] + image[i,j,0]) / 2
                diffr = image[x[0],x[1],0] - image[i,j,0]
                diffg = image[x[0],x[1],1] - image[i,j,1]
                diffb = image[x[0],x[1],2] - image[i,j,2]
                dist = ((2+r/256)*(diffr**2)+4*(diffg**2)+(2+(255-r)/256)*(diffb**2))**0.5
                if dist<=thres:
                    stack.append((i,j))
                    mask[i,j] = 1
        if pixelcol!=0: #can check left
            i = pixelrow
            j = pixelcol -1
            if check[i,j] != 1:
                check[i,j] = 1
                r = (image[x[0],x[1],0] + image[i,j,0]) / 2
                diffr = image[x[0],x[1],0] - image[i,j,0]
                diffg = image[x[0],x[1],1] - image[i,j,1]
                diffb = image[x[0],x[1],2] - image[i,j,2]
                dist = ((2+r/256)*(diffr**2)+4*(diffg**2)+(2+(255-r)/256)*(diffb**2))**0.5
                if dist<=thres:
                    stack.append((i,j))
                    mask[i,j] = 1
        if pixelcol!=col-1: #can check right
            i = pixelrow
            j = pixelcol + 1
            if check[i,j] != 1:
                check[i,j] = 1
                r = (image[x[0],x[1],0] + image[i,j,0]) / 2
                diffr = image[x[0],x[1],0] - image[i,j,0]
                diffg = image[x[0],x[1],1] - image[i,j,1]
                diffb = image[x[0],x[1],2] - image[i,j,2]
                dist = ((2+r/256)*(diffr**2)+4*(diffg**2)+(2+(255-r)/256)*(diffb**2))**0.5
                if dist<=thres:
                    stack.append((i,j))
                    mask[i,j] = 1
        if stack == []:
            break
        else:
            pixel = stack.pop()
        
    return mask # to be removed when filling this function

def compute_edge(mask):           
    rsize, csize = len(mask), len(mask[0]) 
    edge = np.zeros((rsize,csize))
    if np.all((mask == 1)): return edge        
    for r in range(rsize):
        for c in range(csize):
            if mask[r][c]!=0:
                if r==0 or c==0 or r==len(mask)-1 or c==len(mask[0])-1:
                    edge[r][c]=1
                    continue
                
                is_edge = False                
                for var in [(-1,0),(0,-1),(0,1),(1,0)]:
                    r_temp = r+var[0]
                    c_temp = c+var[1]
                    if 0<=r_temp<rsize and 0<=c_temp<csize:
                        if mask[r_temp][c_temp] == 0:
                            is_edge = True
                            break
    
                if is_edge == True:
                    edge[r][c]=1
            
    return edge

def save_image(filename, image):
    img = image.astype(np.uint8)
    mpimg.imsave(filename,img)

def load_image(filename):
    img = mpimg.imread(filename)
    if len(img[0][0])==4: # if png file
        img = np.delete(img, 3, 2)
    if type(img[0][0][0])==np.float32:  # if stored as float in [0,..,1] instead of integers in [0,..,255]
        img = img*255
        img = img.astype(np.uint8)
    mask = np.ones((len(img),len(img[0]))) # create a mask full of "1" of the same size of the laoded image
    img = img.astype(np.int32)
    return img, mask

def display_image(image, mask):
    # if using Spyder, please go to "Tools -> Preferences -> IPython console -> Graphics -> Graphics Backend" and select "inline"
    tmp_img = image.copy()
    edge = compute_edge(mask)
    for r in range(len(image)):
        for c in range(len(image[0])):
            if edge[r][c] == 1:
                tmp_img[r][c][0]=255
                tmp_img[r][c][1]=0
                tmp_img[r][c][2]=0
 
    plt.imshow(tmp_img)
    plt.axis('off')
    plt.show()
    print("Image size is",str(len(image)),"x",str(len(image[0])))

def menu():
    img = mask = np.array([])  
    
    while True:
        print("What do you want to do ?\
              \ne - exit\
              \nl - load a picture")
        if img.size > 0:
              print ("s - save the current picture\
                    \n1 - adjust brightness\
                    \n2 - adjust contrast\
                    \n3 - apply grayscale\
                    \n4 - apply blur\
                    \n5 - edge detection\
                    \n6 - embossed\
                    \n7 - rectangle select\
                    \n8 - magic wand select")
        choice = input ("Your choice: ")

        if choice == "e":
            print ('Exiting program!')
            break
        
        elif choice == "l":
            while True:
                try:
                    filename = input('Enter the filename: ')
                    img, mask = load_image(filename)
                    break
                except:
                    print("Enter correct file name")
            newimg = img.copy()
            
            
        elif choice == "s":
            filename = input('Enter the filename to be saved: ')
            save_image(filename,img)
            print ('File has been saved successfully!')
            
        elif choice == "1":
            while True:
                value=int(input('Enter an integer from -255 to 255 included: '))
                if value<-255 or value>255:
                    print ('Error! Enter an integer between -255 and 255.')
                    print ()  
                    continue
                else:
                    break
            newimg = change_brightness(img,value)            
               
            
        elif choice == "2":
            while True:
                value=int(input('Enter an integer from -255 to 255 included: '))
                if value<-255 or value>255:
                    print ('Error! Enter an integer between -255 and 255.')
                    print ()
                    continue
                else:
                    break
            newimg = change_contrast(img,value)
             
                
        elif choice == "3":
            newimg = grayscale(img)   
            
        elif choice == "4":
            newimg = blur_effect(img)
                
        elif choice == "5":
            newimg = edge_detection(img)
                
        elif choice == "6":
            newimg = embossed(img)
                
        elif choice == "7":
            rowx = len(img)-1
            coly = len(img[0])-1
            while True:
                x1 = int(input('Enter the x-coordinate of the first pixel: '))
                if x1<0:
                    print ('Error! Enter a positive value!')
                    print ()
                elif x1>rowx:
                    print ('Error! Enter a value less than', rowx)
                    print ()
                else:
                    break
            
            while True:    
                y1 = int(input('Enter the y-coordinate of the first pixel: '))
                if y1<0:
                    print ('Error! Enter a positive value!') 
                    print ()
                elif y1>coly:
                    print ('Error! Enter a value less than', coly)
                    print ()
                else:
                    break
                    
                    
            while True:
                x2 = int(input('Enter the x-coordinate of the second pixel: '))
                if x2<0:
                    print ('Error! Enter a positive value!')
                    print ()
                elif x2>rowx:
                    print ('Error! Enter a value less than', rowx)
                    print ()
                else:
                    break
                
            while True:
                y2 = int(input('Enter the y-coordinate of the second pixel: '))
                if y2<0:
                    print ('Error! Enter a positive value!')
                    print ()
                elif y2>coly:
                    print ('Error! Enter a value less than', coly)
                    print ()
                else:
                    break
        
            x = (x1,y1)
            y = (x2,y2)
            mask = rectangle_select(img, x, y)
                
        elif choice == "8":
            row = len(img)-1
            col = len(img[0])-1
            while True:
                x = int(input('Enter the x-coordinate of the chosen pixel: '))
                if x<0:
                    print ('Error! Enter a positive value!')
                    print ()
                elif x>row:
                    print ('Error! Enter a value less than', rowx)
                    print ()
                else:
                    break
            while True:
                y = int(input('Enter the y-coordinate of the chosen pixel: '))
                if y<0:
                    print ('Error! Enter a positive value!')
                    print ()
                elif y>col:
                    print ('Error! Enter a value less than', rowx)
                    print ()
                else:
                    break
            while True:
                thres = int(input('Enter the threshold (200 is optimal): '))
                if thres<0:
                    print ('Error! Enter a positive value!')
                    print ()
                else:
                    break
            mask = magic_wand_select(img, (x,y), thres)
        
        else:
            print ("Error! Enter a valid choice.")
            print()
        
        effects = [str(i) for i in range(1,7)]
        if choice in effects:
            for i in range(len(img)):
                for j in range(len(img[0])):
                    if mask[i,j] == 1:
                        img[i,j] = newimg[i,j]
        display_image(img,mask)
        
        
            
menu()
if __name__ == "__main__":
    menu()
    





