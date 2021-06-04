import os 

my_path = os.path.abspath(os.path.dirname(__file__))

for i in range(20):
    old_file = my_path + "/" + str(i) + "_100_0.6.txt"
    new_file = my_path + "/" + str(i) + "_100_0.5.txt"
    os.rename(old_file, new_file)