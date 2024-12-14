x1 = 20.0
y1 = 500.421

x2 = 21.0
y2 = 9.96304

y_peak = 500.421 

x = x1 + (((x2 - x1)*(y_peak/2 - y1))/(y2-y1)) 


print(f'x1 = {x1}')
print(f'y1 = {y1}')
print(f'x2 = {x2}')
print(f'y2 = {y2}')
print(f'y_піковий = {y_peak}')

print()
print(f'Xб = {x}')