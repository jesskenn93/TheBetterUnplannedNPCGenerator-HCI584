import csv
import random
import sys
from tkinter import messagebox


class NPC:
    #name = ("FirstName","LastName")
    #race = ""
    #age = 0 # Age Ranges will Differ Per Race
    #gender = "" # male, female, nonbinary. Expanded gender options can be end-user configured.
    # physicalChars = ("eyeColor", "skinColor", "height", "build", "")
    # occupation
    # lifestyle # Options: Wretched, Squalid, Poor, Modest, Comfortable, Wealthy, Aristocratic
    # faith

    namesFilePath = "main\\resources\\names\\"

    def __init__(self, options, race, gender, lifeStage, occType, lifestyle, culture):
        self.options = options


        if (race == "Any"):
            self.race = self.generateRace()
        else:
            self.race = race

        raceTraits = []

        for raceTraitOption in self.options:
            if (self.race == raceTraitOption[0]):
                raceTraits = raceTraitOption
                break

        if (raceTraits.count == 0):
            errorMessage = "Somehow you have selected a race option that doesn't exist, or I am a bad programmer."
            messagebox.showerror("NPC Generation Error", errorMessage)
            sys.exit(errorMessage)
        
        #TODO: Need a better way to map these values. Maybe an object?
        raceLifeStages = [  ("Child",raceTraits[2]),
                            ("Adolescent",raceTraits[3]),
                            ("Young Adult",raceTraits[4]),
                            ("Adult",raceTraits[5]),
                            ("Elder",raceTraits[6]),
                            ("Max",raceTraits[7])   ] # Maximum age possible, not its own lifeStage

        if (gender != "Any"):
            self.gender = gender[0:1]
        else:
            self.gender = self.generateGender()

        if (lifeStage == "Any"): # Child, Teenager, Young Adult, Adult, Elder
            self.lifeStage = self.generateLifeStage()
        else:
            self.lifeStage = lifeStage
        
        self.age = str(self.getAge(raceLifeStages, self.lifeStage))

        if (culture == "Traditional"):
            self.name = self.getNameByRaceTradition(raceTraits[8],raceTraits[9],self.gender)
        elif (culture == "Common"):
            self.name = self.getCommonName(self.gender)
        else:
            self.name = self.getTrueRandomName(self.gender)
        
        print(self.name)

    def generateRace(self):
        race = random.choice(self.options)
        return race[0]
        #TODO: Implement weighted selection

    def generateGender(self):
        return random.choice(["M","F"]) 
        #TODO: Load from CSV to allow user to configure custom genders

    def generateLifeStage(self):
        return random.choice(["Child","Adolescent","Young Adult","Adult","Elder"]) 
        #TODO: Implement loading life stage choices

    def getAge(self, raceStages, lifeStage):
        
        lowRange = 0
        upRange = 0

        for index, stage in enumerate(raceStages):
            if (lifeStage == stage[0] and len(raceStages) != index-1):
                lowRange = int(stage[1])
                upRange = int(raceStages[index+1][1])

        if (lowRange == 0 or upRange == 0):
            errorMessage = "Something went wrong determining the age range for a " + lifeStage + " " + self.race + "."
            messagebox.showerror("NPC Generation Error", errorMessage)
            sys.exit(errorMessage)

        return random.randrange(lowRange,upRange)
        #TODO: Need a better way to implement this in general

    def getNameByRaceTradition(self, fnTradition, sTradition, gender):

        if (gender != "M" and gender != "F"):
            gender = "U"

        firstNamesFile = open(self.namesFilePath + fnTradition + " First Names.csv")
        surnamesFile = open(self.namesFilePath + sTradition + " Surnames.csv")

        reader = csv.reader(firstNamesFile)

        firstNames = []
        for name in reader:
            if (gender == "U" or (name[1] == gender or name[1] == "U")):
                firstNames.append(name[0])
                print(name)

        firstNamesFile.close()

        reader = csv.reader(surnamesFile)

        surnames = []
        for surname in reader:
            surnames.append(surname[0])

        surnamesFile.close()

        return (random.choice(firstNames), random.choice(surnames))

    def getCommonName(self, gender):
        return self.getNameByRaceTradition("Common","Common", gender)

    def getTrueRandomName(self, gender):
        fnTrads = ["Common","Draconic","Dwarvish","Elvish","Halfling","Orcish"]
        sTrads = ["Common","Draconic","Dwarvish","Elvish","Halfling"]
        return self.getNameByRaceTradition(random.choice(fnTrads), random.choice(sTrads), gender)