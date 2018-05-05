//genesis
// kkit Version 11 flat dumpfile

// Saved on 100
include kkit {argv 1}
FASTDT = 0.001
SIMDT = 0.001
CONTROLDT = 0.1
PLOTDT = 0.1
MAXTIME = 100
TRANSIENT_TIME = 2
VARIABLE_DT_FLAG = 0
DEFAULT_VOL = 1.03752137708e-15
VERSION = 11.0 
setfield /file/modpath value ~/scripts/modules
kparms

//genesis
initdump -version 3 -ignoreorphans 1
simobjdump table input output alloced step_mode stepsize x y z
simobjdump xtree path script namemode sizescale
simobjdump xcoredraw xmin xmax ymin ymax
simobjdump xtext editable
simobjdump xgraph xmin xmax ymin ymax overlay
simobjdump xplot pixflags script fg ysquish do_slope wy
simobjdump group xtree_fg_req xtree_textfg_req plotfield expanded movealone \
  link savename file version md5sum mod_save_flag x y z
simobjdump geometry size dim shape outside xtree_fg_req xtree_textfg_req x y z
simobjdump kpool DiffConst CoInit Co n nInit mwt nMin vol slave_enable \
  geomname xtree_fg_req xtree_textfg_req x y z
simobjdump kreac kf kb notes xtree_fg_req xtree_textfg_req x y z
simobjdump kenz CoComplexInit CoComplex nComplexInit nComplex vol k1 k2 k3 \
  keepconc usecomplex notes xtree_fg_req xtree_textfg_req link x y z
simobjdump stim level1 width1 delay1 level2 width2 delay2 baselevel trig_time \
  trig_mode notes xtree_fg_req xtree_textfg_req is_running x y z
simobjdump xtab input output alloced step_mode stepsize notes editfunc \
  xtree_fg_req xtree_textfg_req baselevel last_x last_y is_running x y z
simobjdump kchan perm gmax Vm is_active use_nernst notes xtree_fg_req \
  xtree_textfg_req x y z
simobjdump transport input output alloced step_mode stepsize dt delay clock \
  kf xtree_fg_req xtree_textfg_req x y z
simobjdump proto x y z
simundump geometry /kinetics/geometry 0 1.03752137708e-15 3 sphere  "" white black 4 2 0
simundump group /kinetics/mGluR 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 1 2 0
simundump group /kinetics/PI3K_activation 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 1 2 0
simundump group /kinetics/CaM 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 1 2 0
simundump group /kinetics/HomerPIKE 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 1 2 0
simundump group /kinetics/PKC 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 1 2 0
simundump group /kinetics/AKT_activation 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 1 2 0
simundump group /kinetics/PI3K_activation 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 1 2 0
simundump group /kinetics/MAPK 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 1 2 0
simundump group /kinetics/Ras 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 1 2 0
simundump kpool /kinetics/mGluR/mGluR 0 0.0 0 0 0 187443.016262 0 0 624810.054205 0 /kinetics/geometry 9 black 3736 6115 0
simundump kpool /kinetics/mGluR/Rec_Glu 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 22 black 3205 4688 0
simundump kpool /kinetics/mGluR/Glutamate 0 0.0 0 0 0 62481005.4205 0 0 624810.054205 4 /kinetics/geometry 56 black 4520 5348 0
simundump kpool /kinetics/HomerPIKE/Homer 0 0.0 0 0 0 624810.054205 0 0 624810.054205 0 /kinetics/geometry 45 black 2132 5100 0
simundump kpool /kinetics/HomerPIKE/L.mGluR_p.Homer 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 61 black 2090 3596 0
simundump kpool /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 46 black 910 2410 0
simundump kpool /kinetics/HomerPIKE/PIKE_L 0 0.0 0 0 0 624810.054205 0 0 624810.054205 0 /kinetics/geometry 52 black 1089 3774 0
simundump kpool /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L.PI3K 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 59 black -586 2200 0
simundump kpool /kinetics/PI3K_activation/PI3K 0 0.0 0 0 0 62481.0054205 0 0 624810.054205 0 /kinetics/geometry 12 black 409 909 0
simundump kpool /kinetics/PI3K_activation/PIP3 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 39 black -2468 2276 0
simundump kpool /kinetics/PI3K_activation/PTEN 0 0.0 0 0 0 168698.714635 0 0 624810.054205 0 /kinetics/geometry 63 black -2840 3899 0
simundump kpool /kinetics/PI3K_activation/PIP2 0 0.0 0 0 0 4373670.37944 0 0 624810.054205 0 /kinetics/geometry 47 black -1733 2969 0
simundump kpool /kinetics/PI3K_activation/PI3K_basal 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 52 black -1177 1475 0
simundump kpool /kinetics/MAPK/MAPK 0 0.0 0 0 0 2249316.19514 0 0 624810.054205 0 /kinetics/geometry 52 black 4486 -4144 0
simundump kpool /kinetics/AKT_activation/AKT 0 0.0 0 0 0 124962.010841 0 0 624810.054205 0 /kinetics/geometry 52 black -3906 2740 0
simundump kpool /kinetics/AKT_activation/PIP3_AKT 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 1 black -3919 1299 0
simundump kpool /kinetics/AKT_activation/PIP3_AKT_thr308 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 59 black -3922 -479 0
simundump kpool /kinetics/AKT_activation/PIP3_AKT_t308_s473 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 53 black -3050 -2075 0
simundump kpool /kinetics/AKT_activation/PIP3_PDK1 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 49 black -3490 959 0
simundump kpool /kinetics/AKT_activation/PIP3_PDK2 0 0.0 0 0 0 1874.49264571 0 0 624810.054205 0 /kinetics/geometry 25 black -4435 -1739 0
simundump kpool /kinetics/PI3K_activation/PDK1 0 0.0 0 0 0 624810.054205 0 0 624810.054205 0 /kinetics/geometry 39 black -3976 2190 0
simundump kpool /kinetics/Ras/CaM_GEF 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 23 black -709 -1610 0
simundump kpool /kinetics/Ras/inact_GEF 0 0.0 0 0 0 62481.0054205 0 0 624810.054205 0 /kinetics/geometry 57 black -236 -1981 0
simundump kpool /kinetics/Ras/GDP_Ras 0 0.0 0 0 0 312405.027103 0 0 624810.054205 0 /kinetics/geometry 55 black -400 -831 0
simundump kpool /kinetics/Ras/GTP_Ras 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 49 black 825 -892 0
simundump kpool /kinetics/Ras/Ras_GTP_PI3K 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 0 black 1535 282 0
simundump kpool /kinetics/CaM/CaM_Ca4 0 0.0 0 0 0 62481.0054205 0 0 624810.054205 0 /kinetics/geometry 49 black -1289 -3308 0
simundump kpool /kinetics/MAPK/MAPK_p 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 4 black 4208 -2964 0
simundump kpool /kinetics/MAPK/craf_1 0 0.0 0 0 0 312405.027103 0 0 624810.054205 0 /kinetics/geometry 23 black -1319 -2866 0
simundump kpool /kinetics/MAPK/craf_1_p 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 7 black 722 -2430 0
simundump kpool /kinetics/MAPK/MAPK_p_p 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 63 black 2681 -2387 0
simundump kpool /kinetics/MAPK/MAPKK 0 0.0 0 0 0 312405.027103 0 0 624810.054205 0 /kinetics/geometry 54 black 1335 -4449 0
simundump kpool /kinetics/MAPK/MAPKK_p 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 23 black 2214 -3955 0
simundump kpool /kinetics/MAPK/MAPKK_p_p 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 0 black 3165 -3315 0
simundump kpool /kinetics/MAPK/craf_1_p_p 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 62 black 2406 -1652 0
simundump kpool /kinetics/MAPK/Raf_p_GTP_Ras 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 57 black 1569 -2686 0
simundump kpool /kinetics/PKC/PKC_active 0 0.0 0 0 0 62481.0054205 0 0 624810.054205 0 /kinetics/geometry 53 black -347 -3749 0
simundump kpool /kinetics/MAPK/craf_1_p_ser259 0 0.0 0 0 0 0.0 0 0 624810.054205 0 /kinetics/geometry 27 black -2754 -3403 0
simundump kreac /kinetics/mGluR/RecLigandBinding 0 2.68881716722e-05 10.0 "" white black 3728 5300 0
simundump kreac /kinetics/HomerPIKE/L.mGluR_HomerBinding 0 1.60048640907e-07 0.04 "" white black 2476 4335 0
simundump kreac /kinetics/HomerPIKE/L.mGluR.Homer_PIKE_Binding 0 8.00243204531e-07 0.1 "" white black 1432 3076 0
simundump kreac /kinetics/HomerPIKE/L.mGluR.Homer.PIKE_PI3K_Binding 0 8.00243204531e-07 0.1 "" white black 284 1801 0
simundump kreac /kinetics/PI3K_activation/basal_PI3K_act 0 0.00068 0.45 "" white black -394 1110 0
simundump kreac /kinetics/AKT_activation/PIP3_bind_PDK1 0 1.12034048635e-06 0.98 "" white black -3104 1724 0
simundump kreac /kinetics/AKT_activation/PIP3_bind_AKT 0 7.20218884078e-05 0.89 "" white black -3298 2108 0
simundump kreac /kinetics/Ras/CaM_bind_GEF 0 0.000320083411038 1.0 "" white black -921 -2432 0
simundump kreac /kinetics/Ras/PI3K_bind_Ras_GTP 0 2.88087553631e-06 5.0 "" white black 784 54 0
simundump kreac /kinetics/MAPK/Ras_act_craf 0 1.60036904218e-05 0.5 "" white black 1092 -1804 0
simundump kenz /kinetics/AKT_activation/PIP3_PDK1/phospho_thr308 0 0 0 0.0 0 624810.054205 0.000194257706904 40.0 10.0 0 0 "" black 23 "" -3985 414 0
simundump kenz /kinetics/AKT_activation/PIP3_PDK2/phosp_AKTser473 0 0 0 0.0 0 624810.054205 0.000194248382832 80.0 20.0 0 0 "" black 23 "" -3677 -1373 0
simundump kenz /kinetics/PI3K_activation/PI3K_basal/basal_phosp 0 0 0 0.0 0 624810.054205 7.7414606289e-06 16.0 4.0 0 0 "" black 23 "" -1863 1997 0
simundump kenz /kinetics/PI3K_activation/PTEN/PIP3_dephosp 0 0 0 0.0 0 624810.054205 0.000532230643744 22.0 5.5 0 0 "" black 26 "" -2522 3142 0
simundump kenz /kinetics/Ras/CaM_GEF/CaM_GEF_act_Ras 0 0 0 0.0 0 624810.054205 3.07694361516e-06 0.8 0.2 0 0 "" black 23 "" 83 -1025 0
simundump kenz /kinetics/Ras/inact_GEF/basal_GEF_activity 0 0 0 0.0 0 624810.054205 1.53847180757e-08 0.08 0.02 0 0 "" black 52 "" 285 -1275 0
simundump kenz /kinetics/MAPK/MAPKK_p_p/MAPKKtyr 0 0 0 0.0 0 624810.054205 5.03499864298e-05 1.2 0.3 0 0 "" black 23 "" 3910 -3638 0
simundump kenz /kinetics/MAPK/MAPKK_p_p/MAPKKthr 0 0 0 0.0 0 624810.054205 5.03499864298e-05 1.2 0.3 0 0 "" black 23 "" 3451 -2676 0
simundump kenz /kinetics/MAPK/MAPK_p_p/MAPK_p_p_feedback 0 0 0 0.0 0 624810.054205 3.03032325734e-06 40.0 10.0 0 0 "" black 3 "" 1774 -2239 0
simundump kenz /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.1 0 0 0 0.0 0 624810.054205 1.46518460512e-05 1.2 0.3 0 0 "" black 6 "" 1488 -3597 0
simundump kenz /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.2 0 0 0 0.0 0 624810.054205 1.46518460512e-05 1.2 0.3 0 0 "" black 59 "" 2338 -3129 0
simundump kenz /kinetics/PKC/PKC_active/PKC_act_raf 0 0 0 0.0 0 624810.054205 1.55394976637e-06 16.0 4.0 0 0 "" black 23 "" -240 -2906 0
simundump kenz /kinetics/AKT_activation/PIP3_AKT_t308_s473/Enz 0 0 0 0.0 0 624810.054205 7.97300964646e-07 0.4 0.1 0 0 "" black 19 "" -2301 -2675 0
simundump kenz /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L.PI3K/Enz 0 0 0 0.0 0 624810.054205 7.7414606289e-06 16.0 4.0 0 0 "" 27 23 "" -1504 2394 0
simundump xgraph /graphs/conc1 0 0 99 0.001 0.999 0
simundump xgraph /graphs/conc2 0 0 100 0 1 0
 simundump xplot /graphs/conc1/_kinetics_0__HomerPIKE_0__L.mGluR_p.Homer.PIKE_L.PI3K_0_.conc 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" black 0 0 1
simundump xplot /graphs/conc1/kinetics_0__PI3K_activation_0__PIP3_0_.Conc 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" black 0 0 1
simundump xplot /graphs/conc1/kinetics_0__MAPK_0__MAPK_p_0_.Conc 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" black 0 0 1
simundump xplot /graphs/conc1/kinetics_0__MAPK_0__MAPK_p_p_0_.Conc 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" black 0 0 1
simundump xplot /graphs/conc1/kinetics_0__MAPK_0__craf_1_p_ser259_0_.Conc 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" black 0 0 1
simundump xplot /graphs/conc1/kinetics_0__MAPK_0__Raf_p_GTP_Ras_0_.Conc 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" black 0 0 1
simundump xplot /graphs/conc1/kinetics_0__MAPK_0__craf_1_p_0_.Conc 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" black 0 0 1
simundump xgraph /moregraphs/conc3 0 0 100 0 1 0
simundump xgraph /moregraphs/conc4 0 0 100 0 1 0
 simundump xcoredraw /edit/draw 0 -6 4 -2 6
simundump xtree /edit/draw/tree 0 \
  /kinetics/#[],/kinetics/#[]/#[],/kinetics/#[]/#[]/#[][TYPE!=proto],/kinetics/#[]/#[]/#[][TYPE!=linkinfo]/##[] "edit_elm.D <v>; drag_from_edit.w <d> <S> <x> <y> <z>" auto 0.6
simundump xtext /file/notes 0 1
addmsg /kinetics/mGluR/mGluR /kinetics/mGluR/RecLigandBinding SUBSTRATE n 
addmsg /kinetics/mGluR/RecLigandBinding /kinetics/mGluR/mGluR REAC A B 
addmsg /kinetics/mGluR/Glutamate /kinetics/mGluR/RecLigandBinding SUBSTRATE n 
addmsg /kinetics/mGluR/RecLigandBinding /kinetics/mGluR/Glutamate REAC A B 
addmsg /kinetics/mGluR/Rec_Glu /kinetics/mGluR/RecLigandBinding PRODUCT n 
addmsg /kinetics/mGluR/RecLigandBinding /kinetics/mGluR/Rec_Glu REAC B A
addmsg /kinetics/mGluR/Rec_Glu /kinetics/HomerPIKE/L.mGluR_HomerBinding SUBSTRATE n 
addmsg /kinetics/HomerPIKE/L.mGluR_HomerBinding /kinetics/mGluR/Rec_Glu REAC A B 
addmsg /kinetics/HomerPIKE/Homer /kinetics/HomerPIKE/L.mGluR_HomerBinding SUBSTRATE n 
addmsg /kinetics/HomerPIKE/L.mGluR_HomerBinding /kinetics/HomerPIKE/Homer REAC A B 
addmsg /kinetics/HomerPIKE/L.mGluR_p.Homer /kinetics/HomerPIKE/L.mGluR_HomerBinding PRODUCT n 
addmsg /kinetics/HomerPIKE/L.mGluR_HomerBinding /kinetics/HomerPIKE/L.mGluR_p.Homer REAC B A
addmsg /kinetics/HomerPIKE/PIKE_L /kinetics/HomerPIKE/L.mGluR.Homer_PIKE_Binding SUBSTRATE n 
addmsg /kinetics/HomerPIKE/L.mGluR.Homer_PIKE_Binding /kinetics/HomerPIKE/PIKE_L REAC A B 
addmsg /kinetics/HomerPIKE/L.mGluR_p.Homer /kinetics/HomerPIKE/L.mGluR.Homer_PIKE_Binding SUBSTRATE n 
addmsg /kinetics/HomerPIKE/L.mGluR.Homer_PIKE_Binding /kinetics/HomerPIKE/L.mGluR_p.Homer REAC A B 
addmsg /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L /kinetics/HomerPIKE/L.mGluR.Homer_PIKE_Binding PRODUCT n 
addmsg /kinetics/HomerPIKE/L.mGluR.Homer_PIKE_Binding /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L REAC B A
addmsg /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L /kinetics/HomerPIKE/L.mGluR.Homer.PIKE_PI3K_Binding SUBSTRATE n 
addmsg /kinetics/HomerPIKE/L.mGluR.Homer.PIKE_PI3K_Binding /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L REAC A B 
addmsg /kinetics/PI3K_activation/PI3K /kinetics/HomerPIKE/L.mGluR.Homer.PIKE_PI3K_Binding SUBSTRATE n 
addmsg /kinetics/HomerPIKE/L.mGluR.Homer.PIKE_PI3K_Binding /kinetics/PI3K_activation/PI3K REAC A B 
addmsg /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L.PI3K /kinetics/HomerPIKE/L.mGluR.Homer.PIKE_PI3K_Binding PRODUCT n 
addmsg /kinetics/HomerPIKE/L.mGluR.Homer.PIKE_PI3K_Binding /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L.PI3K REAC B A
addmsg /kinetics/PI3K_activation/PI3K /kinetics/PI3K_activation/basal_PI3K_act SUBSTRATE n 
addmsg /kinetics/PI3K_activation/basal_PI3K_act /kinetics/PI3K_activation/PI3K REAC A B 
addmsg /kinetics/PI3K_activation/PI3K_basal /kinetics/PI3K_activation/basal_PI3K_act PRODUCT n 
addmsg /kinetics/PI3K_activation/basal_PI3K_act /kinetics/PI3K_activation/PI3K_basal REAC B A
addmsg /kinetics/PI3K_activation/PDK1 /kinetics/AKT_activation/PIP3_bind_PDK1 SUBSTRATE n 
addmsg /kinetics/AKT_activation/PIP3_bind_PDK1 /kinetics/PI3K_activation/PDK1 REAC A B 
addmsg /kinetics/PI3K_activation/PIP3 /kinetics/AKT_activation/PIP3_bind_PDK1 SUBSTRATE n 
addmsg /kinetics/AKT_activation/PIP3_bind_PDK1 /kinetics/PI3K_activation/PIP3 REAC A B 
addmsg /kinetics/AKT_activation/PIP3_PDK1 /kinetics/AKT_activation/PIP3_bind_PDK1 PRODUCT n 
addmsg /kinetics/AKT_activation/PIP3_bind_PDK1 /kinetics/AKT_activation/PIP3_PDK1 REAC B A
addmsg /kinetics/AKT_activation/AKT /kinetics/AKT_activation/PIP3_bind_AKT SUBSTRATE n 
addmsg /kinetics/AKT_activation/PIP3_bind_AKT /kinetics/AKT_activation/AKT REAC A B 
addmsg /kinetics/PI3K_activation/PIP3 /kinetics/AKT_activation/PIP3_bind_AKT SUBSTRATE n 
addmsg /kinetics/AKT_activation/PIP3_bind_AKT /kinetics/PI3K_activation/PIP3 REAC A B 
addmsg /kinetics/AKT_activation/PIP3_AKT /kinetics/AKT_activation/PIP3_bind_AKT PRODUCT n 
addmsg /kinetics/AKT_activation/PIP3_bind_AKT /kinetics/AKT_activation/PIP3_AKT REAC B A
addmsg /kinetics/Ras/inact_GEF /kinetics/Ras/CaM_bind_GEF SUBSTRATE n 
addmsg /kinetics/Ras/CaM_bind_GEF /kinetics/Ras/inact_GEF REAC A B 
addmsg /kinetics/CaM/CaM_Ca4 /kinetics/Ras/CaM_bind_GEF SUBSTRATE n 
addmsg /kinetics/Ras/CaM_bind_GEF /kinetics/CaM/CaM_Ca4 REAC A B 
addmsg /kinetics/Ras/CaM_GEF /kinetics/Ras/CaM_bind_GEF PRODUCT n 
addmsg /kinetics/Ras/CaM_bind_GEF /kinetics/Ras/CaM_GEF REAC B A
addmsg /kinetics/PI3K_activation/PI3K /kinetics/Ras/PI3K_bind_Ras_GTP SUBSTRATE n 
addmsg /kinetics/Ras/PI3K_bind_Ras_GTP /kinetics/PI3K_activation/PI3K REAC A B 
addmsg /kinetics/Ras/GTP_Ras /kinetics/Ras/PI3K_bind_Ras_GTP SUBSTRATE n 
addmsg /kinetics/Ras/PI3K_bind_Ras_GTP /kinetics/Ras/GTP_Ras REAC A B 
addmsg /kinetics/Ras/Ras_GTP_PI3K /kinetics/Ras/PI3K_bind_Ras_GTP PRODUCT n 
addmsg /kinetics/Ras/PI3K_bind_Ras_GTP /kinetics/Ras/Ras_GTP_PI3K REAC B A
addmsg /kinetics/MAPK/craf_1_p /kinetics/MAPK/Ras_act_craf SUBSTRATE n 
addmsg /kinetics/MAPK/Ras_act_craf /kinetics/MAPK/craf_1_p REAC A B 
addmsg /kinetics/Ras/GTP_Ras /kinetics/MAPK/Ras_act_craf SUBSTRATE n 
addmsg /kinetics/MAPK/Ras_act_craf /kinetics/Ras/GTP_Ras REAC A B 
addmsg /kinetics/MAPK/Raf_p_GTP_Ras /kinetics/MAPK/Ras_act_craf PRODUCT n 
addmsg /kinetics/MAPK/Ras_act_craf /kinetics/MAPK/Raf_p_GTP_Ras REAC B A
addmsg /kinetics/AKT_activation/PIP3_AKT /kinetics/AKT_activation/PIP3_PDK1/phospho_thr308 SUBSTRATE n 
addmsg /kinetics/AKT_activation/PIP3_PDK1/phospho_thr308 /kinetics/AKT_activation/PIP3_AKT REAC sA B 
addmsg /kinetics/AKT_activation/PIP3_PDK1/phospho_thr308 /kinetics/AKT_activation/PIP3_AKT_thr308 MM_PRD pA
addmsg /kinetics/AKT_activation/PIP3_PDK1 /kinetics/AKT_activation/PIP3_PDK1/phospho_thr308 ENZYME n
addmsg /kinetics/AKT_activation/PIP3_PDK1/phospho_thr308 /kinetics/AKT_activation/PIP3_PDK1 REAC eA B
addmsg /kinetics/AKT_activation/PIP3_AKT_thr308 /kinetics/AKT_activation/PIP3_PDK2/phosp_AKTser473 SUBSTRATE n 
addmsg /kinetics/AKT_activation/PIP3_PDK2/phosp_AKTser473 /kinetics/AKT_activation/PIP3_AKT_thr308 REAC sA B 
addmsg /kinetics/AKT_activation/PIP3_PDK2/phosp_AKTser473 /kinetics/AKT_activation/PIP3_AKT_t308_s473 MM_PRD pA
addmsg /kinetics/AKT_activation/PIP3_PDK2 /kinetics/AKT_activation/PIP3_PDK2/phosp_AKTser473 ENZYME n
addmsg /kinetics/AKT_activation/PIP3_PDK2/phosp_AKTser473 /kinetics/AKT_activation/PIP3_PDK2 REAC eA B
addmsg /kinetics/PI3K_activation/PIP2 /kinetics/PI3K_activation/PI3K_basal/basal_phosp SUBSTRATE n 
addmsg /kinetics/PI3K_activation/PI3K_basal/basal_phosp /kinetics/PI3K_activation/PIP2 REAC sA B 
addmsg /kinetics/PI3K_activation/PI3K_basal/basal_phosp /kinetics/PI3K_activation/PIP3 MM_PRD pA
addmsg /kinetics/PI3K_activation/PI3K_basal /kinetics/PI3K_activation/PI3K_basal/basal_phosp ENZYME n
addmsg /kinetics/PI3K_activation/PI3K_basal/basal_phosp /kinetics/PI3K_activation/PI3K_basal REAC eA B
addmsg /kinetics/PI3K_activation/PIP3 /kinetics/PI3K_activation/PTEN/PIP3_dephosp SUBSTRATE n 
addmsg /kinetics/PI3K_activation/PTEN/PIP3_dephosp /kinetics/PI3K_activation/PIP3 REAC sA B 
addmsg /kinetics/PI3K_activation/PTEN/PIP3_dephosp /kinetics/PI3K_activation/PIP2 MM_PRD pA
addmsg /kinetics/PI3K_activation/PTEN /kinetics/PI3K_activation/PTEN/PIP3_dephosp ENZYME n
addmsg /kinetics/PI3K_activation/PTEN/PIP3_dephosp /kinetics/PI3K_activation/PTEN REAC eA B
addmsg /kinetics/Ras/GDP_Ras /kinetics/Ras/CaM_GEF/CaM_GEF_act_Ras SUBSTRATE n 
addmsg /kinetics/Ras/CaM_GEF/CaM_GEF_act_Ras /kinetics/Ras/GDP_Ras REAC sA B 
addmsg /kinetics/Ras/CaM_GEF/CaM_GEF_act_Ras /kinetics/Ras/GTP_Ras MM_PRD pA
addmsg /kinetics/Ras/CaM_GEF /kinetics/Ras/CaM_GEF/CaM_GEF_act_Ras ENZYME n
addmsg /kinetics/Ras/CaM_GEF/CaM_GEF_act_Ras /kinetics/Ras/CaM_GEF REAC eA B
addmsg /kinetics/Ras/GDP_Ras /kinetics/Ras/inact_GEF/basal_GEF_activity SUBSTRATE n 
addmsg /kinetics/Ras/inact_GEF/basal_GEF_activity /kinetics/Ras/GDP_Ras REAC sA B 
addmsg /kinetics/Ras/inact_GEF/basal_GEF_activity /kinetics/Ras/GTP_Ras MM_PRD pA
addmsg /kinetics/Ras/inact_GEF /kinetics/Ras/inact_GEF/basal_GEF_activity ENZYME n
addmsg /kinetics/Ras/inact_GEF/basal_GEF_activity /kinetics/Ras/inact_GEF REAC eA B
addmsg /kinetics/MAPK/MAPK /kinetics/MAPK/MAPKK_p_p/MAPKKtyr SUBSTRATE n 
addmsg /kinetics/MAPK/MAPKK_p_p/MAPKKtyr /kinetics/MAPK/MAPK REAC sA B 
addmsg /kinetics/MAPK/MAPKK_p_p/MAPKKtyr /kinetics/MAPK/MAPK_p MM_PRD pA
addmsg /kinetics/MAPK/MAPKK_p_p /kinetics/MAPK/MAPKK_p_p/MAPKKtyr ENZYME n
addmsg /kinetics/MAPK/MAPKK_p_p/MAPKKtyr /kinetics/MAPK/MAPKK_p_p REAC eA B
addmsg /kinetics/MAPK/MAPK_p /kinetics/MAPK/MAPKK_p_p/MAPKKthr SUBSTRATE n 
addmsg /kinetics/MAPK/MAPKK_p_p/MAPKKthr /kinetics/MAPK/MAPK_p REAC sA B 
addmsg /kinetics/MAPK/MAPKK_p_p/MAPKKthr /kinetics/MAPK/MAPK_p_p MM_PRD pA
addmsg /kinetics/MAPK/MAPKK_p_p /kinetics/MAPK/MAPKK_p_p/MAPKKthr ENZYME n
addmsg /kinetics/MAPK/MAPKK_p_p/MAPKKthr /kinetics/MAPK/MAPKK_p_p REAC eA B
addmsg /kinetics/MAPK/craf_1_p /kinetics/MAPK/MAPK_p_p/MAPK_p_p_feedback SUBSTRATE n 
addmsg /kinetics/MAPK/MAPK_p_p/MAPK_p_p_feedback /kinetics/MAPK/craf_1_p REAC sA B 
addmsg /kinetics/MAPK/MAPK_p_p/MAPK_p_p_feedback /kinetics/MAPK/craf_1_p_p MM_PRD pA
addmsg /kinetics/MAPK/MAPK_p_p /kinetics/MAPK/MAPK_p_p/MAPK_p_p_feedback ENZYME n
addmsg /kinetics/MAPK/MAPK_p_p/MAPK_p_p_feedback /kinetics/MAPK/MAPK_p_p REAC eA B
addmsg /kinetics/MAPK/MAPKK /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.1 SUBSTRATE n 
addmsg /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.1 /kinetics/MAPK/MAPKK REAC sA B 
addmsg /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.1 /kinetics/MAPK/MAPKK_p MM_PRD pA
addmsg /kinetics/MAPK/Raf_p_GTP_Ras /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.1 ENZYME n
addmsg /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.1 /kinetics/MAPK/Raf_p_GTP_Ras REAC eA B
addmsg /kinetics/MAPK/MAPKK_p /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.2 SUBSTRATE n 
addmsg /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.2 /kinetics/MAPK/MAPKK_p REAC sA B 
addmsg /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.2 /kinetics/MAPK/MAPKK_p_p MM_PRD pA
addmsg /kinetics/MAPK/Raf_p_GTP_Ras /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.2 ENZYME n
addmsg /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.2 /kinetics/MAPK/Raf_p_GTP_Ras REAC eA B
addmsg /kinetics/MAPK/craf_1 /kinetics/PKC/PKC_active/PKC_act_raf SUBSTRATE n 
addmsg /kinetics/PKC/PKC_active/PKC_act_raf /kinetics/MAPK/craf_1 REAC sA B 
addmsg /kinetics/PKC/PKC_active/PKC_act_raf /kinetics/MAPK/craf_1_p MM_PRD pA
addmsg /kinetics/PKC/PKC_active /kinetics/PKC/PKC_active/PKC_act_raf ENZYME n
addmsg /kinetics/PKC/PKC_active/PKC_act_raf /kinetics/PKC/PKC_active REAC eA B
addmsg /kinetics/MAPK/craf_1 /kinetics/AKT_activation/PIP3_AKT_t308_s473/Enz SUBSTRATE n 
addmsg /kinetics/AKT_activation/PIP3_AKT_t308_s473/Enz /kinetics/MAPK/craf_1 REAC sA B 
addmsg /kinetics/AKT_activation/PIP3_AKT_t308_s473/Enz /kinetics/MAPK/craf_1_p_ser259 MM_PRD pA
addmsg /kinetics/AKT_activation/PIP3_AKT_t308_s473 /kinetics/AKT_activation/PIP3_AKT_t308_s473/Enz ENZYME n
addmsg /kinetics/AKT_activation/PIP3_AKT_t308_s473/Enz /kinetics/AKT_activation/PIP3_AKT_t308_s473 REAC eA B
addmsg /kinetics/PI3K_activation/PIP2 /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L.PI3K/Enz SUBSTRATE n 
addmsg /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L.PI3K/Enz /kinetics/PI3K_activation/PIP2 REAC sA B 
addmsg /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L.PI3K/Enz /kinetics/PI3K_activation/PIP3 MM_PRD pA
addmsg /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L.PI3K /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L.PI3K/Enz ENZYME n
addmsg /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L.PI3K/Enz /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L.PI3K REAC eA B
addmsg /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L.PI3K /graphs/conc1/_kinetics_0__HomerPIKE_0__L.mGluR_p.Homer.PIKE_L.PI3K_0_.conc PLOT Co *L.mGluR_p.Homer.PIKE_L.PI3K *59
addmsg /kinetics/PI3K_activation/PIP3 /graphs/conc1/kinetics_0__PI3K_activation_0__PIP3_0_.Conc PLOT Co *PIP3 *39
addmsg /kinetics/MAPK/MAPK_p /graphs/conc1/kinetics_0__MAPK_0__MAPK_p_0_.Conc PLOT Co *MAPK_p *4
addmsg /kinetics/MAPK/MAPK_p_p /graphs/conc1/kinetics_0__MAPK_0__MAPK_p_p_0_.Conc PLOT Co *MAPK_p_p *63
addmsg /kinetics/MAPK/craf_1_p_ser259 /graphs/conc1/kinetics_0__MAPK_0__craf_1_p_ser259_0_.Conc PLOT Co *craf_1_p_ser259 *27
addmsg /kinetics/MAPK/Raf_p_GTP_Ras /graphs/conc1/kinetics_0__MAPK_0__Raf_p_GTP_Ras_0_.Conc PLOT Co *Raf_p_GTP_Ras *57
addmsg /kinetics/MAPK/craf_1_p /graphs/conc1/kinetics_0__MAPK_0__craf_1_p_0_.Conc PLOT Co *craf_1_p *7

enddump
 // End of dump
complete_loading
