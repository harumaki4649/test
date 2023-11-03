my_list = [["A", "100", "2"], ["B", "150", "2.3"], ["A", "101", "2"], ["B", "20", "2.3"]]

# 2番目の値（インデックス1）を基準にリストを並び替える
sorted_list = sorted(my_list, key=lambda x: float(x[1]), reverse=True)

print(sorted_list)