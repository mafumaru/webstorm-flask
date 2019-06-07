def quicksort(list,p,r):
    if p<r:
        return
    i=p
    j=r
    key=list[p]
    while(i<j):
        while(i<j and key <=list[j]):
            j-=1
        list[i]=list[j]
        while(i<j and key >= list[i]):
            i+=1
        list[j]=list[i]
    list[i]=key
    quicksort(list,p,i-1)
    quicksort(list,i+1,r)

a = [6,2,7,3,8,9]
quicksort(a,1,len(a))
