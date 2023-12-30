#made by joel hellums
#takes in a list of local html files to scrape (taken from sherwin-williams.com) and returns a list of links to all SDSs

#pdf reader tools
from math import prod
from pydoc import Doc
import PyPDF2 as p2
import pdftotext
#regex
import re 
import unidecode
from collections import OrderedDict 

def GetProductCode(pdftext):
    index = pdftext.find('Product code')
    index = index + 14
    index_two = pdftext.find('Other',index)
    product_code = pdftext[index:index_two]
    product_code = product_code.strip()
    return product_code
    #product_code = pdftext[18:25]
    #product_code = product_code.strip()
    #product_code = product_code.encode('ascii','ignore')
    #product_code = product_code.decode()
    #return product_code



#finds all text between two ':'s after the string "product name" #if everything worked *exactly* this way i could reuse this, but it doesn't so i can't
def GetProductName(pdftext):
    index = pdftext.find('Product name')
    index_two = pdftext.find(':',index)
    index_two = index_two + 1 #prints the : if i dont do this
    index_three = pdftext.find(':',index_two)
    product_name = pdftext[index_two:index_three]
    product_name = product_name.rstrip()
    product_name = product_name.lstrip()
    product_name = product_name.replace('\n',' ')
    product_name = product_name.replace('Product code','')
    product_name = product_name.encode('ascii','ignore')
    product_name = product_name.decode()
    return product_name

#finds text between : and \n after manufacturer #a lot of code is being repeated, but this needs to be done fast over perfect
#def GetManufacturerName(pdftext): #TODO fix manufacturer nane and address for some... or just check if it really is the same accross every single damn one
    index = pdftext.find('Manufacturer')
    index_two = pdftext.find(':',index)
    index_two = index_two + 1 #prints the : if i dont do this
    index_three = pdftext.find('\n',index_two)
    product_name = pdftext[index_two:index_three]
    product_name = product_name.rstrip()
    product_name = product_name.lstrip()
    product_name = product_name.replace('\n',' ')
    return product_name
#once again, always the same but always in a different location, so i'm hardcoding it
def GetManufacturerName(pdftext):
    return 'THE SHERWIN-WILLIAMS COMPANY'

def GetManufacturerAddress(pdftext):
    return '101 W. Prospect Avenue,                                      Cleveland, OH 44115'

#finds the 2 lines of text after the manufactuer name
#def GetManufacturerAddress(pdftext):
    index = pdftext.find('Manufacturer')
    index_two = pdftext.find(':',index)
    index_two = index_two + 1 #prints the : if i dont do this
    index_three = pdftext.find('\n',index_two)
    index_three = index_three + 1 #gets stuck on \n if i dont do this
    index_four = pdftext.find('\n',index_three)
    index_four = index_four + 1 #gets stuck on \n if i dont do this
    index_five = pdftext.find('\n',index_four)
    product_name = pdftext[index_three:index_five]
    product_name = product_name.rstrip()
    product_name = product_name.lstrip()
    product_name = product_name.replace('\n',', ')
    product_name = product_name.replace('\n',', ')
    return product_name

#finds text between : and \n after signal word
def GetSignalWord(pdftext):
    index = pdftext.find('Signal word')
    index_two = pdftext.find(':',index)
    index_two = index_two + 1 #prints the : if i dont do this
    index_three = pdftext.find('\n',index_two)
    product_name = pdftext[index_two:index_three]
    product_name = product_name.rstrip()
    product_name = product_name.lstrip()
    product_name = product_name.replace('\n',' ')
    return product_name

#finds text between ingredient list header and 'Any Concentration' #TODO push off this PITA to another function to be processed
def GetBigIngredients(pdftext):
    if 'The product contains no substances which at their given concentration, are considered to be hazardous to health.' in pdftext:
        return ''
    else:
        index = pdftext.find("CAS number")
        index = index + 148
        index = pdftext.find('\n',index)
        index_two = pdftext.find('Any concentration',index)
        index_two = index_two - 1
        product_name = pdftext[index:index_two]
        return product_name
    

#def CreateFileLocation(magicnumber):
#    DocumentName = './sherwinwilliams/https_www.sherwin-williams.com_document_SDS_en_' + str(magicnumber) + '_US_/https_www.sherwin-williams.com_document_SDS_en_' + str(magicnumber) + '_US_.pdf'
#    return DocumentName

def CreateFileLocation(magicnumber):
    DocumentName = './SW_Docs_Eng_output/' + str(magicnumber) + '.pdf'
    return DocumentName

def WriteErrorFailToReadText(DocumentName):
    file = open('errors.txt', 'a')
    ErrorMessage = 'Failutre to convert file to pdf text at ' + str(DocumentName) + '\n'
    file.write(ErrorMessage)
    file.close()

def WriteErrorFailToReadDoc(DocumentName):
    file = open('errors.txt', 'a')
    ErrorMessage = 'Failutre to read file at ' + str(DocumentName) + '\n'
    file.write(ErrorMessage)
    file.close()

def ReadyProductInfoSheet():
    try:
        open('ProductInfo.csv', 'x')
    except:
        print('!!!WARNING, ProductInfo.csv alrady exists, continuing')
    file = open('ProductInfo.csv', 'a')
    file.write('\n"Magic Number","Product Code","Product Name","Manufacturer Name","Manufacturer Address","Signal Word","Document Location"\n')
    file.close()

def WriteProductInfo(MagicNumber, ProductCode, ProductName, ManufacturerName, ManufacturerAddress, SignalWord, DocumentName, RevDate):
    file = open('ProductInfo.csv', 'a')
    file.write('"' + str(MagicNumber) + '","' + str(ProductCode) + '","' + str(ProductName) + '","' + str(ManufacturerName) + '","' + str(ManufacturerAddress) + '","' + str(SignalWord) + '","' + str(DocumentName) + '","' + str(RevDate) + '"\n')
    file.close()

def GetRevDate(pdftext):
    index = pdftext.find("Date of revision")
    index = index + 17
    indextwo = pdftext.find("Date",(index))
    revdate = pdftext[index:indextwo]
    return revdate

def WriteOutBigIngredients(ingr,magicnumber): #push this off to another program
    file = open('ProductIngredients.txt','a')
    ingr.replace('"','')
    ingr = ingr.split("\n")
    for line in ingr:
        file.write('"' + str(line) + '","' + str(magicnumber) + '"\n')
    #    print(line)
    file.close
    return


def ProcessPDF(magicnumber):
    DocumentName = CreateFileLocation(magicnumber)
    try:
        PDFfile = open(DocumentName,"rb")
    except:
        print('!!!FAILURE TO READ PDF AT ' + str(DocumentName) + 'WRITING TO ERROR LOG!')
        PDFfile.close()
        WriteErrorFailToReadDoc(DocumentName)
        return
    
    try:
        pdfread = pdftotext.PDF(PDFfile)
    except: 
        print('!!!FAILURE TO READ PDF TEXT AT ' + str(DocumentName) + 'WRITING TO ERROR LOG!')
        PDFfile.close()
        WriteErrorFailToReadText(DocumentName)
        return
    #else:
        #pdfread = pdftotext.PDF(PDFfile)
    PDFfile.close()
        
        

    pdftext = ""

    for page in pdfread:
            pdftext = pdftext + page
    #print(pdftext)
    print('File:' + DocumentName)
    print('Magic Number:' + magicnumber)
    print('Product Code:' + GetProductCode(pdftext))
    print('Product Name:' + GetProductName(pdftext))
    print('Manufacturer Name:' + GetManufacturerName(pdftext))
    print('Manufacturer Address:' + GetManufacturerAddress(pdftext))
    print('Signal Word:' + GetSignalWord(pdftext))
    print('Revision Date:' + GetRevDate(pdftext))
    print('Unprocessed Ingredients List:' + GetBigIngredients(pdftext))
    
    WriteProductInfo(magicnumber, GetProductCode(pdftext), GetProductName(pdftext), GetManufacturerName(pdftext), GetManufacturerAddress(pdftext), GetSignalWord(pdftext), DocumentName, GetRevDate(pdftext))
    WriteOutBigIngredients(GetBigIngredients(pdftext),magicnumber)


def GetMagicNumbers():
    file = open('sdslinks.txt', 'r')
    magic_numbers = re.findall('\d\d\d\d\d\d\d\d\d\d\d\d', file.read())
    file.close()
    magic_numbers = list(OrderedDict.fromkeys(magic_numbers))
    return magic_numbers

#main
ReadyProductInfoSheet()

magic_numbers = GetMagicNumbers()
for numbers in magic_numbers:
    ProcessPDF(numbers)
# ProcessPDF('035777949535')
