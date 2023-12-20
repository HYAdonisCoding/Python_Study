# -*- coding: utf-8 -*-

import sqlite3

def main():
    try:
        conn = sqlite3.connect("test.db")
        print('Open database connection')
        
        c = conn.cursor() # 获取游标
        # 建表
        # sql = '''
        #         create table company
        #             (id integer primary key not null,
        #             name text not null,
        #             age integer not null,
        #             address char(50),
        #             salary real);
        #     '''
        
        # 插入数据
        # sql = '''
        #         insert into company
        #             (id, name, age, address, salary)
        #             values (2, 'Eason', 25, '杭州', 14000);
        #     '''
        # c.execute(sql)
        # conn.commit()
        # c.close()
        # print('create table successfully')
        
        # 查询数据
        sql = '''
                select id, name, age, address, salary from company
            '''
        cursor = c.execute(sql)
        for row in cursor:
            print('id = %s, name = %s, age = %s, address = %s' % (row[0], row[1], row[2], row[3]))
        c.close()
        print('查询 successfully')
    except Exception as e:
        print(f'Failed at {e}')
    finally:
         if conn:
            conn.close()
            print('Connection closed')
    
   

if __name__ == '__main__':
    main()