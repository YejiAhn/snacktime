import pandas as pd

cu_all=pd.read_csv('crawling/CU_complete.csv')
cu_pb = pd.read_csv('crawling/cu_PB.csv')

# cu_all=pd.read_csv('CU480-614.csv')
# cu_pb = pd.read_csv('CU500-510.csv')
i_category = 1
i_image = 2
i_name = 3
i_price = 4
i_PB = 5
j_name = 1

for i in range(len(cu_all)):
    name=cu_all.iloc[i,i_name]
    for j in range(len(cu_pb)):
        name_pb = cu_pb.iloc[j,j_name]
        # name_pb = cu_pb.iloc[j,i_name]
        if name in name_pb:
            cu_all.iloc[i,i_PB]=1
            print(i)

cu_all.to_csv('CU_pb_checked.csv')
            