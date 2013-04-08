#!/usr/bin/python

import xml.etree.ElementTree as ET

tabCnt = 1

names = []
nameCls = dict()
childs = dict()
proper = dict()
types = dict()
stack = []
toCallFromConstruct = []

def isConvToDouble(s):
	if s.isdigit():
		return True
	else:
		try:
			float(s)
			return True
		except ValueError:
			return False
	return False

def recu(r):
	#print(r.tag, " ", stack)
	t = None
	try:
		t = r.attrib["type"]
	except KeyError:
		pass

	if r.tag == "object" and t == None:
		if len(stack) > 0:
			childs[stack[-1]].append(r.attrib["id"])

		stack.append(r.attrib["id"])
		nameCls[stack[-1]] = r.attrib["class"]
		childs[r.attrib["id"]] = []
		proper[r.attrib["id"]] = []
		names.append(r.attrib["id"])
		types[r.attrib["id"]] = r.attrib["class"]

	if r.tag == "child" and t == "tab":
		global tabCnt
		na = "tab"+str(tabCnt)
		tabCnt += 1
		if len(stack) > 0:
			childs[stack[-1]].append(na)

		stack.append(na)
		childs[na] = []
		proper[na] = []
		names.append(na)

	if r.tag == "placeholder":
		pn = "placeholder"+str(tabCnt)
		names.append(pn)
		nameCls[pn] = "GtkLabel"
		proper[pn] = []
		if len(stack) > 0:
			childs[stack[-1]].append(pn)
	
	if r.tag == "property":
		proper[stack[-1]].append( (r.attrib["name"], r.text) )	

	for i in r:
		recu(i)

	if r.tag == "object" or (r.tag == "child" and t == "tab"):
		stack.pop()

def buildConstructMethods(f):
	f.write("\nprivate:\n")
	for n in names[1:]:
		if n[0:3] == "tab":
			continue
		if n[0:len("placeholder")] == "placeholder":
			continue

		if nameCls[n] == "GtkBox":
			continue

		f.write("\tinline void make_{}() {{\n".format(n))
		toCallFromConstruct.append("\t\tmake_{}();\n".format(n))
		for a in proper[n]:
			if a[0].find("pos") != -1:
				f.write("\t\t{}.set_{}({});\n".format(n, a[0], "POS_"+a[1].upper()))
			elif a[0].find("orientation") != -1:
				f.write("\t\t{}.set_{}({});\n".format(n, a[0], "ORIENTATION_"+a[1].upper()))
			elif(a[1].lower() == "true" or a[1].lower() == "false" 
					or isConvToDouble(a[1])):
				f.write("\t\t{}.set_{}({});\n".format(n, a[0], a[1].lower()))
			else:
				f.write("\t\t{}.set_{}({});\n".format(n, a[0], '"'+a[1].lower()+'"'))

		f.write("\t\t{}.show();\n".format(n))

		f.write("\t}\n\n")

def buildDataMember(f):
	f.write("protected:\n")
	for n in names[1:]:
		if n[0:3] == "tab":
			continue
		f.write("\tGtk::{} {};\n".format(nameCls[n][3:], n))

def buildBuildWidget(f):
	f.write("\nprivate:\n")
	f.write("\tinline void buildWidget() {\n")
	re = names[1:][::-1]
	for b in re:
		if b.startswith("tab"):
			continue
		elif b.startswith("placeholder"):
			continue
		for c in childs[b]:
			if c.startswith("placeholder"):
				continue
			elif nameCls[b].find("Window") != -1:
				f.write("\t\t{}.add({});\n".format(b, c))
			elif nameCls[b].find("Box") != -1:
				f.write("\t\t{}.pack_start({});\n".format(b, c))
			elif nameCls[b].find("Notebook") != -1:
				t = c[0:3]
				n = c[3:]
				f.write("\t\t{}.insert_page(placeholder{},label{},{});\n".format(b,n,n,n))
			elif nameCls[b].find("MenuItem"):
				f.write("\t\t{}.add({});\n".format(b,c))
			elif nameCls[b].find("MenuBar"):
				f.write("\t\t{}.append({});\n".format(b,c))
			elif nameCls[b].find("Menu"):
				f.write("\t\t{}.append({});\n".format(b,c))
				

	# main layout
	for c in childs[names[0]]:
		f.write("\t\tthis->add({});\n".format(c))

	f.write("\t}\n")

def buildConstructor(f,cn):
	f.write("public:\n")
	f.write("\tinline {}() {{\n".format(cn))
	for a in proper[names[0]]:
		if a[0].find("pos") != -1:
			f.write("\t\tthis->set_{}({});\n".format(a[0], "POS_"+a[1].upper()))
		elif(a[1].lower() == "true" or a[1].lower() == "false" 
				or isConvToDouble(a[1])):
			f.write("\t\tthis->set_{}({});\n".format(a[0], a[1].lower()))
		else:
			f.write("\t\tthis->set_{}({});\n".format(a[0], '"'+a[1].lower()+'"'))
		
	for i in toCallFromConstruct:
		f.write(i)

	f.write("\t\tbuildWidget();\n")
	f.write("\t\tthis->show_all();\n")
	f.write("\t}\n")

def printer(fn,cn,pc):
	f = open(fn, "w")
	f.write("#ifndef {}_HPP\n"
		"#define {}_HPP\n\n"
		"#include <gtkmm.h>\n\n"
		"using namespace Gtk;\n\n"
		"class {} : public Gtk::{} {{\n".format(cn, cn, cn, pc[3:]))
	buildDataMember(f)
	buildConstructMethods(f)
	buildConstructor(f, cn)
	buildBuildWidget(f)
	f.write("};\n\n#endif\n")


fn = "glade"

tree = ET.parse(fn+".glade")
root = tree.getroot()[0]
recu(root)

print(names)
print("\nproperites")
for i in proper:
	print(i," ",proper[i])

print("\nchilds")
for i in childs:
	print(i," ",childs[i])

printer(fn+".hpp",fn,nameCls[names[0]])