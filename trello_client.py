import requests  
import sys
import collections


###


api_key = input("Введите свой Api Key: ")
token = input('Введите свой Token: ')
board_id = input('Введите Id нужной доски : ')


auth_params = {    
    'key': api_key,    
    'token': token
}

 
# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.  
base_url = "https://api.trello.com/1/{}"  


def read():    
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        print(column['name'])    
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'])  


def create_task(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    print(column_data)
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:      
        if column['name'] == column_name:      
            # Создадим задачу с именем _name_ в найденной колонке      
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break


def move(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_id = None    
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name:    
                task_id = task['id']    
                break    
        if task_id:    
            break    
       
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            break


def create_column(column_name):
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    for coloumn in column_data:
        if coloumn['name'] == column_name:
            print('Такая колонка уже существует')
            break    
    requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': column_name, **auth_params})


def counter_of_cards():
    i = 0
    numbers = []
    while i <= 100 :
        i = str(i)
        numbers.append(i)
        i = int(i)
        i+=1
    # запустим счетчик
    count_of_cards = collections.Counter()
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        count_of_cards['cards'] = 0
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:
            count_of_cards['cards'] += 1
        value_of_cards = str(count_of_cards['cards'])
        name_list = column['name'].split(' ')
        print(name_list)
        print(value_of_cards)
        if name_list[-1] in numbers:
            name_list.pop()
            i = 1
            new_name = name_list[0]
            while i < len(name_list):
                new_name = new_name + ' ' + name_list[i]
                i += 1
            column['name'] = new_name + ' {}'.format(value_of_cards)
        else:
            column['name'] = column['name'] + ' {}'.format(value_of_cards)
        requests.put(base_url.format('lists') + '/' + column['id'], data={'name': column['name'], **auth_params})


if __name__ == "__main__":    
    if len(sys.argv) <= 2:    
        read()
        counter_of_cards()
    elif sys.argv[1] == 'create_task':    
        create_task(sys.argv[2], sys.argv[3])   
        counter_of_cards() 
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3])
        counter_of_cards()
    elif sys.argv[1] == 'create_column':    
        create_column(sys.argv[2])
        counter_of_cards()
