from GC_Tester import test
from GC_simple import GC_simple
from GC_complex import GC_complex
from GC_more_complex import GC_more_complex
if __name__ == '__main__':
    test(GC_more_complex,heap_size=100)
