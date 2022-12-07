import random
import matplotlib.pyplot as plt
exp = 100000
de_number = 10
result = [sum([random.randint(1,6) for j in range(de_number)]) for i in range(exp)]

visual = [result.count(i) for i in range(6*de_number)]


plt.plot(visual)
plt.show()


    
    
        
    
    