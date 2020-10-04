# -*- coding: utf-8 -*-
#Antoine Washington
#Pokemon
#normal 0,fire 1,water 2,grass 3,electric 4,ice 5,fighting 6,poison 7,
#ground 8,flying 9,psychic 10,bug 11, #rock 12,ghost 13,dragon 14,
#dark 15,steel 16,fairy 17
#*********to do list: natures, terrains, stat stages, ABILITIES *cough*, moves make contact
#
#

import numpy as np
import astropy.table as tbl
import astropy.io.ascii as asc
import time as t
from moves import getMoveInfo
from moves import umm

rng=np.random.default_rng(24)

class mon:
    def __init__(self,level,named,hpbase=70,atbase=70,debase=70,sabase=70,sdbase=70,spbase=70,tipe=np.array([0])): #add natures
        #print("its a pokemon!")
        self.level=level
        self.hpiv=rng.integers(0,32)
        self.ativ=rng.integers(0,32)
        self.deiv=rng.integers(0,32)
        self.saiv=rng.integers(0,32)
        self.sdiv=rng.integers(0,32)
        self.spiv=rng.integers(0,32)
        self.hpev=0
        self.atev=0
        self.deev=0
        self.saev=0
        self.sdev=0
        self.spev=0
        self.hpb=hpbase
        self.atb=atbase
        self.deb=debase
        self.sab=sabase
        self.sdb=sdbase
        self.spb=spbase
        self.maxhp=HP(self.level,hpbase,self.hpiv,self.hpev)
        self.currenthp=self.maxhp
        self.currenthpp=100
        self.attack=stats(self.level,atbase,self.ativ,self.atev,1)
        self.defense=stats(self.level,debase,self.deiv,self.deev,1)
        self.spatk=stats(self.level,sabase,self.saiv,self.saev,1)
        self.spdef=stats(self.level,sdbase,self.sdiv,self.sdev,1)
        self.speed=stats(self.level,spbase,self.spiv,self.spev,1)
        self.name=named
        self.tipe=tipe
        if len(tipe)>1:
            self.dualType=True
        else:
            self.dualType=False
        self.fainted=False
        self.knownMoves=[19]
        #battle stat stages
        self.atstage=0
        self.destage=0
        self.sastage=0
        self.sdstage=0
        self.spstage=0
        #battle statuses
        self.sleep=False
        self.frozen=False
        self.burned=False
        self.paralyzed=False
        self.poisoined=False
        self.badlypoisoned=False
        self.confused=False
    
    ####things to call when a pokemon is thrown into battle
    def inBattle():
        #stat changes
        self.attack*=statStages[self.atstage+6]
        self.defense*=statStages[self.destage+6]
        self.spatk*=statStages[self.sastage+6]
        self.spdef*=statStages[self.sdstage+6]
        self.speed*=statStages[self.spstage+6]

    def move(self,opponent,moveIndex):
        #print(f"{self.name} used a move!")
        moveInQuestion=getMoveInfo(moveIndex)
        if rng.random()>moveInQuestion['accu']/100:
            print(f"{self.name} missed!")
        else:
            if moveInQuestion['special?']==0:
                ans=damage(self.level,self.attack,self.tipe,opponent.defense,opponent.tipe,moveInQuestion['pwr'],moveInQuestion['type'],moveInQuestion['notes'])
            if moveInQuestion['special?']:
                ans=damage(self.level,self.spatk,self.tipe,opponent.spdef,opponent.tipe,moveInQuestion['pwr'],moveInQuestion['type'],moveInQuestion['notes'])
            eff=checkTypeEffectiveness(moveInQuestion['type'],opponent.tipe)
            opponent.hit(self,ans,eff)
        
    def hit(self,attacker,damagepoints,effectiveness):
        if effectiveness==0:
            print(f"{self.name} is immune!")
        else:
            print(f"{self.name} was hit!")
            #lose HP
            self.currenthp-=damagepoints
            self.currenthpp=100*self.currenthp/self.maxhp
            #show effectiveness
            if effectiveness>2.0:
                print("It was MEGA-effective!!")
            if effectiveness<=2.0 and effectiveness>1:
                print("It was super-effective!")
            if effectiveness<0.5 and effectiveness>0:
                print("It was barely effective...")
            if effectiveness>=0.5 and effectiveness<1:
                print("It was not very effective.")
            #result of hit
            print(f"{self.name} lost {format(100*damagepoints/self.maxhp,'.2f')}% HP!")
            #check for faint
            if self.currenthp<0.0:
                self.currenthp=0.
                self.currenthpp=0
                self.fainted=True
                print(f"{self.name} fainted!")
            else:
                print(f"{self.name} has {format(self.currenthpp,'.2f')}% HP left!")
            ###call attacker.recoil() damage###
    
    #recoil
    def recoil(self,damagedone,recoilAmount):
        print(f"{self.name} takes recoil damage!")
        self.currenthp-=damagedone*recoilAmount

    #recalculate stats
    def reStat(self):
        self.maxhp=HP(self.level,self.hpb,self.hpiv,self.hpev)
        self.attack=stats(self.level,self.atb,self.ativ,self.atev,1)
        self.defense=stats(self.level,self.deb,self.deiv,self.deev,1)
        self.spatk=stats(self.level,self.sab,self.saiv,self.saev,1)
        self.spdef=stats(self.level,self.sdb,self.sdiv,self.sdev,1)
        self.speed=stats(self.level,self.spb,self.spiv,self.spev,1)
        self.currenthp=self.maxhp
        self.currenthpp=100

    def checkup(self):
        print(f"Name: {self.name} // Lv. {self.level}")
        if len(self.tipe)==1:
            print(f"{typeStrings[self.tipe[0]]}")
        if len(self.tipe)>1:
            print(f"{typeStrings[self.tipe[0]]} / {typeStrings[self.tipe[1]]}")
        print(f"Current HP: {self.currenthp}, {self.currenthp/self.maxhp*100}%")
        
    def summary(self):
        print(f"\n###### {self.name} Summary ######")
        if self.dualType:
            print(f"{typeStrings[self.tipe[0]]} // {typeStrings[self.tipe[1]]}")
        else:
            print(f"{typeStrings[self.tipe[0]]}")
        print(f"HP : \t{format(self.currenthp,'.2f')}/{self.maxhp} \t{format(self.currenthpp,'.2f')}%")
        print(f"Atk: \t{self.attack}")
        print(f"Def: \t{self.defense}")
        print(f"Sp.A: \t{self.spatk}")
        print(f"Sp.D: \t{self.spdef}")
        print(f"Spe: \t{self.speed}")
        print(f"############ {self.name}'s Moves #############")
        for i in self.knownMoves:
            print(f"\n{getMoveInfo(i)['name']} \t{getMoveInfo(i)['pp']}PP")
        print("##############################################")

    def showMoves(self):
        print("\n---- {self.name}'s Moves ----")
        for i in range(len(self.knownMoves)):
            print(f"{self.knownMoves[i]['name']} ")
        
        
def damage(level,attack,plaintiffTipe,defense,defendantTipe,power,moveTipe,note):
    ####weather damage boost####
    weatherBonus=1.0
    if weather=='sunny':
        if moveTipe==1:
            weatherBonus=4/3
            print("Sun boost!")
        if moveTipe==2:
            weatherBonus=2/3
            print("Weakened by the sunlight...")
    if weather=='rain':
        if moveTipe==1:
            weatherBonus=2/3
            print("Weakened by the rain...")
        if moveTipe==2:
            weatherBonus=4/3
            print("Rain boost!")
    ####critical hit chance####
    critical=1.0
    if rng.integers(1,25)==24:
        critical=1.5
        print("It's a critical hit!")
    ####random fluctuation 85%-100%
    rando=rng.integers(85,101)*0.01
    ####STAB####
    STAB=1.0
    if moveTipe in plaintiffTipe:
        STAB=1.5
    ####type effectiveness####
    tyype=checkTypeEffectiveness(moveTipe,defendantTipe)
    ####Burn###
    burn=1
    damageModifier=weatherBonus*critical*rando*STAB*tyype*burn
    
    ####damage calculation####
    ans=((((2*level)/5 + 2)*power*attack/defense)/50 + 2)*damageModifier
    return ans

#calculates pokemon stats (non-HP)
def stats(level,base,IV,EV,nature):
    ans=((2*base+IV+EV/4)*level/100+5)*nature
    return ans

#calculates HP stat
def HP(level,base,IV,EV):
    ans=((2*base+IV+EV/4)*level/100)+level+10
    return ans

def checkTypeEffectiveness(moveTipe,defendantTipe):
    matchup1=codex[moveTipe,defendantTipe[0]]
    if len(defendantTipe)>1:
        matchup2=codex[moveTipe,defendantTipe[1]]
    else:
        matchup2=1.0
    return matchup1*matchup2

#moves have pwr, phys/spec, type, accu, descipt
def moveInfo(moveCode):
    movepower=0
    moveSpecial=0
    moveTiipe=0
    return movepower,moveSpecial,moveTiipe

def indexToType(x):
    ["Normal","Fire","Water","Grass","Electric","Ice","Fighting","Poison","Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel","Fairy"]

#class party():
    #def __init__(self):
        
#codex encodes all type matchups, first index is attacking the second index
codex=np.ones((18,18))
#order: normal 0,fire 1,water 2,grass 3,electric 4,ice 5,fighting 6,poison 7,ground 8,flying 9,psychic 10,bug 11,
#rock 12,ghost 13,dragon 14,dark 15,steel 16,fairy 17
codex[0,12],codex[0,13],codex[0,16]=0.5,0,0.5 #normal
codex[1,1],codex[1,2],codex[1,3],codex[1,5],codex[1,11],codex[1,12],codex[1,14],codex[1,16]=0.5,0.5,2.0,2.0,2.0,0.5,0.5,2.0 #fire
codex[2,1],codex[2,2],codex[2,3],codex[2,8],codex[2,12],codex[2,14]=2.0,0.5,0.5,2.0,2.0,0.5 #water
codex[3,1],codex[3,2],codex[3,3],codex[3,7],codex[3,8],codex[3,9],codex[3,11],codex[3,12],codex[3,14],codex[3,16]=0.5,2.0,0.5,0.5,2.0,0.5,0.5,2.0,0.5,0.5 #grass
codex[4,2],codex[4,3],codex[4,4],codex[4,8],codex[4,9],codex[4,14]=2.0,0.5,0.5,0.0,2.0,0.5 #electric
codex[5,1],codex[5,2],codex[5,3],codex[5,5],codex[5,8],codex[5,9],codex[5,14],codex[5,16]=0.5,0.5,2.0,0.5,2.0,2.0,2.0,0.5 #ice
codex[6,1],codex[6,5],codex[6,7],codex[6,9],codex[6,10],codex[6,11],codex[6,12],codex[6,13],codex[6,15],codex[6,16],codex[6,17]=2.0,2.0,0.5,0.5,0.5,0.5,2.0,0.0,2.0,2.0,0.5 #fighting
codex[7,3],codex[7,7],codex[7,8],codex[7,12],codex[7,13],codex[7,16],codex[7,17]=2.0,0.5,0.5,0.5,0.5,0.0,2.0 #poison
codex[8,1],codex[8,3],codex[8,4],codex[8,7],codex[8,9],codex[8,11],codex[8,12],codex[8,16]=2.0,0.5,2.0,2.0,0.0,0.5,2.0,2.0 #ground
codex[9,3],codex[9,4],codex[9,6],codex[9,11],codex[9,12],codex[9,16]=2.0,0.5,2.0,2.0,0.5,0.5 #flying
codex[10,6],codex[10,7],codex[10,10],codex[10,15],codex[10,16]=2.0,2.0,0.5,0.0,0.5 #psychic
codex[11,1],codex[11,3],codex[11,6],codex[11,7],codex[11,9],codex[11,10],codex[11,13],codex[11,15],codex[11,16],codex[11,17]=0.5,2.0,0.5,0.5,0.5,2.0,0.5,2.0,0.5,0.5  #bug
codex[12,1],codex[12,5],codex[12,6],codex[12,8],codex[12,9],codex[12,11],codex[12,16]=2.0,2.0,0.5,0.5,2.0,2.0,0.5 #rock
codex[13,0],codex[13,10],codex[13,13],codex[13,15]=0.0,2.0,2.0,0.5 #ghost
codex[14,14],codex[14,16],codex[14,17]=2.0,0.5,0.0 #dragon
codex[15,6],codex[15,10],codex[15,13],codex[15,15],codex[15,17]=0.5,2.0,2.0,0.5,0.5 #dark
codex[16,1],codex[16,2],codex[16,4],codex[16,5],codex[16,12],codex[16,16],codex[16,17]=0.5,0.5,0.5,2.0,2.0,0.5,2.0 #steel
codex[17,1],codex[17,6],codex[17,7],codex[17,14],codex[17,15],codex[17,16]=0.5,2.0,0.5,2.0,2.0,0.5 #fairy
    
typeStrings=["Normal","Fire","Water","Grass","Electric","Ice","Fighting","Poison","Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel","Fairy"]
statStages=[2/8,2/7,2/6,2/5,2/4,2/3,2/2,3/2,4/2,5/2,6/2,7/2,8/2]

#weather='clear'
#weather='rain'
weather='sunny'
#weather='hail'
#weather='sandstorm'

starter=mon(1,"Bulbasaur",hpbase=45,atbase=49,debase=49,sabase=65,sdbase=65,spbase=45,tipe=np.array([3,7]))
userParty=[starter]
print(umm)
#asc.write(umm,'movedex.dat',overwrite=True)

while 1:
    userChoice=input("\nYou can:\n[P]okemon\n[B]attle!\n[N]ursery\n[T]raining\n[M]ove Learner\n:")
    
    ####Battles####
    if userChoice=='b':
        ####Battle starts####
        print("A battle has started!")
        userMon=userParty[0]
        print(f"{userMon.name}! I choose you!")
        enemy=mon(100,"darwin",tipe=np.array([17]))
        print(f"{enemy.name}! Go!")
        ####turn begins####
        while userMon.currenthp>0 and enemy.currenthp>0:
            ####fight/run/pokemon/bag####
            while 1: #user turn loop, break when users turn ends
                battleOver=False
                #----UI----#
                print("\n****************")
                print(f"Opponent:\n{enemy.name} // Level {enemy.level}")
                print(f"HP: {format(enemy.currenthpp,'.2f')}%")
                print("\n............Your team:")
                print(f"............{userMon.name} // Level {userMon.level}")
                print(f"............HP: {format(userMon.currenthp,'.2f')}/{format(userMon.maxhp,'.2f')}")
                userMove=input(f"What should {userMon.name} do?\n[F]ight\n[P]okemon\n[R]un\n")
                if userMove=='f':                    
                    #fighting options
                    for i in range(len(userMon.knownMoves)):
                        print(f"[{i+1}] \t{getMoveInfo(userMon.knownMoves[i])['name']} \t{getMoveInfo(userMon.knownMoves[i])['pp']} PP")
                    while 1: #move input loop
                        userFight=input(f"What move should {userMon.name} use? [#]\n:")
                        try:
                            fightChoice=int(userFight)-1 #make sure given input refers to a move
                            moveDex=userMon.knownMoves[fightChoice]
                            break #exit move input loop
                        except:
                            print("\n**Enter one of the numbers above.**")
                        #end of move input while block

                    #user faster, both pokemon go, move input while loop 
                    if userMon.speed>=enemy.speed:
                        print(f"{userMon.name} used {getMoveInfo(moveDex)['name']}!")
                        userMon.move(enemy,moveDex)
                        if enemy.fainted:
                            battleOver=True
                            break #ends user turn loop
                        if userMon.fainted:
                            battleOver=True
                            break
                        ####OPPONENT TURN####
                        opChoice=rng.integers(0,len(enemy.knownMoves))
                        print(f"{enemy.name} used {getMoveInfo(enemy.knownMoves[opChoice])['name']}!")
                        enemy.move(userMon,enemy.knownMoves[opChoice])
                        if userMon.fainted:
                            battleOver=True
                            break
                        if enemy.fainted:
                            battleOver=True
                            break
                        #user moved, and enemy moved
                    
                    if enemy.speed>userMon.speed:
                        ####opponent goes####
                        opChoice=rng.integers(0,len(enemy.knownMoves))
                        print(f"{enemy.name} used {getMoveInfo(enemy.knownMoves[opChoice])['name']}!")
                        enemy.move(userMon,enemy.knownMoves[opChoice])
                        if userMon.fainted:
                            battleOver=True
                            break
                        if enemyMon.fainted:
                            battleOver=True
                            break
                        ####User goes####
                        print(f"{userMon.name} used {getMoveInfo(moveDex)['name']}!")
                        userMon.move(enemy,moveDex)
                        if enemy.fainted:
                            battleOver=True
                            break
                        if userMon.fainted:
                            battleOver=True
                            break
                        #enemy moved and user moved
                    #ends if user chose to fight
                    #if user inputs anything else, we go back to fpbr screen
                    
                ####run away to end battle####
                if userMove=='r':
                    print(f"You and {userMon.name} ran away!")
                    battleOver=True
                    break
                #display party pokemon
                if userMove=='p':
                    print("\n****************\nParty Pokemon:")
                    for i in range(len(userParty)):
                        print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {userParty[i].currenthpp}%")
                    while 1:
                        partyChoice=input("Enter a number to see a Pokemon's summary...\nOr Enter [b] to go back:\n")
                        if partyChoice=='b':
                            break #goes back to user turn loop from pokemon selection
                        try:
                            userParty[int(partyChoice)-1].summary()
                        except ValueError:
                            print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
                        except IndexError:
                            print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
                        #end of pokemon selection loop
                    #end of party pokemon block
                ####other user turn options?####
            if battleOver: #if user ran
                break #breaks battle loop, back to main screen
            enMove=np.random.rand(1)
            if enMove>=0.5:
                print(f"{enemy.name} used Slam!")
                enemy.move(userMon,60,0,0)
            if enMove<0.5:
                print(f"{enemy.name} used Fairy Dust!")
                enemy.move(userMon,50,0,17)
            #loop back to "turn begins"
            #if a pokemon has fainted, loop ends
        print("The battle ended!")
        t.sleep(1)
    ###end of battle block###
        
    ####check party pokemon?####
    if userChoice=='p':
        while 1:
            print("\n****************\nParty Pokemon:")
            for i in range(len(userParty)):
                print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level} \tHP: {userParty[i].currenthpp}%")
            print("******************************")
            partyChoice=input("Enter a number to see a Pokemon's summary...\nOr Enter [b] to go back:\n")
            if partyChoice=='b':
                break
            try:
                userParty[int(partyChoice)-1].summary()
            except ValueError:
                print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
            except IndexError:
                print("\nEnter the number corresponding to a Pokemon!\nor [b] to go back")
            #end of while block
        print("Going back to main screen...")
        t.sleep(1)
        #end of party pokemon
    ###end of party display block###

    ####pokemon nursery####
    if userChoice=='n':
        print("\n____Welcome to the Pokemon Nursery!____")
        t.sleep(1)
        print("Here, you can create Pokemon from scratch!")
        t.sleep(1)
        ####nursery loop####
        while 1:
            nurseChoice=input("What do you want to do?\nNew [P]okemon!!\n[B]ack\n:")
            
            ####new pokemon####
            if nurseChoice=='p':
                newName=input("Would you like to give your Pokemon a name?: ")
                print(f"Let's get {newName} some STATS")
                while 1:
                    HPstatS=input("HP stat? 1-255: ")
                    ATstatS=input("Attack stat? 1-255: ")
                    DEstatS=input("Defense stat? 1-255: ")
                    SAstatS=input("Sp. Atk stat? 1-255: ")
                    SDstatS=input("Sp. Def stat? 1-255: ")
                    SPstatS=input("Speed stat? 1-255: ")
                    try:
                        HPstat=int(HPstatS)
                        ATstat=int(ATstatS)
                        DEstat=int(DEstatS)
                        SAstat=int(SAstatS)
                        SDstat=int(SDstatS)
                        SPstat=int(SPstatS)
                        if np.min(np.array([HPstat,ATstat,DEstat,SAstat,SDstat,SPstat]))>0:
                            break #stats acccepted, exits stat input loop
                        else:
                            print("\n**Base stats must be at least 1**")
                    except:
                        print("\n**Stats must be numbers**")
                ##type choice##
                print("****************\nPokemon Types:\n0 Normal\n1 Fire\n2 Water\n3 Grass\n4 Electric\n5 Ice\n6 Fighting\n7 Poison\n8 Ground\n9 Flying\n10 Psychic\n11 Bug\n12 Rock\n13 Ghost\n14 Dragon\n15 Dark\n16 Steel\n17 Fairy\n****************")
                while 1: #type input loop
                    newTipe=input(f"Use the legend above to give {newName} a type or two: ")
                    try:
                        newTipes=newTipe.split()
                        newTipe1=int(newTipes[0])
                        newTipeInt=np.array([newTipe1])
                        if len(newTipes)>1: #if second type was inputted
                            newTipe2=int(newTipes[1])
                            newTipeInt=np.append(newTipeInt,newTipe2)
                        if np.max(newTipeInt)<=17: #no types above 17
                            if np.min(newTipeInt)>=0: #no types below 0
                                break #input valid, exit type input loop
                            else:
                                print("\n**Highest number: 17, lowest number: 0**")
                        else:
                            print("\n**Highest number: 17, lowest number: 0**")
                    except ValueError:
                        print("\n**Use the legend above and enter a number (or 2 separated with a space)**")
                
                ##level input##
                while 1: #level input loop
                    lvlS=input(f"What level should {newName} be? 1-100: ")
                    try:
                        lvl=int(lvlS)
                        if lvl>=1:
                            break
                        else:
                            print("\n**Level must be at least 1!**")
                    except:
                        print("\n**Enter a number!**")
                    #end of while block
                                    
                ##make the pokemon!##
                if len(newTipes)==1:
                    newMon=mon(lvl,newName,hpbase=HPstat,atbase=ATstat,debase=DEstat,sabase=SAstat,sdbase=SDstat,spbase=SPstat,tipe=np.array([newTipe1]))
                if len(newTipes)>1:
                    newMon=mon(lvl,newName,hpbase=HPstat,atbase=ATstat,debase=DEstat,sabase=SAstat,sdbase=SDstat,spbase=SPstat,tipe=np.array([newTipe1,newTipe2]))
                print(f"\n{newName} is born!")
                t.sleep(1)
                userParty.append(newMon)
                print("Take good care of them!")
            
            if nurseChoice=='b':
                break #exits nursery loop
            pass #loops back to start of nursery
        pass #loops back to start of game
    ###end of nursery block
    
    ####training####
    if userChoice=='t':
        print("\n********SuperHyper Training********\nYou can add EVs and IVs to your Pokemon!")
        while 1:
            #choose a pokemon
            print("\n")
            for i in range(len(userParty)):
                print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level}")
            trainChoice=input("\nWhich Pokemon will we train?:\n[#] or [B]ack: ")
            
            #option to go back, from pokemon selection to main screen
            if trainChoice=='b':
                break
            #user input loop, making sure input is poke#
            while 1:
                try:
                    pokeIndex=int(trainChoice)-1
                    pokeTrain=userParty[pokeIndex]
                    break #confirmed numbers are good, exit user loop
                except:
                    print("\n**Must enter a number of a Pokemon**")
                    trainChoice=input("\nWhich Pokemon will we train?:\n[#]")
                    #ends error catch for pokemon selection
            print(f"\n**** {pokeTrain.name} ****")
            superHyper=input("Manage [E]Vs or [I]Vs or [L]evels\n:") #anything other than options below will skip to the next loop of choose a pokemon
            
            #EVs
            if superHyper=='e':
                while 1:
                    evs=input("Enter 6 numbers (0-252) all at once.\nEVs cannot sum >510.:\n")
                    #option to go back
                    if evs=='b':
                        break #throws us back to choose a pokemon
                    else:
                        evs=evs.split()
                        try:
                            eves=np.array([int(evs[0]),int(evs[1]),int(evs[2]),int(evs[3]),int(evs[4]),int(evs[5])])
                            #make sure values are legal
                            if np.max(eves)<=252.:
                                if np.sum(eves)<=510.:
                                    pokeTrain.hpev=int(evs[0])
                                    pokeTrain.atev=int(evs[1])
                                    pokeTrain.deev=int(evs[2])
                                    pokeTrain.saev=int(evs[3])
                                    pokeTrain.sdev=int(evs[4])
                                    pokeTrain.spev=int(evs[5])
                                    pokeTrain.reStat()
                                    t.sleep(1)
                                    print("\nTraining...")
                                    t.sleep(1)
                                    print(f"\n{pokeTrain.name} finished Super Training and has new stats!")
                                    break #ends ev training, sends back to choose a pokemon
                                else:
                                    print("\n**No more than 510 EVs**")
                                    pass
                                pass
                            else:
                                print("\n**No more than 252 EVs in any stat.**")
                                pass
                            pass
                        except: #catch non-numbers, incomplete sets
                            print("\n**Max EV is 252.**\n**Total EVs cannot sum more than 510.**\n**Input 6 numbers separated by spaces.**")    
                        #if code is here, EV training while loop continues
                    pass
                #end of ev training loop
            
            #IVs        
            if superHyper=='i':
                while 1:
                    ivs=input("Enter 6 numbers (0-31) all at once.:\n")
                    #option to go back, from iv input to choose a pokemon
                    if ivs=='b':
                        break
                    else:
                        ivs=ivs.split() #6 numbers into list of strings
                        try:
                            #make sure we have 6 numbers
                            ives=np.array([int(ivs[0]),int(ivs[1]),int(ivs[2]),int(ivs[3]),int(ivs[4]),int(ivs[5])])
                            if np.max(ives)<=31:
                                pokeTrain.hpiv=int(ivs[0])
                                pokeTrain.ativ=int(ivs[1])
                                pokeTrain.deiv=int(ivs[2])
                                pokeTrain.saiv=int(ivs[3])
                                pokeTrain.sdiv=int(ivs[4])
                                pokeTrain.spiv=int(ivs[5])
                                pokeTrain.reStat()
                                t.sleep(1)
                                print("\nTraining...")
                                t.sleep(1)
                                print(f"{pokeTrain.name} finished Hyper Training and has new stats!")
                                t.sleep(1)
                                break #ends IV training, goes back to choose a pokemon
                            else:
                                print("\n**Maximum IV is 31**")
                        except IndexError: #input couldn't fill 6-item array
                            print("\n**Enter !6! numbers separated by spaces**")
                        except ValueError: #we tried to make an int() out of something non-number
                            print("\n**Enter 6 !numbers! separated by spaces**")
                        #if we get here, an IV was more than 31, loops back to IV input
                    #end of iv input loop
                #end of IV training loop
            
            #level
            if superHyper=='l':
                while 1:
                    try:
                        levl=int(input(f"What level should {pokeTrain.name} be?: "))
                        if levl>0.: #if input was a positive number
                            pokeTrain.level=levl #set pokemon's new level
                            pokeTrain.reStat() #recalcs stats
                            print("\nTraining...")
                            t.sleep(1)
                            print(f"\n{pokeTrain.name} finished training and has new stats!")
                            t.sleep(1)
                            break #exits user input loop
                        else:
                            print("\n**Level must be at least 1**")
                    except:
                        print("\n**Enter a number greater than 0.**")
                    #end of level input while block
                #end of level training block
                
            pass #loops back to training screen
        print("\nLeaving SuperHyper Training...")
        t.sleep(1) #exiting training
    ###end of training block###

    ####move learner####
    if userChoice=='m':
        print("\n____Move Learner____\nYou can teach your pokemon moves!\n")
        while 1: #choose a pokemon
            for i in range(len(userParty)):
                print(f"[{i+1}] {userParty[i].name} \tLv. {userParty[i].level}")
            learnChoice=input("Enter the number of a Pokemon\n[#] or [B]ack: ")
            backML1=False
            while 1:
                if learnChoice=='b':
                    print("Leaving Move Learner...")
                    t.sleep(1) #kills
                    backML1=True
                    break
                try:
                    learnChoice=int(learnChoice)
                    studentMon=userParty[learnChoice-1]
                    break
                except:
                    learnChoice=input("**Enter a number corresponding to a Pokemon**\n:")
            if backML1:
                break  #if they choose to go back, reiterate choose a pokemon loop
            #otherwise, print the moves
            print(umm)
            #np.savetxt("movecodex.txt",umm)
            asc.write(umm,'movecodex.txt',overwrite=True)
            while 1: #input loop
                chooseMove=input(f"Which moves should {studentMon.name} learn?\nEnter move indices [#] separated by spaces\n:")
                try:
                    chooseMoves=chooseMove.split() #separate move indices into own strings
                    moveInts=[int(i) for i in chooseMoves] #(try to) convert strings to ints
                    if max(moveInts)<=len(umm):
                        if min(moveInts)>=0:
                            for i in moveInts:
                                studentMon.knownMoves.append(i)
                                print(f"{studentMon.name} learned {getMoveInfo(i)['name']}!")
                            break #after all moves added, breaks loop and goes back to choose a pokemon
                    else:
                        print("**Try again.**")
                except ValueError:
                    print("**Enter numbers corresponding to desired moves**")
                except IndexError:
                    print("**Use move legend to add moves**")
                except:
                    print("**Try Again**")
                #end of move selection while block, moves have been picked
            pass #choose a new pokemon
            #end of choose a pokemon block
        #goes back to choose a pokemon
    ###end of move learner block####

    ####what's the next spot?####

    #end of game, loops back to main screen
'''
bulba=mon(60,"eve",tipe=np.array([3,11]))
chard=mon(50,"steve",tipe=np.array([13]))
bulba.checkup()
bulba.move(chard,100,1,0)
chard.checkup()
chard.move(bulba,40,1,moveTipe=1)
chard.checkup()
bulba.appraise()
'''
#bulba=mon(34,"bulbasaur")
#char=mon(32, "charmander")
#bulba.move(char,60,0,moveTipe='fire')
