    # all_product = pd.read_csv('productpage/productlist/curie.csv')
    # i_category = 1
    # i_image = 2
    # i_name = 3
    # i_price = 4
    # i_PB = 5
    # for i in range(len(all_product)):
    #     Product.objects.create(name=all_product.iloc[i,i_name], price=all_product.iloc[i,i_price], category_code=all_product.iloc[i,i_category], photo=all_product.iloc[i,i_image], pb_store_code=all_product.iloc[i,i_PB])
    # return redirect('/products')

import pandas as pd
import numpy as np

all_product = pd.read_csv('/crawling/CU480-614.csv')
pb_product = pd.read_csv('/crawling/CU500-510csv')
i_name = 3
i_pb = 5
for i in range(len(pb_product)):
    name=pb_product.iloc[i,i_name]
    for j in range(len(all_product)):
        if all_product.ioc[j,i_name] == name:
            all_product.ioc[j,i_pb] = 1

