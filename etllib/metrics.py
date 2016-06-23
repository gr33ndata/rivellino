
class Metrics:

    def __init__(self):
        pass

    @classmethod
    def exists(cls, v1):
        return 0 if not v1 else 1

    @classmethod
    def minlength(cls, v1, minl=0):
        return 0 if len(v1) < int(minl) else 1

    @classmethod
    def isintersect(cls, v1, v2):
        return -1 if set(v1).isdisjoint(set(v2)) else 1

    @classmethod
    def intersection(cls, v1, v2):
        isect = len(set(v1).intersection(set(v2)))
        return -1 if isect == 0 else isect

    @classmethod
    def jaccard(cls, v1, v2):
        if not v1 or not v2:
            return -1
        jcrd =  float(len(
            set(v1).intersection(set(v2))
        )) / float(len(
            set(v1).union(set(v2))
        ))
        return -1 if jcrd == 0 else jcrd


    @classmethod
    def lte(cls, v1, v2):
        if float(v1) < float(v2):
            return 1
        else:
            return -1

    @classmethod
    def gte(cls, v1, v2):
        if float(v1) > float(v2):
            return 1
        else:
            return -1