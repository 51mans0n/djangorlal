from math import sqrt

class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x); self.y = float(y)
    def __repr__(self): return f"Vector({self.x}, {self.y})"
    def __add__(self, other): return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other): return Vector(self.x - other.x, self.y - other.y)
    def dot(self, other): return self.x*other.x + self.y*other.y
    def norm(self): return sqrt(self.x**2 + self.y**2)
    def scale(self, k): return Vector(self.x*k, self.y*k)
    def unit(self):
        n = self.norm()
        return Vector(self.x/n, self.y/n) if n else Vector(0, 0)

def polygon_perimeter(points):
    per = 0.0
    for i in range(len(points)):
        a, b = points[i], points[(i+1)%len(points)]
        dx, dy = b[0]-a[0], b[1]-a[1]
        per += sqrt(dx*dx + dy*dy)
    return per

def moving_average(seq, w=3):
    out=[]; s=0
    for i, v in enumerate(seq):
        s += v
        if i>=w: s -= seq[i-w]
        if i>=w-1: out.append(s/w)
    return out

def clamp(x, lo, hi): return max(lo, min(hi, x))

def lerp(a,b,t): return a + (b-a)*t

def resample(seq, n=10):
    if not seq or n<=1: return seq[:]
    out=[]; m=len(seq)-1
    for i in range(n):
        t=i/(n-1); pos=t*m
        i0=int(pos); i1=min(i0+1, m)
        out.append(lerp(seq[i0], seq[i1], pos-i0))
    return out

def histogram(seq, bins=10):
    if not seq: return [0]*bins
    lo=min(seq); hi=max(seq); rng=hi-lo if hi!=lo else 1.0
    cnt=[0]*bins
    for v in seq:
        k=int((v-lo)/rng*bins)
        if k==bins: k=bins-1
        cnt[k]+=1
    return cnt

if __name__ == "__main__":
    pts=[(0,0),(1,0),(1,1),(0,1)]
    print("perimeter:", polygon_perimeter(pts))
