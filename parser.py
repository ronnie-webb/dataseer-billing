import xlrd
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from forex_python.converter import CurrencyRates
import sys
 

#Currency Converter 
def CurrencyConverter(amount):
      c = CurrencyRates()
      rate = c.get_rate('NOK','USD')
      price = rate * amount 
      return price

#Calculate Prod charges and Pre's cluster charges 
def getCharges(cvsfile):
      DataseerPreClusterCost = 9954.53
      DataseerGpuCost = 6519.67
      DataseerClusterCost = DataseerPreClusterCost + DataseerGpuCost
      resourceGroup_values = ['worleyparsonsrnd-00','WORLEYPARSONSRND-00']
      resourceLocation_values = ['ussouthcentral','SouthCentralUS']
      datas = pd.read_csv('./'+cvsfile, skiprows=2)
      FilterByResourceGroup = datas.loc[(datas['Resource Group'].str.contains('|'.join(resourceGroup_values )))
                                          & (datas['Resource Location'].str.contains('|'.join(resourceLocation_values )))
                                          & (datas['Product'] != 'Virtual Machines BS Series - B8ms - US South Central') 
                                          & (datas['Product'] != 'Virtual Machines Dv3/DSv3 Series - D8 v3/D8s v3 - US South Central')
                                          & (datas['Consumed Service'].str.contains('Microsoft.Compute') == False )
                                          & (datas['Instance ID'].str.contains('pre') == False)
                                          & (datas['Instance ID'].str.contains('dev') == False)]

      ProdCost = FilterByResourceGroup['ExtendedCost'].sum()
      TotalCost = CurrencyConverter(DataseerClusterCost+ProdCost)
      return '${:,.2f}'.format(TotalCost)

def main():     
  cvsfile = sys.argv[1]
  print(getCharges(cvsfile))

if __name__ == '__main__':
     
    main()