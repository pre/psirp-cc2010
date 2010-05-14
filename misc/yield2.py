
def summaa(alkio, testi):
  for toisto in range(1, 3):
    yield(str(toisto) + "alkio on " + str(alkio))
  
def iteraattori():
  for alkio in range(1, 5):
    yield(summaa(alkio), "testi")
#    yield(alkio)
    
for i in iteraattori():
  for o in i:
    print "tuli:", o