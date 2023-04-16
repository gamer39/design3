import matplotlib.pyplot as plt
import csv
import numpy as np

#importe les données
with open('thermistancecentre.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

with open('reference3.csv', newline='') as f:
    reader = csv.reader(f)
    refdata = list(reader)

t = [] #temps
vals = [] #valeurs de température du filtre
refvals = [] #températures d'une thermistance de référence
    
for i in data[2:]:
    if float(i[0]) < 480:
        t.append(float(i[0]))
        vals.append(float(i[1]))

for i in refdata[2:]:
    if float(i[0]) < 480:
        refvals.append(float(i[1]))


mi = min(vals) #min des valeurs de température du filtre
refmi = min(refvals) #min des températures de référence

#soustraction du min pour setter à 0
for i in range(len(vals)):
    vals[i] = vals[i]-mi

for i in range(len(vals)):
    refvals[i] = refvals[i]-refmi

t = np.array(t)
vals = np.array(vals)

#différence des températures du filtre avec celles de référence pour éliminer accumulation de chaleur
corvals = vals-refvals

#fonction qui trouve la valeur dans un array la plus proche d'une valeur voulue
def closest(array,val):
    dif = abs(array-val)
    ne = min(dif) 
    return np.where(dif == ne)

#dérivée d'une array y selon x
def diff(x,y):
    deriv = []
    for i in range(len(x)-1):
        deriv.append((y[i+1]-y[i])/(x[i+1]-x[i]))
    deriv.append(deriv[-1])
    return np.array(deriv)

#fonction de puissance selon température à un temps t donné (constantes selon simulation --> à changer avec tests du protoype)
def P(t,T):
    return (T/0.781383) + (7.406/0.781383)*diff(t,T)

#trouve puissance à partir des températures corrigées (différence entre température filtre et température de référence)
power = P(t,corvals)

p = np.array([2.5,2.5,5,5,7.5,7.5,10,10,7.5,7.5,5,5,2.5,2.5,0,0])
time = np.array([0,60,60,120,120,180,180,240,240,300,300,360,360,420,420,480])

plt.plot(time,p,'-',color='orange',label='Puissance réelle du laser')

plt.plot(t,power,'-',label='Puissance convertie à partir de la température')
plt.legend()
plt.show()
