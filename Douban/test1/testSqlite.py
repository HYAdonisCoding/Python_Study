# -*- coding: utf-8 -*-

import sqlite3
import re

def main():
    try:
        conn = sqlite3.connect("movietop250.db")
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
        # sql = '''
        #         select id, name, age, address, salary from company
        #     '''
        # cursor = c.execute(sql)
        # for row in cursor:
        #     print('id = %s, name = %s, age = %s, address = %s' % (row[0], row[1], row[2], row[3]))
        # c.close()
        # print('查询 successfully')
        
        # 插入
        # sql = 'select info,id from movie_top250'
        # cursor = c.execute(sql)
        # data = []
        # for row in cursor:
        #     year=''
        #     country = ''
        #     # 匹配年份和国家
        #     match = re.search(r'(\d{4})\s*([\u4e00-\u9fa5]+)', row[0])
        #     if match:
        #         year = match.group(1)
        #         country = match.group(2)
        #         # print("年份:", year, "国家:", country)
        #     else:
        #         print("------------------------------------------------")
        #         matches = re.findall(r'(\d{4})\s*\(([\u4e00-\u9fa5]+)\)', row[0])
                
        #         year = matches[len(matches)-1][0]
        #         country = matches[len(matches)-1][1]
        #         print("年份:", year)
        #         print("国家:", country)
        #         print("------------------------------------------------")
        #     data.append((year, country, row[1]))
        #     # cursor.execute("UPDATE movie_top250 SET year=?, nation=? WHERE id=?", (year, country, row[1]))
        # print(data)
        # for item in data:
        #     cursor.execute("UPDATE movie_top250 SET year=?, nation=? WHERE id=?", (item[0], item[1], item[2]))
        # conn.commit()
        # cursor.close
        # c.close()
        
        sql = 'select year, count(year) from movie_top250 group by year'
        cursor = c.execute(sql)
        for row in cursor:
            print(row[0], row[1])
        sql = 'select nation, count(nation) from movie_top250 group by nation'
        cursor = c.execute(sql)
        for row in cursor:
            print(row[0], row[1])
        cursor.close
        c.close()
    except Exception as e:
        print(f'Failed at {e}')
    finally:
         if conn:
            conn.close()
            print('Connection closed')
    
   

if __name__ == '__main__':
    main()
    text = "导演: 爱德华·兹威克 Edward Zwick 主演: 布拉德·皮特 Brad Pitt 安东... 1994 美国 剧情 爱情 战争 西部"

    
    