import itertools
import random
def inside_circle(x1, y1, x2, y2, r1, r2): 
   
        distSq = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2);  
        radSumSq = (r1 + r2) * (r1 + r2);  
        if (distSq == radSumSq): 
            return 1 
        elif (distSq > radSumSq): 
            return -1 
        else: 
            return 0 


def circ(x,y,y0,x0):
        return ((x-x0)**2+(y-y0)**2) 


def intersect_2_or_3(circ_ra, overlapping_regions, ind_circ):
    threeintersectvals=[]
    threeintersectsets=[]
    twointersectvals=[]
    twointersectsets=[]
    newinds=ind_circ
    for d in range(0,len(circ_ra)):

        for s in range(0,len(overlapping_regions)):

            for t in range(0,len(overlapping_regions[s])):

                if d==s and overlapping_regions[s][t][0]!=d:

                    threeintersectvals.append([d,overlapping_regions[s][t][0], overlapping_regions[s][t][1]])
                    threeintersectsets.append(set(ind_circ[d]).intersection(ind_circ[overlapping_regions[s][t][0]], ind_circ[overlapping_regions[s][t][1]]))
                if d==s and overlapping_regions[s][t][0]!=d:
                    if [d,overlapping_regions[s][t][0]] not in twointersectvals and [overlapping_regions[s][t][0],d] not in twointersectvals:
                        twointersectvals.append([d,overlapping_regions[s][t][0]])
                        twointersectsets.append(set(ind_circ[d]).intersection(ind_circ[overlapping_regions[s][t][0]]))

                        twointersectsets[-1]=[elem for elem in twointersectsets[-1] if elem not in threeintersectsets]
                        
                if d==s and overlapping_regions[s][t][1]!=d:
                    if [d,overlapping_regions[s][t][1]] not in twointersectvals and [overlapping_regions[s][t][1],d ] not in twointersectvals:
                        twointersectvals.append([d,overlapping_regions[s][t][1]])
                        twointersectsets.append(set(ind_circ[d]).intersection(ind_circ[overlapping_regions[s][t][1]]))
                        twointersectsets[-1]=[elem for elem in twointersectsets[-1] if elem not in threeintersectsets]
                if d==s and overlapping_regions[s][t][0]!=overlapping_regions[s][t][1]:
                    if [overlapping_regions[s][t][0],overlapping_regions[s][t][1]] not in twointersectvals and [overlapping_regions[s][t][1],overlapping_regions[s][t][0]] not in twointersectvals:
                        
                        
                        twointersectvals.append([overlapping_regions[s][t][0],overlapping_regions[s][t][1]])
                        twointersectsets.append(set(ind_circ[overlapping_regions[s][t][0]]).intersection(ind_circ[overlapping_regions[s][t][1]]))
                        twointersectsets[-1]=[elem for elem in twointersectsets[-1] if elem not in threeintersectsets]
    

    threelist=list(itertools.chain.from_iterable(threeintersectsets))
    return twointersectsets, threeintersectsets, twointersectvals, threeintersectvals,threelist


def split_between_3_overlap(circ_ra, threeintersectvals, threeintersectsets, ra_incirc, dec_incirc, ind_circ,ra_incontour,dec_incontour):
    
    for d in range(0,len(circ_ra)):

        for t in range(0,len(threeintersectvals)):
            if threeintersectvals[t][0]==d:

                if len(threeintersectsets[t])>=3:
                    first=threeintersectvals[t][0]
                    second=threeintersectvals[t][1]
                    third=threeintersectvals[t][2]
                    slen = round(len(set(threeintersectsets[t])) / 3) # we need 3 subsets
                    
                    set1 = set(random.sample(threeintersectsets[t], slen)) # 1st random subset
                    set11 = [ra_incontour[i] for i in list(set1)] 
                    set11d = [dec_incontour[i] for i in list(set1)] 
                    set1ind=[i for i in list(set1)]
                   
                    ra_incirc[first]+=set11
                    dec_incirc[first]+=set11d
                    ind_circ[first]+=set1ind
                    threeintersectsets[t] -= set1

                    set2 = set(random.sample(threeintersectsets[t], slen)) # 2nd random subset
                    set21 = [ra_incontour[i] for i in list(set2)] 
                    set21d = [dec_incontour[i] for i in list(set2)] 
                    set21ind = [i for i in list(set2)] 
                    ra_incirc[second]+=set21
                    dec_incirc[second]+=set21d
                    ind_circ[second]+=set21ind
                    threeintersectsets[t] -= set2
                    set3 = threeintersectsets[t] # 3rd random subset
                    set31=[ra_incontour[i] for i in list(set3)] 
                    set31d=[dec_incontour[i] for i in list(set3)]
                    set31ind=[i for i in list(set3)]
                    ra_incirc[third]+=set31
                    dec_incirc[third]+=set31d
                    ind_circ[third]+=set31ind
                    
                    

                elif len(threeintersectsets[t])>0:
                    first=threeintersectvals[t][0]

                    set1=threeintersectsets[t]
                    set11=[ra_incontour[i] for i in list(set1)] 
                    set11d=[dec_incontour[i] for i in list(set1)] 
                    set11ind=[i for i in list(set1)] 
                    
                    ra_incirc[first]+=set11
                    dec_incirc[first]+=set11d
                    ind_circ[first]+=set11ind

    return ra_incirc, dec_incirc, ind_circ
def split_between_2_overlap(circ_ra, twointersectvals, twointersectsets, ra_incirc, dec_incirc, ind_circ,ra_incontour,dec_incontour):
    for d in range(0,len(circ_ra)):

        for t in range(0,len(twointersectvals)):
            if twointersectvals[t][0]==d:

                if len(twointersectsets[t])>=2:
                    first=twointersectvals[t][0]
                    second=twointersectvals[t][1]
                    
                    slen = round(len(set(twointersectsets[t])) / 2) # we need 2 subsets
                    
                    set1 = set(random.sample(twointersectsets[t], slen)) # 1st random subset
                    set11 = [ra_incontour[i] for i in list(set1)] 
                    set11d = [dec_incontour[i] for i in list(set1)]
                    set11ind = [i for i in list(set1)]  
                   
                    ra_incirc[first]+=set11
                    dec_incirc[first]+=set11d
                    ind_circ[first]+=set11ind
                    twointersectsets[t] = [item for item in twointersectsets[t] if item not in set1]
                    

                    set2 = twointersectsets[t] # 2nd random subset
                    set21 = [ra_incontour[i] for i in list(set2)] 
                    set21d = [dec_incontour[i] for i in list(set2)] 
                    set21ind = [i for i in list(set2)] 
                    ra_incirc[second]+=set21
                    dec_incirc[second]+=set21d
                    ind_circ[second]+=set21ind
                    
                    
 
                elif len(twointersectsets[t])>0:
                    first=twointersectvals[t][0]

                    set1=twointersectsets[t]
                    
                    set11=[ra_incontour[i] for i in list(set1)] 
                    set11d=[dec_incontour[i] for i in list(set1)] 
                    set11ind=[i for i in list(set1)] 
                    
                    ra_incirc[first]+=set11
                    dec_incirc[first]+=set11d
                    ind_circ[first]+=set11ind

    return ra_incirc, dec_incirc, ind_circ