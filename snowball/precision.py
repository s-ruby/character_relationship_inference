import os

def precision_k(total, comp_set, k):
  names = []
  unique_pairs = set()
  # matchers = ['abc','def']
  for pair in friend_list:
    if pair:
      temp = pair.split(" ")
      temp = temp[1].split('\t')
      pair_names = set(temp[0:2])
      names.append(pair_names)

  uniq_top_k = set()
  i = 0
  while len(uniq_top_k) < 10 and i < len(names):
      pair_names_sort = sorted(names[i])
      uniq_top_k.add(f"{pair_names_sort[0]} and {pair_names_sort[1]}")
      i += 1
  uniq_top = [value for value in uniq_top_k if value in friend_pairs]
  print(f"Top 10 Unique Friend Pairs: {len(uniq_top)/10 * 100}")
  
  top_k = names[:k]
  top = [value for value in top_k if value in comp_set]
  for friends in top:
      pair_names_sort = sorted(friends)
      unique_pairs.add(f"{pair_names_sort[0]} and {pair_names_sort[1]}")
  print(f"Unique friend pairs: {len(unique_pairs)}")
  return len(top)/k

def precision_per(total, comp_set, per):
  names = []
  # matchers = ['abc','def']
  for pair in friend_list:
    if pair:
      temp = pair.split(" ")
      temp = temp[1].split('\t')
      score = float(temp[2].split('\n')[0][6:])
      if score >= per:
        names.append(set(temp[0:2]))
  top = [value for value in names if value in comp_set]
  return len(top)/len(names)


friends = [{'Harry', 'Ron'},{'Harry', 'Hermione'},{'Hermione', 'Ron'},{'Harry', 'Hagrid'},{'Hagrid', 'Ron'},\
           {'Hermione', 'Hagrid'},{'Ginny', 'Hermione'},{'Harry', 'Ginny'},{'Ginny', 'Ron'},{'Harry', 'Dumbledore'}, \
           {'Dumbledore', 'Ron'}, {'Hermione', 'Dumbledore'}, {'McGonagall', 'Hagrid'}, {'Hermione', 'McGonagall'}, \
           {'Harry', 'McGonagall'}, {'Ron', 'McGonagall'}, {'Dumbledore', 'McGonagall'}, {'Dumbledore', 'Hagrid'}, \
           {'Ginny', 'Hagrid'}, {'Ginny', 'Dumbledore'}, {'Ginny', 'McGonagall'}, {'Neville', 'Dumbledore'}, \
           {'Harry', 'Cho'},{'Cho', 'Hermione'},{'Cho', 'Ron'},{'Cho', 'Ginny'},{'Hagrid', 'Neville'},\
           {'Hermione', 'Neville'},{'Harry', 'Neville'},{'Neville', 'Ron'}, {'Voldemort', 'Snape'},{'Dumbledore', 'Snape'} ]

friend_pairs = set()
for friend in friends:
    sorted_pairs = sorted(friend)
    friend_pairs.add(f"{sorted_pairs[0]} and {sorted_pairs[1]}")

    


foes = [{'Harry', 'Malfoy'}, {'Ron', 'Malfoy'}, {'Hermione', 'Malfoy'}, {'Ginny', 'Malfoy'}, {'Hagrid', 'Malfoy'},\
        {'Dumbledore', 'Malfoy'}, {'Neville', 'Malfoy'}, {'McGonagall', 'Malfoy'}, \
        {'Harry', 'Voldemort'}, {'Ron', 'Voldemort'}, {'Hermione', 'Voldemort'}, {'Ginny', 'Voldemort'}, {'Hagrid', 'Voldemort'},\
        {'Dumbledore', 'Voldemort'}, {'Neville', 'Voldemort'}, {'McGonagall', 'Voldemort'}, \
        {'Harry', 'Ballatrix'}, {'Ron', 'Ballatrix'}, {'Hermione', 'Ballatrix'}, {'Ginny', 'Ballatrix'}, {'Hagrid', 'Ballatrix'},\
        {'Dumbledore', 'Ballatrix'}, {'Neville', 'Ballatrix'}, {'McGonagall', 'Ballatrix'}, \
        {'Harry', 'Umbridge'}, {'Ron', 'Umbridge'}, {'Hermione', 'Umbridge'}, {'Ginny', 'Umbridge'}, {'Hagrid', 'Umbridge'},\
        {'Dumbledore', 'Umbridge'}, {'Neville', 'Umbridge'}, {'McGonagall', 'Umbridge'}, \
        {'Harry', 'Quirrell'}, {'Ron', 'Quirrell'}, {'Hermione', 'Quirrell'}, {'Ginny', 'Quirrell'}, {'Hagrid', 'Quirrell'},\
        {'Dumbledore', 'Quirrell'}, {'Neville', 'Quirrell'}, {'McGonagall', 'Quirrell'}, \
        {'Harry', 'Snape'}, {'Ron', 'Snape'}, {'Hermione', 'Snape'}, {'Ginny', 'Snape'}, {'Hagrid', 'Snape'},\
        {'Dumbledore', 'Snape'}, {'Voldemort', 'Snape'}, {'McGonagall', 'Snape'}, \
        {'Quirrell', 'Snape'}, {'Harry', 'Dudley'}, {'Hermione', 'Lucius'}, {'Ginny', 'Lucius'}, {'Hagrid', 'Lucius'},\
        {'Dumbledore', 'Lucius'}, {'Neville', 'Lucius'}, {'McGonagall', 'Lucius'} ]

files_friends = []
files_foe = []

sim_conf = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
books = ['1', '2', '3', '4', '5', '6', '7']

for book in books:
    for sc in sim_conf:
        # files_friends.append(f"snowball_results_friends/hp{book}_anaphora_{sc}_{sc}.txt")
        files_foe.append(f"snowball_results_foes/hp{book}__foes_anaphora_{sc}_{sc}.txt")
        

for f in files_friends:
    res = open(f)
    temp = (res.read())
    friend_list = temp.split('\n\n')
    k = 10
    per = .5
    print(f"For file: '{f}':")
    print(f"Precision at {k} is : {precision_k(friend_list, friends, 10) *100}%\n")
    # if per > .5:
    #     print(f"Precision above {per} is : {precision_per(friend_list, friends, per) *100}%")
res.close()

for f in files_foe:
  if os.path.exists(f):
    res = open(f)
    temp = (res.read())
    friend_list = temp.split('\n\n')
    k = 10
    per = .03
    print(f"For file: '{f}':")
    print(f"Precision at {k} is : {precision_k(friend_list, foes, 10) *100}%")
    #   print(f"Precision above {per} is : {precision_per(friend_list, foes, per) *100}%")
    print('\n')
    res.close()
  else:
      print(f"{f} FILE NOT FOUND")
