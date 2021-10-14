import json
import numpy as np
from scipy.stats import norm
import math
from scipy.linalg import cholesky

# Basis function of the Metalog
def basis(y,t) -> int:
    ret = 0
    if(t == 1):
        ret = 1
    elif(t == 2):
        ret = math.log(y/(1-y))
    elif(t == 3):
        ret = (y-0.5)*math.log(y/(1-y))
    elif(t == 4):
        ret = y-0.5
    elif(t >= 5 ) and (t%2 == 1):
        ret = math.pow((y - 0.5), ((t-1) // 2))
    elif(t >= 6 ) and (t%2 == 0):
        ret = math.pow((y - 0.5), ((t-1) // 2)) * math.log(y/(1-y))
    return ret

def metalog(y, a, bl = "", bu = ""):
    t = range(1,len(a)+1)
    vector = []
    np_a = np.array(a).reshape(-1,1)

    for n in t:
        vector.append(basis(y,n))

    vector = np.array(vector, dtype=object)
    mky = np.matmul(vector,np_a)

    # Unbounded
    if (type(bl) == str) and (type(bu) == str):
        return float(mky)
    # Bounded lower
    elif (type(bl) != str) and (type(bu) == str):
        float(bl)
        return bl + math.exp(mky)
    # Bounded upper
    elif (type(bl) == str) and (type(bu) != str):
        float(bu)
        return (bu - math.exp(-mky))
    # Bounded
    elif (type(bl) != str) and (type(bu) != str):
        return bl+bu*math.exp(mky)/(1+math.exp(mky))

def hdr(pm_trials, var=0, ent=0, attr1=0, attr2=0, round_off= 15, Seedlist=None):
    if (type(Seedlist) == list):

        while len(Seedlist) < 4:
            Seedlist.append(0)

        """Hubbard Decision Research counter-based PRNG"""
        values = []
        for pm_index in range(1, pm_trials+1):
            eq = ((((
                (((999999999999989 % ((
                (pm_index * 2499997 + Seedlist[0] * 1800451 + Seedlist[1] * 2000371 + Seedlist[2] * 1796777 + Seedlist[3] * 2299603)
                    % 7450589) * 4658 + 7450581)) * 383) % 99991) * 7440893 +
                (((999999999999989 % ((
                (pm_index * 2246527 + Seedlist[0] * 2399993 + Seedlist[1] * 2100869 + Seedlist[2] * 1918303 + Seedlist[3] * 1624729)
                    % 7450987) * 7580 + 7560584)) * 17669) % 7440893)) * 1343)
                    % 4294967296) + 0.5) / 4294967296

            eq = round(eq, ndigits=round_off)

            values.append(eq)

        return values
    else:
        values = []
        for pm_index in range(1, pm_trials+1):
            eq = ((((
                (((999999999999989 % ((
                (pm_index * 2499997 + var * 1800451 + ent * 2000371 + attr1 * 1796777 + attr2 * 2299603)
                    % 7450589) * 4658 + 7450581)) * 383) % 99991) * 7440893 +
                (((999999999999989 % ((
                (pm_index * 2246527 + var * 2399993 + ent * 2100869 + attr1 * 1918303 + attr2 * 1624729)
                    % 7450987) * 7580 + 7560584)) * 17669) % 7440893)) * 1343)
                    % 4294967296) + 0.5) / 4294967296

            eq = round(eq, ndigits=round_off)

            values.append(eq)

        return values

def convertMx(correlationMatrix):
    variables = []

    # gotta figure out all of the variables in the matrix
    for vars in correlationMatrix:
        if vars["row"] not in variables:
            variables.append(vars["row"])

    variableCount = len(set(variables))

    returnArray = np.zeros(shape=[variableCount, variableCount])
    for items in correlationMatrix:
        i = variables.index(items["row"])
        j = variables.index(items["col"])
        value = items["value"]
        returnArray[i][j] = value
        returnArray[j][i] = value

    return returnArray

## function to import json
class ImportJSON:
    def __init__(self, jsonfile):
        # Viewable attributes
        self.jsonData = json.loads(jsonfile)
        self.randoms = {}
        self.copula = None
        self.SIPs = {}

        # Initially set all values of hidden variables
        self.__rng = None
        self.__copulaValues = None
        self.__SIPs = None
        self.enviroment = "generic"

        self.__x = json.loads(jsonfile)
        try:
            self.__rng = self.__x["U01"]["rng"]
        except: Exception: ...
        try:
            self.__copulaValues = self.__x["U01"]['copula']
        except: Exception: ...
        try:
            self.__SIPs = self.__x['sips']
        except: Exception: ...

    def randomList(self):
        for i in self.__rng:
            print(i['name'])

    def generateRandom(self, random):
        randomIndex = [item.get("name") for item in self.__rng].index(random)

        fxn = self.__rng[randomIndex]["function"]

        # TODO: Check if arguments all have the same dictionary labels

        entity = self.__rng[randomIndex]["arguments"]["entity"]
        varId = self.__rng[randomIndex]["arguments"]["varId"]
        seed3 = self.__rng[randomIndex]["arguments"]["seed3"]
        seed4 = self.__rng[randomIndex]["arguments"]["seed4"]

        if (type(seed3) == dict):
            if "seed3" in self.__kwargDict[random]:
                seed3 = self.__kwargDict[random]["seed3"]
            else:
                raise ValueError(seed3["name"],". Seed3 needs to have a value.")

        if (type(seed4) == dict):
            if "seed4" in self.__kwargDict[random]:
                seed4 = self.__kwargDict[random]["seed4"]
            else:
                raise ValueError(seed4["name"],"Seed4 needs to have a value.")


        args = [varId, entity, seed3, seed4]

        if (fxn == "HDR_2_0"):
            val = hdr(1000,*args)
            self.randoms[random] = val
            return val
        else:
            return eval(fxn.format(*args,all=args))

    def generateCopula(self, random):
        ret = []

        # TODO: need to check for copula in document
        # Do all of this for all copulas in document
        for copulas in self.__copulaValues:

            if (copulas["function"] == "GaussianCopula"):
                # now get the cholesky factors
                # get the global variable
                specifyCorrelationMatrix = copulas["arguments"]["correlationMatrix"]["value"]

                copulaArgs = copulas["arguments"]['rng']

                randomMatrix = np.zeros(shape=(1, 1000))

                for i in range(len(copulaArgs)):
                    val = self.generateRandom(copulaArgs[i])
                    randomMatrix = np.append(randomMatrix, [val], axis=0)

                for index, item in enumerate(self.__x["globalVariables"]):
                    if item["name"] == specifyCorrelationMatrix:
                        whichCorrelationMatrix = index
                        break
                else:
                    index = -1

                thisCorrelationMatrix = self.__x["globalVariables"][whichCorrelationMatrix]["value"]["matrix"]
                correlationMatrix = convertMx(thisCorrelationMatrix)

                # Find the Cholesky Factors
                cho = cholesky(correlationMatrix, lower=False)
                #print("Cholesky: \n", cho)

                cho = np.matrix(cho)
                # Apply the Cholesky Factors to the randoms
                for i in range(0, 1000):
                    # find out what rows of the hdr ret matrix to use based on what was asked for
                    col = copulas["copulaLayer"].index(random)
                    choSubSample = cho[:col+1,col]
                    trial = randomMatrix[1:col+2, i]

                    invCdf = norm.ppf(trial).reshape(-1,col+1)
                    # get HDRs from matrix
                    mMult = np.dot(invCdf,choSubSample)
                    val = float(norm.cdf(mMult))

                    ret.append(val)

            else:
                raise TypeError("The function type for this copula is unsupported. ")

        # Add the result of the cholesky to the copula variable
        self.copula = ret
        return ret

    def sipList(self):
        for i in self.__SIPs:
            print(i['name'])

    def simulateSIP(self, sip, **kwargs):
        # TODO: Add an all option for doing all sips

        #example keyword argument for input: simulateSIP("Variable1", HDR2= {"seed3":0, "seed4":1})
        self.__kwargDict = kwargs

        randomarray = []

        sipIndex = [item.get("name") for item in self.__SIPs].index(sip)

        if (self.__SIPs[sipIndex]["ref"]["source"]  == "copula"):
            randomarray = ImportJSON.generateCopula(self, self.__SIPs[sipIndex]["ref"]["copulaLayer"])

        elif (self.__SIPs[sipIndex]["ref"]["source"] == "rng"):
            randomarray = ImportJSON.generateRandom(self, self.__SIPs[sipIndex]["ref"]["name"])

        args = self.__SIPs[sipIndex]['arguments']["aCoefficients"]

        lowerBound = ""
        upperBound = ""

        try:
            lowerBound = self.__SIPs[sipIndex]["arguments"]["lowerBound"]
            pass
        except:
            pass
        try:
            upperBound = self.__SIPs[sipIndex]["arguments"]["upperBound"]
            pass
        except:
            pass

        function = self.__SIPs[sipIndex]["function"]
        returnValue = []

        # if the function is a built in function Metalog_1_0 then,
        # for each item
        if ( function == "Metalog_1_0"):

            # TODO: change for loop into a vectorized numpy function
            for trial in randomarray:

                ml = metalog(trial, a=args, bl=lowerBound,bu=upperBound)

                returnValue.append(ml)

        self.SIPs = returnValue
        return returnValue
