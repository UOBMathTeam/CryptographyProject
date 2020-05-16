import numba

@numba.jit('boolean(int64)', nopython = True)
def isprime_basic_fast(n):
    '''
    Checks whether the argument n is a prime number using a brute force 
    search for factors between 1 and n. We made it verbose here for 
    illustration. (I.e. it prints out its results.)
    '''
    # If n is even then it is only prime if it is 2
    if n==1:
        return False
    
    if n % 2 == 0:
        if n == 2: 
            return True
        else:
            return False
        
    # So now we can consider odd numbers only. 
    j = 3
    rootN = n**0.5
    # Now check all numbers 3,5,... up to sqrt(n)
    while j <= rootN: 
        if n % j == 0:
            return False
        j = j + 2
    return True 

def isprime_basic(n,verbose=False): 
    '''
    Checks whether the argument n is a prime number using a brute force 
    search for factors between 1 and n. We made it verbose here for 
    illustration. (I.e. it prints out its results.)
    '''
    # If n is even then it is only prime if it is 2
    if n==1:
        return False
    if n % 2 == 0:
        if n == 2: 
            return True
        else:
            if verbose:
                print("{} is not prime: {} is a factor. ".format(n,2))
            return False
    # So now we can consider odd numbers only. 
    j = 3
    rootN = n**0.5
    # Now check all numbers 3,5,... up to sqrt(n)
    while j <= rootN: 
        if n % j == 0:
            if verbose:
                print("{} is not prime: {} is a factor.".format(n,j))
            return False
        j = j + 2
    if verbose:
        print("{} is prime.".format(n))
    return True 

@numba.jit('int64(int64,int64)', nopython = True)
def gcd_fast(a,b):
    """Returns the greatest common divisor of integers a and b using Euclid's algorithm.
    The order of a and b does not matter and nor do the signs."""
    if not(a%1 ==0 and b%1==0):
        return -1
    if b==0:
        return abs(a)                           #Use abs to ensure this is positive
    else:
        return gcd_fast(b,a%b)

def gcd(a,b):
    """Returns the greatest common divisor of integers a and b using Euclid's algorithm.
    The order of a and b does not matter and nor do the signs."""
    if not(a%1 ==0 and b%1==0):
        return "Need to use integers for gcd."
    if b==0:
        return abs(a)                           #Use abs to ensure this is positive
    else:
        return gcd(b,a%b)



def gcd_ext(a,b):
    """Wish to output (gcd,x,y) such that gcd=ax+by."""
    if not(a%1 ==0 and b%1==0):                         #Reject if trying to use for non-integers
        return "Need to use integers for gcd."          
    if a == 0:                                          #Base case is when a=0.
        return (abs(b), 0, abs(b)//b)                   #Then gcd =|b| and is 0*a+1*b or 0*a-1*b. Use abs(b)//b
    else:
        quot=b//a                                       #The rule is that g=gcd(a,b)=gcd(b%a,a).
                                                        #Let b=qa+r where r=b%a
        g, x, y = gcd_ext(b%a, a)                       #And if  g=x1*r + y1*a then since r=b-qa
        return (g, y - quot * x, x)                     #We get g = a*(y1-q*x1)+x1*b.
                                                        #So x=y1-q*x1 and y=x1.
        
@numba.jit(nopython = True)
def gcd_ext_fast(a,b):
    """Wish to output (gcd,x,y) such that gcd=ax+by."""
      
    if a == 0:                                          #Base case is when a=0.
        return (abs(b), 0, abs(b)//b)                   #Then gcd =|b| and is 0*a+1*b or 0*a-1*b. Use abs(b)//b
    else:
        quot=b//a                                       #The rule is that g=gcd(a,b)=gcd(b%a,a).
                                                        #Let b=qa+r where r=b%a
        g, x, y = gcd_ext_fast(b%a, a)                       #And if  g=x1*r + y1*a then since r=b-qa
        return (g, y - quot * x, x)
    

def smallest_factor(n):
    """Returns the smallest factor of a positive integer n."""
    sqrt=n**0.5
    i=2
    while i<=sqrt:
        if n%i==0:
            return i                            #If we get here, return i as the value.
        i+=1
    return n                                    #If we get through the whole while loop, return n.


def recompose(dict):
    """Recomposes an integer from the factor dictionary."""
    result=1                                                #start with 1 and multiply
    for p in dict.keys():
        result = result*(p**dict[p])
    return result                                           #Stop once we've run through the whole dict


def decompose(n):
    """Generates a dictionary representing the prime decomposition."""
    factors={}
    current_number=n                            #divide current_number by the factors found until it reaches 1
    while current_number > 1:
        p=smallest_factor(current_number)
        if p in factors.keys():                 #if p is not a new factor, increase the power
            factors[p]+=1
        else:
            factors[p]=1                        #if p is a new factor, create a new entry
        current_number = current_number//p
    return factors


def make_mult_func(fun_pp):
    """Takes a function fun_pp that is only defined on prime power and the associated
    multiplicative function defined on all positive integers."""
    def mult_version(n):                        #The output should be another function -- this one
        n=decompose(n)
        result=1
        for p in n.keys():
            result*=fun_pp(p,n[p])
        return result
    return mult_version                         #Return the function made.

def mult_div_no(n):
    """Find the number of divisors relying on the fact this is a multiplicative function."""
    n=decompose(n)                 #calculate from the factorisation
    result=1
    for p in n.keys():
        result *= (n[p]+1)
    return result
