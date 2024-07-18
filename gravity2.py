import math
import pyglet
import numpy
from bodies import *
            
class myApp(pyglet.window.Window):
    ''' there are moving masses present '''
   
    def __init__(self,awidth,acbodies,alist):
        self.startup=awidth,acbodies,alist # restart option
        center=awidth/2
        
        assert len(alist) ==2
        super().__init__(width=awidth,height=awidth,visible=True)
    
        image1 = pyglet.resource.image(alist[0])
        image2 = pyglet.resource.image(alist[1])
        self.sprite1 = pyglet.sprite.Sprite(img=image1)
        
        self.batch=pyglet.graphics.Batch()

        self.bodies = acbodies
#         self.lofobj=[]
        self.x=32
        self.y=32
        self.vx=0
        self.vy=0
        self.plus=[]
        self.ticks:float=0
        # here is a link taking place but position AND shape have to be updated
        for a in self.bodies:
            self.plus.append(pyglet.shapes.Rectangle(*a.coords,11,11,
                        color =((150+int(a.coords[0]))%256,225,
                                (30+int(a.coords[1]))%256),
        
                            batch=self.batch))
            a.name = f"O{len(self.plus)}" # debug help
            a.link(pyglet.shapes.Circle(*a.coords,10,
                        color =((150+int(a.coords[0]))%256,225,(30+int(a.coords[1]))%256),batch=self.batch))
        t=1+math.cos(math.pi/180*35)
            
        self.label = pyglet.text.Label("0",x=t*center,y=t*center)
        self.cursor=pyglet.shapes.Rectangle(self.x-12,self.y-12,25,25)
        #self.clock=pyglet.clock.Clock()
        #pyglet.clock.set_default(self.clock)
        self.stopped=True
        
    def setspeed(self,*a):
        self.vx=a[0]
        self.vy=a[1]
    
    def calcspeed(self,dt)->np.ndarray:
        #print("calcspeed")
        accel = self.bodies.sumofforces((self.x,self.y),3000)
        
        #print("net force =",accel,", speed=",
        #      np.linalg.norm(accel*dt))
           
        if accel[np.abs(accel)>10].any():
            print("jump/collision ahead")
        return accel*dt
            
    def on_draw(self):
        self.clear()       
        self.sprite1.x=self.x-12
        self.sprite1.y=self.y-12
        self.sprite1.draw()
        
        self.batch.draw()
        self.label.draw()
        #print(".")
        
    def updateshapes(self):
        ''' the correct coords are in bodies, shapes have to be informed '''
        for a in self.bodies:
            #print("update",a.coords)
#             a.shape.x = a.coords[0]
#             a.shape.y = a.coords[1]
            pass
        
    def update(self,dt):
        if self.stopped:
            return
        
        self.vx,self.vy = self.calcspeed(dt)
        self.x+=self.vx*dt
        self.y+=self.vy*dt
         
        self.ticks+=float(dt)
        self.label.text="  "
        self.label.text=f'{self.ticks:.4}'
        mid=self.bodies.updatepos(dt)
        self.updateshapes()
        print("updated, but mid is",mid)
        pass
    def on_key_press(self,symbol,modif):
        if symbol == pyglet.window.key.SPACE:
            self.stopped= self.stopped != True
        if symbol == pyglet.window.key.Q:
            self.close()
            pyglet.app.exit()
        if symbol == pyglet.window.key.R:
            self.close()
            pyglet.app.exit()
            main()
            #self.__init__(*self.startup)
    
def main1():
    myshapes=bodies()
    
    for x,y in ((100,50),(100,50)):
        myshapes.append((x,y),(0,0),True)
        
    print(myshapes)
    lims=("cursor1.png","cursor2.png")
    x=myApp(500,myshapes,lims) #myshape.sumforces,myshapes.cycle,iter myshapes
    x.setspeed(0,0)
    pyglet.clock.schedule_interval(x.update,0.6)
    pyglet.app.run()
    print("Should not be reached")
    
def main():
    num=3
    anglestep=2*math.pi/num
   
    myshapes=bodies()
    radius=50
    sumcoords=0,0
    for a in range(0,num): #setup of the gravity sinks
        angle=a*anglestep
        coords=math.cos(angle)*radius+300,math.sin(angle)*radius+300
        speed = 0,0
        #-math.sin(angle)*radius,math.cos(angle)*radius
        myshapes.append(coords,speed,True)
          
    
    print(myshapes)
    lims=("cursor1.png","cursor2.png")
    x=myApp(500,myshapes,lims) #myshape.sumforces,myshapes.cycle,iter myshapes
    x.setspeed(0,0)
    pyglet.clock.schedule_interval(x.update,0.1)
    pyglet.app.run()
    print("Should not be reached")
    

if __name__ == "__main__":
    main()




