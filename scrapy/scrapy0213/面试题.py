input_str = input('请输入字符串：')
while True:
	num = input('请输入要判断的长度：')
	res_list = []
	for x in range(len(input_str)):
		end = x+int(num)
		res_list.append(input_str[x:end])
	# print(res_list)
	distance_list = set(res_list)
	max_count = max([res_list.count(x) for x in distance_list])
	res = [[x, max_count] for x in distance_list if res_list.count(x) == max_count]
	print(res)
