# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth
# Floor, Boston, MA 02110-1301, USA.
# 

'''
*******************************************************************
 * File:            GenSbmlGraph.py
 * Description:
 * Author:          G.V. Harsha Rani
 * E-mail:          hrani@ncbs.res.in
 ********************************************************************/

/**********************************************************************
** This program converts Genesis/SBML models reaction diagrams. 
** It draws on the 'dot' program for graphical layout of networks.
**           copyright (C) 2021 Harsha Rani
**********************************************************************/
'''

import sys,os
from subprocess import call
import matplotlib
from collections import OrderedDict
import argparse 


use_bw = False

matplotcolors = []
for name,hexno in matplotlib.colors.cnames.items():
	matplotcolors.append(name)


def countX(lst, x):
	return lst.count(x)

def unique(list1):
	output = []
	for x in list1:
		if x not in output:
			output.append(x)
	return output

def populate(startstringdigit,grp,sp,nsp):
	if grp in startstringdigit:
		startstringdigit[grp][sp] = nsp 
	else:
		startstringdigit[grp] ={sp:nsp}

def checkSpecialChar(startstringdigit,grp,sp):
	found = False
	spOrg = sp
	if sp.find('.') != -1:
		sp = sp.replace(".","_dot_")
		found = True
	if sp.find("(") != -1:
		sp = sp.replace("(","_bo_")
		found = True
	if sp.find(")") != -1:
		sp = sp.replace(")","_bc_")
		found = True
	if sp.find("_") != -1:
		sp = sp.replace(")","_un_")
		found = True
	if sp.startswith(tuple('0123456789')):
		sp = "s"+sp
		found = True
	# if spOrg != sp:
	# 	print("81 ",grp,spOrg,sp)
	if found:
		populate(startstringdigit,grp,spOrg,sp)
	
	
def checkdigitEqu(startstringdigit,grp,sp1):
	sp = sp1.name
	if grp in startstringdigit:
		grpitems = startstringdigit[grp]
		for k,v in grpitems.items():
			if k == sp:
				sp = v
	return(sp)

def getColor(gIndex,fwd_rev="forward"):
	ignorecolors= ['yellow',"chartreuse","peachpuff","paleturquoise","palegreen","olive","slategray","slategrey","lavenderblush","lemonchiffon","lightblue","lightcyan","lightgoldenrodyellow","lavender","khaki","seashell","gainsboro","burlywood","darkgrey","darkgray","palegoldenrod","linen","silver","darkkhaki","lightpink","mediumpurple","lightgreen","thistle","papayawhip","preachpuff","pink","tan","powderBlue","navajowhite","moccasin","mistyrose","lightgrey","lightgray","grey","gray","aquamarine","cadetblue","white","wheat","aqua","whitesmoke","mintcream","oldlace","black","snow","aliceblue","azure","cornsilk","beige","bisque","blanchedalmond","antiquewhite","lightyellow","lightsteelblue","ghostwhite","floralwhite","ivory","honeydew"];

	if use_bw:
		return( "black", gIndex )

	if gIndex < len(matplotcolors):
		grpcolor = matplotcolors[gIndex]
		if grpcolor in ignorecolors:#["white","wheat","aqua","whitesmoke","mintcream","oldlace","black","snow","aliceblue","azure","cornsilk","beige","bisque","blanchedalmond","antiquewhite","lightyellow","lightsteelblue","ghostwhite","floralwhite","ivory","honeydew"]:#mediumpurple","mediumvioletred","mediumseagreen"]:
			if fwd_rev == "reverse":
				gIndex = gIndex -1
			else:
				gIndex = gIndex +1

			return getColor(gIndex,fwd_rev)
		else:
			if fwd_rev == "reverse":
				gIndex = gIndex -1
			else:
				gIndex = gIndex +1
			return(grpcolor,gIndex)
	else:
		return getColor(0)

def genesis_sbmltoPng(modelpath, outputfile, ranksep = 0, hasLegend = True, fontsize = 18, showGroups = True,specific_group = [],show_blockdiagram=False):
	group_no = 0;
	groupmap = OrderedDict()
	global startstringdigit
	startstringdigit= OrderedDict()
	global groupTogroup
	groupTogroup = OrderedDict()
	global node_color
	node_color = {}
	edge_arrowsize = 1.5
	edge_weight = 1
	reac_edgelist = ""
	global dictionary_MFCRE
	dictionary_MFCRE = {}
	s = ""
	if show_blockdiagram:
		specific_group = None

	st = os.path.splitext(outputfile)
	outputfilename = st[0]
	if len( st ) > 1: 
		outputfiletype = st[1][1:]
	else:
		outputfiletype = "png"
	
	f_graph = open(outputfilename+".dot", "w")
	f_graph.write("digraph mygraph {\n\trank=TB;\ncompound=True\n")
	if ranksep > 0.0:
		f_graph.write("\tranksep={};\n".format( ranksep ))
	#f_graph.write("ratio = 1.0\n")
	#f_graph.write("ratio = \"fill\"\n")
	#f_graph.write("size = \"4,4!\"\n")
	#f_graph.write("node [shape=box, penwidth=2, height=0.01, width=0.01 ];")
	f_graph.write("node [shape=box, penwidth=2,fontsize={}];".format( fontsize ) )
	
	
	displayGroups = []
	#print("specific_group ",specific_group)
	# if specific_group == None:
	# 	displayGroups = modelpath.grpInfo
	# else:
	# 	if any(i in specific_group for i in modelpath.grpInfo):
	# 		displayGroups = specific_group
	# 	else:
	# 		displayGroups = modelpath.grpInfo
	#print('165',specific_group)		

	if specific_group == None:
		displayGroups = moose.wildcardFind(modelpath.path+"/##[TYPE=Neutral],/##[ISA=ChemCompt]")
		#print("168 ",displayGroups)
	else:
		#print("171 ")
		foundgroup = False
		fgrp = ""

		for i in specific_group:
			#print("i ",i)
			#print("i ",i,moose.wildcardFind(modelpath.path+'/##[FIELD(name)=='+i+')'))
			fgrp =  moose.wildcardFind(modelpath.path+'/##[FIELD(name)=='+i+')')
			if fgrp:
				#print(fgrp)
				foundgroup = True
				for fgrp1  in fgrp:
					displayGroups.append(fgrp1)
				#print(displayGroups)
		if not foundgroup:
			displayGroups = moose.wildcardFind('/modelpath/##[ISA=Neutral]')
		
	#print("132 ",displayGroups)
	writeSpecies(modelpath,groupmap)
	chanlist = writechan(modelpath,groupmap,f_graph,edge_arrowsize,edge_weight, displayGroups, fontsize = fontsize - 2)
	
	writeFunc(modelpath,groupmap)#,f_graph,edge_arrowsize,edge_weight, displayGroups, fontsize = fontsize - 2)
	writeReac(modelpath,groupmap)#,f_graph,edge_arrowsize,edge_weight,displayGroups,fontsize = fontsize - 2)
	
	
	writeEnz(modelpath,groupmap)#,f_graph,edge_arrowsize,edge_weight,displayGroups,fontsize = fontsize - 2)
	# print("---- ")
	# for k,v in groupTogroup.items():
	# 	for vk,vv in v.items():
	# 		print("\n",k,"\t ",vk,"\n \t ",vv)
	#print("177 dictionary_MFCRE ",dictionary_MFCRE)
	#print("178 groupmap ",groupmap)
	
	#print("----------- gr2gr ",groupTogroup)
	
	nIndex = len(matplotcolors)-1
	grp_cluster_info = {}
	#print("-----------------186")
	#print("190 ",specieslist_rec)
	for grp,items in groupmap.items():
		#print('201',displayGroups)
		if grp in displayGroups:
			#print("202 ")
			color,nIndex = getColor(nIndex)
			if show_blockdiagram or showGroups:
				s = s + "\nsubgraph cluster_"+str(group_no)+"i\n{"
				s = s+"\nsubgraph cluster_"+str(group_no)+"\n{"+"\n"+"label=\""+grp.name+"\";\npenwidth=4; margin=10.0\ncolor=\""+color+"\";\nfontsize="+str(fontsize + 2)+";\n"			

			sps = ""
			items = list(unique(items))
			#print("206 ",items)
			#print("211 ",show_blockdiagram)
			if not show_blockdiagram:
				#print("209--------",grp,items)

				for ss in items:

					#print("ss ",ss)
					ds = ""
					mooseObj = dictionary_MFCRE[ss]
					print("214 ",node_color)
					if mooseObj.className in ['Pool','BufPool']:
						color = node_color[ss]
						ds = ss+' [label=\"'+mooseObj.name+'\"color=\"'+color+'\",tooltip = \"concInit = '+str(float("{:.6f}".format(mooseObj.concInit)))+' n = '+str(float("{:.6f}".format(mooseObj.n)))+'"]'
					elif mooseObj.className in ['Reac']:
						ds = ss+' [label=< > shape=square, width=0.2, tooltip =\"'+mooseObj.name +' kf = '+str(float("{:.6f}".format(mooseObj.Kf)))+' kb = '+str(float("{:.6f}".format(mooseObj.Kb)))+'"]'
					elif mooseObj.className in ['Enz']:
						ds = ss+' [label=< > shape=circle, width=0.2, tooltip =\"'+mooseObj.name +' km = '+str(float("{:.6f}".format(mooseObj.Km)))+' kcat = '+str(float("{:.6f}".format(mooseObj.kcat)))+'"]'
					elif mooseObj.className in ['MMenz']:
						ds = ss+' [label=< > shape=doublecircle, width=0.2, tooltip =\"'+mooseObj.name +' km = '+str(float("{:.6f}".format(mooseObj.Km)))+' kcat = '+str(float("{:.6f}".format(mooseObj.kcat)))+'"]'
					elif mooseObj.className in ['ConcChan']:
						#print("224 channel")
						ds = ss+' [label=< > shape=noverhang, width=1, tooltip =\"'+mooseObj.name+'"]'
						
					elif mooseObj.className in ['Function']:
						#print("226-----------------------Function need to be added ",mooseObj.className)
						
						if ss.startswith('plus'):
							ds = ss+"[label=\"+\",shape=circle,width=0, height=0, margin=0]"
						elif ss.startswith("sigma"):
							ds = ss +"[label=<&Sigma;>,shape=circle,width=0, height=0, margin=0]"
						#print("-----------------------Function need to be added ")
					#print("ds ",ds)
					if items.index(ss) !=0:
						#print('1')
						sps = sps +'\n'+ds
					else:
						sps = sps+ds
						#print('2')
					# for spk,sp in ss.items():
					# 	print("201 ",spk.className)
					# 	if items.index(ss) != 0:
					# 		if spk.className in ["Pool","BufPool"]:
					# 			sps = sps+'\n'+sp+' [label=\"'+spk.name+'\"'+',tooltip = \"concInit = '+str(float("{:.6f}".format(spk.concInit)))+'\nn = '+str(float("{:.6f}".format(spk.n)))+'"]'
					# 		else:
					# 			sps = sps+'\n'+sp
					# 	else:
					# 		if spk.className in ["Pool","BufPool"]:
					# 			sps = sps+sp[0]+' [label=\"'+spk.name+'\"'+',tooltip = \"concInit = '+str(float("{:.6f}".format(spk.concInit)))+'\nn = '+str(float("{:.6f}".format(spk.n)))+'"]'
					# 		else:
					# 			sps = sps+'\n'+sp	
				s = s+sps+"\n"
					
			else:
				#print("264 ")
				s = s+"grp"+str(group_no)+" [shape=point style=invis] "
				grp_cluster_info[grp.name] ={"grpObj":"grp"+str(group_no),"cluster":"cluster_"+str(group_no),"color":color}


			if show_blockdiagram or showGroups:
					s = s +"\n} style=invisible\n}style=rounded"

			group_no += 1;
		else:
			#print("other group object need to show ")
			if specific_group != None:
				''' when specific group is asked to display, info of input's coming from differnt
				    Group need to identified'''
				for spg in specific_group:
					#print("groupTogroup ",groupTogroup)
					#print("292 ",spg)
					for k,v in groupTogroup.items():
						#print("v ",v,)
						moosepatharray = [ vk for vk in v.keys() if spg in moose.element(vk).name]
						if moosepatharray:
							#print(moosepatharray[0])
							#print("\t r true ",k,v.keys())
							#print("k ",k,spg)
							if k.name not in [spg]:
								# 	#print("\n 296 ",k,moosepatharray[0],v)
								# 	#print("298 ",v[moosepatharray[0]])
									for ps in v[moosepatharray[0]]:
										#print(ps)
										#str_subMol = dictionary_MFCRE[ps[0]]
										#print("str_subMol ",str_subMol)
										subgroup = [key for key,value in groupmap.items() if ps[1] in value][0]
										#print("$$$$",ps[1],subgroup)
										if subgroup.name != spg:
											ds = ""
											mooseObj = dictionary_MFCRE[ps[1]]
											if mooseObj.className in ['Pool','BufPool']:
												ds = ps[1]+' [label=\"'+mooseObj.name+'\"'+',tooltip = \"concInit = '+str(float("{:.6f}".format(mooseObj.concInit)))+' n = '+str(float("{:.6f}".format(mooseObj.n)))+'"]'
											# elif mooseObj.className in ['Reac']:
											# 	ds = ps[1]+' [label=< > shape=square, width=0.2, tooltip =\"'+mooseObj.name +' kf = '+str(float("{:.6f}".format(mooseObj.Kf)))+' kb = '+str(float("{:.6f}".format(mooseObj.Kb)))+'"]'
											# elif mooseObj.className in ['Enz']:
											# 	ds = ps[1]+' [label=< > shape=circle, width=0.2, tooltip =\"'+mooseObj.name +' km = '+str(float("{:.6f}".format(mooseObj.Km)))+' kcat = '+str(float("{:.6f}".format(mooseObj.kcat)))+'"]'
											elif mooseObj.className in ['MMenz']:
												ds = ps[1]+' [label=< > shape=doublecircle, width=0.2, tooltip =\"'+mooseObj.name +' km = '+str(float("{:.6f}".format(mooseObj.Km)))+' kcat = '+str(float("{:.6f}".format(mooseObj.kcat)))+'"]'
											elif mooseObj.className in ['ConcChan']:
												#print("224 channel")
												ds = ps[1]+' [label=< > shape=noverhang, width=1, tooltip =\"'+mooseObj.name+'"]'
												
											elif mooseObj.className in ['Function']:
												#print("226-----------------------Function need to be added ",mooseObj.className)
												
												if ss.startswith('plus'):
													ds = ps[1]+"[label=\"+\",shape=circle,width=0, height=0, margin=0]"
												elif ss.startswith("sigma"):
													ds = ps[1]+"[label=<&Sigma;>,shape=circle,width=0, height=0, margin=0]"
											f_graph.write(ds)
											
	#print("#$#$#$# ",s)
	f_graph.write(s)
	print("333",specific_group)
	if not show_blockdiagram:
		#print("---------------------------------------------------218 ")
		'''Blockdiagram is false'''
		''' group and output from group'''
		layedoutGroup = dict()
		func_edgekey = dict()
		for k,v in groupTogroup.items():
			if k in displayGroups:
				if k not in layedoutGroup:
					layedoutGroup[k]=[]
				for key,val in v.items():
					layedoutGroup[k].append(key)
					for n in val:
						if not n[0].startswith('pluse') and not n[0].startswith('sigma'):
							print("348 ",n,n[0],n[1],dictionary_MFCRE[n[0]],dictionary_MFCRE[n[1]])
							reac_edgelist,nIndex = writeReacedge(nIndex,n,reac_edgelist,edge_weight,edge_arrowsize,fontsize,groupmap,displayGroups)
						else:
							reac_edgelist,nIndex = writeFuncedge(nIndex,n,reac_edgelist,edge_weight,edge_arrowsize,fontsize)
		if specific_group != None:
			print("353")
			''' when specific group is asked to display, info of input's coming from differnt
			    Group need to identified'''
			for spg in specific_group:
				#print("groupTogroup ",groupTogroup)
				#print("292 ",spg)
				for k,v in groupTogroup.items():
					#print("v ",v,)
					moosepatharray = [ vk for vk in v.keys() if spg in moose.element(vk).name]
					if moosepatharray:
						print(moosepatharray[0],"k ",k, 'lg ',layedoutGroup)
						#print("\t r true ",k,v.keys())
						if k not in layedoutGroup:
							#print("\n 296 ",k,moosepatharray[0],v)
							#print("298 ",v[moosepatharray[0]])
							print(moosepatharray,v[moosepatharray[0]])
							for ps in v[moosepatharray[0]]:
								print("\t \t 367",ps)
								if not ps[2].startswith('pluse') and not ps[2].startswith('sigma'):
									reac_edgelist,nIndex = writeReacedge(nIndex,ps,reac_edgelist,edge_weight,edge_arrowsize,fontsize,groupmap,displayGroups)
								else:
									reac_edgelist,nIndex= writeFuncedge(nIndex,ps,reac_edgelist,rec,edge_weight,edge_arrowsize,fontsize)
					
		f_graph.write(reac_edgelist)
	else:
		''' Display Block diagram '''
		print("##")
		test1 = dict()
		for k,v in groupTogroup.items():
			test = dict()		
			for kv,l in v.items():
				for y in l:

					if k != kv:
						if kv in test:
							#print(y[2])
							if (y[2] == 'par'):
								test[kv].append("par")
							elif (y[2] == 'sub'):
								test[kv].append("input")
							elif (y[2] == 'prd'):
								test[kv].append('output')
							
						else:
							if (y[2] == 'par'):
								test[kv] = ["par"]
							elif (y[2] == 'sub'):
								test[kv] = ["input"]
							elif (y[2] == 'prd'):
								test[kv] = ['output']
							
							
						if len(test) != 0:
							test1[k] = [test]
		con_arrow={"input":"normal","output":"vee","par":"none"}
		for gk,gv in test1.items():
			#print(gk,gv)
			for vl in gv:
				for vlk,vll in vl.items():
					#print("388",vll,grp_cluster_info)
					reac_edgelist =reac_edgelist+"\n"+grp_cluster_info[gk.name]["grpObj"]+"->"+grp_cluster_info[vlk.name]["grpObj"]+"[arrowhead ="
					#print("400 ",vll)
					if len(unique(vll)) == 1:
						#print(vll)
						arrowtype = con_arrow[vll[0]]
						kg_color = grp_cluster_info[gk.name]["color"]
					else:
						arrowtype = "dot"
						kg_color = grp_cluster_info[gk.name]["color"]
						complex_exist = True
						
					reac_edgelist = reac_edgelist+str(arrowtype)+" weight = "+str(edge_weight)+ " minlen = 1 arrowsize = "+str(edge_arrowsize)+" color=\""+kg_color+"\" fontsize="+str(fontsize)+ " ltail="+grp_cluster_info[gk.name]["cluster"]+",lhead="+grp_cluster_info[vlk.name]["cluster"]+"]"
		
		f_graph.write(reac_edgelist)		
		
	if not show_blockdiagram:

		pass
		# splist = specieslist.values()
		# print("338 ")
		# for le in specieslist_rec:
		# 	le = checkdigit_mol(le)
		# 	if le.className in['Pool','BufPool']:
		# 		if le in node_color:
		# 			v = node_color[le]
		# 			f_graph.write("\n"+le.name+"[color=\""+v+"\",shape=Mrecord, width=0, height=0, margin=0.1,tooltip = \"concInit = "+str(float("{:.5f}".format(le.concInit)))+"\"]")
		# for p,q in startstringdigit.items():
		# 	print("308 ")
		# 	if p in displayGroups:
		# 		for m,n in q.items():
		# 			f_graph.write("\n"+n+"[label=\""+m+"\"]")	
	
	if hasLegend:
		start = ""
		center = ""
		end = ""
		sub_exist = True
		prd_exist = True
		par_exist = True
		f_graph.write("\nnode [shape=plaintext]\nsubgraph cluster_01 {\n\tlabel = \"Legend\";\n\t{ rank=sink;\n\tkey [label=<<table border=\"0\" cellpadding=\"2\" cellspacing=\"0\" cellborder=\"0\">\n")
		if sub_exist:
			start = start+"\t<tr><td align=\"right\" port=\"i1\">Input</td></tr>\n"
			center = center+"<tr><td port=\"i1\">&nbsp;</td></tr>\n"
			end = end+"\tkey:i1 -> key2:i1 [arrowhead=normal]\n"
		if prd_exist:
			start = start+"\t<tr><td align=\"right\" port=\"i2\">ligand-Act</td></tr>\n"
			center = center+"\t<tr><td port=\"i2\">&nbsp;</td></tr>\n"
			end = end+"\tkey:i2 -> key2:i2 [arrowhead=vee]\n"
		if par_exist:
			start = start+"\t<tr><td align=\"right\" port=\"i3\">Modifier</td></tr>\n"
			center = center+"\t<tr><td port=\"i3\">&nbsp;</td></tr>\n"
			end = end+"\tkey:i3 -> key2:i3 [arrowhead=none]\n"
		
		f_graph.write(start)
		f_graph.write("\t</table>>]\n\tkey2 [label=<<table border=\"0\" cellpadding=\"2\" cellspacing=\"0\" cellborder=\"0\">\n\t")
		f_graph.write(center)
		f_graph.write("\t</table>>]\n")
		f_graph.write(end)
		f_graph.write("\t}\n\t}")
	'''
	if hasLegend:
		start = ""
		center = ""
		end = ""
		sub_exist = True
		prd_exist = True
		par_exist = True


		f_graph.write("\nnode [shape=plaintext]\nsubgraph cluster_01 {\n\tlabel = \"Legend\";\n\t{ rank=sink;\n\tkey [label=<<table border=\"0\" cellpadding=\"2\" cellspacing=\"0\" cellborder=\"0\">\n")
		if sub_exist:
			start = start+"\t<tr><td align=\"right\" port=\"i1\">Input</td></tr>\n"
			center = center+"<tr><td port=\"i1\">&nbsp;</td></tr>\n"
			end = end+"\tkey:i1 -> key2:i1 [arrowhead=normal]\n"
		if prd_exist:
			start = start+"\t<tr><td align=\"right\" port=\"i2\">ligand-Act</td></tr>\n"
			center = center+"\t<tr><td port=\"i2\">&nbsp;</td></tr>\n"
			end = end+"\tkey:i2 -> key2:i2 [arrowhead=vee]\n"
		if par_exist:
			start = start+"\t<tr><td align=\"right\" port=\"i3\">Modifier</td></tr>\n"
			center = center+"\t<tr><td port=\"i3\">&nbsp;</td></tr>\n"
			end = end+"\tkey:i3 -> key2:i3 [arrowhead=none]\n"

		# if sub_exist:
		# 	start = start+"\t<tr><td align=\"right\" port=\"i1\">Substrate</td></tr>\n"
		# 	center = center+"<tr><td port=\"i1\">&nbsp;</td></tr>\n"
		# 	end = end+"\tkey:i1 -> key2:i1 [arrowhead=normal]\n"
		# if prd_exist:
		# 	start = start+"\t<tr><td align=\"right\" port=\"i2\">Product</td></tr>\n"
		# 	center = center+"\t<tr><td port=\"i2\">&nbsp;</td></tr>\n"
		# 	end = end+"\tkey:i2 -> key2:i2 [arrowhead=vee]\n"
		# if par_exist:
		# 	start = start+"\t<tr><td align=\"right\" port=\"i3\">Parent</td></tr>\n"
		# 	center = center+"\t<tr><td port=\"i3\">&nbsp;</td></tr>\n"
		# 	end = end+"\tkey:i3 -> key2:i3 [arrowhead=none]\n"
		print("end ",end)
		f_graph.write(start)
		f_graph.write("\t</table>>]\n\tkey2 [label=<<table border=\"0\" cellpadding=\"2\" cellspacing=\"0\" cellborder=\"0\">\n\t")
		f_graph.write(center)
		f_graph.write("\t</table>>]\n")
		f_graph.write(end)
		f_graph.write("\t}\n\t}")
	'''
	f_graph.write("\n}")
	f_graph.close()
	
	command = "dot -T"+ outputfiletype + " "+ outputfilename+".dot -o "+outputfile
	call([command], shell=True)
	print("file written ",outputfile)
	return(outputfile)
	'''
	if showGroups:
		color,nIndex = getColor(nIndex,"reverse")
		compt_no = 0
		group_no = 0
		for Cmpt in moose.wildcardFind(modelpath.path+'/##[ISA=ChemCompt]'):
			#print("cmpt ",Cmpt)
			if specific_group == None:
				s = s+"\nsubgraph cluster_"+str(compt_no)+"\n{"+"\n"+"label=\""+Cmpt.name+"\";\npenwidth=4; margin=10.0\ncolor=\""+color+"\";\nfontsize="+str(fontsize + 2)+";\n"
				sps = ""
				if Cmpt in groupmap:
					items = groupmap[Cmpt]
					
					for sp in items:
							if items.index(sp) != 0:
								if type(sp) is tuple:
									#print("111--- ",sp[1].name,moose.element(sp[1]).concInit, moose.element(sp[1]).n )

									sps = sps+'\n'+sp[0]+' [label=\"'+moose.element(sp[1]).name+'\"'+',tooltip = \"concInit = '+str(float("{:.6f}".format(moose.element(sp[1]).concInit)))+'\nn = '+str(float("{:.6f}".format(moose.element(sp[1]).n)))+'"]'
								else:
									sps = sps+'\n'+sp
							else:
								if type(sp) is tuple:
									sps = sps+sp[0]+' [label=\"'+moose.element(sp[1]).name+'\"'+',tooltip = \"concInit = '+str(float("{:.6f}".format(moose.element(sp[1]).concInit)))+'\nn = '+str(float("{:.6f}".format(moose.element(sp[1]).n)))+'"]'
								else:
									sps = sps+'\n'+sp	
					s = s+sps
					compt_no += 1;
			for grp in moose.wildcardFind(Cmpt.path+'/##[TYPE=Neutral]'):
				if grp in groupmap:
					s = s + "\nsubgraph cluster_"+str(group_no)+"_"+str(compt_no)+"i\n{"
					s = s+"\nsubgraph cluster_"+str(group_no)+"\n{"+"\n"+"label=\""+grp.name+"\";\npenwidth=4; margin=10.0\ncolor=\""+color+"\";\nfontsize="+str(fontsize + 2)+";\n"
					sps = ""
					#print("groupmap ",groupmap,grp)
					items = groupmap[grp]
					items = list(unique(items))
					for sp in items:
						if items.index(sp) != 0:
							if type(sp) is tuple:
								sps = sps+'\n'+sp[0]+' [label=\"'+moose.element(sp[1]).name+'\"'+',tooltip = \"concInit = '+str(float("{:.6f}".format(moose.element(sp[1]).concInit)))+'\nn = '+str(float("{:.6f}".format(moose.element(sp[1]).n)))+'"]'
							else:
								sps = sps+'\n'+sp
						else:
							if type(sp) is tuple:
								sps = sps+sp[0]+' [label=\"'+moose.element(sp[1]).name+'\"'+',tooltip = \"concInit = '+str(float("{:.6f}".format(moose.element(sp[1]).concInit)))+'\nn = '+str(float("{:.6f}".format(moose.element(sp[1]).n)))+'"]'
							else:
								sps = sps+'\n'+sp	
					s = s+sps+"\n} style=invisible\n}"
					group_no += 1;
			if specific_group == None:
				s = s +"\n}"
	f_graph.write(s)
	f_graph.write(chanlist)
	f_graph.write(funclist)
	f_graph.write(reaclist)
	f_graph.write(enzlist)
	
	nodeIndex = 0
	for k,uu in groupmap.items():
		#print("s ",k)
		if k in displayGroups:
			
			for vl in uu:
				if type(vl) is tuple:
					l = vl[0]
					if l in node_color:
						v = node_color[l]
						v,nodeIndex = getColor(nodeIndex)
						ii = modelpath.path+'/##[FIELD(name)='+l+']'
						# for ll in moose.wildcardFind(ii):
						# 	if(len(ll.neighbors['nOut']) == 0  and  len(ll.neighbors['reacDest']) == 0):
						# 		#print("pools not connected to any obj ",ll)
						# 		pass
						# 	else:
						# 		f_graph.write("\n"+l+"[color=\""+v+"\"]")
						f_graph.write("\n"+l+"[color=\""+v+"\"]")
	for p,q in startstringdigit.items():
		if p in displayGroups:
			for m,n in q.items():
				pass #print("n",n,m)
				#f_graph.write("\n"+n+"[label=\""+m+"\"]")	
	
	if hasLegend:
		
		f_graph.write("\nnode [shape=plaintext]\nsubgraph cluster_01 {\n\tlabel = \"Legend\";\n\t{ rank=sink;\n\tkey [label=<<table border=\"0\" cellpadding=\"2\" cellspacing=\"0\" cellborder=\"0\">\n\t\
			<tr><td align=\"right\" port=\"i1\">Input/Output</td></tr>\
			<tr><td align=\"right\" port=\"i4\">Enzyme parent </td></tr>\
			\n")
		
		f_graph.write("\t</table>>]\n\tkey2 [label=<<table border=\"0\" cellpadding=\"2\" cellspacing=\"0\" cellborder=\"0\">\
			\n\t<tr><td port=\"i1\">&nbsp;</td></tr>\
			<tr><td port=\"i4\">&nbsp;</td></tr>\n")
		
		f_graph.write("\t</table>>]\n\tkey:i1:e -> key2:i1:w [arrowhead=normal  color=\"black:black\" style=bold]\
								   \n\tkey:i4:e -> key2:i4:w [arrowhead=none color=\"black:black\" style=bold]\
								   \n")

		
		f_graph.write("\t}\n\t}")

	f_graph.write("\n}")
	f_graph.close()
	
	command = "dot -T"+ outputfiletype + " "+ outputfilename+".dot -o "+outputfile
	call([command], shell=True)
'''
				  
def writeFuncedge(nIndex,ps,reac_edgelist,edge_weight,edge_arrowsize,fontsize):
	color,nIndex = getColor(nIndex)
	#pscolor = checkdigit_mol(ps[0])
	reaction_color = node_color[ps[1]]
	arrowtype = "vee"
	
	#ps0 = checkdigit_mol(ps[0])
	#ps1 = checkdigit_mol(ps[1])
	#plusesize = "pluse"+str(equ_p_s)
	# if ps[2].startswith('plus'):
	# 	reac_edgelist = reac_edgelist+"\n"+ps[0]+"[label=\"+\",shape=circle,width=0, height=0, margin=0]"
	# elif ps[2].startswith("sigma"):
	# 	reac_edgelist = reac_edgelist+"\n"+ps[0]+"[label=<&Sigma;>,shape=circle,width=0, height=0, margin=0]"
	#print("ps0 ",ps0)
	#print('2 ',ps[2])
	if ps[2] == 'input':
		reac_edgelist =reac_edgelist+"\n"+ps[1]+"->"+ps[0]+"[arrowhead ="+str(arrowtype)+" weight = "+str(edge_weight)+ " minlen = 1 arrowsize = "+str(edge_arrowsize)+" color=\""+reaction_color+"\" fontsize="+str(fontsize)
	if ps[2] == 'output':
		reac_edgelist =reac_edgelist+"\n"+ps[0]+"->"+ps[1]+"[arrowhead ="+str(arrowtype)+" weight = "+str(edge_weight)+ " minlen = 1 arrowsize = "+str(edge_arrowsize)+" color=\""+reaction_color+"\" fontsize="+str(fontsize)
	# if ps[0] not in specieslist_rec:
	# 	specieslist_rec.append(ps0)
	# if ps[1] not in specieslist_rec:
	# 	specieslist_rec.append(ps1)
	if ps[3] != 1:
		reac_edgelist =reac_edgelist+" label=\""+str(ps[3])+"\"]"
	else:
		reac_edgelist =reac_edgelist+"]"
	# if ps[2] not in func_edgekey.keys():
	# 	func_edgekey[ps[2]]=[ps1]
	# 	reac_edgelist = reac_edgelist+"\n"+ps[2]+"->"+ps1.name+"[arrowhead ="+str(arrowtype)+" weight = "+str(edge_weight)+ " arrowsize = "+str(edge_arrowsize)+"]"
	
	return reac_edgelist,nIndex	
def writeReacedge(nIndex,ps,reac_edgelist,edge_weight,edge_arrowsize,fontsize,groupmap,displayGroups):
	# print("------------------------------ slr")
	# print
	# pscolor = checkdigit_mol(ps[0])
	# ps0 = checkdigit_mol(ps[0])
	# ps1 = checkdigit_mol(ps[1])
	# value = groupmap[findGroup_compt(ps0)]
	# for ii in value:
	# 	for k,v in ii.items():
	# 		if k == ps0:
	# 			ps0name = v
	# value1 = groupmap[findGroup_compt(ps1)]
	# for ii in value1:
	# 	for k,v in ii.items():
	# 		if k == ps1:
	# 			ps1name = v

	# if ps0.className == "Reac":
	# 	reac_edgelist =reac_edgelist+"\n"+ps[0]+"[label=<" "> shape=square,width=0.2, tooltip =\""+ ps0.name+" kf = "+str(float("{:.2f}".format(ps0.getField('Kf'))))+"kb = "+str(float("{:.2f}".format(ps0.getField('Kb'))))+"\"]"
	# elif ps0.className == "Enz":
	# 	reac_edgelist =reac_edgelist+"\n"+ps[0]+"[label=<" "> shape=circle,width=0.2, tooltip =\""+ ps0.name+" km = "+str(float("{:.2f}".format(ps0.getField('Km'))))+"kcat = "+str(float("{:.2f}".format(ps0.getField('kcat'))))+"\"]"
	# elif ps0.className == "MMenz": 
	# 	reac_edgelist =reac_edgelist+"\n"+ps[0]+"[label=<" "> shape=oval,width=0.2, tooltip =\""+ ps0.name+" km = "+str(float("{:.2f}".format(ps0.getField('Km'))))+"kcat = "+str(float("{:.2f}".format(ps0.getField('kcat'))))+"\"]"
	reaction_color = node_color[ps[1]]
	#print("609 ",ps)
	
	end = False
	mooseObj = dictionary_MFCRE[ps[0]]
	#print("612",mooseObj)
	
	subgroup = [key for key,value in groupmap.items() if ps[0] in value][0]
	if mooseObj.className in ['Reac'] and subgroup in displayGroups:
		reac_edgelist = reac_edgelist + '\n'+ps[0]+' [label=< > shape=square width=0.1, tooltip =\"'+mooseObj.name +' kf = '+str(float("{:.6f}".format(mooseObj.Kf)))+' kb = '+str(float("{:.6f}".format(mooseObj.Kb)))+'"]'
	elif mooseObj.className in ['Enz'] and subgroup in displayGroups:
		reac_edgelist = reac_edgelist + '\n'+ ps[0]+' [label=< > shape=circle, width=0.1, tooltip =\"'+mooseObj.name +' km = '+str(float("{:.6f}".format(mooseObj.Km)))+' kcat = '+str(float("{:.6f}".format(mooseObj.kcat)))+'"]'
	#print("617 ",reac_edgelist)
	
	if ps[0] == 'mol232' and ps[1] == 'Enz111':
		exit()
	if ps[2] == 'sub':
		subgroup = [key for key,value in groupmap.items() if ps[0] in value][0]
		print("687 ",ps[0],"1", dictionary_MFCRE[ps[0]],"@",subgroup,"@@",displayGroups)
	
		if subgroup in displayGroups:
			arrowtype = "normal"
			reac_edgelist =reac_edgelist+"\n"+ps[1]+"->"+ps[0]+"[arrowhead ="+str(arrowtype)+" weight = "+str(edge_weight)+ " minlen = 1 arrowsize = "+str(edge_arrowsize)+" color=\""+reaction_color+"\" fontsize="+str(fontsize)
			end = True
		
			if ps[3] != 1:
				print('716')
				reac_edgelist =reac_edgelist+" label=\""+str(ps[3])+"\"]"
			else:
				reac_edgelist =reac_edgelist+"]"
				print('719',reac_edgelist)
				
	elif ps[2] == 'prd':
		if subgroup in displayGroups:
			arrowtype = "vee"
			reac_edgelist =reac_edgelist+"\n"+ps[0]+"->"+ps[1]+"[arrowhead ="+str(arrowtype)+" weight = "+str(edge_weight)+ " minlen = 1 arrowsize = "+str(edge_arrowsize)+" color=\""+reaction_color+"\" fontsize="+str(fontsize)
			end = True
			if ps[3] != 1:
				print('716')
				reac_edgelist =reac_edgelist+" label=\""+str(ps[3])+"\"]"
			else:
				reac_edgelist =reac_edgelist+"]"
				print('719',reac_edgelist)
			
	elif ps[2] == 'par':
		arrowtype = "none"
		# reaction_color = "black"
		# if ps1.name == ps0name:
		# 	print("here some thing is wrong ",ps0name,ps1name)
		subgroup = [key for key,value in groupmap.items() if ps[0] in value][0]
		print("687 ",ps[0],"1", dictionary_MFCRE[ps[0]],"@",subgroup,"@@",displayGroups)
		
		reac_edgelist =reac_edgelist+"\n"+ps[1]+"->"+ps[0]+"[arrowhead ="+str(arrowtype)+" weight = "+str(edge_weight)+ " minlen = 1 arrowsize = "+str(edge_arrowsize)+" color=\""+reaction_color+"\" fontsize="+str(fontsize)+']'
	print("end ",end)
			
	# #print("ps0 ",ps0,ps1)
	# reaction_color = node_color[ps1]
	# if ps[2] == 'sub':
	# 	arrowtype = 'normal'
	# 	#print("ps0 ",ps0)
	# 	if ps0.className == "Reac":
	# 		reac_edgelist =reac_edgelist+"\n"+ps0.name+"[label=<" "> shape=square,width=0.2, tooltip =\""+ ps0.name+" kf = "+str(float("{:.2f}".format(ps0.getField('Kf'))))+"kb = "+str(float("{:.2f}".format(ps0.getField('Kb'))))+"\"]"
	# 	else:
	# 		print("sub-enz ",ps0)
	# 		if ps0.className == "Enz":
	# 			reac_edgelist =reac_edgelist+"\n"+ps0.name+"[label=<" "> shape=oval,width=0.25]"
	# 		else:
	# 			reac_edgelist =reac_edgelist+"\n"+ps0.name+"[label=<" "> shape=doublecircle,width=0.25]"
	# 			#reac_edgelist =reac_edgelist+"\n"+ps0.name+"[label=<" "> shape=square,width=0.25]:sw" 


	# 	reac_edgelist =reac_edgelist+"\n"+ps1.name+"->"+ps0.name+"[arrowhead ="+str(arrowtype)+" weight = "+str(edge_weight)+ " minlen = 1 arrowsize = "+str(edge_arrowsize)+" color=\""+reaction_color+"\" fontsize="+str(fontsize)
	# elif ps[2] == 'prd':
	# 	arrowtype = 'vee'
	# 	# if ps0.className == "Reac":
	# 	# 	reac_edgelist =reac_edgelist+"\n"+ps0.name+"[label=<" "> shape=square,width=0.2, tooltip = \" kf = "+str(float("{:.2f}".format(ps0.getField('Kf'))))+"kb = "+str(float("{:.2f}".format(ps0.getField('Kb'))))+"\""
	# 	# else:
	# 	# 	#reac_edgelist =reac_edgelist+"\n"+ps0.name+"[label=<" "> shape=square,width=0.2]"
	# 	reac_edgelist =reac_edgelist+"\n"+ps0.name+"->"+ps1.name+"[arrowhead ="+str(arrowtype)+" weight = "+str(edge_weight)+ " minlen = 1 arrowsize = "+str(edge_arrowsize)+" color=\""+reaction_color+"\" fontsize="+str(fontsize)
	# elif ps[2] == 'par':
	# 	arrowtype = 'none'
	# 	reaction_color = "black"		
	# 	reac_edgelist =reac_edgelist+"\n"+ps1.name+"->"+ps0.name+"[arrowhead ="+str(arrowtype)+" weight = "+str(edge_weight)+ " minlen = 1 arrowsize = "+str(edge_arrowsize)+" color=\""+reaction_color+"\" fontsize="+str(fontsize)+"]"
	
	# if ps[0] not in specieslist_rec:
	# 	specieslist_rec.append(ps0)
	# if ps[1] not in specieslist_rec:
	# 	specieslist_rec.append(ps1)
	# print("!! 502 ",ps[2])
	# if ps[2] in ['sub','prd']:
	# 	if ps[3] != 1:
	# 		reac_edgelist =reac_edgelist+" label=\""+str(ps[3])+"#\"]"
	# 	else:
	# 		reac_edgelist =reac_edgelist+"]"
	return reac_edgelist,nIndex

def mooseIsInstance(melement, classNames):
	return moose.element(melement).className in classNames

def checkdigit_mol(sp):
	#print(sp)
	if sp.name.startswith(tuple('0123456789')):
		sp = "s"+sp.name
	
	return sp

def checkdigit(startstringdigit,grp,sp):
	if sp.startswith(tuple('0123456789')):
		if grp in startstringdigit:
			startstringdigit[grp][sp] = "s"+sp
		else:
			startstringdigit[grp] ={sp:"s"+sp}

def findGroup_compt(melement):
	while not (mooseIsInstance(melement, ["Neutral","CubeMesh", "CyclMesh"])):
		melement = melement.parent
	return melement

def writeSpecies(modelpath,groupmap):
	# getting all the species
	mIndex = 0
	numMol = 0 
	for mol in ( moose.wildcardFind(modelpath.path+'/##[ISA=PoolBase]') ):
		molname = mol.name
		molsize = "mol"+str(numMol)
		numMol+=1
		
		if (mol.parent).className != 'Enz':
			molgrp = findGroup_compt(mol)
			dictionary_MFCRE[molsize] = mol
			if molsize not in node_color:
				spe_color,mIndex = getColor(mIndex)
				node_color[molsize] = spe_color
			if molgrp in groupmap:
				groupmap[molgrp].append(molsize)
			else:
				groupmap[molgrp] = [molsize]
	
def writeFunc(modelpath,groupmap):#,funclist):#,f_graph,edge_arrowsize,edge_weight,displayGroups, fontsize = 16):
	equation_pluse = 0
	funcno = 0
	for t in moose.wildcardFind(modelpath.path+'/##[ISA=Function]'):
		tgrp = findGroup_compt(t)
		tname_no = t.name+str(funcno)
		funcno = funcno+1
		allpluse = True
		tt = moose.element(t.path)
		plusesize = 'sigma'+str(equation_pluse)
		equation_pluse+=1
		if tgrp in groupmap:
			groupmap[tgrp].append(plusesize)
		else:
			groupmap[tgrp] = [plusesize]
		dictionary_MFCRE[plusesize]=tt
		inputlist = moose.element(tt.path+'/x').neighbors['input']
		print("inputlist ",inputlist)
		for tsubs in unique(moose.element(tt.path+'/x').neighbors['input']):
			c = countX(inputlist,tsubs)
			print("tsub ",tsubs,c)
			#c = 1
			# print("657 ",tsubs)
			# for k,v in groupmap.items():
			# 	print( k,v)
			# exit()
			#print("tsubs ",tsubs)
			
			str_func = [key for key,value in dictionary_MFCRE.items() if moose.element(tsubs) == value][0]
			#print("str_subMol ",str_enzparent)
			#print("682 ",str_func)
			subgroup = [key for key,value in groupmap.items() if str_func in value][0]
			
			#str_tsubs = [key for key,value in groupmap.items() if moose.element(tsubs) in value][0] 
			#subgroup = [key for key,value in groupmap.items() if moose.element(tsubs) in value][0]
			if subgroup not in groupTogroup:
				groupTogroup[subgroup] = {tgrp:[((plusesize,str_func,"input",c))]}
			else:

				if tgrp in groupTogroup[subgroup].keys():
					groupTogroup[subgroup][tgrp].append(((plusesize,str_func,"input",c)))
				else:
					groupTogroup[subgroup].update({tgrp:[((plusesize,str_func,"input",c))]})
		
		for oo in t.neighbors['valueOut']:
			str_Ofunc = [key for key,value in dictionary_MFCRE.items() if moose.element(oo) == value][0]
			#print("str_subMol ",str_enzparent)
			subgroup = [key for key,value in groupmap.items() if str_Ofunc in value][0]
			if subgroup not in groupTogroup:
				groupTogroup[subgroup] = {tgrp:[((plusesize,str_Ofunc,"output",c))]}
			else:

				if tgrp in groupTogroup[subgroup].keys():
					groupTogroup[subgroup][tgrp].append(((plusesize,str_Ofunc,"output",c)))
				else:
					groupTogroup[subgroup].update({tgrp:[((plusesize,str_Ofunc,"output",c))]})
		
			
	
def writechan(modelpath,groupmap,f_graph,edge_arrowsize,edge_weight,displayGroups,fontsize = 16):
	chanlist = ""
	chan_color_list =[]
	sIndex = 0
	pIndex = 0 
	numchan = 0
	for chan in moose.wildcardFind( modelpath.path+'/##[ISA=ConcChan]'):
		#print("chan here 719",chan.className)
		changrp = findGroup_compt(chan)
		chansize = "chan"+str(numchan)
		numchan+=1
		if changrp in groupmap:
			groupmap[changrp].append(chansize)
		else:
			groupmap[changrp] = [chansize]
		
		dictionary_MFCRE[chansize]=chan

		str_chanparent = [key for key,value in dictionary_MFCRE.items() if moose.element(chan.parent) == value][0]
		subgroup = [key for key,value in groupmap.items() if str_chanparent in value][0]
			
		if subgroup not in groupTogroup:
				groupTogroup[subgroup] = {changrp:[((chansize,str_chanparent,'par',1))]}
		else:
			if changrp in groupTogroup[subgroup].keys():
				groupTogroup[subgroup][changrp].append(((chansize,str_chanparent,'par',1)))
			else:
				''' under subgroup, reac.grp exist then update the connect to the same list
					A :{A:((list of values),( list of values))}
				'''
				groupTogroup[subgroup].update({changrp:[((chansize,str_chanparent,'par',1))]})

		for chsubs in unique(moose.element(chan).neighbors['inPoolOut']):
			c = 1
			str_chan = [key for key,value in dictionary_MFCRE.items() if moose.element(chsubs) == value][0]
			subgroup = [key for key,value in groupmap.items() if str_chan in value][0]

			if subgroup not in groupTogroup:
				groupTogroup[subgroup] = {changrp:[((chansize,str_chan,"sub",c))]}
			else:

				if changrp in groupTogroup[subgroup].keys():
					groupTogroup[subgroup][changrp].append(((chansize,str_chan,"sub",c)))
				else:
					groupTogroup[subgroup].update({changrp:[((chansize,str_chan,"sub",c))]})
		for chprd in unique(moose.element(chan).neighbors['outPoolOut']):
			c = 1
			str_chan = [key for key,value in dictionary_MFCRE.items() if moose.element(chprd) == value][0]
			subgroup = [key for key,value in groupmap.items() if str_chan in value][0]

			if subgroup not in groupTogroup:
				groupTogroup[subgroup] = {changrp:[((chansize,str_chan,"prd",c))]}
			else:

				if changrp in groupTogroup[subgroup].keys():
					groupTogroup[subgroup][changrp].append(((chansize,str_chan,"prd",c)))
				else:
					groupTogroup[subgroup].update({tgrp:[((chansize,str_chan,"prd",c))]})
		
		'''
		for oo in t.neighbors['valueOut']:
			str_Ofunc = [key for key,value in dictionary_MFCRE.items() if moose.element(oo) == value][0]
			#print("str_subMol ",str_enzparent)
			subgroup = [key for key,value in groupmap.items() if str_Ofunc in value][0]
			print("689line ",str_Ofunc,subgroup)
			if subgroup not in groupTogroup:
				groupTogroup[subgroup] = {tgrp:[((plusesize,str_Ofunc,"output",c))]}
			else:

				if tgrp in groupTogroup[subgroup].keys():
					groupTogroup[subgroup][tgrp].append(((plusesize,str_Ofunc,"output",c)))
				else:
					groupTogroup[subgroup].update({tgrp:[((plusesize,str_Ofunc,"output",c))]})
		'''
		# groupmap[changrp].append(chansize)
		# for oo in groupmap[parChan.parent]:
		# 		#print(" k, l ",oo)
		# 		if type(oo) is tuple:
		# 			if oo[1] == moose.element(parChan):
		# 				parchan1 = oo[0]
		# 		chanlist = chanlist+"\n"+chansize+"[label=<> shape=restrictionsite]"
		# chanlist = chanlist+"\n"+parchan1+"->"+chansize+"[arrowhead=none]"
		# inputChan = chan.neighbors['inPoolOut']
		# for oo in groupmap[moose.element(inputChan[0]).parent]:
		# 		if type(oo) is tuple:
		# 			if oo[1] == moose.element(inputChan[0]):
		# 				inpchan1 = oo[0]
		
		# chanlist = chanlist +"\n"+inpchan1+"->"+chansize+"[arrowhead=normal weight = "+str(edge_weight)+ " arrowsize = "+str(edge_arrowsize)+ " style=bold]"
		# outputChan = chan.neighbors['outPoolOut']
		# for oo in groupmap[moose.element(outputChan[0]).parent]:
		# 		if type(oo) is tuple:
		# 			if oo[1] == moose.element(outputChan[0]):
		# 				outchan1 = oo[0]
		
		# chanlist = chanlist +"\n"+chansize+"->"+outchan1+"[arrowhead=normal weight = "+str(edge_weight)+ " arrowsize = "+str(edge_arrowsize)+ " style=bold]"
		
	return(chanlist)
	
def writeEnz(modelpath,groupmap):#,f_graph,edge_arrowsize,edge_weight,displayGroups,fontsize = 16):
	edgelist1 = ""
	enzyme_color_list =[]
	sIndex = 0
	pIndex = 0 
	numenz = 0
	for enz in moose.wildcardFind( modelpath.path+'/##[ISA=EnzBase]'):
		enzgrp = findGroup_compt(enz)
		enzname = enz.name
		sublist = enz.neighbors['sub']
		sublistU = unique(enz.neighbors['sub'])
		prdlist = enz.neighbors['prd']
		prdlistU = unique(enz.neighbors['prd'])
		enzsize = "Enz"+str(numenz)
		numenz+=1
		dictionary_MFCRE[enzsize] = enz
		#print("enz ",enz,enzgrp.name)
		if enzgrp in groupmap:
			groupmap[enzgrp].append(enzsize)
		else:
			groupmap[enzgrp] = [enzsize]

		# for k,v in groupmap.items():
		# 		print(k,"v",v)
		# 		for vv in v:
		# 			for key,value in vv.items():
		# 				if moose.element(enz.parent) == key:
		# 					subgroup = k
		# 					break
						
		#subgroup = [key for key,value in groupmap.items() if enz.parent in value][0]
		str_enzparent = [key for key,value in dictionary_MFCRE.items() if moose.element(enz.parent) == value][0]
		#print("str_subMol ",str_enzparent)
		subgroup = [key for key,value in groupmap.items() if str_enzparent in value][0]
		#print("subgroup ",subgroup)
			
		if subgroup not in groupTogroup:
				groupTogroup[subgroup] = {enzgrp:[((enzsize,str_enzparent,'par',1))]}
		else:
			'''  
				A: {A:((list of values)())
					B : ((list of values))
					}
			'''
			if enzgrp in groupTogroup[subgroup].keys():
				groupTogroup[subgroup][enzgrp].append(((enzsize,str_enzparent,'par',1)))
			else:
				''' under subgroup, reac.grp exist then update the connect to the same list
					A :{A:((list of values),( list of values))}
				'''
				groupTogroup[subgroup].update({enzgrp:[((enzsize,str_enzparent,'par',1))]})

		for sub in unique(enz.neighbors['sub']):
		# 	for k,v in groupmap.items():
		# 		print(k,"v",v)
		# 		for vv in v:
		# 			for key,value in vv.items():
		# 				if moose.element(sub) == key:
		# 					subgroup = k
		# 					break
				
			#subgroup = [key for key,value in groupmap.items() if moose.element(sub) in value][0]
			# if reac.grp in startstringdigit:
			# 	t = startstringdigit[reac.grp]
			# 	if newsub in t:
			# 		newsub = t[newsub]
			''' if string starting with number, then replace with s+string'''
			# if moose.element(sub) in node_color:
			# 	reaction_color = node_color[moose.element(sub)]
			# else:
			# 	reaction_color,sIndex = getColor(sIndex)
			# 	node_color[moose.element(sub)] = reaction_color
			# #checkdigit(startstringdigit,reac.grp,sub)
			c = countX(sublist,sub)
			#sub = checkdigitEqu(startstringdigit,reac.grp,sub)
			ctype = 'sub'
			'''Creating dictionary with
				key : {key:((value)(value))
					   }
				A : {A :((list of values )(list of values))
					 B : ((list of values))
					}
			'''
			str_subMol = [key for key,value in dictionary_MFCRE.items() if moose.element(sub) == value][0]
			#print("str_subMol ",str_subMol)
			subgroup = [key for key,value in groupmap.items() if str_subMol in value][0]
			#print("subgroup ",subgroup)
			
			if subgroup not in groupTogroup:
				groupTogroup[subgroup] = {enzgrp:[((enzsize,str_subMol,ctype,c))]}
			else:
				'''  
					A: {A:((list of values)())
						B : ((list of values))
						}
				'''
				if enzgrp in groupTogroup[subgroup].keys():
					groupTogroup[subgroup][enzgrp].append(((enzsize,str_subMol,ctype,c)))
				else:
					''' under subgroup, reac.grp exist then update the connect to the same list
						A :{A:((list of values),( list of values))}
					'''
					groupTogroup[subgroup].update({enzgrp:[((enzsize,str_subMol,ctype,c))]})

		for prd in unique(enz.neighbors['prd']):
		# 	for k,v in groupmap.items():
		# 		print(k,"v",v)
		# 		for vv in v:
		# 			for key,value in vv.items():
		# 				if moose.element(prd) == key:
		# 					subgroup = k
		# 					break
			
			#subgroup = [key for key,value in groupmap.items() if moose.element(prd) in value][0]
		
			# if reac.grp in startstringdigit:
			# 	t = startstringdigit[reac.grp]
			# 	if newsub in t:
			# 		newsub = t[newsub]
			''' if string starting with number, then replace with s+string'''
			# if moose.element(prd) in node_color:
			# 	reaction_color = node_color[moose.element(prd)]
			# else:
			# 	reaction_color,sIndex = getColor(sIndex)
			# 	node_color[moose.element(prd)] = reaction_color
			#checkdigit(startstringdigit,reac.grp,sub)
			c = countX(prdlist,prd)
			#sub = checkdigitEqu(startstringdigit,reac.grp,sub)
			ctype = 'prd'
			'''Creating dictionary with
				key : {key:((value)(value))
					   }
				A : {A :((list of values )(list of values))
					 B : ((list of values))
					}
			'''
			str_prdMol = [key for key,value in dictionary_MFCRE.items() if moose.element(prd) == value][0]
			#print("str_subMol ",str_prdMol)
			subgroup = [key for key,value in groupmap.items() if str_prdMol in value][0]
			#print("subgroup ",subgroup)
			
			if subgroup not in groupTogroup:
				groupTogroup[subgroup] = {enzgrp:[((enzsize,str_prdMol,ctype,c))]}		
			else:
				'''  
					A: {A:((list of values)())
						B : ((list of values))
						}
				'''
				if enzgrp in groupTogroup[subgroup].keys():
					groupTogroup[subgroup][enzgrp].append(((enzsize,str_prdMol,ctype,c)))
				else:
					''' under subgroup, reac.grp exist then update the connect to the same list
						A :{A:((list of values),( list of values))}
					'''
					groupTogroup[subgroup].update({enzgrp:[((enzsize,str_prdMol,ctype,c))]})
	
def writeReac(modelpath,groupmap):
	edgelist1 = ""
	reaction_color_list =[]
	sIndex = 0
	pIndex = 0 
	numReac = 0

	for reac in moose.wildcardFind(modelpath.path+'/##[ISA=Reac]'):
		reacgrp = findGroup_compt(reac)
		reacname = reac.name
		sublist = reac.neighbors['sub']
		sublistU = unique(reac.neighbors['sub'])
		prdlist = reac.neighbors['prd']
		prdlistU = unique(reac.neighbors['prd'])
		reacsize = "Reac"+str(numReac)
		numReac+=1
		dictionary_MFCRE[reacsize] = reac
		if reacgrp in groupmap:
			groupmap[reacgrp].append(reacsize)
		else:
			groupmap[reacgrp] = [reacsize]

		for sub in unique(reac.neighbors['sub']):
			# for k,v in groupmap.items():
			# 	print(k,"v",v)
			# 	for vv in v:
			# 		for key,value in vv.items():
			# 			if moose.element(sub) == key:
			# 				subgroup = k
			# 				break
			
			#subgroup = [key for key,value in groupmap.items() if moose.element(sub) in value][0]
			# if reac.grp in startstringdigit:
			# 	t = startstringdigit[reac.grp]
			# 	if newsub in t:
			# 		newsub = t[newsub]
			''' if string starting with number, then replace with s+string'''
			# if moose.element(sub) in node_color:
			# 	reaction_color = node_color[moose.element(sub)]
			# else:
			# 	reaction_color,sIndex = getColor(sIndex)
			# 	node_color[moose.element(sub)] = reaction_color
			#checkdigit(startstringdigit,reac.grp,sub)
			c = countX(sublist,sub)
			#sub = checkdigitEqu(startstringdigit,reac.grp,sub)
			ctype = 'sub'
			'''Creating dictionary with
				key : {key:((value)(value))
					   }
				A : {A :((list of values )(list of values))
					 B : ((list of values))
					}
			'''
			str_subMol = [key for key,value in dictionary_MFCRE.items() if moose.element(sub) == value][0]
			#print("str_subMol ",str_subMol)
			subgroup = [key for key,value in groupmap.items() if str_subMol in value][0]
			#print("subgroup ",subgroup)
			if subgroup not in groupTogroup:
				groupTogroup[subgroup] = {reacgrp:[((reacsize,str_subMol,ctype,c))]}
			else:
				'''  
					A: {A:((list of values)())
						B : ((list of values))
						}
				'''
				if reacgrp in groupTogroup[subgroup].keys():
					groupTogroup[subgroup][reacgrp].append(((reacsize,str_subMol,ctype,c)))
				else:
					''' under subgroup, reac.grp exist then update the connect to the same list
						A :{A:((list of values),( list of values))}
					'''
					groupTogroup[subgroup].update({reacgrp:[((reacsize,str_subMol,ctype,c))]})

		for prd in unique(reac.neighbors['prd']):
			# for k,v in groupmap.items():
			# 	print("b ",v)
			# 	for vi in v:
			# 		print(vi)
			# 		if len(vi) > 1:
			# 			if moose.element(prd) == vi[0]:
			# 				subgroup = k
			# 				break
			#subgroup = [key for key,value in groupmap.items() if moose.element(prd) in value][0]
		
			# if reac.grp in startstringdigit:
			# 	t = startstringdigit[reac.grp]
			# 	if newsub in t:
			# 		newsub = t[newsub]
			''' if string starting with number, then replace with s+string'''
			# if moose.element(prd) in node_color:
			# 	reaction_color = node_color[moose.element(prd)]
			# else:
			# 	reaction_color,sIndex = getColor(sIndex)
			# 	node_color[moose.element(prd)] = reaction_color
			#checkdigit(startstringdigit,reac.grp,sub)
			c = countX(prdlist,prd)
			#sub = checkdigitEqu(startstringdigit,reac.grp,sub)
			ctype = 'prd'
			'''Creating dictionary with
				key : {key:((value)(value))
					   }
				A : {A :((list of values )(list of values))
					 B : ((list of values))
					}
			'''

			str_prdMol = [key for key,value in dictionary_MFCRE.items() if moose.element(prd) == value][0]
			#print("str_prdMol ",str_prdMol)
			subgroup = [key for key,value in groupmap.items() if str_prdMol in value][0]
			#print("subgroup ",subgroup)

			if subgroup not in groupTogroup:
				groupTogroup[subgroup] = {reacgrp:[((reacsize,str_prdMol,ctype,c))]}		
			else:
				'''  
					A: {A:((list of values)())
						B : ((list of values))
						}
				'''
				if reacgrp in groupTogroup[subgroup].keys():
					groupTogroup[subgroup][reacgrp].append(((reacsize,str_prdMol,ctype,c)))
				else:
					''' under subgroup, reac.grp exist then update the connect to the same list
						A :{A:((list of values),( list of values))}
					'''
					groupTogroup[subgroup].update({reacgrp:[((reacsize,str_prdMol,ctype,c))]})

def file_choices(choices,fname,iotype):
	ext = (os.path.splitext(fname)[1][1:]).lower()
	if iotype == "outputfile":
		if ext not in choices:
			parser.error("Requires output filetype {}".format(choices))
	else:
		if ext != "xml" and ext != "g":
			parser.error("Requires Genesis or SBML file format ")
			
	return fname

if __name__ == "__main__":

	parser = argparse.ArgumentParser( description = 'This program generates a reaction diagram for a SBML/Genesis model. It converts the specified Genesis/SBML, to the dot format. The dot file is further converted to an image in png/svg format\n')
	parser.add_argument('model',type=lambda s:file_choices((".xml",".g"),s,"input"), help='Required: filename of model, in Genesis format.')
	#parser.add_argument( 'model', type = str, help='Required: filename of model, in JSON format.')
	parser.add_argument( '-o', '--output', type=lambda out:file_choices(("png","svg"),out,"outputfile"), help='Optional: writes out the png model into named file. default takes json filename')
	parser.add_argument( '-r', '--ranksep', type=float, default = 0, help='Optional: set rank separation (vertical spacing) in output.')
	parser.add_argument( '-fs', '--fontsize', type=float, default = 18, help='Optional: set font size for node labels.')
	parser.add_argument( '-nl', '--no_legend', action='store_true', help='Optional: Turns off generation of legend')
	parser.add_argument( '-ng', '--no_groups', action='store_true', help='Optional: Removes grouping. All molecules and reactions sit together.')
	parser.add_argument( '-bw', '--bw', action='store_true', help='Optional: Goes into black-and-white plotting mode')
	parser.add_argument('-sg', '--specific_group', help='Optional: Specfiy group names for display,delimited groupname seprated by comma.',type=lambda s:s.split(","))
	parser.add_argument( '-bd', '--block-diagram', action='store_true', help='Optional: Block diagram of the model with connection are retained.')
	#parser.add_argument('-bd', '--block-diagram',help='Optional: Block diagram of the model with connection are retained.')
	args = parser.parse_args()
	use_bw = args.bw

	if args.output == None:
		dirpath = os.path.dirname(args.model)
		basename = os.path.basename(args.model)
		if dirpath:
			outputfile = os.path.dirname(args.model)+"/"+os.path.splitext(os.path.basename(args.model))[0]+".png"	
		else:
			outputfile = os.path.splitext(args.model)[0]+".png"
	else:
		outputfile = args.output
	import moose
	#jsonDict = loadModel( args.model )
	#modelpath = parseModel( jsonDict )
	#modelpath = moose.loadModel(args.model,'/model')
	ext = (os.path.splitext(args.model)[1][1:]).lower()
	if ext == "xml":
		modelpath,errormsg = moose.readSBML(args.model,'/model' ,"ee")
	elif ext == "g":
		modelpath = moose.loadModel(args.model,'/model',"ee")
	else:
		print ("Input file should be genesis or SBML")
		exit()
	#print("#######",modelpath)
	genesis_sbmltoPng(modelpath, outputfile, ranksep = args.ranksep, hasLegend = not args.no_legend, fontsize = args.fontsize, showGroups = not args.no_groups,specific_group = args.specific_group,show_blockdiagram=args.block_diagram )
