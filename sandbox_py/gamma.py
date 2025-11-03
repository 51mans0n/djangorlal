class EventBus:
    def __init__(self):
        self._subs={}
    def on(self, event, fn):
        self._subs.setdefault(event, []).append(fn)
    def emit(self, event, *args, **kwargs):
        for fn in self._subs.get(event, []):
            fn(*args, **kwargs)

bus=EventBus()

class Store:
    def __init__(self):
        self.state={}
    def set(self, key, value):
        self.state[key]=value
        bus.emit("change", key, value)
    def get(self, key, default=None):
        return self.state.get(key, default)

store=Store()

def logger(event, key, value):
    print(f"[{event}] {key} -> {value}")

bus.on("change", logger)

def reduce_sum(seq):
    s=0
    for x in seq: s+=x
    return s

def map_square(seq): return [x*x for x in seq]

def filter_even(seq): return [x for x in seq if x%2==0]

def dedup(seq):
    seen=set(); out=[]
    for x in seq:
        if x not in seen:
            seen.add(x); out.append(x)
    return out

if __name__=="__main__":
    store.set("mode", "demo")
    print(dedup([1,1,2,3,3,3,4]))
print("dup5 gamma change")


print("dup4 gamma change")


print("dup3 gamma change")


print("dup2 gamma change")
print("dup1 gamma change")


