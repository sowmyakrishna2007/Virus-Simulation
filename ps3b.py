# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import pylab

class NoChildException(Exception):
   pass

class SimpleVirus(object):
    
    def __init__(self, maxBirthProb, clearProb):
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        
    def getMaxBirthProb(self):
        return self.maxBirthProb

    def getClearProb(self):
        return self.clearProb

    def doesClear(self):
        population = random.random()
        if self.clearProb > population:
            return True
        else:
            return False

    def reproduce(self, popDensity):
        population = random.random()
        if self.maxBirthProb*(1-popDensity) > population:
            return SimpleVirus(self.maxBirthProb,self.clearProb)
        else:
            raise NoChildException

class Patient(object):
    
    def __init__(self, viruses, maxPop):
        self.viruses = viruses
        self.maxPop = maxPop
        
    def getViruses(self):
        return self.viruses

    def getMaxPop(self):
        return self.maxPop

    def getTotalPop(self):
        return len(self.viruses)        

    def update(self):
        for i in self.viruses:
            if i.doesClear() == True:
                self.viruses.remove(i)
        popDensity = len(self.viruses)/self.maxPop
        new = []
        for j in self.viruses:
            try:
                new.append(j.reproduce(popDensity))
            except NoChildException:
                pass
        for virus in new:
                self.viruses.append(virus)
        return len(self.viruses)

class ResistantVirus(SimpleVirus):
   
    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        super().__init__(maxBirthProb,clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

    def getResistances(self):
        return self.resistances

    def getMutProb(self):
        return self.mutProb

    def isResistantTo(self, drug):
        for (a,b) in self.resistances.items():
            if a == drug:
                return b

    def reproduce(self, popDensity, activeDrugs):
        new_dict = {}
        count = 0
        currentStatus = True
        for (a,b) in self.resistances.items():
            if a in activeDrugs:
                if b == False:
                    currentStatus = False
        if currentStatus:
            probability = random.random()
            if self.maxBirthProb*(1-popDensity)>=probability:
                if self.mutProb == 0.0:
                    return ResistantVirus(self.maxBirthProb,self.clearProb,self.resistances,self.mutProb)
                else:
                    mutation = len(self.resistances)*self.mutProb
                for (c,d) in self.resistances.items():
                    if count < mutation:
                        new_dict[c] = not d
                    else:
                        new_dict[c] = d
                    count += 1
                return ResistantVirus(self.maxBirthProb,self.clearProb,new_dict,self.mutProb)
            else:
                raise NoChildException
        else:
            raise NoChildException
                        
class TreatedPatient(Patient):
    
    def __init__(self, viruses, maxPop):
        drugs = []
        self.drugs = drugs
        super().__init__(viruses,maxPop)

    def addPrescription(self, newDrug):
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)

    def getPrescriptions(self):
        return self.drugs

    def getResistPop(self, drugResist):
        population = []
        pop = 0
        for i in self.viruses:
            current = []
            for (a,b) in i.resistances.items():
                if b == True:
                    current.append(a)
            population.append(current)
        for j in population:
            currentStatus = True
            for q in drugResist:
                if q not in j:
                    currentStatus = False
            if currentStatus:
                pop += 1
        return pop
            
    def update(self):
        new = []
        for i in self.viruses:
            if i.doesClear():
                self.viruses.remove(i)
        popDensity = len(self.viruses)/self.maxPop
        for j in self.viruses:
            try:
                new.append(j.reproduce(popDensity,self.drugs))
            except NoChildException:
                pass
        for a in new:
            self.viruses.append(a)
        return len(self.viruses)

def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb, numTrials):
    viruses = []
    virus_stim = []
    for j in range(numTrials):
        for i in range(numViruses):
            viruses.append(SimpleVirus(maxBirthProb,clearProb))
        patient = Patient(viruses,maxPop)
        for p in range(300):
            patient.update()
            if j == 0:   
                virus_stim.append(patient.getTotalPop())
            else:
                virus_stim[p] += patient.getTotalPop()
    new = []
    for i in virus_stim:
        new.append(i/numTrials)
                
    pylab.plot(new, label = "Virus Population")
    pylab.title(f"SimpleVirus Simulation ({numTrials} Trials)")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc = "best")
    pylab.show()

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numTrials):
    total = []
    gutt_resist = []
    
    for j in range(numTrials):
        viruses = []
        virus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
        for i in range(numViruses):
            viruses.append(virus)
        patient = TreatedPatient(viruses,maxPop)
        for i in range(150):
            patient.update()
            if j == 0:
                total.append(patient.getTotalPop())
                gutt_resist.append(patient.getResistPop(["guttagonol"]))
            else:
                total[i] += patient.getTotalPop()
                gutt_resist[i] += patient.getResistPop(["guttagonol"])
        patient.addPrescription("guttagonol")
        for q in range(150):
            patient.update()
            if j == 0:
                total.append(patient.getTotalPop())
                gutt_resist.append(patient.getResistPop(["guttagonol"]))
            else:
                total[q+150] += patient.getTotalPop()
                gutt_resist[q+150] += patient.getResistPop(["guttagonol"])
    new1 = []
    new2 = []
    for i in total:
        new1.append(i/numTrials)
    for i in gutt_resist:
        new2.append(i/numTrials)

    pylab.title(f"ResistantVirus Simulation ({numTrials} Trials)")
    pylab.plot(new1,label="Total Population")
    pylab.legend(loc = "best")
    pylab.plot(new2,label="Resistant Population")
    pylab.legend(loc = "best")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.show()
    
simulationWithoutDrug(1, 90, 0.8, 0.2, 10)
simulationWithDrug(75, 100, 0.8, 0.1, {"guttagonol": True}, 0.2, 10)
