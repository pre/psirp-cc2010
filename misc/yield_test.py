
#import sys
# 
# def anonymous_function(param):
#   yield "Param oli" + str(param)
# 
# 
# def generator():
#   yield
# 
# def twice(f):
#     f()
#     f()
# 
# twice(lambda: sys.stdout.write("hello world\n"))

# > ## Ruby #####################
# > def twice
# >      yield
# >      yield
# > twice { puts "hello world" }
# > #############################



# def my_range(first, count, step):
#    while count > 0:
#       yield first
#       first += step
#       count -= 1
# 
# for i in my_range(1, 10, 2):
#    print i
# 