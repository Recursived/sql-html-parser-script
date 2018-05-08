#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import io
import re

see_mores = [
			'batiment.php', 'pont.php', 'square.php', 'autre.php',
			'batimentEN.php', 'pontEN.php', 'squareEN.php', 'autreEN.php'
			]

files = [
		'notredame.php', 'stChap.php', 'conciergerie.php',
		'hdieu.php', 'ccassation.php', 'palaisjustice.php',
		'P9.php', 'pstmichel.php', 'psaintlouis.php',
		'pauchange.php', 'pndame.php', 'parcole.php',
		'pparcheveque.php', 'pdauphine.php', 'plepine.php',
		'svgalant.php', 'sjeanxi.php', 'mmartyr.php',
		'carcheo.php', 'tdelhorloge.php', 'mafi.php',
		'maisonu.php', 'maisonha.php', 'shenry4.php',
		'charlemagne.php', 'JPdeux.php', 'pointzero.php'
	    ]


lst_href_to_change = []

#primary key should be the static name of the file in the db without the php

text_batiment = ""
text_pont = ""
text_square = ""
text_autre = ""

# variable that stores the type of the monuments as a string
type_monument = ""

try:

########### Part to determine the type of the monument (check with the file variable and the text string) ##########################
	with io.open("batiment.php","r") as f:
		text_batiment = f.read()
	with io.open("pont.php","r") as f:
		text_pont = f.read()
	with io.open("square.php","r") as f:
		text_square = f.read()
	with io.open("autre.php","r") as f:
		text_autre = f.read()

	print(text_batiment)

################### Parsing part############################
	with io.open('sqlinsert.txt','w', encoding="utf-8")as writer:
		for file in files:
			with io.open(file,'r', encoding="utf-8") as reader:

				# English file opening
				en_file = open(file[:-4]+"EN.php", "r")
				en_text = en_file.read()
				en_file.close()


				html_text = reader.read()
				print("\n\n\nprocessing the file "+file)
				# should get the href for image and content for p elem

				soup = BeautifulSoup(html_text,'lxml')
				soupe = BeautifulSoup(en_text,'lxml')


				#################### Conditional part to determine the type ##################
				if file in text_batiment:
					type_monument = "batiment"
				elif file in text_square:
					type_monument = "square"
				elif file in text_pont:
					type_monument = "pont"
				else:
					type_monument = "autre"
				print(file, type_monument)
				##############################################################################

				title_mon = str(soup.findAll("div",{"class":"titlem"})[0])
				title_mon = title_mon.replace('"','\\"').replace("'","\\'")

				img_thumb = str(soup.findAll("img",{"class":"img-thumbnail"})[0])
				img_thumb = img_thumb.replace('"','\\"').replace("'","\\'")

				info_mon = ",".join(list(map(lambda x: str(x) ,soup.findAll("p", {"class": "textmon"}))))
				info_mon = info_mon.replace('"','\\"').replace("'","\\'")
				titlem_en = ",".join(list(map(lambda x: str(x) ,soupe.findAll("p", {"class": "textmon"}))))
				titlem_en = titlem_en.replace('"','\\"').replace("'","\\'")

				litle_img = soup.findAll("img",{"class":"img-responsive"})[0].get("src")
				litle_img = litle_img.replace('"','\\"').replace("'","\\'")

				descr_mon = max(map(lambda x: x.get_text(),soup.findAll("p")), key=len)
				descr_mon = descr_mon.replace('"','\\"').replace("'","\\'")
				descr_en = max(map(lambda x: x.get_text(),soupe.findAll("p")), key=len)
				descr_en = descr_en.replace('"','\\"').replace("'","\\'")


				href_img = list(map(lambda x: x.find_parent().get("href"),soup.findAll("div",{"class":"lselect"})))
				href_img = list(map(lambda x: "monument_viewer.php?static="+x[:-37]+"&type="+type_monument,href_img))
				lst_href_to_change.extend(list(zip(href_img, list(map(lambda x: x.find_parent().get("href"),soup.findAll("div",{"class":"lselect"})))))) 
				href_img = ",".join(href_img)
				href_img = href_img.replace('"','\\"').replace("'","\\'")

				text_href_img = ",".join(list(map(lambda x: x.get_text(),soup.findAll("div",{"class":"selectertext"}))))
				text_href_img = text_href_img.replace('"','\\"').replace("'","\\'")

				link_img_href = ",".join(list(map(lambda x : x.get("src"), soup.findAll("img",{"class":"limgselecter"}))))
				link_img_href = link_img_href.replace('"','\\"').replace("'","\\'")

				map_href = str(soup.findAll("div",{"class":"time-container"})[1])
				map_href = map_href.replace('"','\\"').replace("'","\\'")

				wiki_link = soup.find("a").get("href")
				wiki_link = wiki_link.replace('"','\\"').replace("'","\\'")

				query = "INSERT INTO table_monu (id_monu, titre_monu, img_thumb, info_monu, little_img, descr_monu, href_selecter, text_selecter, link_selecter, ref_map_monu, type_monu, wiki_link, titlem_en, descr_en) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');\n\n".format(file[:-4], title_mon, img_thumb, info_mon, litle_img, descr_mon, href_img, text_href_img, link_img_href, map_href, type_monument, wiki_link, titlem_en, descr_en  )
				writer.write(query)

	# the previous link is the left elem of the tuple and new one is on the right
	print(lst_href_to_change)
	"""for see_more in see_mores:
		text = ''
		with open(see_more,'r') as f:
			text = f.read()
			for replacer, to_be_replaced in lst_href_to_change:
				text = text.replace(to_be_replaced, replacer+"&theme=<?php echo($_GET[theme])?>")
		with open(see_more,'w') as f:
			f.write(text)"""



except Exception as e:
	print(e)
