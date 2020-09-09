import pickle

src = ["-1001278649804"]
# # 1001278649804
des = ["-1001192163198"]
# # 1001192163198
#
# with open("des.pkl","wb") as file:
#     pickle.dump(des, file)
# with open('des.pkl',"rb") as file:
#     data = pickle.load(file)
# print(data)
# if -1001278649804 not in data:
#     print("fghjk")
dc = {-1001192163198: 'coder_saga', -1001278649804: 'Coder_saga' }
with open("channel1.pickle", "wb") as file:
    pickle.dump(dc,file)

# with open("channel1.pickle", "rb") as file:
#     data = pickle.load(file)
# print(data)