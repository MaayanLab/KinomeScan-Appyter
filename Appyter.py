#!/usr/bin/env python
# coding: utf-8

# In[1]:


#%%appyter init
from appyter import magic
magic.init(lambda _=globals: _())

import xlrd
import csv
import requests
import pandas as pd


# In[2]:


get_ipython().run_cell_magic('appyter', 'markdown', "\n# {{ StringField(\n    name='title',\n    label='Title',\n    default='My Title',\n).render_value }}")


# In[3]:


get_ipython().run_cell_magic('appyter', 'code_exec', '\n# if small molecule name inputted, will go through its CSV file and sort by target affinity\n\nsm_name = {{ StringField(\n        name = \'Small molecule name\',\n        label = \'Small molecule name\',\n        description = \'The small molecule name\',\n        default = "Seliciclib",\n)}}\n\nkinome_df = pd.read_excel(\'http://lincs.hms.harvard.edu/wordpress/wp-content/uploads/2013/11/HMS-LINCS_KinomeScan_Datasets_2018-01-18.xlsx\')\nkinome_df[\'sm_hms_id\'] = kinome_df[\'sm_hms_id\'].str.replace(r\'\\D\', \'\') #remove HMSL before the ID\nhms_id = kinome_df.loc[kinome_df[\'sm_name\'] == sm_name, \'sm_hms_id\']\n\n# remove the row number\nhms_id_list = []\nfor hms_id in hms_id:\n    hms_id_list.append(hms_id)\n    \nhms_id_string = str(hms_id_list[0])\n\nold_url = \'http://lincs.hms.harvard.edu/db/datasets/20000/results?small+molecules=HMS_ID&output_type=.csv\'\nnew_url = old_url.replace("HMS_ID", hms_id_string) # fills in HMS_ID with the correct small molecule \n\ndata = pd.read_csv(new_url)\ndf = pd.DataFrame(data)\n\ntarget_affinity_1 = df.loc[df[\'Binding Class\'] == 1, \'HUGO Gene Symbol\']\ntarget_affinity_2 = df.loc[df[\'Binding Class\'] == 2, \'HUGO Gene Symbol\']\ntarget_affinity_3 = df.loc[df[\'Binding Class\'] == 3, \'HUGO Gene Symbol\']\ntarget_affinity_10 = df.loc[df[\'Binding Class\'] == 10, \'HUGO Gene Symbol\'] \n\nkinase1_list = []\nkinase2_list = []\nkinase3_list = []\n\nfor kinase in target_affinity_1:\n    kinase1_list.append(str(kinase))\n\nif len(kinase1_list) != 0:\n    print(\'Kinases with Kd < 100 nM: \')\n    kinase1_string = \', \'.join(kinase1_list)\n    print(kinase1_string)\n\nfor kinase in target_affinity_2:\n    kinase2_list.append(str(kinase)) \n\nif len(kinase2_list) != 0:\n    print(\'Kinases with 100 nM ≤ Kd < 1µM: \')\n    kinase2_string = \', \'.join(kinase2_list)\n    print(kinase2_string)\n    \nfor kinase in target_affinity_3:\n    kinase3_list.append(str(kinase))\n    \nif len(kinase3_list) != 0:\n    print("Kinases with 1µM ≤ Kd < 10 µM: ")\n    kinase3_string = \', \'.join(kinase3_list)\n    print(kinase3_string)')


# In[ ]:


get_ipython().run_cell_magic('appyter', 'code_exec', '\n# if kinase inputted, go through all small molecules 10001-12007 for : \n# check all the rows for each small molecule - if \'HUGO Gene Symbol\' includes the kinase then: \n# then go through all of those small molecules and determine which ones have target affinities of \n# 1, 2, and 3\n\n\nkinase_name = {{ StringField(\n        name = \'Kinase name\',\n        label = \'Kinase name\',\n        description = \'The kinase name\',\n        default = "CCNA1",\n)}}\n\nold_url = \'http://lincs.hms.harvard.edu/db/datasets/20000/results?small+molecules=HMS_ID&output_type=.csv\'\n\ndf = []\n\n# retrieve the CSV file for every small molecule, 10001-12007\nfor x in range(10001, 12007): \n    new_url = old_url.replace("HMS_ID", str(x)) # fills in HMS_ID with the correct small molecule \n    data = pd.read_csv(new_url)\n    print(x)\n    df.append(pd.DataFrame(data))\n\n# lists for each target affinity for the small molecules \ntarget_aff1 = []\ntarget_aff2 = []\ntarget_aff3 = []\ntarget_aff1_id = []\ntarget_aff2_id = []\ntarget_aff3_id = []\n\n# go through every datafile for every small molecule \nfor sm in df:\n    if kinase_name in sm.values: # if the protein kinase was studied for that particular small molecule \n        # determine targ aff for the inputted kinase\n        target_aff = sm.loc[sm[\'HUGO Gene Symbol\'] == kinase_name, \'Binding Class\'] \n        \n        # remove the column number \n        targ_aff_list = []\n        for targ in target_aff:\n            targ_aff_list.append(targ)\n        target_aff = targ_aff_list[0]\n        \n        # add small molecule to the appropriate list \n        if target_aff == 1:\n            target_aff1.append(sm.iloc[1][\'HMSL Small Mol Name\'])\n            hms_id = str(sm.iloc[1][\'HMSL Small Mol HMS LINCS ID\'])   \n            head, sep, tail = hms_id.partition(\'-\') # head is the hms_id of the small molecule \n            target_aff1_id.append(head) # HMS ID of the small molecule\n        elif target_aff == 2:\n            target_aff2.append(sm.iloc[1][\'HMSL Small Mol Name\'])\n        elif target_aff == 3:\n            target_aff3.append(sm.iloc[1][\'HMSL Small Mol Name\'])\n        else:\n            continue\n    \nprint("Small molecules that bind to the inputted kinase with Kd < 100 nM: ")\nprint(target_aff1)\nprint("Small molecules that bind to the inputted kinase with 100 nM ≤ Kd < 1µM: ")\nprint(target_aff2)\nprint("Small molecules that bind to the inputted kinase with 1µM ≤ Kd < 10 µM: ")\nprint(target_aff3)')


# In[ ]:





# In[ ]:




