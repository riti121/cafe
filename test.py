lst=sorted(list(map(int,input().split())))[::-1]
temp=lst[0]
for i in range(1,len(lst)):
    if temp==lst[i]:
        continue
    else:
        print(lst[i])
        break


