import pandas as pd
import numpy as np
import os


path = '' 
data = pd.read_csv('', sep = ';')

data = data[['ContactID', 'ClientFullName', 'Phone', 'Email', 'AddedAt', 'ConfirmationToken', 'Notes', 'Region2', 'Specialization']]

# Берём раздельно непустые мэйлы, телефоны и доп.поле 'notes', отбираем для каждого contactID макс. дату добавления

last_mail = data[['ContactID', 'AddedAt']][data[['Email']].notnull().all(1)].groupby('ContactID')['AddedAt'].max().reset_index()
last_phone = data[['ContactID', 'AddedAt']][data[['Phone']].notnull().all(1)].groupby('ContactID')['AddedAt'].max().reset_index()
last_note = data[['ContactID', 'AddedAt']][data[['Notes']].notnull().all(1)].groupby('ContactID')['AddedAt'].max().reset_index()

# Джойним изначальный файл, чтобы по дате и ContactID достать значения и токен

last_mail = pd.merge(last_mail, data,
                     left_on = ['ContactID', 'AddedAt'], right_on = ['ContactID', 'AddedAt'],
                     how = 'left')

last_phone = pd.merge(last_phone, data,
                     left_on = ['ContactID', 'AddedAt'], right_on = ['ContactID', 'AddedAt'],
                     how = 'left')

last_note = pd.merge(last_note, data,
                     left_on = ['ContactID', 'AddedAt'], right_on = ['ContactID', 'AddedAt'],
                     how = 'left')

# Оставляем только значения и токен, убираем пустые и дубли

last_mail = last_mail[['ContactID', 'AddedAt', 'Email', 'ConfirmationToken']][last_mail[['Email']].notnull().all(1)].drop_duplicates()
last_phone = last_phone[['ContactID', 'AddedAt', 'Phone', 'ConfirmationToken']][last_phone[['Phone']].notnull().all(1)].drop_duplicates()
last_note = last_note[['ContactID', 'AddedAt', 'Notes']][last_note[['Notes']].notnull().all(1)].drop_duplicates()

# Набираем личные данные юзеров, к которым будем джойнить контакты

contacts = data[['ContactID', 'ClientFullName', 'Region2', 'Specialization']][data[['ContactID']].notnull().all(1)].drop_duplicates()

# Джойним все последние значения, собираем финальный, удаляем дубли на всякий случай

final = contacts.merge(last_mail, on = 'ContactID', how = 'left').merge(last_phone, on = 'ContactID', how = 'left').merge(last_note, on = 'ContactID', how = 'left')
final = final[['ContactID', 'ClientFullName', 'Phone', 'ConfirmationToken_y', 'Email', 'ConfirmationToken_x', 'Region2', 'Specialization', 'Notes']].drop_duplicates()


# Переименовываем столбцы, меняем float на вменяемый формат

rename = {'ClientFullName': 'ФИО',
          'Phone' : 'Телефон',
          'ConfirmationToken_y': 'Phone.ConfirmationToken',
          'Email': 'Почта',
          'ConfirmationToken_x': 'Email.ConfirmationToken',
          'Region2': 'Регион',
          'Specialization': 'Специальность'
          }

final.rename(columns=rename, inplace=True)

final['ContactID'] = final['ContactID'].astype(int)
final['Телефон'] = final['Телефон'].astype(str).str.replace('.0', '')
final['Phone.ConfirmationToken'] = final['Phone.ConfirmationToken'].astype(str).str.replace('.0', '')
final['Email.ConfirmationToken'] = final['Email.ConfirmationToken'].astype(str).str.replace('.0', '')
final = final.replace('nan','')

# Ранжируем каждый айдишник, чтобы убрать дубли.
# По договорённости с клиентом, если у одного ContactID несколько одинаковых максимальных дат, оставляем только первый вариант.
# row_num дропаем

final['row_num'] = final.groupby(['ContactID']).cumcount() + 1
final = final[final.row_num == 1]
final = final.drop(['row_num'], axis=1)

# Сохраняем с датой изначального csv, чтоб не запутаться от какого числа обновление

final.to_csv('D:/Python/' + os.path.basename(path).split('/')[-1], index = False, encoding = 'utf-8')


