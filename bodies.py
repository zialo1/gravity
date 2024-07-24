#bodies.py
import numpy as np
import math
#np.set_printoptions(suppress=True)

def angle(a1):
    a=a1/180*math.pi
    return math.cos(a),math.sin(a)
    
''' calculate metric of 2 vectors without sqrt '''

def metr(a1,a2):
    return np.linalg.norm(a1-a2)

def metr2(a1,a2):
#    assert len(a1) == len(a2)
  
    res = pow(a1[0]-a2[0],2)
    res+= pow(a1[1]-a2[1],2)
    return res

''' class contains various shapes with and without mass '''
class massobject:
    def __init__(self,apos,avel,mass=0):
        self.shape = None
        self.pos=np.array(apos,dtype=np.float64)
        self.vel=np.array(avel,dtype=np.float64)
        self.mymass = mass
        self.locked = False
        self.name=None
        self.num=0
        
    def link(self,ashape):
        self.shape=ashape
        
    ''' forces change acceleration, change speed, change position '''
    def update(self,accel:np.ndarray,adt):
        if self.locked:
            print('object is locked')
            return
    
        print("updating pos of ",self.name," old",
              self.pos, " update+=", self.vel*adt+0.5*accel*pow(adt,2))
        
        self.pos += self.vel*adt+0.5*accel*pow(adt,2)
        self.vel += accel * adt
        #print(self.coords)
        #these values are correct but the work done with it isnt
        
        
        return self.coords
    
    @property
    def mass(self):
        return self.mymass
    
    @property
    def coords(self)->tuple:
        return self.pos.item(0),self.pos.item(1)
    
    def has_mass(self)->bool:
        return self.mymass>0
    
    def lock(self):
        self.vel=0
        self.locked=True

class bodies:
#      class values
    current:int=-1
    max:int=-1
    allshapes:list=[]
    
    def __init__(self,*alcoords):
        self.allshapes=[]
        self.max=len(alcoords)
        self.current=-1
        for a in alcoords:
            # velocity is zero
            self.allshapes.append(massobject(a,(0,0),mass=1))
        self.dist=np.zeros((self.max,self.max)
        self.forces=np.zeros((self.max,self.max))
        
                           
        print(f"middle of {self} is {self.middlepoint}")
            
    def append(self,apos,avel,aflag=True):
        self.allshapes.append(massobject(apos,avel,aflag))
    
    def sumofforces(self,pos,gfactor=1e3,exclude=None):     
        forcefield=np.zeros(2)
        for a in self.cycle(exclude):
            b=metr(np.array(pos),a.pos)
            if b < 1e-27:
                continue
            else:
                #print(f"DIST to {pos} is {b:3}")
                pass
            
            dist=pow(b,-3) #
            r=np.array((-pos[0],pos[1]))+a.pos
            forcefield+=dist*r*gfactor*a.mass
        # setting the individual coors to zero if too small
        forcefield[np.abs(forcefield)<1e-14]=0
        
        if (np.dot(forcefield,forcefield)<1e-28 or
            np.dot(forcefield,(1,1)) == 0.0 or
            np.dot(forcefield, (-1,1)) == 0.0):
            return np.zeros(2)
        else:
            return forcefield
        
    def updatepos(self,adt):
        for a in self.cycle(): # every object with matter
            #print("-- Calculating forces for ",a.pos)
            accel=self.sumofforces(a.coords,gfactor=1e3,exclude=a) # relates to every other
            a.update(accel,adt)
            #print("END UPDATEPOS",ax,ay)
        return self.middlepoint
    
    @property
    def middlepoint(self)->np.ndarray:
        res=np.zeros(2)
        
        for a in self.cycle():
            res+=np.array(a.pos*a.mass)
        res[np.abs(res)<1e-14]=0
        return res/len(self.allshapes)
    def cycle(self,exclude=None):
        if exclude:
            #print(f"(cycle) exclude{exclude.pos}")
            pass
        for a in self.allshapes:
            if a.has_mass and a is not exclude:
                #print("++",a.pos)
                yield  a
            else:
#                 print("excluded ",a.pos)
                pass
            
    def __next__(self):
        if self.current+1<self.max :
            self.current+=1
            return self.allshapes[self.current]
        self.current=-1
        return None
    
    def __iter__(self):
        for a in self.allshapes:
            yield a
    
    def __repr__(self):
        return f"Number of Masselements: {len(self.allshapes)}"
    
    #check if this works first.
    def freezedistances(self):
        for a in self.cycle():
            for b in self.cycle():
                print(a,b)
                #self.distances[a,b]=metr(a,b)
                           
        
            
def pytest_test0():
    x=bodies()
    y=massobject((0,0),(0,0))
    x.append((0,0),(0,0))
    x.append((0,0),(0,0))
    
    for a in x.cycle():
        print(a.pos)
        
        
