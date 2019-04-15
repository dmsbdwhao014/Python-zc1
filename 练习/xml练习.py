from xml.etree import ElementTree as ET

# 第一种解析方式
"""
root = ET.XML(open('first.xml','r',encoding='utf-8').read())
for node in root:
    print(node,type(node))
    print(node.tag,node.attrib,node.find("gdppc").text,type(node.find("gdppc")))
"""

# 第二种解析方式
"""
tree = ET.parse('first.xml')
root = tree.getroot()
for node in root.iter("year"):
    new_year = int(node.text) + 1
    node.text = str(new_year)
    node.set('name',"cheng")
    del node.attrib['name']
tree.write("first.xml")
"""

# 第三种解析方式

# 创建XML文档
# 创建父节点
new_xml = ET.Element("namelist")
# 创建子节点
name1 = ET.SubElement(new_xml,"name",attrib={"enrollen":"yes"})
age1 = ET.SubElement(name1,"age",attrib={"checked":"no"})
sex1 = ET.SubElement(name1,"sex")
sex1.text = '33'

et = ET.ElementTree(new_xml)
et.write('test.xml',encoding='utf-8',xml_declaration=True)





