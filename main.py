from tabulate import tabulate
from pulp import *

# Transport muammosini aniqlash
c = [[4,3,4,1,4],[2,5,3,6,4],[1,3,3,2,2],[3,4,6,4,5]] # birlik xarajatlar matritsasi
Zaxira = [10,25,20,30]  # Zaxira
Talab = [20,20,10,10,25]  # Talab

_x = len(c)
_y = len(c[0])
# Muommoni aniqlsh
prob = LpProblem("Transportation Problem", LpMinimize)

# O'zgaruvchilarini aniqlash
# x[i][j] i manbadan j manziliga tashilgan tovarlar miqdorini bildiradi
x = LpVariable.dicts("x", [(i, j) for i in range(_x) for j in range(_y)], lowBound=0, cat='Integer')

# Maqsad funksiyasini aniqlash
prob += lpSum([x[(i, j)] * c[i][j] for i in range(_x) for j in range(_y)]), "Total Cost"

# Cheklovlarni aniqlash
for i in range(_x):
    prob += lpSum([x[(i, j)] for j in range(_y)]) == Zaxira[i], f"Zaxira {i}"
for j in range(_y):
    prob += lpSum([x[(i, j)] for i in range(_x)]) == Talab[j], f"Talab {j}"

# Muammoni hal qilish
prob.solve()

# Optimal yechimni chop etish uchun jadvalga tayyorlash
headers = ["Ishlab chiqaruvchi/Mijoz"] + [f"B{j+1}" for j in range(_y)] + ["Zaxira"]
data = [[f"A{i+1}"] + [value(x[(i, j)]) for j in range(_y)] + [Zaxira[i]] for i in range(_x)]
data.append(["Talab"] + Talab + [""])

#jadvlani chop etish
print(tabulate(data, headers=headers, tablefmt="grid"))
#umumiy narxni chop etish
print(f"Umumiy narx: ${value(prob.objective)}")