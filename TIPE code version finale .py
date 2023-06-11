
from vpython import *
from time import *

scene.width = 1000
scene.height = 600
scene.range = 2000
scene.background = color.black

lim_cube_univers = 10**4
G = 6.7e-11
Rsun = 2E9
vitesse = sqrt(G*2E30/Rsun)

scene.width = scene.height = 600
scene.range = 2000
scene.background = color.white

soleil = sphere(pos = vector (0,0,0),radius = 30, color = color.yellow, emissive = True, make_trail=True, trail_type='points', interval=10, retain=50)
soleil.masse = 2e30
soleil.vitesse = vector (0,0,0)
soleilC = ((soleil.pos.x,soleil.pos.y,soleil.pos.z),soleil.masse,soleil.vitesse)

mercure = sphere(pos = vector (110,0,0),radius = 5, color = vector(0.6,0.6,0.6), make_trail=True, trail_type='points', interval=10, retain=25)
mercure.masse = 3.3e23
mercure.vitesse = vector(0,0,-4*vitesse*10e2)
mercureC = ((mercure.pos.x,mercure.pos.y,mercure.pos.z),mercure.masse, mercure.vitesse)

venus = sphere(pos = vector (180,0,0),radius = 7, color = vector(0.6,0.6,1), make_trail=True, trail_type='points', interval=10, retain=40)
venus.masse = 4.9e24
venus.vitesse = vector(0,0,-3.5*vitesse*10e2)
venusC = ((venus.pos.x,venus.pos.y,venus.pos.z),venus.masse, venus.vitesse)

terre = sphere(pos = vector (240,0,0),radius = 8, color = vector(0.2,0.2,1), make_trail=True, trail_type='points', interval=10, retain=50)
terre.masse = 6e24
terre.vitesse = vector(0,0,-3*vitesse*10e2)
terreC = ((terre.pos.x,terre.pos.y,terre.pos.z),terre.masse, terre.vitesse)

mars = sphere(pos = vector (290,0,0),radius = 7, color = color.red, make_trail=True, trail_type='points', interval=10, retain=50)
mars.masse = 6.4e23
mars.vitesse = vector(0,0,-2.7*vitesse*10e2)
marsC = ((mars.pos.x,mars.pos.y,mars.pos.z),mars.masse, mars.vitesse)

jupiter = sphere(pos = vector (500,0,0),radius = 12, color = vector(1,0.7,0), make_trail=True, trail_type='points', interval=10, retain=100)
jupiter.masse = 1.9e27
jupiter.vitesse = vector(0,0,-2*vitesse*10e2)
jupiterC = ((jupiter.pos.x,jupiter.pos.y,jupiter.pos.z),jupiter.masse, jupiter.vitesse)

saturne = sphere(pos = vector (800,0,0),radius = 10, color = vector(1,0.9,0), make_trail=True, trail_type='points', interval=10, retain=100)
saturne.masse = 5.6e26
saturne.vitesse = vector(0,0,-1.6*vitesse*10e2)
saturneC = ((saturne.pos.x,saturne.pos.y,saturne.pos.z),saturne.masse, saturne.vitesse)

uranus = sphere(pos = vector (1200,0,0),radius = 9, color = vector(0.2,0.2,0.5), make_trail=True, trail_type='points', interval=10, retain=100)
uranus.masse = 8.6e25
uranus.vitesse = vector(0,0,-1.2*vitesse*10e2)
uranusC = ((uranus.pos.x,uranus.pos.y,uranus.pos.z),uranus.masse, uranus.vitesse)

neptune = sphere(pos = vector (1600,0,0),radius = 9, color = vector(0.2,0.2,0.7), make_trail=True, trail_type='points', interval=10, retain=1000)
neptune.masse = 1e26
neptune.vitesse = vector(0,0,-1.1*vitesse*10e2)
neptuneC = ((neptune.pos.x,neptune.pos.y,neptune.pos.z),neptune.masse, neptune.vitesse)

tracteur = sphere(pos = vector (1e10,1e10,1e10), radius = 3)

liste_corps_P = [soleilC ,mercureC ,venusC, terreC, marsC, jupiterC, saturneC, uranusC, neptuneC]
liste_corps_V = [soleil ,mercure, venus, terre, mars, jupiter, saturne, uranus, neptune]



class Octree:
  def __init__(self, masse_totale = None, centre_masse = None, liste_corps = None, centre_cube = None, profondeur = None):
    if masse_totale != None:
        self.masse_totale = masse_totale
    else :
        self.masse_totale = 0
    if centre_masse != None :
        self.centre_masse = centre_masse
    else :
        self.centre_masse = None
    if liste_corps != None :
        self.liste_corps = liste_corps
    else :
        self.liste_corps = [ ]
    if centre_cube != None :
        self.centre_cube = centre_cube
    else :
        self.centre_cube = None
    if profondeur != None :
        self.profondeur = profondeur
    else :
        self.profondeur = 1
    self.branche1 = None
    self.branche2 = None
    self.branche3 = None
    self.branche4 = None
    self.branche5 = None
    self.branche6 = None
    self.branche7 = None
    self.branche8 = None

def position(corps,centre_cube):
    if corps[0] <= centre_cube[0] and corps[1] <= centre_cube[1] and corps[2] <= centre_cube[2] :
        return 3
    elif corps[0] >= centre_cube[0] and corps[1] <= centre_cube[1] and corps[2] <= centre_cube[2] :
        return 4
    elif corps[0] <= centre_cube[0] and corps[1] >= centre_cube[1] and corps[2] <= centre_cube[2] :
        return 7
    elif corps[0] <= centre_cube[0] and corps[1] <= centre_cube[1] and corps[2] >= centre_cube[2] :
        return 1
    elif corps[0] >= centre_cube[0] and corps[1] >= centre_cube[1] and corps[2] <= centre_cube[2] :
        return 8
    elif corps[0] >= centre_cube[0] and corps[1] <= centre_cube[1] and corps[2] >= centre_cube[2] :
        return 2
    elif corps[0] <= centre_cube[0] and corps[1] >= centre_cube[1] and corps[2] >= centre_cube[2] :
        return 5
    else:
        return 6

def calcul_centre_cube (arbre,centre_cube,nouvelle_subdivision) :
    n = lim_cube_univers/2**(arbre.profondeur)
    if nouvelle_subdivision == 1 :
        return (centre_cube[0]-n,centre_cube[1]-n,centre_cube[2]+n)
    elif nouvelle_subdivision == 2 :
        return (centre_cube[0]+n,centre_cube[1]-n,centre_cube[2]+n)
    elif nouvelle_subdivision == 3 :
        return (centre_cube[0]-n,centre_cube[1]-n,centre_cube[2]-n)
    elif nouvelle_subdivision == 4 :
        return (centre_cube[0]+n,centre_cube[1]-n,centre_cube[2]-n)
    elif nouvelle_subdivision == 5 :
        return (centre_cube[0]-n,centre_cube[1]+n,centre_cube[2]+n)
    elif nouvelle_subdivision == 6 :
        return (centre_cube[0]+n,centre_cube[1]+n,centre_cube[2]+n)
    elif nouvelle_subdivision == 7 :
        return (centre_cube[0]-n,centre_cube[1]+n,centre_cube[2]-n)
    else :
        return (centre_cube[0]+n,centre_cube[1]+n,centre_cube[2]-n)

def calcul_centre_masse (univers,corps) :
    ((x,y,z),m,v) = corps
## calcul le nouveau centre de masse lorsqu’on ajoute un corps dans un cube univers
    return (((univers.centre_masse[0]*univers.masse_totale+x*m)/(univers.masse_totale+m),(univers.centre_masse[1]*univers.masse_totale+y*m)/(univers.masse_totale+m), (univers.centre_masse[2]*univers.masse_totale+z*m)/(univers.masse_totale+m)))

def triage (corps, univers, precision) :
    if univers.liste_corps == [ ] : ## cas où le cube univers est vide ou une feuille
        univers.liste_corps.append(corps)
        univers.masse_totale += corps[1]
        univers.centre_masse = corps[0]
    else : ## il y a des corps dans l'univers
        if univers.profondeur == precision :
            univers.liste_corps.append(corps)
            univers.centre_masse = calcul_centre_masse (univers,corps)
            univers.masse_totale += corps[1]
## cas où il n'y a qu'un corps
        elif len(univers.liste_corps) == 1:
## replacer le corps déjà présent
            if position(univers.liste_corps[0][0],univers.centre_cube) == 1 :
                univers.branche1 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,1),profondeur=univers.profondeur + 1)
                triage(univers.liste_corps[0],univers.branche1, precision)
            elif position(univers.liste_corps[0][0],univers.centre_cube) == 2 :
                univers.branche2 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,2),profondeur=univers.profondeur + 1)
                triage(univers.liste_corps[0],univers.branche2, precision)
            elif position(univers.liste_corps[0][0],univers.centre_cube) == 3 :
                univers.branche3 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,3),profondeur=univers.profondeur + 1)
                triage(univers.liste_corps[0],univers.branche3, precision)
            elif position(univers.liste_corps[0][0],univers.centre_cube) == 4 :
                univers.branche4 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,4),profondeur=univers.profondeur + 1)
                triage(univers.liste_corps[0],univers.branche4, precision)
            elif position(univers.liste_corps[0][0],univers.centre_cube) == 5 :
                univers.branche5 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,5),profondeur=univers.profondeur + 1)
                triage(univers.liste_corps[0],univers.branche5, precision)
            elif position(univers.liste_corps[0][0],univers.centre_cube) == 6 :
                univers.branche6 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,6),profondeur=univers.profondeur + 1)
                triage(univers.liste_corps[0],univers.branche6, precision)
            elif position(univers.liste_corps[0][0],univers.centre_cube) == 7 :
                univers.branche7 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,7),profondeur=univers.profondeur + 1)
                triage(univers.liste_corps[0],univers.branche7, precision)
            else :
                univers.branche8 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,8),profondeur=univers.profondeur + 1)
                triage(univers.liste_corps[0],univers.branche8, precision)
## désormais on place le corps que l'on doit trier
            univers.liste_corps.append(corps)
            univers.centre_masse = calcul_centre_masse (univers,corps)
            univers.masse_totale += corps[1]
            if position(corps[0],univers.centre_cube) == 1 :
                if univers.branche1 == None :
                    univers.branche1 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,1),profondeur=univers.profondeur + 1)
                    triage(corps,univers.branche1, precision)
                else :
                    triage(corps,univers.branche1, precision)
            elif position(corps[0],univers.centre_cube) == 2 :
                if univers.branche2 == None :
                    univers.branche2 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,2),profondeur=univers.profondeur + 1)
                    triage(corps,univers.branche2, precision)
                else :
                    triage(corps,univers.branche2, precision)
            elif position(corps[0],univers.centre_cube) == 3 :
                if univers.branche3 == None :
                    univers.branche3 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,3),profondeur=univers.profondeur + 1)
                    triage(corps,univers.branche3, precision)
                else :
                    triage(corps,univers.branche3, precision)
            elif position(corps[0],univers.centre_cube) == 4 :
                if univers.branche4 == None :
                    univers.branche4 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,4),profondeur=univers.profondeur + 1)
                    triage(corps,univers.branche4, precision)
                else :
                    triage(corps,univers.branche4, precision)
            elif position(corps[0],univers.centre_cube) == 5 :
                if univers.branche5 == None :
                    univers.branche5 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,5),profondeur=univers.profondeur + 1)
                    triage(corps,univers.branche5, precision)
                else :
                    triage(corps,univers.branche5, precision)
            elif position(corps[0],univers.centre_cube) == 6 :
                if univers.branche6 == None :
                    univers.branche6 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,6),profondeur=univers.profondeur + 1)
                    triage(corps,univers.branche6, precision)
                else :
                    triage(corps,univers.branche6, precision)
            elif position(corps[0],univers.centre_cube) == 7 :
                if univers.branche7 == None :
                    univers.branche7 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,7),profondeur=univers.profondeur + 1)
                    triage(corps,univers.branche7, precision)
                else :
                    triage(corps,univers.branche7, precision)
            else :
                if univers.branche8 == None :
                    univers.branche8 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,8),profondeur=univers.profondeur + 1)
                    triage(corps,univers.branche8, precision)
                else :
                    triage(corps,univers.branche8, precision)
## cas où il y a plus d'un corps dans l'univers
        else :
            univers.liste_corps.append(corps)
            univers.centre_masse = calcul_centre_masse (univers,corps)
            univers.masse_totale += corps[1]
## on a modifié les propriétés du noeud interne, désormais on insère judicieusement le corps dans une branche en fonction de sa position
            if position(corps[0],univers.centre_cube) == 1 :
                if univers.branche1 == None :
                    univers.branche1 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,1),profondeur=univers.profondeur + 1)
                    triage(corps,univers.branche1, precision)
                else :
                    triage(corps,univers.branche1, precision)
            elif position(corps[0],univers.centre_cube) == 2 :
                if univers.branche2 == None :
                    univers.branche2 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,2),profondeur=univers.profondeur + 1)
                    triage(corps,univers.branche2, precision)
                else :
                    triage(corps,univers.branche2, precision)
            elif position(corps[0],univers.centre_cube) == 3 :
                if univers.branche3 == None :
                    univers.branche3 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,3),profondeur=univers.profondeur + 1)
                    triage(corps,univers.branche3, precision)
                else :
                    triage(corps,univers.branche3, precision)
            elif position(corps[0],univers.centre_cube) == 4 :
                if univers.branche4 == None :
                    univers.branche4 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,4),profondeur=univers.profondeur + 1)
                    triage(corps,univers.branche4, precision)
                else :
                    triage(corps,univers.branche4, precision)
            elif position(corps[0],univers.centre_cube) == 5 :
                if univers.branche5 == None :
                    univers.branche5 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,5),profondeur=univers.profondeur + 1)
                    triage(corps,univers.branche5, precision)
                else :
                    triage(corps,univers.branche5, precision)
            elif position(corps[0],univers.centre_cube) == 6 :
                if univers.branche6 == None :
                    univers.branche6 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,6),profondeur=univers.profondeur + 1)
                    triage(corps,univers.branche6, precision)
                else :
                    triage(corps,univers.branche6, precision)
            elif position(corps[0],univers.centre_cube) == 7 :
                if univers.branche7 == None :
                    univers.branche7 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,7),profondeur=univers.profondeur + 1)
                    triage(corps,univers.branche7, precision)
                else :
                    triage(corps,univers.branche7, precision)
            else :
                if univers.branche8 == None :
                    univers.branche8 = Octree(masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = calcul_centre_cube(univers,univers.centre_cube,8),profondeur=univers.profondeur + 1)
                    triage(corps,univers.branche8, precision)
                else :
                    triage(corps,univers.branche8, precision)

def arbre_Barnes_Hut (liste_corps_a_trier, precision) :
    univers = Octree (masse_totale = 0, centre_masse = (0,0,0), liste_corps = [ ], centre_cube = (0,0,0), profondeur = 0)
    while liste_corps_a_trier != [] :
        corps = liste_corps_a_trier[0]
        triage (corps, univers, precision)
        liste_corps_a_trier = liste_corps_a_trier [1:]
    return univers

def force_grav(octree, corps, theta, taille_univers): ## c est le corps étudié sous la forme (centre de masse, masse), k est la profondeur du noeud étudié (0 pour la racine), theta est le paramètre déterminant si les corps sont assez proches pour faire l'approximation
    ((x,y,z),m,v) = corps
    force = vector(0,0,0)
    largeur_cube = taille_univers/2**(octree.profondeur) ##largeur du cube de base divisé par 2 à chaque fois qu'on va plus profond dans l'arbre
    distance = sqrt(abs(x-octree.centre_masse[0])**2 + abs(y-octree.centre_masse[1])**2 + abs(z-octree.centre_masse[2])**2) ##distance entre le corps c et le centre de masse du noeud
##si l'arbre est vide la force appliquée sur c est nulle
    if octree == None :
        return force
##si le noeud est une feuille (=> si on tombe sur un corps) on ajoute sa contribution à la force appliquée sur c
    elif octree.branche1 == None and octree.branche2 == None and octree.branche3 == None and octree.branche4 == None and octree.branche5 == None and octree.branche6 == None and octree.branche7 == None and octree.branche8 == None and (octree.centre_masse[0],octree.centre_masse[1],octree.centre_masse[2]) != (x,y,z) :
        ur = vector(x-octree.centre_masse[0],y-octree.centre_masse[1],z-octree.centre_masse[2])
        force += (-G * octree.masse_totale * m / distance**2)*norm(ur)
        return force
##si il y a au moins 2 corps dans le cube et qu'on peut approximer le groupe de corps en un seul on ajoute à la force totale la force de ce groupe
    elif octree.branche1 == None and octree.branche2 == None and octree.branche3 == None and octree.branche4 == None and octree.branche5 == None and octree.branche6 == None and octree.branche7 == None and octree.branche8 == None and (octree.centre_masse[0],octree.centre_masse[1],octree.centre_masse[2]) == (x,y,z) :
        return vector(0,0,0)
    elif largeur_cube/distance <= theta :
        ur = vector(x-octree.centre_masse[0],y-octree.centre_masse[1],z-octree.centre_masse[2])
        force += (-G * octree.masse_totale * m / distance**2)*norm(ur)
        return force
##si on ne peut pas approximer on calcule la force de chaque branche
    else:
        if octree.branche1 != None :
            force += force_grav(octree.branche1, corps, theta, taille_univers)
        if octree.branche2 != None :
            force += force_grav(octree.branche2, corps, theta, taille_univers)
        if octree.branche3 != None :
            force += force_grav(octree.branche3, corps, theta, taille_univers)
        if octree.branche4 != None :
            force += force_grav(octree.branche4, corps, theta, taille_univers)
        if octree.branche5 != None :
            force += force_grav(octree.branche5, corps, theta, taille_univers)
        if octree.branche6 != None :
            force += force_grav(octree.branche6, corps, theta, taille_univers)
        if octree.branche7 != None :
            force += force_grav(octree.branche7, corps, theta, taille_univers)
        if octree.branche8 != None :
            force += force_grav(octree.branche8, corps, theta, taille_univers)
    return force

# valeur par défaut dt=10**-10
dt = 10e-10
theta = 0.5
# données : masse satellite : 50 tonnes, distance satellite-astéroïde : 14 , puissance de la
#bombe P : 5e17, vitesse du souffle de l'explosion v : , force de l'explosion F = P/v
force_bombe = 5e7
force_gravitationnel = 2e34

##activer les systèmes de défense planétaire :
explosion_nucleaire = False
tracteur_gravitationnel = False

debut = time()
asteroide_bool = False

def dist(planete1,planete2) :
  return(mag(planete1.pos - planete2.pos))
  
def explosion(planete):
  if asteroide_bool == True :
    if explosion_nucleaire == True and planete == asteroide and dist(terre,planete) <= 200 :
      explosion_nucleaire == False
      return(vector (-force_bombe, 0, -force_bombe))
    else :
      return vector(0,0,0)
  else:
    return vector(0,0,0)

def tracteur_grav(planete):
  if asteroide_bool == True :
    if tracteur_gravitationnel == True and planete == asteroide and dist(terre,planete)<=1200:
      tracteur.pos = asteroide.pos + vector (-10,0,-10)
      return(vector(-force_gravitationnel,0,-force_gravitationnel))
    else :
      return(vector(0,0,0))
  else :
    return(vector(0,0,0))

while True :
    rate(100)
    univers = arbre_Barnes_Hut (liste_corps_P,10)
    if time()-debut >= 25 and asteroide_bool == False :
        asteroide = sphere(pos = vector(2000,-2000,0), radius = 5, color = vector(0.6,0.3,0.5),make_trail=True, trail_type='points', interval=1, retain=5000)
        asteroide.masse = 2e19
        asteroide.vitesse = vector(-8.605*vitesse*10e2,7.36*vitesse*10e2,0)
        asteroideC = ((asteroide.pos.x,asteroide.pos.y,asteroide.pos.z),asteroide.masse,asteroide.vitesse)
        liste_corps_P.append(asteroideC)
        liste_corps_V.append(asteroide)
        asteroide_bool = True
    for i in range(1,len(liste_corps_P)) :
        force = force_grav(univers, liste_corps_P[i], theta, lim_cube_univers)
        ((x,y,z),m,v) = liste_corps_P[i]
        v = v + force*dt/m + explosion(liste_corps_V[i])*dt/m + tracteur_grav(liste_corps_V[i])*dt/m
        x = x + v.x*dt
        y = y + v.y*dt
        z = z + v.z*dt
        liste_corps_P[i] = ((x,y,z),m,v)
        liste_corps_V[i].pos.x = x
        liste_corps_V[i].pos.y = y
        liste_corps_V[i].pos.z = z

