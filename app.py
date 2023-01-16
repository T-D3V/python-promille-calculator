#according to the test cases something is wrong in my code like I don't get the correct result of by like .2 Pronille but might be due to code differences

import datetime
from dateutil.relativedelta import relativedelta
from cmd import Cmd

def main():
  promille_clac = PromilleClaculator()
  promille_clac.cmdloop()

class Drink:
  #there are no constants in python
  #comonly programmers in python just use UPPERCASE names and everybody knows it's a constant
  #also there is no double data type in python but float does the job equally good here
  BEER_ALCOHOLIC_STRENGTH:float = 0.05
  WINE_ALCOHOLIC_STRENGTH:float = 0.10
  SCHNAPS_ALCOHOLIC_STRENGTH:float = 0.40
  DENSITY_ALCOHOL:float = 0.8
  
  def __init__(self, volumeInMilliliter: int, alcoholicStrength: int, drankAt: datetime.datetime) -> None:
    self.__volumeInMilliliter:int = volumeInMilliliter
    self.__alcoholicStrength:float = [Drink.BEER_ALCOHOLIC_STRENGTH, Drink.WINE_ALCOHOLIC_STRENGTH, Drink.SCHNAPS_ALCOHOLIC_STRENGTH][alcoholicStrength]
    self.__drankAt:datetime.datetime = drankAt
  
  @property
  def hoursSinceIntake(self) -> float:
    return (datetime.datetime.now() - self.__drankAt).total_seconds() // 3600
  
  @property
  def alcoholMassInGramms(self) -> float:
    return self.__volumeInMilliliter * self.__alcoholicStrength * self.DENSITY_ALCOHOL
    

class Person:
  MAN:int = 0
  WOMAN:int = 1
  DECONSTRUCTION_WAITTIME_HOURS:float = 1.0
  DECONTSTRUCTION_PER_HOUR:float = 0.1
  PROPORTION_WATER_IN_BLOOD:float = 0.8
  DENSITY_BLOOD_GRAMM_PER_CCM:float = 1.055
  
  def __init__(self, bodyMass: float, bodySizeInCM: float, birthday: datetime.datetime, sex: int) -> None:
    self.__bodyMass:float = bodyMass
    self.__bodySizeInCM:float = bodySizeInCM
    self.__birthday:datetime.datetime = birthday
    self.__sex:int = sex
    self.__alcoholPromille:float = 0.0
  
  @property
  def ageInYears(self) -> float:
    return relativedelta(datetime.datetime.now(), self.__birthday).years
  
  @property
  def alcoholPromille(self) -> float:
    return self.__alcoholPromille
  
  @property
  def wholeBodyWaterIndex(self) -> float:
    if self.__sex == self.WOMAN:
      return 0.203 - (0.07*self.ageInYears) + (0.1069 * self.__bodySizeInCM) + (0.2466 * self.__bodyMass)
    else:
      return 2.447 - (0.09516*self.ageInYears) + (0.1074 * self.__bodySizeInCM) + (0.3362 * self.__bodyMass)
  
  def drink(self, drink: Drink) -> None:
    alcoholPromilleOriginal = (self.PROPORTION_WATER_IN_BLOOD * drink.alcoholMassInGramms) / (self.DENSITY_BLOOD_GRAMM_PER_CCM * self.wholeBodyWaterIndex)
    
    deconstruction = (self.DECONTSTRUCTION_PER_HOUR * (drink.hoursSinceIntake - self.DECONSTRUCTION_WAITTIME_HOURS))
    
    self.__alcoholPromille += alcoholPromilleOriginal - deconstruction
    
    

class Pun:
  def __init__(self, alcoholPromille: float) -> None:
    self.__alcoholPromille = alcoholPromille
    
  def getPun(self) -> str:
    if(self.__alcoholPromille > 0.5):
      return "You're not allowed to drive anymore"
    else:
      return "You're safe to drive"

class PromilleClaculator(Cmd):
  prompt = 'pc> '
  intro = "Welcome to the PromilleCalculator! Type ? to list commands"
  person:Person = Person(1, 1, datetime.datetime.strptime("22.10.2005 00:00:00", '%d.%m.%y %H:%M:%S'), 0)
  
  def do_exit(self, inp):
    print("Bye")
    return True
  
  def help_exit(self):
    print("exit the application.")
  
  def do_add_person(self, inp: str):
    '''Define the person in Format: add_person "body mass in kg"(75) "body size in cm"(175) "birthday"(22.10.2005 00:00:00) "Your sex 0 for male and 1 for women"(0/1)'''
    try:       
      self.__AskPersonData(inp)
    except Exception as e:
      print("The pervious command failed, please look over the command you typed, if it still doesn't work contact the maintainer.")
      print("Define the person in Format: add_person \"body mass in kg\"(75) \"body size in cm\"(175) \"birthday\"(22.10.2005 00:00:00) \"Your sex 0 for male and 1 for women\"(0/1)")
  def do_add_drink(self, inp:str):
    '''Add the drinks you've had in Format: add_drink "volume in milliliter"(500) "0: Beer, 1: Wine, 2: Schnaps"(0/1/2) "time of intake"(22.10.05 22:48:35)'''
    if(isinstance(self.person, Person)):
      try:       
        self.__AskDrinkData(inp)
      except Exception as e:
        print("The pervious command failed, please look over the command you typed, if it still doesn't work contact the maintainer.")
        print("Add the drinks you've had in Format: add_drink \"volume in milliliter\"(500) \"0: Beer, 1: Wine, 2: Schnaps\"(0/1/2) \"time of intake\"(22.10.05 22:48:35)")
    else:
      print('Please first define a person with: add_person')
  
  def do_calculate_promille(self, inp):
    '''calculate if you're safe to drive'''
    if(isinstance(self.person, Person)):
      print(self.person.alcoholPromille)
      print(Pun(self.person.alcoholPromille).getPun())
    else:
      print('Please first define a person with: add_person')
  
  def default(self, inp):
    if inp == 'x' or inp == 'q':
      return self.do_exit(inp)
    print("Default: {}".format(inp))
    
  do_EOF = do_exit
  help_EOF = help_exit
  
  def __AskPersonData(self, inp:str) -> Person:
    self.person = Person(float(inp.split(" ")[0]), float(inp.split(" ")[1]), datetime.datetime.strptime(inp.split(" ")[2]+" "+inp.split(" ")[3], '%d.%m.%Y %H:%M:%S'), int(inp.split(" ")[4]))
    return self.person
  def __AskDrinkData(self, inp:str) -> Drink:
    currentDrink = Drink(int(inp.split(" ")[0]), int(inp.split(" ")[1]), datetime.datetime.strptime(inp.split(" ")[2]+" "+inp.split(" ")[3], '%d.%m.%y %H:%M:%S'))
    self.person.drink(currentDrink)
    return currentDrink   

  
if __name__=="__main__":
  main()