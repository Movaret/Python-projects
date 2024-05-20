{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: openpyxl in c:\\users\\сергей\\appdata\\local\\programs\\python\\python312\\lib\\site-packages (3.1.2)\n",
      "Requirement already satisfied: et-xmlfile in c:\\users\\сергей\\appdata\\local\\programs\\python\\python312\\lib\\site-packages (from openpyxl) (1.1.0)\n"
     ]
    }
   ],
   "source": [
    "# Модуль для работы с excel\n",
    "\n",
    "!pip install openpyxl"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import os"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "path = ''\n",
    "NPS = pd.read_excel('')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 83,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Ранжируем по айдишнику, оставляем только первый вариант и дропаем ненужный столбец\n",
    "\n",
    "NPS['row_num'] = NPS.groupby(['id']).cumcount() + 1\n",
    "NPS = NPS[NPS.row_num == 1]\n",
    "NPS = NPS.drop(['row_num'], axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 84,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Сохраняем с именем изначального файла, чтоб не запутаться в датах\n",
    "\n",
    "NPS.to_excel('D:/Python/' + os.path.basename(path).split('/')[-1], index = False)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
