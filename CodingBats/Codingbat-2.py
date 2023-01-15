def string_times(str, n):
  return str * n
def front_times(str, n):
  return str[:3]*n
def string_bits(str):
  return str[::2]
def string_splosion(str):
  return "".join([str[:i] for i in range(len(str) + 1)]) 
def last2(str):
  return sum(str[i:i+2] == str[-2:] for i in range(len(str)-2))
def array_count9(nums):
  return nums.count(9) 
def array_front9(nums):
  return 9 in nums[:4]  
def array123(nums):
  return (1,2,3) in zip(nums, nums[1:], nums[2:])
def double_char(str):
  return "".join([i*2 for i in str])
def count_hi(str):
  return str.count("hi")
def count_hi(str):
  return str.count("hi")
def cat_dog(str):
  return str.count("cat") == str.count("dog")
def count_code(str):
  return sum([ str[i:i+2] + str[i + 3] == "coe" for i in range(len(str) - 3)]) 
def end_other(a, b):
  return a.lower().endswith(b.lower()) or b.lower().endswith(a.lower())
def string_match(a, b):
  return sum([1 for i in range(len(a)-1) if a[i:i+2] == b[i:i+2]])  
def xyz_there(str):
  return str.count("xyz") != str.count(".xyz") 
def centered_average(nums):
  return (sum(nums) - max(nums) - min(nums))//(len(nums)-2)
def sum13(nums):
  return sum([v for i, v in enumerate(nums) if v != 13 and (i == 0 or nums[i-1] != 13)])
def has22(nums):
  return (2,2) in zip (nums, nums[1:])
def make_bricks(small, big, goal):
  return (small + big * 5 >= goal) and (goal % 5 <= small) 
def lone_sum(a, b, c):
  return sum([i for i in [a, b, c] if [a, b, c].count(i) == 1]) 
def lucky_sum(a, b, c):
 return (a != 13) * (a+ ((b!=13)*(b + (c * (c!=13)))))
def no_teen_sum(a, b, c):
  return sum([i for i in [a, b, c] if i not in range(13, 20) or i in range (15,17)])
def round_sum(a, b, c):
  return sum([x + ((p:=x % 10) >= 5) * (10 - p) - (x%10 < 5) * p for x in [a, b, c]]) 
def count_evens(nums):
  return sum([1 for i in nums if i % 2 == 0])
def big_diff(nums):
  return max(nums) - min(nums)
def close_far(a, b, c):
  return (min(abs(a-c),abs(a-b)) <= 1)* (max(abs(a-c),abs(a-b)) >= 2) * abs(b-c) >= 2
def make_chocolate(small, big, goal):
  return  (y:=small >= (g:=((w := (goal >= big*5)* (goal - 5*big)) + (not w) * (goal % 5)))) * g + (not y) *-1 
def sum67(nums): 
  while 6 in nums: nums = nums[:(p:=nums.index(6))] + (nums[p:])[nums[p:].index(7) + 1:]
  return sum(nums) 
#Santiago Criado, period 6, 2024