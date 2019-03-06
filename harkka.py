# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 23:28:19 2019

@author: Matias
"""

import math
import matplotlib.pyplot as plt

OPPIMISNOPEUS = 0.1
EKAN_TUOTTEEN_VALMISTUSAIKA = 100
RAAKA_AINE_KUSTANNUKSET_PER_YKSIKKO = 14700

MARKKINOINNIN_KULUT_W = 2000
HALLINTOKULUT_W = 400
VARASTO_KAPASITEETTI = 200
UUSI_VARASTO_KAPASITEETTI = 400
TYONTEKIJOIDEN_TUNTIHINTA = 123

ALOITUS_W = 1
LOPETUS_W = 52
AIKAVALI = 1

# %% Perustapaus

VARASTO = 0
KOKONAISTULOS = 0
VALMISTETUT_YKSIKOT = 0
MYYNTIHINTA = 23500

perus_v_ajat = []
perus_v_yksikot = []
perus_varasto = []
perus_voitto = []
perus_tappio = []
perus_tulos = []
perus_kokonaistulos = []
perus_tv_kust = []
perus_kiint_kust = []

for t in range(ALOITUS_W, LOPETUS_W +1, AIKAVALI):
    KYSYNTA_W = 50
    TUOTANTO_W = 50
    VALMISTETUT_YKSIKOT += TUOTANTO_W
    VARASTO += TUOTANTO_W - KYSYNTA_W
    
    N_TUOTTEEN_VALMISTUSAIKA = EKAN_TUOTTEEN_VALMISTUSAIKA * VALMISTETUT_YKSIKOT ** (math.log2(1-OPPIMISNOPEUS))
    
    if VARASTO > VARASTO_KAPASITEETTI:
        VAKUUTUSMAKSUT_W = 500+VARASTO*10
        VUOKRAKUSTANNUKSET_W = 1200 + 200
    else:
        VAKUUTUSMAKSUT_W = 500
        VUOKRAKUSTANNUKSET_W = 1200
        
    SAHKOMAKSUT_W = 20 * TUOTANTO_W
    VESIMAKSUT_W = 2 * TUOTANTO_W
    
    KIINTEAT_KUSTANNUKSET_W = MARKKINOINNIN_KULUT_W + HALLINTOKULUT_W + VAKUUTUSMAKSUT_W + VUOKRAKUSTANNUKSET_W + SAHKOMAKSUT_W + VESIMAKSUT_W
    RAAKA_AINE_KUSTANNUKSET_W = RAAKA_AINE_KUSTANNUKSET_PER_YKSIKKO * TUOTANTO_W
    TYOVOIMAKUSTANNUKSET_W = TUOTANTO_W * N_TUOTTEEN_VALMISTUSAIKA * TYONTEKIJOIDEN_TUNTIHINTA
    
    VOITTO_W = KYSYNTA_W * MYYNTIHINTA
    TAPPIO_W = TYOVOIMAKUSTANNUKSET_W + RAAKA_AINE_KUSTANNUKSET_W + KIINTEAT_KUSTANNUKSET_W
    TULOS_W = VOITTO_W - TAPPIO_W
    
    KOKONAISTULOS += TULOS_W
    
    perus_v_ajat.append(N_TUOTTEEN_VALMISTUSAIKA)
    perus_v_yksikot.append(VALMISTETUT_YKSIKOT)
    perus_varasto.append(VARASTO)
    perus_voitto.append(VOITTO_W)
    perus_tappio.append(TAPPIO_W)
    perus_tulos.append(TULOS_W)
    perus_kokonaistulos.append(KOKONAISTULOS)
    perus_tv_kust.append(TYOVOIMAKUSTANNUKSET_W)
    perus_kiint_kust.append(KIINTEAT_KUSTANNUKSET_W)
    
fig = plt.figure(1)
plt.subplots_adjust(left=0.15, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
plt.suptitle('Peruskausi')
ax1 = fig.add_subplot(2,2,1)
ax1.plot(range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), perus_voitto, 'go-')
ax1.set_title('Voitto')
ax1.set_xlabel('w')
ax1.set_ylabel('e')

ax2 = fig.add_subplot(2,2,2)
ax2.plot(range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), perus_tappio, 'ro-')
ax2.set_title('Tappio')
ax2.set_xlabel('w')
ax2.set_ylabel('e')

ax3 = fig.add_subplot(2,2,3)
ax3.plot(range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), perus_tulos, 'bo-')
ax3.set_title('Tulos')
ax3.set_xlabel('w')
ax3.set_ylabel('e')

ax4 = fig.add_subplot(2,2,4)
ax4.plot(range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), perus_kokonaistulos, 'bo-')
ax4.set_title('Kokonaistulos')
ax4.set_xlabel('w')
ax4.set_ylabel('e')

plt.savefig('perus_tulos.png', format='png', dpi=1200)
#plt.show()

# %% Lama

VARASTO = 0
KOKONAISTULOS = 0
VALMISTETUT_YKSIKOT = 0
MYYNTIHINTA = 22000
VARASTO_STATE = 0

lama_v_ajat = []
lama_v_yksikot = []
lama_varasto = []
lama_voitto = []
lama_tappio = []
lama_tulos = []
lama_kokonaistulos = []
lama_tv_kust = []
lama_kiint_kust = []

for t in range(ALOITUS_W, LOPETUS_W +1, AIKAVALI):
    KYSYNTA_W = max(50 - t, 25)
    if VARASTO + 50 > VARASTO_KAPASITEETTI:
        TUOTANTO_W = 0
        VARASTO_STATE = -1
    elif VARASTO_STATE == -1 and VARASTO - KYSYNTA_W > 10:
        TUOTANTO_W = 0
    else:
        TUOTANTO_W = 50
        VARASTO_STATE = 0
    VALMISTETUT_YKSIKOT += TUOTANTO_W
    VARASTO += TUOTANTO_W - KYSYNTA_W
    
    N_TUOTTEEN_VALMISTUSAIKA = EKAN_TUOTTEEN_VALMISTUSAIKA * VALMISTETUT_YKSIKOT ** (math.log2(1-OPPIMISNOPEUS))
       
    if VARASTO > VARASTO_KAPASITEETTI:
        VAKUUTUSMAKSUT_W = 500+VARASTO*10
        VUOKRAKUSTANNUKSET_W = 1200 + 200
    else:
        VAKUUTUSMAKSUT_W = 500
        VUOKRAKUSTANNUKSET_W = 1200
        
    SAHKOMAKSUT_W = 20 * TUOTANTO_W
    VESIMAKSUT_W = 2 * TUOTANTO_W
    
    KIINTEAT_KUSTANNUKSET_W = MARKKINOINNIN_KULUT_W + HALLINTOKULUT_W + VAKUUTUSMAKSUT_W + VUOKRAKUSTANNUKSET_W + SAHKOMAKSUT_W + VESIMAKSUT_W
    RAAKA_AINE_KUSTANNUKSET_W = RAAKA_AINE_KUSTANNUKSET_PER_YKSIKKO * TUOTANTO_W
    TYOVOIMAKUSTANNUKSET_W = TUOTANTO_W * N_TUOTTEEN_VALMISTUSAIKA * TYONTEKIJOIDEN_TUNTIHINTA
    
    VOITTO_W = KYSYNTA_W * MYYNTIHINTA
    TAPPIO_W = TYOVOIMAKUSTANNUKSET_W + RAAKA_AINE_KUSTANNUKSET_W + KIINTEAT_KUSTANNUKSET_W
    TULOS_W = VOITTO_W - TAPPIO_W
    
    KOKONAISTULOS += TULOS_W
    
    lama_v_ajat.append(N_TUOTTEEN_VALMISTUSAIKA)
    lama_v_yksikot.append(VALMISTETUT_YKSIKOT)
    lama_varasto.append(VARASTO)
    lama_voitto.append(VOITTO_W)
    lama_tappio.append(TAPPIO_W)
    lama_tulos.append(TULOS_W)
    lama_kokonaistulos.append(KOKONAISTULOS)
    lama_tv_kust.append(TYOVOIMAKUSTANNUKSET_W)
    lama_kiint_kust.append(KIINTEAT_KUSTANNUKSET_W)
    
fig = plt.figure(2)
plt.subplots_adjust(left=0.15, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
plt.suptitle('Lama')
ax1 = fig.add_subplot(2,2,1)
ax1.plot(range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), lama_voitto, 'go-')
ax1.set_title('Voitto')
ax1.set_xlabel('w')
ax1.set_ylabel('e')

ax2 = fig.add_subplot(2,2,2)
ax2.plot(range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), lama_tappio, 'ro-')
ax2.set_title('Tappio')
ax2.set_xlabel('w')
ax2.set_ylabel('e')

ax3 = fig.add_subplot(2,2,3)
ax3.plot(range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), lama_tulos, 'bo-')
ax3.set_title('Tulos')
ax3.set_xlabel('w')
ax3.set_ylabel('e')

ax4 = fig.add_subplot(2,2,4)
ax4.plot(range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), lama_kokonaistulos, 'bo-')
ax4.set_title('Kokonaistulos')
ax4.set_xlabel('w')
ax4.set_ylabel('e')

plt.savefig('lama_tulos.png', format='png', dpi=1200)
#plt.show()

# %% Nousu

nousu_v_ajat = []
nousu_v_yksikot = []
nousu_varasto = []
nousu_voitto = []
nousu_tappio = []
nousu_tulos = []
nousu_kokonaistulos = []
nousu_tv_kust = []
nousu_kiint_kust = []

VARASTO = 0
KOKONAISTULOS = 0
VALMISTETUT_YKSIKOT = 0
MYYNTIHINTA = 25000
VARASTO_STATE = 0
KYSYNTA_LAST = 50

for t in range(ALOITUS_W, LOPETUS_W +1, AIKAVALI):
    KYSYNTA_W = min(50 + t, 65)
    if VARASTO + 50 > VARASTO_KAPASITEETTI:
        TUOTANTO_W = 0
        VARASTO_STATE = -1
    elif VARASTO_STATE == -1 and VARASTO - KYSYNTA_W > 10:
        TUOTANTO_W = 0
    elif KYSYNTA_W > TUOTANTO_W:
        KYSYNTA_LAST = KYSYNTA_W + 5
        TUOTANTO_W = KYSYNTA_LAST
        VARASTO_STATE = 1
    else:
        TUOTANTO_W = KYSYNTA_LAST
        VARASTO_STATE = 0
    VALMISTETUT_YKSIKOT += TUOTANTO_W
    VARASTO += TUOTANTO_W - KYSYNTA_W
    
    N_TUOTTEEN_VALMISTUSAIKA = EKAN_TUOTTEEN_VALMISTUSAIKA * VALMISTETUT_YKSIKOT ** (math.log2(1-OPPIMISNOPEUS))
       
    if VARASTO > VARASTO_KAPASITEETTI:
        VAKUUTUSMAKSUT_W = 500+VARASTO*10
        VUOKRAKUSTANNUKSET_W = 1200 + 200
    else:
        VAKUUTUSMAKSUT_W = 500
        VUOKRAKUSTANNUKSET_W = 1200
        
    SAHKOMAKSUT_W = 20 * TUOTANTO_W
    VESIMAKSUT_W = 2 * TUOTANTO_W
    
    if t > 20:
        TYONTEKIJOIDEN_TUNTIHINTA = 150
        RAAKA_AINE_KUSTANNUKSET_PER_YKSIKKO = 15000
    
    KIINTEAT_KUSTANNUKSET_W = MARKKINOINNIN_KULUT_W + HALLINTOKULUT_W + VAKUUTUSMAKSUT_W + VUOKRAKUSTANNUKSET_W + SAHKOMAKSUT_W + VESIMAKSUT_W
    RAAKA_AINE_KUSTANNUKSET_W = RAAKA_AINE_KUSTANNUKSET_PER_YKSIKKO * TUOTANTO_W
    TYOVOIMAKUSTANNUKSET_W = TUOTANTO_W * N_TUOTTEEN_VALMISTUSAIKA * TYONTEKIJOIDEN_TUNTIHINTA
    
    VOITTO_W = KYSYNTA_W * MYYNTIHINTA
    TAPPIO_W = TYOVOIMAKUSTANNUKSET_W + RAAKA_AINE_KUSTANNUKSET_W + KIINTEAT_KUSTANNUKSET_W
    TULOS_W = VOITTO_W - TAPPIO_W
    
    KOKONAISTULOS += TULOS_W
    
    nousu_v_ajat.append(N_TUOTTEEN_VALMISTUSAIKA)
    nousu_v_yksikot.append(VALMISTETUT_YKSIKOT)
    nousu_varasto.append(VARASTO)
    nousu_voitto.append(VOITTO_W)
    nousu_tappio.append(TAPPIO_W)
    nousu_tulos.append(TULOS_W)
    nousu_kokonaistulos.append(KOKONAISTULOS)
    nousu_tv_kust.append(TYOVOIMAKUSTANNUKSET_W)
    nousu_kiint_kust.append(KIINTEAT_KUSTANNUKSET_W)

fig = plt.figure(3)
plt.subplots_adjust(left=0.15, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
plt.suptitle('Nousukausi')
ax1 = fig.add_subplot(2,2,1)
ax1.plot(range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), nousu_voitto, 'go-')
ax1.set_title('Voitto')
ax1.set_xlabel('w')
ax1.set_ylabel('e')

ax2 = fig.add_subplot(2,2,2)
ax2.plot(range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), nousu_tappio, 'ro-')
ax2.set_title('Tappio')
ax2.set_xlabel('w')
ax2.set_ylabel('e')

ax3 = fig.add_subplot(2,2,3)
ax3.plot(range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), nousu_tulos, 'bo-')
ax3.set_title('Tulos')
ax3.set_xlabel('w')
ax3.set_ylabel('e')

ax4 = fig.add_subplot(2,2,4)
ax4.plot(range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), nousu_kokonaistulos, 'bo-')
ax4.set_title('Kokonaistulos')
ax4.set_xlabel('w')
ax4.set_ylabel('e')

fig.savefig('nousu_tulos.png', format='png', dpi=1200)

# %% Figs

#fig = plt.figure(figsize = [10,10])
plt.figure(4)
plt.subplots_adjust(left=0.15, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
plt.title('Voitot')
plt.xlabel('w')
plt.ylabel('e')

plt.plot(range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), nousu_voitto, 'go-'       
         , range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), perus_voitto, 'bo-'
         , range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), lama_voitto, 'ro-')
plt.legend(['Nousukausi', 'Perus', 'Lama'])

plt.savefig('voitot.png', format='png', dpi=1200)

# %%

plt.figure(5)
plt.subplots_adjust(left=0.15, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
plt.title('Tappiot')
plt.xlabel('w')
plt.ylabel('e')

plt.plot(range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), nousu_tappio, 'go-'
         , range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), perus_tappio, 'bo-'
         , range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), lama_tappio, 'ro-')
plt.legend(['Nousukausi', 'Perus', 'Lama'])

plt.savefig('tappiot.png', format='png', dpi=1200)

# %%

plt.figure(6)
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
plt.title('Kokonaistulos')
plt.xlabel('w')
plt.ylabel('e')

plt.plot(range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), nousu_kokonaistulos, 'go-'
         , range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), perus_kokonaistulos, 'bo-'
         , range(ALOITUS_W, LOPETUS_W +1, AIKAVALI), lama_kokonaistulos, 'ro-')
plt.legend(['Nousukausi', 'Perus', 'Lama'])

plt.savefig('koktulokset.png', format='png', dpi=1200)

# %% Simulaatio tasolle 0,25 viikko 20 Perus

Oppimisnopeus = 0.1
EKAN_TUOTTEEN_VALMISTUSAIKA = 100
RAAKA_AINE_KUSTANNUKSET_PER_YKSIKKO = 14700

MARKKINOINNIN_KULUT_W = 2000
HALLINTOKULUT_W = 400
VARASTO_KAPASITEETTI = 200
UUSI_VARASTO_KAPASITEETTI = 400
TYONTEKIJOIDEN_TUNTIHINTA = 123

ALOITUS_W = 1
LOPETUS_W = 20
AIKAVALI = 1
n = 128

MYYNTIHINTA = 23500

ERROR = 0.005

perus_v_ajat = [35]

while (perus_v_ajat[-1] > 25 or perus_v_ajat[-1] <= 25 - ERROR):
    
    VARASTO = 0
    KOKONAISTULOS = 0
    VALMISTETUT_YKSIKOT = 0
    
    Oppimisnopeus_VANHA = Oppimisnopeus
    if perus_v_ajat[-1] > 25:
        Oppimisnopeus += 0.0001 * n
        n = max(n/2,0.01)
    else:
        Oppimisnopeus -= 0.0001 * n
        n = max(n/2,0.01)

    perus_v_ajat = []
    perus_v_yksikot = []
    perus_varasto = []
    perus_voitto = []
    perus_tappio = []
    perus_tulos = []
    perus_kokonaistulos = []
    perus_tv_kust = []
    perus_kiint_kust = []
    
    
    
    for t in range(ALOITUS_W, LOPETUS_W +1, AIKAVALI):
        KYSYNTA_W = 50
        TUOTANTO_W = 50
        VALMISTETUT_YKSIKOT += TUOTANTO_W
        VARASTO += TUOTANTO_W - KYSYNTA_W
        
        N_TUOTTEEN_VALMISTUSAIKA = EKAN_TUOTTEEN_VALMISTUSAIKA * VALMISTETUT_YKSIKOT ** (math.log2(1-Oppimisnopeus))
        
        if VARASTO > VARASTO_KAPASITEETTI:
            VAKUUTUSMAKSUT_W = 500+VARASTO*10
            VUOKRAKUSTANNUKSET_W = 1200 + 200
        else:
            VAKUUTUSMAKSUT_W = 500
            VUOKRAKUSTANNUKSET_W = 1200
            
        SAHKOMAKSUT_W = 20 * TUOTANTO_W
        VESIMAKSUT_W = 2 * TUOTANTO_W
        
        KIINTEAT_KUSTANNUKSET_W = MARKKINOINNIN_KULUT_W + HALLINTOKULUT_W + VAKUUTUSMAKSUT_W + VUOKRAKUSTANNUKSET_W + SAHKOMAKSUT_W + VESIMAKSUT_W
        RAAKA_AINE_KUSTANNUKSET_W = RAAKA_AINE_KUSTANNUKSET_PER_YKSIKKO * TUOTANTO_W
        TYOVOIMAKUSTANNUKSET_W = TUOTANTO_W * N_TUOTTEEN_VALMISTUSAIKA * TYONTEKIJOIDEN_TUNTIHINTA
        
        VOITTO_W = KYSYNTA_W * MYYNTIHINTA
        TAPPIO_W = TYOVOIMAKUSTANNUKSET_W + RAAKA_AINE_KUSTANNUKSET_W + KIINTEAT_KUSTANNUKSET_W
        TULOS_W = VOITTO_W - TAPPIO_W
        
        KOKONAISTULOS += TULOS_W
        
        perus_v_ajat.append(N_TUOTTEEN_VALMISTUSAIKA)
        perus_v_yksikot.append(VALMISTETUT_YKSIKOT)
        perus_varasto.append(VARASTO)
        perus_voitto.append(VOITTO_W)
        perus_tappio.append(TAPPIO_W)
        perus_tulos.append(TULOS_W)
        perus_kokonaistulos.append(KOKONAISTULOS)
        perus_tv_kust.append(TYOVOIMAKUSTANNUKSET_W)
        perus_kiint_kust.append(KIINTEAT_KUSTANNUKSET_W)
        
    #print(perus_v_ajat[-1])
    
print("Oppimisnopeus peruskautena: ", Oppimisnopeus)

# %% Simulaatio tasolle 0,25 viikko 20 Lama

Oppimisnopeus = 0.1
ALOITUS_W = 1
LOPETUS_W = 20
n = 128
lama_v_ajat = [35]

while (lama_v_ajat[-1] > 25 or lama_v_ajat[-1] <= 25 - ERROR):
    
    VARASTO = 0
    KOKONAISTULOS = 0
    VALMISTETUT_YKSIKOT = 0
    MYYNTIHINTA = 22000
    VARASTO_STATE = 0
    
    Oppimisnopeus_VANHA = Oppimisnopeus
    if lama_v_ajat[-1] > 25:
        Oppimisnopeus += 0.0001 * n
        n = max(n/2,0.01)
    else:
        Oppimisnopeus -= 0.0001 * n
        n = max(n/2,0.01)

    lama_v_ajat = []
    lama_v_yksikot = []
    lama_varasto = []
    lama_voitto = []
    lama_tappio = []
    lama_tulos = []
    lama_kokonaistulos = []
    lama_tv_kust = []
    lama_kiint_kust = []
    
    for t in range(ALOITUS_W, LOPETUS_W +1, AIKAVALI):
        KYSYNTA_W = max(50 - t, 25)
        if VARASTO + 50 > VARASTO_KAPASITEETTI:
            TUOTANTO_W = 0
            VARASTO_STATE = -1
        elif VARASTO_STATE == -1 and VARASTO - KYSYNTA_W > 10:
            TUOTANTO_W = 0
        else:
            TUOTANTO_W = 50
            VARASTO_STATE = 0
        VALMISTETUT_YKSIKOT += TUOTANTO_W
        VARASTO += TUOTANTO_W - KYSYNTA_W
        
        N_TUOTTEEN_VALMISTUSAIKA = EKAN_TUOTTEEN_VALMISTUSAIKA * VALMISTETUT_YKSIKOT ** (math.log2(1-Oppimisnopeus))
           
        if VARASTO > VARASTO_KAPASITEETTI:
            VAKUUTUSMAKSUT_W = 500+VARASTO*10
            VUOKRAKUSTANNUKSET_W = 1200 + 200
        else:
            VAKUUTUSMAKSUT_W = 500
            VUOKRAKUSTANNUKSET_W = 1200
            
        SAHKOMAKSUT_W = 20 * TUOTANTO_W
        VESIMAKSUT_W = 2 * TUOTANTO_W
        
        KIINTEAT_KUSTANNUKSET_W = MARKKINOINNIN_KULUT_W + HALLINTOKULUT_W + VAKUUTUSMAKSUT_W + VUOKRAKUSTANNUKSET_W + SAHKOMAKSUT_W + VESIMAKSUT_W
        RAAKA_AINE_KUSTANNUKSET_W = RAAKA_AINE_KUSTANNUKSET_PER_YKSIKKO * TUOTANTO_W
        TYOVOIMAKUSTANNUKSET_W = TUOTANTO_W * N_TUOTTEEN_VALMISTUSAIKA * TYONTEKIJOIDEN_TUNTIHINTA
        
        VOITTO_W = KYSYNTA_W * MYYNTIHINTA
        TAPPIO_W = TYOVOIMAKUSTANNUKSET_W + RAAKA_AINE_KUSTANNUKSET_W + KIINTEAT_KUSTANNUKSET_W
        TULOS_W = VOITTO_W - TAPPIO_W
        
        KOKONAISTULOS += TULOS_W
        
        lama_v_ajat.append(N_TUOTTEEN_VALMISTUSAIKA)
        lama_v_yksikot.append(VALMISTETUT_YKSIKOT)
        lama_varasto.append(VARASTO)
        lama_voitto.append(VOITTO_W)
        lama_tappio.append(TAPPIO_W)
        lama_tulos.append(TULOS_W)
        lama_kokonaistulos.append(KOKONAISTULOS)
        lama_tv_kust.append(TYOVOIMAKUSTANNUKSET_W)
        lama_kiint_kust.append(KIINTEAT_KUSTANNUKSET_W)

    #print(lama_v_ajat[-1])
    
print("Oppimisnopeus lamakautena: ", Oppimisnopeus)    


# %% Simulaatio tasolle 0,25 viikko 20 Nousu

Oppimisnopeus = 0.1
n = 128
nousu_v_ajat = [35]

while (nousu_v_ajat[-1] > 25 or nousu_v_ajat[-1] <= 25 - ERROR):
    
    VARASTO = 0
    KOKONAISTULOS = 0
    VALMISTETUT_YKSIKOT = 0
    MYYNTIHINTA = 25000
    VARASTO_STATE = 0
    KYSYNTA_LAST = 50
    
    Oppimisnopeus_VANHA = Oppimisnopeus
    if nousu_v_ajat[-1] > 25:
        Oppimisnopeus += 0.0001 * n
        n = max(n/2,0.01)
    else:
        Oppimisnopeus -= 0.0001 * n
        n = max(n/2,0.01)

    nousu_v_ajat = []
    nousu_v_yksikot = []
    nousu_varasto = []
    nousu_voitto = []
    nousu_tappio = []
    nousu_tulos = []
    nousu_kokonaistulos = []
    nousu_tv_kust = []
    nousu_kiint_kust = []
    
    
    for t in range(ALOITUS_W, LOPETUS_W +1, AIKAVALI):
        KYSYNTA_W = min(50 + t, 65)
        if VARASTO + 50 > VARASTO_KAPASITEETTI:
            TUOTANTO_W = 0
            VARASTO_STATE = -1
        elif VARASTO_STATE == -1 and VARASTO - KYSYNTA_W > 10:
            TUOTANTO_W = 0
        elif KYSYNTA_W > TUOTANTO_W:
            KYSYNTA_LAST = KYSYNTA_W + 5
            TUOTANTO_W = KYSYNTA_LAST
            VARASTO_STATE = 1
        else:
            TUOTANTO_W = KYSYNTA_LAST
            VARASTO_STATE = 0
        VALMISTETUT_YKSIKOT += TUOTANTO_W
        VARASTO += TUOTANTO_W - KYSYNTA_W
        
        N_TUOTTEEN_VALMISTUSAIKA = EKAN_TUOTTEEN_VALMISTUSAIKA * VALMISTETUT_YKSIKOT ** (math.log2(1-Oppimisnopeus))
           
        if VARASTO > VARASTO_KAPASITEETTI:
            VAKUUTUSMAKSUT_W = 500+VARASTO*10
            VUOKRAKUSTANNUKSET_W = 1200 + 200
        else:
            VAKUUTUSMAKSUT_W = 500
            VUOKRAKUSTANNUKSET_W = 1200
            
        SAHKOMAKSUT_W = 20 * TUOTANTO_W
        VESIMAKSUT_W = 2 * TUOTANTO_W
        
        if t > 20:
            TYONTEKIJOIDEN_TUNTIHINTA = 150
            RAAKA_AINE_KUSTANNUKSET_PER_YKSIKKO = 15000
        
        KIINTEAT_KUSTANNUKSET_W = MARKKINOINNIN_KULUT_W + HALLINTOKULUT_W + VAKUUTUSMAKSUT_W + VUOKRAKUSTANNUKSET_W + SAHKOMAKSUT_W + VESIMAKSUT_W
        RAAKA_AINE_KUSTANNUKSET_W = RAAKA_AINE_KUSTANNUKSET_PER_YKSIKKO * TUOTANTO_W
        TYOVOIMAKUSTANNUKSET_W = TUOTANTO_W * N_TUOTTEEN_VALMISTUSAIKA * TYONTEKIJOIDEN_TUNTIHINTA
        
        VOITTO_W = KYSYNTA_W * MYYNTIHINTA
        TAPPIO_W = TYOVOIMAKUSTANNUKSET_W + RAAKA_AINE_KUSTANNUKSET_W + KIINTEAT_KUSTANNUKSET_W
        TULOS_W = VOITTO_W - TAPPIO_W
        
        KOKONAISTULOS += TULOS_W
        
        nousu_v_ajat.append(N_TUOTTEEN_VALMISTUSAIKA)
        nousu_v_yksikot.append(VALMISTETUT_YKSIKOT)
        nousu_varasto.append(VARASTO)
        nousu_voitto.append(VOITTO_W)
        nousu_tappio.append(TAPPIO_W)
        nousu_tulos.append(TULOS_W)
        nousu_kokonaistulos.append(KOKONAISTULOS)
        nousu_tv_kust.append(TYOVOIMAKUSTANNUKSET_W)
        nousu_kiint_kust.append(KIINTEAT_KUSTANNUKSET_W)

    #print(nousu_v_ajat[-1])
    
print("Oppimisnopeus nousukautena: ", Oppimisnopeus)