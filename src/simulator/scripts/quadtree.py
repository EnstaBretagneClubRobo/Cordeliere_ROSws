# -*- coding: utf-8 -*-


class Point :
    def __init__(self, coord, donnees=None) :
        self.x, self.y = coord
        self.donnees = donnees

class Rectangle :
    def __init__(self, zone) :
        self.l = zone[0]
        self.r = zone[1]
        self.b = zone[2]
        self.t = zone[3]

        self.zone = zone

    def contient_point(self, p) :
        return p.x >= self.l and p.x <= self.r and p.y >= self.b and p.y <= self.t

    def intersecte(self, r) :
        return not (self.l > r.r or self.r < r.l or self.b > r.t or self.t < r.b)
        

CAPACITE = 1

NO, NE, SO, SE = l, r, b, t = 0, 1, 2, 3
    

class Quadtree :    
    def __init__(self, zone) :
        
        self.l = zone[l]
        self.r = self.l + max(zone[r] - zone[l], zone[t] - zone[b])
        self.b = zone[b]
        self.t = self.b + max(zone[r] - zone[l], zone[t] - zone[b])
        
        self.zone = Rectangle([self.l, self.r, self.b, self.t]) #On veut un carré
        self.points = []
        self.fils = [None, None, None, None]
        

    def taille(self) :
        return len(self.points)
        
        
    def insert(self, point) :

        if not self.zone.contient_point(point) :
            return False #Le point est en dehors du carré

        if self.taille() < CAPACITE and self.fils[0] == None:
            self.points.append(point)
            return True

        else :
            if self.fils[0] == None : self.subdivise()
            if Quadtree.insert(self.fils[NO], point) : return True
            if Quadtree.insert(self.fils[NE], point) : return True
            if Quadtree.insert(self.fils[SO], point) : return True
            if Quadtree.insert(self.fils[SE], point) : return True
    
        return False #ne devrait pas arriver        
            

    def subdivise(self) :
        milong = 0.5 * self.l + 0.5 * self.r
        mihaut = 0.5 * self.b + 0.5 * self.t
        self.fils[NO] = Quadtree([self.l, milong, mihaut, self.t])
        self.fils[NE] = Quadtree([milong, self.r, mihaut, self.t])
        self.fils[SO] = Quadtree([self.l, milong, self.b, mihaut])
        self.fils[SE] = Quadtree([milong, self.r, self.b, mihaut])

        for p in self.points :
            if not (self.fils[NO].insert(p) or self.fils[NE].insert(p) or self.fils[SO].insert(p)or self.fils[SE].insert(p)) :
                    return False #Ne devrait pas arriver
        self.points = []

    def nb_sub(self) :
        if self.fils[0] is None :
            return 0
        else :
            nb = 1
            for i in range(4) :
                nb += Quadtree.nb_sub(self.fils[i])
            return nb

    def hauteur(self) :
        if self.fils[0] is None :
            return 1
        else :
            return 1 + max([Quadtree.hauteur(self.fils[i]) for i in range(4)])


    def recherche(self, zone) :
        zone_rech = Rectangle(zone)
        zone_q = self.zone
        points_trouves = []

        if not zone_rech.intersecte(zone_q) :
            return points_trouves #L'intersection avec le quadtree est vide

        if self.fils[0] is None :
            for v in self.points :
                if zone_rech.contient_point(v) : points_trouves += [Point((v.x, v.y), donnees=v.donnees)]
            
        else :
            for i in range(4) :
                points_trouves += Quadtree.recherche(self.fils[i], zone)

        return points_trouves


    def represente(self) :
        print(self.zone.l, self.zone.r, self.zone.b, self.zone.t)
        for p in self.points :
            print(p.x, p.y, p.donnees, '\n')
        if self.fils[0] is not None :
            print('\n')
            for i in range(4):
                Quadtree.represente(self.fils[i])

    def rech_autour(self, point, rayon) :
        #rayon *= 1 / 111.195 #pour région parisienne
        try:
            point = Point(point)
        except:
            pass
        l = point.x - rayon
        r = point.x + rayon
        b = point.y - rayon
        t = point.y + rayon
        return self.recherche((l,r,b,t))






   
def q_ex() :

    q = Quadtree([0,10,0,10])
    q.insert(Point((1,1)))
    q.insert(Point((2,2)))
    q.insert(Point((3,1)))
    q.insert(Point((7,6)))
    q.insert(Point((6,1)))
    q.insert(Point((7,2)))
    q.insert(Point((8,3)))
    q.insert(Point((9,4)))
    q.insert(Point((1,3)))
    q.insert(Point((4,1)))
    return q


