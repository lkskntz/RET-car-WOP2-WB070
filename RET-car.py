import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

#info
c_veer = 9.5e-3 #Nm/graad
r_hefboom = 0.21 #m
r_wiel = 0.055
r_as = 0.002
massa_kar = 1.4
c_skatewiel = 0.0025
c_glijlager = 0.25
c_rollager = 0.0018

#simpele berekeningen
gewicht_kar = massa_kar*9.81
omtrek_wiel = math.pi * 2 * r_wiel
omtrek_as = math.pi * 2 * r_as
l_touw_totaal = math.sqrt(r_hefboom**2+r_hefboom**2)

#weerstanden
F_rol = c_skatewiel*gewicht_kar
F_glijlager = c_glijlager*gewicht_kar
F_rollager = c_rollager*gewicht_kar

#startwaarden
graden_veer_begin = 90
graden_veer = graden_veer_begin
dt = 0.1
t = 0.0
v = 0.0
s = 0.0
s_2 = 0.0
s_3 = 0.0

stage = 1

a_list = []
v_list = []
s_list = []
F_netto_list = []
graden_list = []
tijd_list = []
l_touw_over_list = []

for i in range(1):

    while (stage == 1): #het karretje accelereert door de opgespannen veer
        
        Fveer = 2*((graden_veer*c_veer)/r_hefboom)
        Tas = Fveer*r_as
        Faandrijf = Tas/r_wiel
    
        Fnetto = Faandrijf - F_rol - F_rollager
    
        F_netto_list.append(Fnetto)
        
        a = Fnetto / massa_kar
        a_list.append(a)
        
        v = v + a*dt
        v_list.append(v)
        
        s = s + v*dt
        s_list.append(s)
        
        omwentelingen = s / omtrek_wiel
        
        l_touw_wentel = omwentelingen * omtrek_as
        l_touw = l_touw_totaal - l_touw_wentel
        l_touw_over_list.append(l_touw)
        
        cosinus = math.acos(((l_touw**2) - (r_hefboom**2) - (r_hefboom**2)) / (-2*r_hefboom**2))
            
        graden_veer = math.degrees(cosinus)
        graden_list.append(graden_veer)
            
        t = t + dt
        tijd_list.append(t)
            
        if l_touw < 0:
            stage = 2
            l_touw = 0
            break
    
    while (stage == 2): #het karretje laadt de veer weer op
        
        Fveer = 2*((graden_veer*c_veer)/r_hefboom)
        Tas = Fveer*r_as
        Faandrijf = Tas/r_wiel
    
        Fnetto = -Faandrijf - F_rol - F_rollager
        F_netto_list.append(Fnetto)
        
        a = Fnetto / massa_kar
        a_list.append(a)
        
        v = v + a*dt
        v_list.append(v)
        
        s_2 = s_2 + v*dt
        s = s + v*dt
        s_list.append(s)
        
        omwentelingen = s_2 / omtrek_wiel
        l_touw_wentel = omwentelingen * omtrek_as
        l_touw = l_touw_wentel
        
        l_touw_over_list.append(l_touw)
        
        cosinus = math.acos(((l_touw**2) - (r_hefboom**2) - (r_hefboom**2)) / (-2*r_hefboom**2))
            
        graden_veer = math.degrees(cosinus)
        graden_list.append(graden_veer)
            
        t = t + dt
        tijd_list.append(t)
            
        if v < 0:
            stage = 3
            l_touw_totaal = l_touw
            break
    
    while (stage == 3): #het karretje rijdt terug
        Fveer = 2*((graden_veer*c_veer)/r_hefboom)
        Tas = Fveer*r_as
        Faandrijf = Tas/r_wiel
    
        Fnetto = Faandrijf - F_rol - F_rollager
        F_netto_list.append(Fnetto)
        
        a = Fnetto / massa_kar
        a_list.append(a)
        
        v = v + -a*dt
        v_list.append(v)
        
        s_3 = s_3 + -v*dt
        s = s + v*dt
        s_list.append(s)
        
        omwentelingen = s_3 / omtrek_wiel
        
        l_touw_wentel = omwentelingen * omtrek_as
        l_touw = l_touw_totaal - l_touw_wentel
        l_touw_over_list.append(l_touw)
        
        cosinus = math.acos(((l_touw**2) - (r_hefboom**2) - (r_hefboom**2)) / (-2*r_hefboom**2))
            
        graden_veer = math.degrees(cosinus)
        graden_list.append(graden_veer)
            
        t = t + dt
        tijd_list.append(t)
            
        if l_touw < 0:
            l_touw = 0
            
            while (v < 0): #de veer levert geen kracht meer, maar het karretje heeft nog wel snelheid en rijdt nog steeds terug
               Fnetto = -F_rol - F_rollager
               F_netto_list.append(Fnetto)
               
               a = Fnetto / massa_kar
               a_list.append(a)
               
               v = v + -a*dt
               v_list.append(v)
               
               s_3 = s_3 + -v*dt
               s = s + v*dt
               s_list.append(s)
               
               l_touw_over_list.append(l_touw)
               
               graden_list.append(graden_veer)
                   
               t = t + dt
               tijd_list.append(t)
            break             
    
dictionary = {'Tijd': tijd_list, 'Veer': graden_list, 'Fnetto': F_netto_list, 'a':a_list, 'v':v_list, 's': s_list, 'Touw':l_touw_over_list}

data = pd.DataFrame(dictionary)

print(data)

fig, ax = plt.subplots(1, 1, figsize=(8, 5), dpi=150)
ax.plot(data['Tijd'], data['Veer'])
ax.set_xlabel('Tijd')
ax.set_ylabel('Graden Torsieveer')
ax.grid()

fig, ax2 = plt.subplots(1, 1, figsize=(8, 5), dpi=150)
ax2.plot(data['Tijd'], data['a'])
ax2.set_xlabel('Tijd')
ax2.set_ylabel('Versnelling')
ax2.grid()

fig, ax3 = plt.subplots(1, 1, figsize=(8, 5), dpi=150)
ax3.plot(data['Tijd'], data['v'])
ax3.set_xlabel('Tijd')
ax3.set_ylabel('Snelheid')
ax3.grid()

fig, ax4 = plt.subplots(1, 1, figsize=(8, 5), dpi=150)
ax4.plot(data['Tijd'], data['s'])
ax4.set_xlabel('Tijd')
ax4.set_ylabel('Afstand tot startlijn')
ax4.grid()

plt.show()
