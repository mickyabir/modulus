from modulus.core.resources.tool import function


@function("Returns true if x is even")
def foofn(x: int):
    return x % 2
