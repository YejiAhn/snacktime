import pandas as pd
import numpy as np
from .models import Product

CU = pd.read_csv("crawling/cu.csv") 

i_category = 1
i_image = 2
i_name = 3
i_price = 4


for i in range(10):
    Product.objects.create(name=CU.iloc[i,i_name], price=CU.iloc[i,i_price], category=CU.iloc[i,i_category], photo=CU.iloc[i,i_image])
    
