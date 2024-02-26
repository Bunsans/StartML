def find_set(v):
    if v == parent[v]:
        return (v, 0)
    else:
        res = find_set(parent[v])
        parent[v] = res[0]
        add[v] += res[1]
        return (parent[v], add[v])

def make_set(v):
    parent[v] = v
    sz[v] = 1

def union_sets(a, b):
    a = find_set(a)[0]
    b = find_set(b)[0]
    if a != b:
        if sz[a] < sz[b]:
            a, b = b, a
        parent[b] = a
        add[b] -= add[a]
        add[a] += 1
        sz[a] += sz[b]

if __name__ == "__main__":
    n, q = map(int, input().split())
    parent = list(range(n + 1))
    sz = [0] * (n + 1)
    add = [0] * (n + 1)

    for i in range(1, n + 1):
        make_set(i)

    for _ in range(q):
        query = list(map(int, input().split()))
        type = query[0]
        x = query[1]

        if type != 3:
            y = query[2]

        if type == 1:
            union_sets(x, y)
        elif type == 2:
            x = find_set(x)[0]
            y = find_set(y)[0]
            if x == y:
                print("YES")
            else:
                print("NO")
        else:
            res = find_set(x)
            print(res[1] + add[res[0]] + 1)
