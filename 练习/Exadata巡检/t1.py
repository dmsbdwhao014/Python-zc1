# import psutil
import os
from jinja2 import Environment,FileSystemLoader
import webbrowser
import cx_Oracle
dsn = cx_Oracle.makedsn("192.168.148.10", 1521, service_name="orcl")

def getResults():
    conn = cx_Oracle.connect('sys', 'oracle', dsn, mode=cx_Oracle.SYSDBA)
    cursor = conn.cursor()

    selectSql = """select  a.tablespace_name,
        a.file_id,
        round(a.free/1024/1024,2) || 'M' as "free_size",
        b.total/1024/1024 || 'M' as "total_size",
        round(b.maxbytes/1024/1024,2) || 'M' as "can_max_auto_allocated_size",
        round(((b.total-a.free)/total)*100,2) || '%' as "used_percent",
        round(((b.maxbytes-b.total)/b.maxbytes)*100,2) || '%' as "can_auto_allocated_percent"
from
(select tablespace_name,file_id,sum(bytes) as free
        from dba_free_space group by tablespace_name,file_id) a,
(select tablespace_name,file_id,sum(bytes) as total,maxbytes
        from dba_data_files
        group by tablespace_name,file_id,maxbytes) b
where a.file_id = b.file_id
order by file_id"""
    cursor.execute(selectSql)
    results = []
    emp_title_list = []

    for desc in cursor.description:
        emp_title_list.append(desc[0])
    results.append(emp_title_list)

    result = cursor.fetchall()
    results.append(result)

    cursor.close()
    conn.close()

    return results

"""获取网页内容函数"""
def render(tplPath,**kwargs):
    path,fileName = os.path.split(tplPath)
    template = Environment(loader=FileSystemLoader(path)).get_template(fileName)
    content = template.render(**kwargs)

    return content

def getContent():
    emp_title_list = getResults()[0]
    emp = 'emp'
    results = getResults()[1]

    return render('Test.html',**locals())

"""show web immediate"""
def showWeb():
    html = 'testJinja2.html'

    with open(html,'w') as fObj:
        fObj.write(getContent())
        fObj.close()

    webbrowser.open(html,new=1)

if __name__ == '__main__':
	showWeb()