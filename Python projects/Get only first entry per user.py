# Модуль для работы с excel

!pip install openpyxl

import pandas as pd
import os

path = ''
NPS = pd.read_excel('')

# Ранжируем по айдишнику, оставляем только первый вариант и дропаем ненужный столбец

NPS['row_num'] = NPS.groupby(['id']).cumcount() + 1
NPS = NPS[NPS.row_num == 1]
NPS = NPS.drop(['row_num'], axis=1)

# Сохраняем с именем изначального файла, чтоб не запутаться в датах

NPS.to_excel('D:/Python/' + os.path.basename(path).split('/')[-1], index = False)


