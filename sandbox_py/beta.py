def fib(n):
    a,b=0,1; out=[]
    for _ in range(n):
        out.append(a)
        a,b=b,a+b
    return out

def sieve(n):
    if n<2: return []
    p=[True]*(n+1); p[0]=p[1]=False
    for i in range(2,int(n**0.5)+1):
        if p[i]:
            step=i; start=i*i
            p[start:n+1:step]=[False]*(((n-start)//step)+1)
    return [i for i,v in enumerate(p) if v]

def chunked(seq, size):
    return [seq[i:i+size] for i in range(0, len(seq), size)]

def pairwise(seq):
    return list(zip(seq, seq[1:]))

def levenshtein(a,b):
    dp=[[0]*(len(b)+1) for _ in range(len(a)+1)]
    for i in range(len(a)+1): dp[i][0]=i
    for j in range(len(b)+1): dp[0][j]=j
    for i in range(1,len(a)+1):
        for j in range(1,len(b)+1):
            cost=0 if a[i-1]==b[j-1] else 1
            dp[i][j]=min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
    return dp[-1][-1]

def normalize(vec):
    s=sum(vec) or 1.0
    return [v/s for v in vec]

def cosine(a,b):
    import math
    dot=sum(x*y for x,y in zip(a,b))
    na=math.sqrt(sum(x*x for x in a))
    nb=math.sqrt(sum(x*x for x in b))
    return dot/(na*nb) if na and nb else 0.0

if __name__=="__main__":
    print("fib 10:", fib(10))
    print("primes up to 50:", sieve(50))
print("dup4 beta change")
