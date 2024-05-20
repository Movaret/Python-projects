{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import os"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Сергей\\AppData\\Local\\Temp\\ipykernel_8652\\3201993588.py:2: DtypeWarning: Columns (10,11) have mixed types. Specify dtype option on import or set low_memory=False.\n",
      "  data = pd.read_csv('Petrovax base/Base 2024-04-08.csv', sep = ';')\n"
     ]
    }
   ],
   "source": [
    "path = '' \n",
    "data = pd.read_csv('', sep = ';')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "data = data[['ContactID', 'ClientFullName', 'Phone', 'Email', 'AddedAt', 'ConfirmationToken', 'Notes', 'Region2', 'Specialization']]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Берём раздельно непустые мэйлы, телефоны и доп.поле 'notes', отбираем для каждого contactID макс. дату добавления\n",
    "\n",
    "last_mail = data[['ContactID', 'AddedAt']][data[['Email']].notnull().all(1)].groupby('ContactID')['AddedAt'].max().reset_index()\n",
    "last_phone = data[['ContactID', 'AddedAt']][data[['Phone']].notnull().all(1)].groupby('ContactID')['AddedAt'].max().reset_index()\n",
    "last_note = data[['ContactID', 'AddedAt']][data[['Notes']].notnull().all(1)].groupby('ContactID')['AddedAt'].max().reset_index()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Джойним изначальный файл, чтобы по дате и ContactID достать значения и токен\n",
    "\n",
    "last_mail = pd.merge(last_mail, data,\n",
    "                     left_on = ['ContactID', 'AddedAt'], right_on = ['ContactID', 'AddedAt'],\n",
    "                     how = 'left')\n",
    "\n",
    "last_phone = pd.merge(last_phone, data,\n",
    "                     left_on = ['ContactID', 'AddedAt'], right_on = ['ContactID', 'AddedAt'],\n",
    "                     how = 'left')\n",
    "\n",
    "last_note = pd.merge(last_note, data,\n",
    "                     left_on = ['ContactID', 'AddedAt'], right_on = ['ContactID', 'AddedAt'],\n",
    "                     how = 'left')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Оставляем только значения и токен, убираем пустые и дубли\n",
    "\n",
    "last_mail = last_mail[['ContactID', 'AddedAt', 'Email', 'ConfirmationToken']][last_mail[['Email']].notnull().all(1)].drop_duplicates()\n",
    "last_phone = last_phone[['ContactID', 'AddedAt', 'Phone', 'ConfirmationToken']][last_phone[['Phone']].notnull().all(1)].drop_duplicates()\n",
    "last_note = last_note[['ContactID', 'AddedAt', 'Notes']][last_note[['Notes']].notnull().all(1)].drop_duplicates()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Набираем личные данные юзеров, к которым будем джойнить контакты\n",
    "\n",
    "contacts = data[['ContactID', 'ClientFullName', 'Region2', 'Specialization']][data[['ContactID']].notnull().all(1)].drop_duplicates()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Джойним все последние значения, собираем финальный, удаляем дубли на всякий случай\n",
    "\n",
    "final = contacts.merge(last_mail, on = 'ContactID', how = 'left').merge(last_phone, on = 'ContactID', how = 'left').merge(last_note, on = 'ContactID', how = 'left')\n",
    "final = final[['ContactID', 'ClientFullName', 'Phone', 'ConfirmationToken_y', 'Email', 'ConfirmationToken_x', 'Region2', 'Specialization', 'Notes']].drop_duplicates()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Переименовываем столбцы, меняем float на вменяемый формат\n",
    "\n",
    "rename = {'ClientFullName': 'ФИО',\n",
    "          'Phone' : 'Телефон',\n",
    "          'ConfirmationToken_y': 'Phone.ConfirmationToken',\n",
    "          'Email': 'Почта',\n",
    "          'ConfirmationToken_x': 'Email.ConfirmationToken',\n",
    "          'Region2': 'Регион',\n",
    "          'Specialization': 'Специальность'\n",
    "          }\n",
    "\n",
    "final.rename(columns=rename, inplace=True)\n",
    "\n",
    "final['ContactID'] = final['ContactID'].astype(int)\n",
    "final['Телефон'] = final['Телефон'].astype(str).str.replace('.0', '')\n",
    "final['Phone.ConfirmationToken'] = final['Phone.ConfirmationToken'].astype(str).str.replace('.0', '')\n",
    "final['Email.ConfirmationToken'] = final['Email.ConfirmationToken'].astype(str).str.replace('.0', '')\n",
    "final = final.replace('nan','')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Ранжируем каждый айдишник, чтобы убрать дубли.\n",
    "# По договорённости с клиентом, если у одного ContactID несколько одинаковых максимальных дат, оставляем только первый вариант.\n",
    "# row_num дропаем\n",
    "\n",
    "final['row_num'] = final.groupby(['ContactID']).cumcount() + 1\n",
    "final = final[final.row_num == 1]\n",
    "final = final.drop(['row_num'], axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Сохраняем с датой изначального csv, чтоб не запутаться от какого числа обновление\n",
    "\n",
    "final.to_csv('D:/Python/' + os.path.basename(path).split('/')[-1], index = False, encoding = 'utf-8')"
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
