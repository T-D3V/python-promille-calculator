import helper
import datetime
from dateutil.relativedelta import relativedelta

def main():
  promille_clac = PromilleClaculator()
  promille_clac.CalculatePromille()

class Drink:
  #since there are no constants in python I decided to implement a helper that provides a sort of constant,
  #comonly programmers in python just use UPPERCASE names and everybody knows it's a constant
  #also there is no double data type in python but float does the job equally good here
  @helper.constant
  def BEER_ALCOHOLIC_STRENGTH() -> float:
    return 0.05
  
  @helper.constant
  def WINE_ALCOHOLIC_STRENGTH() -> float:
    return 0.10
  
  @helper.constant
  def SCHNAPS_ALCOHOLIC_STRENGTH() -> float:
    return 0.40
  
  @helper.constant
  def DENSITY_ALCOHOL() -> float:
    return 0.8
  
  def __init__(self, volumeInMilliliter: int, alcoholicStrength: float, drankAt: datetime.datetime) -> None:
    self.__volumeInMilliliter = volumeInMilliliter
    self.__alcoholicStrength = alcoholicStrength
    self.__drankAt = drankAt
    
  def __get_hoursSinceIntake(self) -> float:
    return (datetime.datetime.now() - self.__drankAt).total_seconds() // 3600
  
  hoursSinceIntake = property(__get_hoursSinceIntake)
    
  def __get_alcoholMassInGramms(self) -> float:
    return self.__volumeInMilliliter * self.__alcoholicStrength * self.DENSITY_ALCOHOL
  
  alcoholMassInGramms = property(__get_alcoholMassInGramms)
    

class Person:
  @helper.constant
  def MAN() -> int:
    return 0
  
  @helper.constant
  def WOMAN() -> int:
    return 1

  @helper.constant
  def DECONSTRUCTION_WAITTIME_HOURS() -> float:
    return 1.0
  
  @helper.constant
  def DECONTSTRUCTION_PER_HOUR() -> float:
    return 0.1
  
  @helper.constant
  def PROPORTION_WATER_IN_BLOOD() -> float:
    return 0.8
  
  @helper.constant
  def DENSITY_BLOOD_GRAMM_PER_CCM() -> float:
    return 1.055
  
  def __init__(self, bodyMass: float, bodySizeInCM: float, birthday: datetime.datetime, sex: int) -> None:
    self.__bodyMass = bodyMass
    self.__bodySizeInCM = bodySizeInCM
    self.__birthday = birthday
    self.__sex = sex
    self.__set_alcoholPromille(0.0)
  
  def __get_ageInYears(self) -> float:
    return relativedelta(datetime.datetime.now(), self.__birthday).years
  
  ageInYears = property(__get_ageInYears)
  
  def __get_alcoholPromille(self) -> float:
    return self.__alcoholPromille

  def __set_alcoholPromille(self, var: float) -> None:
    self.__alcoholPromille = var
  
  alcoholPromille = property(__get_alcoholPromille, __set_alcoholPromille)
  
  def __get_wholeBodyWaterIndex(self) -> float:
    if self.__sex == self.WOMAN:
      return 0.203 - (0.07*self.ageInYears) + (0.1069 * self.__bodySizeInCM) + (0.2466 * self.__bodyMass)
    else:
      return 2.447 - (0.09516*self.ageInYears) + (0.1074 * self.__bodySizeInCM) + (0.3362 * self.__bodyMass)
    
  wholeBodyWaterIndex = property(__get_wholeBodyWaterIndex)
  
  def Drink(self, drink: Drink) -> None:
    self.alcoholPromille += (self.PROPORTION_WATER_IN_BLOOD * drink.alcoholMassInGramms) / (self.DENSITY_BLOOD_GRAMM_PER_CCM * self.wholeBodyWaterIndex)
    
    

class Pun:
  def __init__(self, alcoholPromille: float) -> None:
    self.__alcoholPromille = alcoholPromille
    
  def getPun(self) -> str:
    if(self.__alcoholPromille > 0.5):
      return "Sie sind nichtmehr fahrtüchtig."
    else:
      return "Sie können noch weiterfahren"

class PromilleClaculator:
  def __init__(self) -> None:
    pass
  def __AskPersonData(self) -> None:
    pass
  def __AskDrinkData(self) -> None:
    pass
  def CalculatePromille(self) -> None:
    pass
    

  
if __name__=="__main__":
  main()