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
DEFAULT_VOL = 1.04904995573e-15
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
simundump group /kinetics/compartment_1 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2748 5101 0
simundump geometry /kinetics/geometry[1] 0 1.04904995573e-15 3 sphere  "" white black -2750 5101 0
simundump geometry /kinetics/geometry[1] 0 1.04904995573e-15 3 sphere  "" white black -2750 5101 0
simundump geometry /kinetics/geometry 0 1.74841659288e-21 3 sphere  "" white black -2750 5101 0
simundump group /kinetics/compartment_1 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/PKC 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/PLA2 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/PLCbeta 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/mGluRAntag 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/MAPK 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/Ras 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/EGFR 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/Sos 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/PLC_g 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/CaMKII 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/CaM 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/PP1 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/PP2B 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/PKA 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/AC 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/mGluR 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/Gprotein 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/Phosphatase 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/Ca 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/PI3K_activation 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/AKT_activation 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/TrKB 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/mTORC1 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/S6Kinase 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/4E_BP 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/43S_complex 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/protein 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/BDNF 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/CaMKIII 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/Translation_initiation 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/Translation_elongation 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/40S 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/TSC1_TSC2 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/HomerPIKE 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump group /kinetics/barr2_signaling 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -2753 5101 0
simundump kpool /kinetics/PKC/PKC_Ca 0 0.0 0 0 0 2.35064660655e-11 0 0 631752.727399 0 /kinetics/geometry[1] red black -4 1 0
simundump kpool /kinetics/PKC/PKC_DAG_AA_p 0 0.0 0 0 0 3.1042223182e-12 0 0 631752.727399 0 /kinetics/geometry[1] cyan blue 0 5 0
simundump kpool /kinetics/PKC/PKC_Ca_AA_p 0 0.0 0 0 0 1.10556727295e-10 0 0 631752.727399 0 /kinetics/geometry[1] orange blue 0 6 0
simundump kpool /kinetics/PKC/PKC_Ca_memb_p 0 0.0 0 0 0 8.77883589992e-12 0 0 631752.727399 0 /kinetics/geometry[1] pink blue -2 6 0
simundump kpool /kinetics/PKC/PKC_DAG_memb_p 0 0.0 0 0 0 5.9606922751e-15 0 0 631752.727399 0 /kinetics/geometry[1] yellow blue -1 5 0
simundump kpool /kinetics/PKC/PKC_basal_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] pink blue -4 5 0
simundump kpool /kinetics/PKC/PKC_AA_p 0 0.0 0 0 0 1.14557827899e-11 0 0 631752.727399 0 /kinetics/geometry[1] cyan blue 1 6 0
simundump kpool /kinetics/PKC/PKC_Ca_DAG 0 0.0 0 0 0 5.34662862407e-17 0 0 631752.727399 0 /kinetics/geometry[1] white blue 0 1 0
simundump kpool /kinetics/PKC/PKC_DAG 0 0.0 0 0 0 7.33475445722e-11 0 0 631752.727399 0 /kinetics/geometry[1] white blue 0 -1 0
simundump kpool /kinetics/PKC/PKC_DAG_AA 0 0.0 0 0 0 1.5912798282e-13 0 0 631752.727399 0 /kinetics/geometry[1] white blue 0 0 0
simundump kpool /kinetics/PKC/PKC_cytosolic 0 0.0 0 0 0 631752.727399 0 0 631752.727399 0 /kinetics/geometry[1] white blue -6 0 0
simundump kpool /kinetics/PKC/DAG 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] green black 0 -7 0
simundump kpool /kinetics/PKC/Arachidonic_Acid 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] darkgreen black -3 -9 0
simundump kpool /kinetics/PKC/PKC_active 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] red black 0 9 0
simundump kpool /kinetics/PLA2/PLA2_cytosolic 0 0.0 0 0 0 252701.090961 0 0 631752.727399 0 /kinetics/geometry[1] yellow darkgreen -11 -8 0
simundump kpool /kinetics/PLA2/PLA2_Ca_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] yellow darkgreen -8 -11 0
simundump kpool /kinetics/PLA2/PIP2_PLA2_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] cyan darkgreen -8 -6 0
simundump kpool /kinetics/PLA2/PIP2_Ca_PLA2_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] cyan darkgreen -8 -7 0
simundump kpool /kinetics/PLA2/DAG_Ca_PLA2_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] pink darkgreen -8 -10 0
simundump kpool /kinetics/PLA2/APC 0 0.0 0 0 0 18952581.822 0 0 631752.727399 4 /kinetics/geometry[1] yellow darkgreen -8 -9 0
simundump kpool /kinetics/PLA2/PLA2_p_Ca 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] orange darkgreen -7 -12 0
simundump kpool /kinetics/PLA2/PLA2_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] orange darkgreen -9 -14 0
simundump kpool /kinetics/MAPK/MAPK_p_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] orange yellow 17 -11 0
simundump kpool /kinetics/PI3K_activation/temp_PIP2 0 0.0 0 0 0 1579381.8185 0 0 631752.727399 4 /kinetics/geometry[1] green black -15 -7 0
simundump kpool /kinetics/PI3K_activation/IP3 0 0.0 0 0 0 461179.491 0 0 631752.727399 0 /kinetics/geometry[1] pink black 0 -4 0
simundump kpool /kinetics/mGluR/Glutamate 0 0.0 0 0 0 0.0 0 0 631752.727399 4 /kinetics/geometry[1] green black 0 13 0
simundump kpool /kinetics/PLCbeta/PLC 0 0.0 0 0 0 505402.181919 0 0 631752.727399 0 /kinetics/geometry[1] cyan maroon 10 -16 0
simundump kpool /kinetics/PLCbeta/Inositol 0 0.0 0 0 0 0.0 0 0 631752.727399 4 /kinetics/geometry[1] green maroon 4 -8 0
simundump kpool /kinetics/PC 0 0.0 0 0 0 0.0 0 0 1.05292121233 4 /kinetics/geometry green maroon 4 -7 0
simundump kpool /kinetics/PLCbeta/PLC_Ca 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] cyan maroon 7 -12 0
simundump kpool /kinetics/PLCbeta/PLC_Ca_Gq 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] cyan maroon 10 -13 0
simundump kpool /kinetics/PLCbeta/PLC_Gq 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] cyan maroon 15 -13 0
simundump kpool /kinetics/PI3K_activation/PIP2 0 0.0 0 0 0 6317527.27399 0 0 631752.727399 4 /kinetics/geometry[1] green black 3 -6 0
simundump kpool /kinetics/Gprotein/BetaGamma 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] yellow black 15 -2 0
simundump kpool /kinetics/Gprotein/G_pGTP 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] red black 7 -7 0
simundump kpool /kinetics/Gprotein/G_pGDP 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] yellow black 13 -5 0
simundump kpool /kinetics/Gprotein/G_GDP 0 0.0 0 0 0 631752.727399 0 0 631752.727399 0 /kinetics/geometry[1] yellow blue 10 -2 0
simundump kpool /kinetics/mGluR/mGluR 0 0.0 0 0 0 189525.81822 0 0 631752.727399 0 /kinetics/geometry[1] green blue 6 -1 0
simundump kpool /kinetics/mGluR/Rec_Glu 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] green blue 5 -3 0
simundump kpool /kinetics/mGluR/Rec_Gq 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] green blue 4 0 0
simundump kpool /kinetics/mGluR/Rec_Glu_Gq 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] orange blue 4 -5 0
simundump kpool /kinetics/mGluRAntag/mGluRAntag 0 0.0 0 0 0 0.0 0 0 631752.727399 4 /kinetics/geometry[1] seagreen blue 0 -2 0
simundump kpool /kinetics/mGluRAntag/Blocked_Rec_Gq 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] seagreen blue 2 -5 0
simundump kpool /kinetics/MAPK/craf_1 0 0.0 0 0 0 126350.545477 0 0 631752.727399 0 /kinetics/geometry[1] pink brown 6 8 0
simundump kpool /kinetics/MAPK/craf_1_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] pink brown 9 7 0
simundump kpool /kinetics/MAPK/MAPKK 0 0.0 0 0 0 113715.490931 0 0 631752.727399 0 /kinetics/geometry[1] pink brown 6 3 0
simundump kpool /kinetics/MAPK/MAPK 0 0.0 0 0 0 227430.981865 0 0 631752.727399 0 /kinetics/geometry[1] pink brown 6 1 0
simundump kpool /kinetics/MAPK/craf_1_p_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] hotpink brown 12 7 0
simundump kpool /kinetics/MAPK/MAPK_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] orange brown 8 0 0
simundump kpool /kinetics/MAPK/MAPKK_p_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] pink brown 12 4 0
simundump kpool /kinetics/MAPK/MAPKK_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] pink brown 9 4 0
simundump kpool /kinetics/MAPK/Raf_p_GTP_Ras 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] red brown 4 6 0
simundump kpool /kinetics/Phosphatase/MKP_1 0 0.0 0 0 0 1516.20654577 0 0 631752.727399 0 /kinetics/geometry[1] hotpink black 5 2 0
simundump kpool /kinetics/Phosphatase/PPhosphatase2A 0 0.0 0 0 0 141512.610939 0 0 631752.727399 0 /kinetics/geometry[1] hotpink yellow 9 9 0
simundump kpool /kinetics/Ras/GEF_Gprot_bg 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] hotpink blue 10 17 0
simundump kpool /kinetics/Ras/inact_GEF 0 0.0 0 0 0 63175.2727399 0 0 631752.727399 0 /kinetics/geometry[1] hotpink blue 12 18 0
simundump kpool /kinetics/Ras/GEF_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] hotpink blue 6 17 0
simundump kpool /kinetics/Ras/GTP_Ras 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] orange blue 12 13 0
simundump kpool /kinetics/Ras/GDP_Ras 0 0.0 0 0 0 126350.545477 0 0 631752.727399 0 /kinetics/geometry[1] pink blue 6 14 0
simundump kpool /kinetics/Ras/GAP_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] red blue 1 14 0
simundump kpool /kinetics/Ras/GAP 0 0.0 0 0 0 1263.50545477 0 0 631752.727399 0 /kinetics/geometry[1] red blue 6 12 0
simundump kpool /kinetics/Ras/inact_GEF_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] hotpink blue 15 19 0
simundump kpool /kinetics/Ras/CaM_GEF 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] pink blue 5 19 0
simundump kpool /kinetics/PKA/PKA_active 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] yellow black -33 -12 0
simundump kpool /kinetics/CaM/CaM_Ca4 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] blue yellow -22 -2 0
simundump kpool /kinetics/Sos/SHC_p.Sos.Grb2 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] brown yellow 11 27 0
simundump kpool /kinetics/EGFR/EGFR 0 0.0 0 0 0 105292.121233 0 0 631752.727399 0 /kinetics/geometry[1] red yellow 1 39 0
simundump kpool /kinetics/EGFR/L.EGFR 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] red yellow 6 36 0
simundump kpool /kinetics/EGFR/EGF 0 0.0 0 0 0 0.0 0 0 631752.727399 4 /kinetics/geometry[1] red yellow 2 36 0
simundump kpool /kinetics/Sos/SHC 0 0.0 0 0 0 315876.3637 0 0 631752.727399 0 /kinetics/geometry[1] orange yellow 8 33 0
simundump kpool /kinetics/Sos/SHC_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] orange yellow 12 33 0
simundump kpool /kinetics/EGFR/Internal_L.EGFR 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] red yellow 6 41 0
simundump kpool /kinetics/Sos/Sos_p.Grb2 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] orange blue 12 41 0
simundump kpool /kinetics/Sos/Grb2 0 0.0 0 0 0 631752.727399 0 0 631752.727399 0 /kinetics/geometry[1] orange blue 14 35 0
simundump kpool /kinetics/Sos/Sos.Grb2 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] orange blue 13 30 0
simundump kpool /kinetics/Sos/Sos_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] red blue 15 40 0
simundump kpool /kinetics/Sos/Sos 0 0.0 0 0 0 63175.2727399 0 0 631752.727399 0 /kinetics/geometry[1] red blue 17 36 0
simundump kpool /kinetics/PLC_g/PLC_g 0 0.0 0 0 0 518037.236467 0 0 631752.727399 0 /kinetics/geometry[1] pink darkgreen 0 31 0
simundump kpool /kinetics/PLC_g/PLC_g_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] pink darkgreen 7 31 0
simundump kpool /kinetics/PLC_g/Ca.PLC_g 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] pink darkgreen 2 27 0
simundump kpool /kinetics/PLC_g/Ca.PLC_g_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] pink darkgreen 7 26 0
simundump kpool /kinetics/CaMKII/CaMKII 0 0.0 0 0 0 44222690.9179 0 0 631752.727399 0 /kinetics/geometry[1] palegreen purple -23 3 0
simundump kpool /kinetics/CaMKII/CaMKII_CaM 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] palegreen purple -27 3 0
simundump kpool /kinetics/CaMKII/CaMKII_thr286_p_CaM 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] palegreen purple -27 1 0
simundump kpool /kinetics/CaMKII/CaMKII_p_p_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] cyan purple -27 -1 0
simundump kpool /kinetics/CaMKII/CaMKII_thr286 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] red purple -27 0 0
simundump kpool /kinetics/CaMKII/CaMKII_thr306 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] palegreen purple -27 -3 0
simundump kpool /kinetics/CaMKII/tot_CaM_CaMKII 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] green purple -31 3 0
simundump kpool /kinetics/CaMKII/tot_autonomous_CaMKII 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] green purple -32 2 0
simundump kpool /kinetics/PP1/PP1_active 0 0.0 0 0 0 1137154.90931 0 0 631752.727399 0 /kinetics/geometry[1] cyan yellow -31 0 0
simundump kpool /kinetics/CaM/CaM 0 0.0 0 0 0 12635054.5477 0 0 631752.727399 0 /kinetics/geometry[1] pink blue -45 4 0
simundump kpool /kinetics/CaM/neurogranin_CaM 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] red blue -54 -4 0
simundump kpool /kinetics/CaM/neurogranin_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] red blue -47 -6 0
simundump kpool /kinetics/CaM/neurogranin 0 0.0 0 0 0 6317527.27399 0 0 631752.727399 0 /kinetics/geometry[1] red blue -52 -6 0
simundump kpool /kinetics/CaM/CaM_Ca3 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] hotpink yellow -41 0 0
simundump kpool /kinetics/CaM/CaM_TR2_Ca2 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] pink yellow -40 2 0
simundump kpool /kinetics/CaM/CaM(Ca)n_CaNAB 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] darkblue yellow -30 -6 0
simundump kpool /kinetics/PP1/I1 0 0.0 0 0 0 1137154.90931 0 0 631752.727399 0 /kinetics/geometry[1] orange yellow -38 -14 0
simundump kpool /kinetics/PP1/I1_p 0 0.0 0 0 0 631.752727399 0 0 631752.727399 0 /kinetics/geometry[1] orange yellow -42 -14 0
simundump kpool /kinetics/PP1/PP1_I1_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] brown yellow -43 -8 0
simundump kpool /kinetics/PP1/PP1_I1 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] brown yellow -36 -8 0
simundump kpool /kinetics/Phosphatase/PP2A 0 0.0 0 0 0 75810.3272876 0 0 631752.727399 0 /kinetics/geometry[1] red black -36 -3 0
simundump kpool /kinetics/CaM/CaNAB_Ca4 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] tan yellow -24 -8 0
simundump kpool /kinetics/PP2B/CaNAB 0 0.0 0 0 0 631752.727399 0 0 631752.727399 0 /kinetics/geometry[1] tan red3 -18 -8 0
simundump kpool /kinetics/PP2B/CaNAB_Ca2 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] tan red3 -21 -8 0
simundump kpool /kinetics/PP2B/CaMCa3_CaNAB 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] blue red3 -29 -10 0
simundump kpool /kinetics/PP2B/CaMCa2_CaNAB 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] blue red3 -27 -10 0
simundump kpool /kinetics/PP2B/CaMCa4_CaNAB 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] blue red3 -30 -9 0
simundump kpool /kinetics/PKA/R2C2 0 0.0 0 0 0 315876.3637 0 0 631752.727399 0 /kinetics/geometry[1] white blue -46 -27 0
simundump kpool /kinetics/PKA/R2C2_cAMP 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] white blue -43 -27 0
simundump kpool /kinetics/PKA/R2C2_cAMP2 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] white blue -40 -26 0
simundump kpool /kinetics/PKA/R2C2_cAMP3 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] white blue -37 -27 0
simundump kpool /kinetics/PKA/R2C2_cAMP4 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] white blue -35 -25 0
simundump kpool /kinetics/PKA/R2C_cAMP4 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] white blue -37 -24 0
simundump kpool /kinetics/PKA/R2_cAMP4 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] white blue -43 -25 0
simundump kpool /kinetics/PKA/PKA_inhibitor 0 0.0 0 0 0 157938.18185 0 0 631752.727399 0 /kinetics/geometry[1] cyan blue -44 -23 0
simundump kpool /kinetics/PKA/inhibited_PKA 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] cyan blue -45 -21 0
simundump kpool /kinetics/AC/cAMP 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] green black -30 -32 0
simundump kpool /kinetics/AC/ATP 0 0.0 0 0 0 3158763637.0 0 0 631752.727399 4 /kinetics/geometry[1] red blue -18 -18 0
simundump kpool /kinetics/AC/AC1_CaM 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] orange blue -20 -17 0
simundump kpool /kinetics/AC/AC1 0 0.0 0 0 0 12635.0545477 0 0 631752.727399 0 /kinetics/geometry[1] orange blue -24 -15 0
simundump kpool /kinetics/AC/AC2_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] yellow blue -18 -22 0
simundump kpool /kinetics/AC/AC2_Gs 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] yellow blue -21 -21 0
simundump kpool /kinetics/AC/AC2 0 0.0 0 0 0 9476.29091098 0 0 631752.727399 0 /kinetics/geometry[1] yellow blue -17 -24 0
simundump kpool /kinetics/AC/AC1_Gs 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] orange blue -22 -16 0
simundump kpool /kinetics/AMP 0 0.0 0 0 0 342715.3254 0 0 1.05292121233 0 /kinetics/geometry pink blue -23 -17 0
simundump kpool /kinetics/AC/AC2_p_Gs 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] green blue -20 -22 0
simundump kpool /kinetics/AC/cAMP_PDE 0 0.0 0 0 0 284288.727329 0 0 631752.727399 0 /kinetics/geometry[1] green blue -26 -15 0
simundump kpool /kinetics/AC/cAMP_PDE_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] green blue -26 -17 0
simundump kpool /kinetics/AC/PDE1 0 0.0 0 0 0 1263505.45477 0 0 631752.727399 0 /kinetics/geometry[1] green blue -30 -12 0
simundump kpool /kinetics/AC/CaM.PDE1 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] green blue -30 -14 0
simundump kpool /kinetics/Gprotein/Gs_alpha 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] red black -23 -28 0
simundump kpool /kinetics/Ca/Ca 0 0.0 0 0 0 50540.2181919 0 0 631752.727399 4 /kinetics/geometry[1] red black -37 0 0
simundump kpool /kinetics/AKT_activation/PIP3_AKT 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 53 yellow -8 4 0
simundump kpool /kinetics/AKT_activation/PIP3_PDK1 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 9 yellow -4 10 0
simundump kpool /kinetics/AKT_activation/PIP3_PDK2 0 0.0 0 0 0 1895.32135958 0 0 631752.727399 0 /kinetics/geometry[1] 39 yellow 2 10 0
simundump kpool /kinetics/AKT_activation/PIP3_AKT_thr308 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 60 yellow -4 4 0
simundump kpool /kinetics/AKT_activation/PIP3_AKT_t308_s473 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 25 yellow 4 11 0
simundump kpool /kinetics/AKT_activation/AKT 0 0.0 0 0 0 126354.757303 0 0 631752.727399 0 /kinetics/geometry[1] 4 yellow -11 1 0
simundump kpool /kinetics/TrKB/Int_BDNF_TrKB2_p_clx 0 0.0 0 0 0 157943.446632 0 0 631752.727399 4 /kinetics/geometry[1] yellow white -9 12 0
simundump kpool /kinetics/TrKB/TrKB 0 0.0 0 0 0 157932.917067 0 0 631752.727399 0 /kinetics/geometry[1] 3 white -7 3 0
simundump kpool /kinetics/TrKB/BDNF_TrKB2_clx 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 38 white -5 3 0
simundump kpool /kinetics/TrKB/BDNF_TrKB_clx 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 45 white -6 -3 0
simundump kpool /kinetics/TrKB/BDNF_TrKB2_p_clx 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] red white -3 3 0
simundump kpool /kinetics/PI3K_activation/PIP3 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 43 black -3 -11 0
simundump kpool /kinetics/PI3K_activation/PDK1 0 0.0 0 0 0 631773.786524 0 0 631752.727399 0 /kinetics/geometry[1] 37 black 3 6 0
simundump kpool /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_PI3K_clx 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] brown white 2 -3 0
simundump kpool /kinetics/PI3K_activation/PI3K 0 0.0 0 0 0 63175.2727399 0 0 631752.727399 0 /kinetics/geometry[1] cyan brown 4 -18 0
simundump kpool /kinetics/PI3K_activation/PI3K_basal 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 10 brown -3 -17 0
simundump kpool /kinetics/PI3K_activation/Gab1 0 0.0 0 0 0 442241.650566 0 0 631752.727399 0 /kinetics/geometry[1] 44 brown 2 -5 0
simundump kpool /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_clx 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 50 brown 6 -9 0
simundump kpool /kinetics/PI3K_activation/PTEN 0 0.0 0 0 0 170578.922361 0 0 631752.727399 0 /kinetics/geometry[1] 37 black 1 -16 0
simundump kpool /kinetics/mTORC1/Rheb_GTP 0 0.0 0 0 0 631773.786524 0 0 631752.727399 0 /kinetics/geometry[1] 28 black 20 10 0
simundump kpool /kinetics/mTORC1/Rheb_GDP 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 39 black 15 4 0
simundump kpool /kinetics/mTORC1/TOR_clx 0 0.0 0 0 0 379064.271914 0 0 631752.727399 0 /kinetics/geometry[1] 25 8 10 -13 0
simundump kpool /kinetics/mTORC1/TOR_Rheb_GTP_clx 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 44 black 12 -19 0
simundump kpool /kinetics/S6Kinase/S6K_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 46 6 3 4 0
simundump kpool /kinetics/S6Kinase/S6K 0 0.0 0 0 0 789717.233154 0 0 631752.727399 0 /kinetics/geometry[1] Pink 6 0 3 0
simundump kpool /kinetics/S6Kinase/S6K_thr_412 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 48 6 7 -16 0
simundump kpool /kinetics/S6Kinase/S6K_thr_252 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 6 black -6 17 0
simundump kpool /kinetics/S6Kinase/S6K_basal 0 0.0 0 0 0 631.773786524 0 0 631752.727399 0 /kinetics/geometry[1] 45 black 24 21 0
simundump kpool /kinetics/4E_BP/4E_BP 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 47 white -11 -18 0
simundump kpool /kinetics/4E_BP/4E_BP_t37_46_s65 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 59 white -11 -13 0
simundump kpool /kinetics/4E_BP/eIF4E_BP 0 0.0 0 0 0 126354.757303 0 0 631752.727399 0 /kinetics/geometry[1] 52 white -13 -11 0
simundump kpool /kinetics/4E_BP/eIF4E_BP_thr37_46 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 56 white -11 -5 0
simundump kpool /kinetics/4E_BP/eIF4E_BP_t37_46_s65 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 39 white -11 -1 0
simundump kpool /kinetics/4E_BP/4E_BP_t37_46 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 60 black -7 -14 0
simundump kpool /kinetics/43S_complex/Q.R 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] blue yellow 5 14 0
simundump kpool /kinetics/43S_complex/RM 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] pink yellow -7 3 0
simundump kpool /kinetics/43S_complex/Quaternary_clx 0 0.0 0 0 0 29693.3679668 0 0 631752.727399 0 /kinetics/geometry[1] 28 yellow -5 11 0
simundump kpool /kinetics/43S_complex/43Scomplex 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] hotpink black 18 13 0
simundump kpool /kinetics/CaM/CaM_Ca2 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] pink blue 16 30 0
simundump kpool /kinetics/CaM/CaM_Ca 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] pink blue 11 29 0
simundump kpool /kinetics/Ras/Ras_GTP_PI3K 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 31 black 5 -24 0
simundump kpool /kinetics/Sos/SHC_p_Grb2_clx 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 42 brown 2 -7 0
simundump kpool /kinetics/protein/AA 0 0.0 0 0 0 63177.3786524 0 0 631752.727399 4 /kinetics/geometry[1] cyan black 22 -1 0
simundump kpool /kinetics/protein/peptide 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] brown black 16 -6 0
simundump kpool /kinetics/protein/degraded_protein 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] white black 25 -18 0
simundump kpool /kinetics/protein/protein 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] red black 16 -18 0
simundump kpool /kinetics/protein/rad_AA 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 45 black 27 -4 0
simundump kpool /kinetics/protein/rad_peptide 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 1 black 18 -8 0
simundump kpool /kinetics/protein/rad_protein 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 47 black 19 -14 0
simundump kpool /kinetics/protein/rad_deg_pro 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 2 black 27 -14 0
simundump kpool /kinetics/PLC_g/PLCg_basal 0 0.0 0 0 0 442.241650566 0 0 631752.727399 0 /kinetics/geometry[1] 33 black -3 11 0
simundump kpool /kinetics/BDNF/BDNF 0 0.0 0 0 0 31.5876363699 0 0 631752.727399 4 /kinetics/geometry[1] 44 black -14 16 0
simundump kpool /kinetics/CaMKIII/CaMKIII 0 0.0 0 0 0 37906.4271914 0 0 631752.727399 0 /kinetics/geometry[1] 32 black -2 18 0
simundump kpool /kinetics/CaMKIII/CaMKIII_CaM_Ca4 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 58 black 18 22 0
simundump kpool /kinetics/CaMKIII/CaMKIII_basal 0 0.0 0 0 0 6.31773786524 0 0 631752.727399 0 /kinetics/geometry[1] 45 black 10 11 0
simundump kpool /kinetics/CaMKIII/CaMKIII_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 57 black 2 11 0
simundump kpool /kinetics/Translation_initiation/eIF4E 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 42 black -15 1 0
simundump kpool /kinetics/Translation_initiation/eIF4G_A_clx 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] cyan black -6 4 0
simundump kpool /kinetics/Translation_initiation/eIF4A 0 0.0 0 0 0 126354.757303 0 0 631752.727399 0 /kinetics/geometry[1] pink black -1 15 0
simundump kpool /kinetics/Translation_initiation/eIF4G 0 0.0 0 0 0 25270.9514611 0 0 631752.727399 0 /kinetics/geometry[1] 21 black 0 14 0
simundump kpool /kinetics/Translation_initiation/eIF4F 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 6 black 2 -2 0
simundump kpool /kinetics/Translation_initiation/mRNA 0 0.0 0 0 0 50540.8499656 0 0 631752.727399 0 /kinetics/geometry[1] 60 black 7 3 0
simundump kpool /kinetics/Translation_initiation/eIF4F_mRNA_clx 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 59 black 13 -5 0
simundump kpool /kinetics/Translation_elongation/eEF2 0 0.0 0 0 0 315886.893262 0 0 631752.727399 0 /kinetics/geometry[1] 27 black 26 18 0
simundump kpool /kinetics/Translation_elongation/eEFthr_56 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] white black 15 15 0
simundump kpool /kinetics/Translation_elongation/60S_R 0 0.0 0 0 0 42960.6174837 0 0 631752.727399 4 /kinetics/geometry[1] 46 black 22 15 0
simundump kpool /kinetics/Translation_elongation/Translation_clx 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 52 black 17 0 0
simundump kpool /kinetics/Translation_elongation/80S_ribos_clx 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] blue black 19 7 0
simundump kpool /kinetics/Translation_elongation/Basal_Translation 0 0.0 0 0 0 126.354757303 0 0 631752.727399 0 /kinetics/geometry[1] 53 black 22 -7 0
simundump kpool /kinetics/40S/40S_inact 0 0.0 0 0 0 12635.4757303 0 0 631752.727399 4 /kinetics/geometry[1] 3 6 16 12 0
simundump kpool /kinetics/40S/40S 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 7 black -11 15 0
simundump kpool /kinetics/40S/40S_basal 0 0.0 0 0 0 63.1773786524 0 0 631752.727399 0 /kinetics/geometry[1] 44 black 20 3 0
simundump kpool /kinetics/TSC1_TSC2/TSC1_TSC2_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 40 yellow 5 2 0
simundump kpool /kinetics/TSC1_TSC2/TSC1_TSC2 0 0.0 0 0 0 631773.786524 0 0 631752.727399 0 /kinetics/geometry[1] 51 black 12 9 0
simundump kpool /kinetics/HomerPIKE/Homer 0 0.0 0 0 0 631752.727399 0 0 631752.727399 0 /kinetics/geometry[1] 45 black 2132 5100 0
simundump kpool /kinetics/HomerPIKE/L.mGluR_p.Homer 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 61 black 2090 3596 0
simundump kpool /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 46 black 910 2410 0
simundump kpool /kinetics/HomerPIKE/PIKE_L 0 0.0 0 0 0 631752.727399 0 0 631752.727399 0 /kinetics/geometry[1] 52 black 1089 3774 0
simundump kpool /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L.PI3K 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 59 black -586 2200 0
simundump kpool /kinetics/MAPK/craf_1_p_ser259 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 27 black -2754 -3403 0
simundump kpool /kinetics/barr2_signaling/GRK 0 0.0 0 0 0 728947.884511 0 0 631752.727399 0 /kinetics/geometry[1] 42 black 1434 -4215 0
simundump kpool /kinetics/barr2_signaling/L.mGluR_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 24 black 1057 -2794 0
simundump kpool /kinetics/barr2_signaling/barr2 0 0.0 0 0 0 197422.727313 0 0 631752.727399 0 /kinetics/geometry[1] 19 black 29 -1207 0
simundump kpool /kinetics/barr2_signaling/Internal_mGluR_p.barr2 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 0 black -71 234 0
simundump kpool /kinetics/barr2_signaling/L.mGluR_p.barr2 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 53 black 1521 -1915 0
simundump kpool /kinetics/barr2_signaling/Internal_mGluR 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 61 black -2192 -2080 0
simundump kpool /kinetics/barr2_signaling/Internal_mGluR_p 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 39 black -1381 -718 0
simundump kpool /kinetics/barr2_signaling/mGluR_p.barr2 0 0.0 0 0 0 0.0 0 0 631752.727399 0 /kinetics/geometry[1] 50 black 1132 -804 0
simundump kreac /kinetics/PKC/PKC_act_by_Ca 0 9.49738677774e-07 0.5 "" white blue -4 0 0
simundump kreac /kinetics/PKC/PKC_act_by_DAG 0 1.26628657906e-08 8.6348 "" white blue -2 0 0
simundump kreac /kinetics/PKC/PKC_Ca_to_memb 0 1.2705 3.5026 "" white blue -3 4 0
simundump kreac /kinetics/PKC/PKC_DAG_to_memb 0 1.0 0.1 "" white blue -2 2 0
simundump kreac /kinetics/PKC/PKC_act_by_Ca_AA 0 1.89947735556e-09 0.1 "" white blue 0 3 0
simundump kreac /kinetics/PKC/PKC_act_by_DAG_AA 0 2.0 0.2 "" white blue 1 3 0
simundump kreac /kinetics/PKC/PKC_basal_act 0 1.0 50.0 "" white blue -4 3 0
simundump kreac /kinetics/PKC/PKC_act_by_AA 0 1.89947735556e-10 0.1 "" white blue -4 -1 0
simundump kreac /kinetics/PKC/PKC_n_DAG 0 9.49738677774e-10 0.1 "" white blue -3 -1 0
simundump kreac /kinetics/PKC/PKC_n_DAG_AA 0 2.84921603332e-08 2.0 "" white blue -1 -2 0
simundump kreac /kinetics/PLA2/PLA2_Ca_act 0 1.58292945425e-06 0.1 "" white darkgreen -11 -11 0
simundump kreac /kinetics/PLA2/PIP2_PLA2_act 0 1.89947735556e-09 0.5 "" white darkgreen -11 -6 0
simundump kreac /kinetics/PLA2/PIP2_Ca_PLA2_act 0 1.89947735556e-08 0.1 "" white darkgreen -10 -7 0
simundump kreac /kinetics/PLA2/DAG_Ca_PLA2_act 0 4.74869338889e-09 4.0 "" white darkgreen -10 -9 0
simundump kreac /kinetics/PLA2/Degrade_AA 0 0.4 0.0 "" white darkgreen -6 -5 0
simundump kreac /kinetics/PLA2/PLA2_p_Ca_act 0 9.49738677774e-06 0.1 "" white darkgreen -10 -12 0
simundump kreac /kinetics/PLA2/dephosphorylate_PLA2_p 0 0.17 0.0 "" white darkgreen -13 -11 0
simundump kreac /kinetics/PLCbeta/Act_PLC_Ca 0 4.74869338889e-06 1.0 "" white maroon 3 -16 0
simundump kreac /kinetics/PLCbeta/Degrade_IP3 0 2.5 0.0 "" white maroon 2 -7 0
simundump kreac /kinetics/PLCbeta/Degrade_DAG 0 0.15 0.0 "" white maroon 0 -7 0
simundump kreac /kinetics/PLCbeta/Act_PLC_by_Gq 0 3.98890244665e-05 1.0 "" white maroon 2 -15 0
simundump kreac /kinetics/PLCbeta/Inact_PLC_Gq 0 0.0133 0.0 "" white maroon 11 -10 0
simundump kreac /kinetics/PLCbeta/PLC_bind_Gq 0 3.98890244665e-06 1.0 "" white maroon 14 -16 0
simundump kreac /kinetics/PLCbeta/PLC_Gq_bind_Ca 0 4.74869338889e-05 1.0 "" white maroon 14 -11 0
simundump kreac /kinetics/mGluR/RecLigandBinding 0 2.65926829776e-05 10.0 "" white blue 7 -3 0
simundump kreac /kinetics/Gprotein/Basal_Act_Gq 0 0.0001 0.0 "" white blue 9 -4 0
simundump kreac /kinetics/Gprotein/Trimerize_G 0 9.49738677774e-06 0.0 "" white blue 12 -4 0
simundump kreac /kinetics/Gprotein/Inact_Gq 0 0.0133 0.0 "" white blue 10 -7 0
simundump kreac /kinetics/mGluR/Rec_Glu_bind_Gq 0 9.49738677774e-09 0.0001 "" white blue 4 -2 0
simundump kreac /kinetics/mGluR/Glu_bind_Rec_Gq 0 2.65926829776e-05 0.1 "" white blue 2 -3 0
simundump kreac /kinetics/mGluR/Activate_Gq 0 0.01 0.0 "" white blue 7 -4 0
simundump kreac /kinetics/mGluR/Rec_bind_Gq 0 9.49738677774e-07 1.0 "" white blue 6 0 0
simundump kreac /kinetics/mGluRAntag/Antag_bind_Rec_Gq 0 9.49738677774e-05 0.01 "" white blue 2 -4 0
simundump kreac /kinetics/Ras/Ras_act_craf 0 3.7989547111e-05 0.5 "" white black 3 10 0
simundump kreac /kinetics/Ras/bg_act_GEF 0 9.49738677774e-06 1.0 "" white blue 13 14 0
simundump kreac /kinetics/Ras/dephosph_GEF 0 1.0 0.0 "" white blue 9 17 0
simundump kreac /kinetics/Ras/Ras_intrinsic_GTPase 0 0.0001 0.0 "" white blue 9 13 0
simundump kreac /kinetics/Ras/dephosph_GAP 0 0.1 0.0 "" white blue 4 15 0
simundump kreac /kinetics/Ras/CaM_bind_GEF 0 9.49738677774e-05 1.0 "" white blue 2 21 0
simundump kreac /kinetics/Ras/dephosph_inact_GEF_p 0 1.0 0.0 "" white blue 14 21 0
simundump kreac /kinetics/EGFR/act_EGFR 0 6.64817074441e-06 0.25 "" white yellow 4 38 0
simundump kreac /kinetics/Sos/SHC_p_dephospho 0 0.0016667 0.0 "" white yellow 9 31 0
simundump kreac /kinetics/EGFR/Internalize 0 0.002 0.00033 "" white yellow 4 39 0
simundump kreac /kinetics/Sos/SHC_bind_Sos.Grb2 0 7.9141724019e-07 0.1 "" white blue 10 29 0
simundump kreac /kinetics/Sos/Grb2_bind_Sos_p 0 3.95727614867e-08 0.0168 "" white blue 10 38 0
simundump kreac /kinetics/Sos/dephosph_Sos 0 0.001 0.0 "" white blue 13 37 0
simundump kreac /kinetics/Sos/Grb2_bind_Sos 0 3.95727614867e-08 0.0168 "" white blue 16 33 0
simundump kreac /kinetics/PLC_g/Ca_act_PLC_g 0 0.000284921603332 10.0 "" white darkgreen -1 28 0
simundump kreac /kinetics/PLC_g/Ca_act_PLC_g_p 0 1.89947735556e-05 10.0 "" white darkgreen 2 29 0
simundump kreac /kinetics/PLC_g/dephosph_PLC_g 0 0.05 0.0 "" white darkgreen 4 32 0
simundump kreac /kinetics/CaMKII/CaMKII_bind_CaM 0 7.9144573235e-05 5.0 "" white purple -23 1 0
simundump kreac /kinetics/CaMKII/CaMKII_thr286_bind_CaM 0 0.00158321437583 0.1 "" white purple -23 0 0
simundump kreac /kinetics/CaMKII/basal_activity 0 0.003 0.0 "" white purple -25 0 0
simundump kreac /kinetics/CaM/CaM_TR2_bind_Ca 0 1.80400711212e-10 72.0 "" white blue -43 3 0
simundump kreac /kinetics/CaM/CaM_TR2_Ca2_bind_Ca 0 5.69843206665e-06 10.0 "" white blue -44 1 0
simundump kreac /kinetics/CaM/CaM_Ca3_bind_Ca 0 7.36047475274e-07 10.0 "" white blue -45 -1 0
simundump kreac /kinetics/CaM/neurogranin_bind_CaM 0 4.74869338889e-07 1.0 "" white blue -50 -3 0
simundump kreac /kinetics/CaM/dephosph_neurogranin 0 0.005 0.0 "" white blue -45 -5 0
simundump kreac /kinetics/PP1/Inact_PP1 0 0.00079141724019 0.1 "" white yellow -45 -12 0
simundump kreac /kinetics/PP1/dissoc_PP1_I1 0 1.0 0.0 "" white yellow -42 -12 0
simundump kreac /kinetics/PP2B/Ca_bind_CaNAB_Ca2 0 9.02003556063e-12 1.0 "" white red3 -22 -9 0
simundump kreac /kinetics/PP2B/Ca_bind_CaNAB 0 2.50756988585e-08 1.0 "" white red3 -20 -9 0
simundump kreac /kinetics/PP2B/CaM_Ca2_bind_CaNAB 0 3.7989547111e-07 1.0 "" white red3 -26 -9 0
simundump kreac /kinetics/PP2B/CaMCa3_bind_CaNAB 0 3.54252526811e-06 1.0 "" white red3 -27 -8 0
simundump kreac /kinetics/PP2B/CaMCa4_bind_CaNAB 0 0.000949738677774 1.0 "" white red3 -27 -7 0
simundump kreac /kinetics/PKA/cAMP_bind_site_B1 0 8.54764809997e-05 33.0 "" white blue -44 -31 0
simundump kreac /kinetics/PKA/cAMP_bind_site_B2 0 8.54764809997e-05 33.0 "" white blue -41 -29 0
simundump kreac /kinetics/PKA/cAMP_bind_site_A1 0 0.000118717334723 110.0 "" white blue -39 -30 0
simundump kreac /kinetics/PKA/cAMP_bind_site_A2 0 0.000118717334723 32.5 "" white blue -35 -29 0
simundump kreac /kinetics/PKA/Release_C1 0 60.0 2.84921603332e-05 "" white blue -35 -22 0
simundump kreac /kinetics/PKA/Release_C2 0 60.0 2.84921603332e-05 "" white blue -40 -24 0
simundump kreac /kinetics/PKA/inhib_PKA 0 9.49738677774e-05 1.0 "" white blue -41 -22 0
simundump kreac /kinetics/AC/CaM_bind_AC1 0 7.9144573235e-05 1.0 "" white blue -22 -15 0
simundump kreac /kinetics/AC/dephosph_AC2 0 0.1 0.0 "" white blue -19 -25 0
simundump kreac /kinetics/AC/Gs_bind_AC2 0 0.00079144573235 1.0 "" white blue -20 -27 0
simundump kreac /kinetics/AC/Gs_bind_AC1 0 0.000199445122332 1.0 "" white blue -24 -16 0
simundump kreac /kinetics/AC/Gs_bind_AC2_p 0 0.00131899707569 1.0 "" white blue -20 -23 0
simundump kreac /kinetics/AC/dephosph_PDE 0 0.1 0.0 "" white blue -28 -18 0
simundump kreac /kinetics/AC/CaM_bind_PDE1 0 0.00113968641334 5.0 "" white blue -27 -13 0
simundump kreac /kinetics/AKT_activation/PIP3_bind_AKT 0 7.12308756075e-05 0.089 "" white yellow -11 4 0
simundump kreac /kinetics/AKT_activation/PIP3_bind_PDK1 0 1.10802318002e-06 0.98 "" white yellow -8 6 0
simundump kreac /kinetics/TSC1_TSC2/TSC1_TSC2_dephospho 0 0.01 0.0 "" white yellow 10 7 0
simundump kreac /kinetics/TrKB/Autophos_TrKB 0 0.02 0.0 "" white white -4 -2 0
simundump kreac /kinetics/TrKB/Dimeriz_TrKB 0 1.58287668993e-06 0.02 "" white white -7 0 0
simundump kreac /kinetics/TrKB/Ligand_binding 0 1.58297166064e-06 0.05 "" white white -9 0 0
simundump kreac /kinetics/PLC_g/PLC_g_p_dephospho 0 0.07 0.0 "" white white -1 12 0
simundump kreac /kinetics/TrKB/LR_Internalize 0 0.01 0.0 "" white white -5 9 0
simundump kreac /kinetics/TrKB/LR_cycling 0 0.001 0.001 "" white white -9 9 0
simundump kreac /kinetics/Sos/Grb2_bind_SHC 0 1.58287668993e-06 1.0 "" white brown 0 -4 0
simundump kreac /kinetics/PI3K_activation/bind_Gab1 0 4.74853509911e-07 1.0 "" white brown 5 -5 0
simundump kreac /kinetics/PI3K_activation/PI3K_act 0 7.91447842038e-06 0.08 "" white brown 4 -13 0
simundump kreac /kinetics/PI3K_activation/basal_PI3K_act 0 0.00068 0.45 "" white brown 1 -19 0
simundump kreac /kinetics/mTORC1/Rheb_GTP_bind_TORclx 0 9.4970701982e-06 3.0 "" white 8 13 -7 0
simundump kreac /kinetics/S6Kinase/S6_dephosph 0 0.01 0.0 "" white 6 14 5 0
simundump kreac /kinetics/4E_BP/eIF4E_bind_BP2 0 7.91419350827e-05 0.15 "" white white -14 -18 0
simundump kreac /kinetics/4E_BP/eIF4E_BP2_disso 0 4.0 1.58287668993e-06 "" white white -16 -17 0
simundump kreac /kinetics/Translation_initiation/eIF4F_clx 0 4.74863006979e-05 0.1 "" white black -15 10 0
simundump kreac /kinetics/Translation_initiation/eIF4G_A_clx_formation 0 4.74863006979e-07 1.0 "" white black -7 9 0
simundump kreac /kinetics/Translation_initiation/eIF4F_mRNA_clx_formation 0 3.16575337987e-07 0.077 "" white black 9 -4 0
simundump kreac /kinetics/43S_complex/Q_binds_R 0 7.59765615855e-07 0.5 "" white yellow -4 13 0
simundump kreac /kinetics/43S_complex/QR_binds_M 0 7.75597231877e-07 0.0045 "" white yellow 6 11 0
simundump kreac /kinetics/43S_complex/R_binds_M 0 2.02600998538e-06 0.719 "" white yellow -3 4 0
simundump kreac /kinetics/43S_complex/RM_binds_Q 0 1.55115647547e-07 0.00169 "" white yellow -6 7 0
simundump kreac /kinetics/CaM/CaM_bind_Ca 0 1.34298069672e-05 8.4853 "" white blue 7 26 0
simundump kreac /kinetics/CaM/CaM_Ca2_bind_Ca 0 5.69833708962e-06 10.0 "" white blue 13 26 0
simundump kreac /kinetics/CaM/CaM_Ca_bind_Ca 0 1.34298069672e-05 8.4853 "" white blue 19 26 0
simundump kreac /kinetics/CaMKIII/CaMKIII_dephospho 0 0.07 0.0 "" white black 1 20 0
simundump kreac /kinetics/Translation_elongation/elongation 0 6.33141178904e-05 10.0 "" white black 25 2 0
simundump kreac /kinetics/Translation_elongation/activation 0 1.58287668993e-06 0.9 "" white black 23 10 0
simundump kreac /kinetics/CaM/CaMKIII_bind_CaM_Ca4 0 0.000156701658271 0.09 "" white black -8 20 0
simundump kreac /kinetics/protein/pep_elongation 0 0.1 0.001 "" white black 16 -11 0
simundump kreac /kinetics/protein/protein_deg 0 1.0 0.0 "" white black 20 -17 0
simundump kreac /kinetics/mTORC1/GDP_to_GTP 0 0.2 0.0 "" white black 15 1 0
simundump kreac /kinetics/4E_BP/eIF4E_BP_disso 0 1.0 1.58287668993e-07 "" white black -7 -5 0
simundump kreac /kinetics/S6Kinase/basal_S6K 0 0.01 0.0 "" white black 4 -1 0
simundump kreac /kinetics/protein/rad_pep_elongation 0 0.1 0.001 "" white black 22 -10 0
simundump kreac /kinetics/protein/rad_protein_deg 0 1.0 0.0 "" white black 23 -14 0
simundump kreac /kinetics/protein/labelling 0 0.0 0.0 "" white black 27 1 0
simundump kreac /kinetics/Ras/PI3K_bind_Ras_GTP 0 2.84912105946e-06 5.0 "" white black 13 -24 0
simundump kreac /kinetics/HomerPIKE/L.mGluR_HomerBinding 0 1.5828977963e-07 0.04 "" white black 2476 4335 0
simundump kreac /kinetics/HomerPIKE/L.mGluR.Homer_PIKE_Binding 0 7.91448898146e-07 0.1 "" white black 1432 3076 0
simundump kreac /kinetics/HomerPIKE/L.mGluR.Homer.PIKE_PI3K_Binding 0 7.91448898146e-07 0.1 "" white black 284 1801 0
simundump kreac /kinetics/barr2_signaling/mGluR_barr2_assoc 0 3.16579559261e-08 0.00578 "" white black 676 -1952 0
simundump kreac /kinetics/barr2_signaling/mGluR_internalize 0 0.005 0.0 "" white black 692 -115 0
simundump kreac /kinetics/barr2_signaling/barr2_dissoc 0 0.005 0.0 "" white black -529 -497 0
simundump kreac /kinetics/barr2_signaling/mGluR_recycling 0 0.01 0.0 "" white black -1888 -2859 0
simundump kreac /kinetics/barr2_signaling/ligand_dissoc 0 10.0 9.41824188791e-12 "" white black 943 -1646 0
simundump kreac /kinetics/MAPK/mGluR_barr2_Raf_scaffolding 0 2.37434669443e-09 0.001 "" white black 19 1086 0
simundump kenz /kinetics/PKC/PKC_active/PKC_act_raf 0 0 0 0.0 0 631752.727399 4.51001778033e-07 16.0 4.0 0 0 "" yellow red "" 16 20 0
simundump kenz /kinetics/PKC/PKC_active/PKC_inact_GAP 0 0 0 0.0 0 631752.727399 9.02003556063e-06 16.0 4.0 0 0 "" yellow red "" 13 21 0
simundump kenz /kinetics/PKC/PKC_active/PKC_act_GEF 0 0 0 0.0 0 631752.727399 9.02003556063e-06 16.0 4.0 0 0 "" yellow red "" 9 27 0
simundump kenz /kinetics/PKC/PKC_active/PKC_phosph_neurogranin 0 0 0 0.0 0 631752.727399 1.5334060453e-07 2.34 0.58 0 0 "" red red "" -38 5 0
simundump kenz /kinetics/PKC/PKC_active/PKC_phosph_ng_CaM 0 0 0 0.0 0 631752.727399 9.20043627187e-08 1.4 0.35 0 0 "" red red "" -42 8 0
simundump kenz /kinetics/PKC/PKC_active/phosph_AC2 0 0 0 0.0 0 631752.727399 9.02003556063e-07 16.0 4.0 0 0 "" red red "" -6 -11 0
simundump kenz /kinetics/PLA2/PLA2_Ca_p/kenz 0 0 0 0.0 0 631752.727399 2.02950800114e-06 21.6 5.4 0 0 "" yellow red "" -6 -11 0
simundump kenz /kinetics/PLA2/PIP2_PLA2_p/kenz 0 0 0 0.0 0 631752.727399 4.1492163579e-06 44.16 11.04 0 0 "" cyan red "" -6 -6 0
simundump kenz /kinetics/PLA2/PIP2_Ca_PLA2_p/kenz 0 0 0 0.0 0 631752.727399 1.35300533409e-05 144.0 36.0 0 0 "" cyan red "" -5 -7 0
simundump kenz /kinetics/PLA2/DAG_Ca_PLA2_p/kenz 0 0 0 0.0 0 631752.727399 2.25500889015e-05 240.0 60.0 0 0 "" pink red "" -5 -10 0
simundump kenz /kinetics/PLA2/PLA2_p_Ca/kenz 0 0 0 0.0 0 631752.727399 4.51001778033e-05 480.0 120.0 0 0 "" orange red "" -6 -12 0
simundump kenz /kinetics/MAPK/MAPK_p_p/MAPK_p_p 0 0 0 0.0 0 631752.727399 5.8630231144e-06 80.0 20.0 0 0 "" orange red "" -12 -14 0
simundump kenz /kinetics/MAPK/MAPK_p_p/MAPK_p_p_feedback 0 0 0 0.0 0 631752.727399 2.93151155722e-06 40.0 10.0 0 0 "" orange red "" 10 10 0
simundump kenz /kinetics/MAPK/MAPK_p_p/phosph_Sos 0 0 0 0.0 0 631752.727399 2.93151155722e-05 40.0 10.0 0 0 "" orange red "" 18 40 0
simundump kenz /kinetics/PLCbeta/PLC_Ca/PLC_Ca 0 0 0 0.0 0 631752.727399 3.78841493545e-06 40.0 10.0 0 0 "" cyan red "" -2 -11 0
simundump kenz /kinetics/PLCbeta/PLC_Ca_Gq/PLCb_Ca_Gq 0 0 0 0.0 0 631752.727399 7.21602844849e-05 192.0 48.0 0 0 "" cyan red "" 2 -11 0
simundump kenz /kinetics/MAPK/MAPKK_p_p/MAPKKtyr 0 0 0 0.0 0 631752.727399 2.43540960136e-05 0.6 0.15 0 0 "" pink red "" 8 3 0
simundump kenz /kinetics/MAPK/MAPKK_p_p/MAPKKthr 0 0 0 0.0 0 631752.727399 2.43540960136e-05 0.6 0.15 0 0 "" pink red "" 12 3 0
simundump kenz /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.1 0 0 0 0.0 0 631752.727399 4.96101955835e-06 0.42 0.105 0 0 "" red red "" 7 6 0
simundump kenz /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.2 0 0 0 0.0 0 631752.727399 4.96101955835e-06 0.42 0.105 0 0 "" red red "" 10 6 0
simundump kenz /kinetics/Phosphatase/MKP_1/MKP1_tyr_deph 0 0 0 0.0 0 631752.727399 0.000112750444507 4.0 1.0 0 0 "" hotpink red "" 6 3 0
simundump kenz /kinetics/Phosphatase/MKP_1/MKP1_thr_deph 0 0 0 0.0 0 631752.727399 0.000112750444507 4.0 1.0 0 0 "" hotpink red "" 10 2 0
simundump kenz /kinetics/Phosphatase/PPhosphatase2A/craf_dephospho 0 0 0 0.0 0 631752.727399 2.976611735e-06 25.0 6.0 0 0 "" hotpink red "" 7 10 0
simundump kenz /kinetics/Phosphatase/PPhosphatase2A/MAPKK_dephospho 0 0 0 0.0 0 631752.727399 2.976611735e-06 25.0 6.0 0 0 "" hotpink red "" 13 6 0
simundump kenz /kinetics/Phosphatase/PPhosphatase2A/MAPKK_dephospho_ser 0 0 0 0.0 0 631752.727399 2.976611735e-06 25.0 6.0 0 0 "" hotpink red "" 4 5 0
simundump kenz /kinetics/Phosphatase/PPhosphatase2A/craf_p_p_dephospho 0 0 0 0.0 0 631752.727399 2.976611735e-06 25.0 6.0 0 0 "" hotpink red "" 12 9 0
simundump kenz /kinetics/Ras/GEF_Gprot_bg/GEF_bg_act_Ras 0 0 0 0.0 0 631752.727399 2.976611735e-07 0.08 0.02 0 0 "" hotpink red "" 10 16 0
simundump kenz /kinetics/Ras/GEF_p/GEF_p_act_Ras 0 0 0 0.0 0 631752.727399 2.976611735e-07 0.08 0.02 0 0 "" hotpink red "" 7 16 0
simundump kenz /kinetics/Ras/GAP/GAP_inact_Ras 0 0 0 0.0 0 631752.727399 7.43936452898e-05 40.0 10.0 0 0 "" red red "" 9 12 0
simundump kenz /kinetics/Ras/CaM_GEF/CaM_GEF_act_Ras 0 0 0 0.0 0 631752.727399 2.976611735e-07 0.08 0.02 0 0 "" pink red "" 5 18 0
simundump kenz /kinetics/PKA/PKA_active/PKA_phosph_GEF 0 0 0 0.0 0 631752.727399 9.02003556063e-06 36.0 9.0 0 0 "" yellow red "" 10 21 0
simundump kenz /kinetics/PKA/PKA_active/PKA_phosph_I1 0 0 0 0.0 0 631752.727399 9.02003556063e-06 36.0 9.0 0 0 "" yellow red "" -36 -17 0
simundump kenz /kinetics/PKA/PKA_active/phosph_PDE 0 0 0 0.0 0 631752.727399 9.02003556063e-06 36.0 9.0 0 0 "" yellow red "" -30 -13 0
simundump kenz /kinetics/Sos/SHC_p.Sos.Grb2/Sos.Ras_GEF 0 0 0 0.0 0 631752.727399 2.976611735e-07 0.08 0.02 0 0 "" brown red "" 11 24 0
simundump kenz /kinetics/EGFR/L.EGFR/Ca.PLC_g_phospho 0 0 0 0.0 0 631752.727399 4.51001778033e-06 0.8 0.2 0 0 "" red red "" 6 35 0
simundump kenz /kinetics/EGFR/L.EGFR/SHC_phospho 0 0 0 0.0 0 631752.727399 1.80400711212e-06 0.8 0.2 0 0 "" red red "" 9 36 0
simundump kenz /kinetics/PLC_g/Ca.PLC_g/PIP2_hydrolysis 0 0 0 0 0 631752.727399 1.13968641334e-06 56.0 14.0 0 1 "" pink red "" 0 0 0
simundump kenz /kinetics/PLC_g/Ca.PLC_g_p/PIP2_hydrolysis 0 0 0 0 0 631752.727399 2.27937282665e-05 228.0 57.0 0 1 "" pink red "" 3 -2 0
simundump kenz /kinetics/CaMKII/tot_CaM_CaMKII/CaM_act_305 0 0 0 0.0 0 631752.727399 3.97007845167e-07 24.0 6.0 0 0 "" green red "" -29 0 0
simundump kenz /kinetics/CaMKII/tot_CaM_CaMKII/CaM_act_286 0 0 0 0.0 0 631752.727399 3.30836864293e-08 2.0 0.5 0 0 "" green red "" -25 2 0
simundump kenz /kinetics/CaMKII/tot_autonomous_CaMKII/auton_305 0 0 0 0.0 0 631752.727399 2.57711436001e-07 24.0 6.0 0 0 "" green red "" -29 0 0
simundump kenz /kinetics/CaMKII/tot_autonomous_CaMKII/auton_286 0 0 0 0.0 0 631752.727399 2.14767046698e-08 2.0 0.5 0 0 "" green red "" -25 1 0
simundump kenz /kinetics/PP1/PP1_active/Deph_thr286 0 0 0 0.0 0 631752.727399 5.15946034068e-07 1.4 0.35 0 0 "" cyan red "" -31 1 0
simundump kenz /kinetics/PP1/PP1_active/Deph_thr305 0 0 0 0.0 0 631752.727399 5.15946034068e-07 1.4 0.35 0 0 "" cyan red "" -30 -1 0
simundump kenz /kinetics/PP1/PP1_active/Deph_thr306 0 0 0 0.0 0 631752.727399 5.15946034068e-07 1.4 0.35 0 0 "" cyan red "" -25 3 0
simundump kenz /kinetics/PP1/PP1_active/Deph_thr286c 0 0 0 0.0 0 631752.727399 5.15946034068e-07 1.4 0.35 0 0 "" cyan red "" -30 -2 0
simundump kenz /kinetics/PP1/PP1_active/Deph_thr286b 0 0 0 0.0 0 631752.727399 5.15946034068e-07 1.4 0.35 0 0 "" cyan red "" -24 -1 0
simundump kenz /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_neurogranin 0 0 0 0.0 0 631752.727399 5.01513977173e-07 2.67 0.67 0 0 "" darkblue red "" -51 -9 0
simundump kenz /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_inhib1 0 0 0 0.0 0 631752.727399 5.14142026955e-07 1.36 0.34 0 0 "" darkblue red "" -42 -17 0
simundump kenz /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_PP1_I_p 0 0 0 0.0 0 631752.727399 5.14142026955e-07 1.36 0.34 0 0 "" darkblue white "" -41 -6 0
simundump kenz /kinetics/Phosphatase/PP2A/PP2A_dephospho_I1 0 0 0 0.0 0 631752.727399 5.95322347001e-06 25.0 6.0 0 0 "" red red "" -38 -10 0
simundump kenz /kinetics/Phosphatase/PP2A/PP2A_dephospho_PP1_I_p 0 0 0 0.0 0 631752.727399 5.95322347001e-06 25.0 6.0 0 0 "" red red "" -36 -4 0
simundump kenz /kinetics/CaM/CaNAB_Ca4/dephosph_inhib1_noCaM 0 0 0 0.0 0 631752.727399 5.14142026955e-08 0.136 0.034 0 0 "" tan red "" -35 -10 0
simundump kenz /kinetics/AC/AC1_CaM/kenz 0 0 0 0 0 631752.727399 7.12304008331e-06 72.0 18.0 0 1 "" orange red "" -20 -18 0
simundump kenz /kinetics/AC/AC2_p/kenz 0 0 0 0 0 631752.727399 2.75424216555e-06 28.0 7.0 0 1 "" yellow red "" -18 -21 0
simundump kenz /kinetics/AC/AC2_Gs/kenz 0 0 0 0 0 631752.727399 7.12304008331e-06 72.0 18.0 0 1 "" yellow red "" -21 -20 0
simundump kenz /kinetics/AC/AC1_Gs/kenz 0 0 0 0 0 631752.727399 7.12304008331e-06 72.0 18.0 0 1 "" orange red "" -21 -17 0
simundump kenz /kinetics/AC/AC2_p_Gs/kenz 0 0 0 0 0 631752.727399 7.12304008331e-06 216.0 54.0 0 1 "" green red "" -20 -21 0
simundump kenz /kinetics/AC/cAMP_PDE/PDE 0 0 0 0.0 0 631752.727399 3.78841493545e-06 40.0 10.0 0 0 "" green red "" -26 -23 0
simundump kenz /kinetics/AC/cAMP_PDE_p/PDE_p 0 0 0 0.0 0 631752.727399 7.57682987093e-06 80.0 20.0 0 0 "" green red "" -25 -22 0
simundump kenz /kinetics/AC/PDE1/PDE1 0 0 0 0.0 0 631752.727399 3.15701244621e-07 6.67 1.667 0 0 "" green red "" -27 -22 0
simundump kenz /kinetics/AC/CaM.PDE1/CaM.PDE1 0 0 0 0.0 0 631752.727399 1.89420746774e-06 40.0 10.0 0 0 "" green red "" -28 -21 0
simundump kenz /kinetics/PI3K_activation/PDK1/S6K_phospho 0 0 0 0.0 0 631752.727399 7.62823542565e-07 4.0 1.0 0 0 "" red 37 "" 7 -7 0
simundump kenz /kinetics/Phosphatase/PP2A/dephos_clus_S6K 0 0 0 0.0 0 631752.727399 8.66839525599e-07 4.0 1.0 0 0 "" red 25 "" 3 1 0
simundump kenz /kinetics/Phosphatase/PP2A/dephos_S6K 0 0 0 0.0 0 631752.727399 8.66839525599e-07 4.0 1.0 0 0 "" red 25 "" 9 -2 0
simundump kenz /kinetics/Phosphatase/PP2A/dephosp_S6K 0 0 0 0.0 0 631752.727399 8.66839525599e-07 4.0 1.0 0 0 "" red 25 "" 13 -2 0
simundump kenz /kinetics/Phosphatase/PP2A/Dephos_AKTser473 0 0 0 0.0 0 631752.727399 2.86059972702e-06 7.2 1.8 0 0 "" red 46 "" 3 -8 0
simundump kenz /kinetics/Phosphatase/PP2A/Dephosph_AKTthr308 0 0 0 0.0 0 631752.727399 2.86050818782e-06 7.2 1.8 0 0 "" red 46 "" 0 -8 0
simundump kenz /kinetics/Phosphatase/PP2A/eEF2thr_56_dephospho 0 0 0 0.0 0 631752.727399 4.07404324642e-07 1.88 0.47 0 0 "" red 4 "" 23 8 0
simundump kenz /kinetics/Phosphatase/PP2A/PP2A_4E_BP_p_p 0 0 0 0.0 0 631752.727399 8.66848679518e-07 4.0 1.0 0 0 "" red 4 "" -11 -10 0
simundump kenz /kinetics/Phosphatase/PP2A/PP2A_4E_BP_p 0 0 0 0.0 0 631752.727399 8.66848679518e-07 4.0 1.0 0 0 "" red 4 "" -9 -17 0
simundump kenz /kinetics/Phosphatase/PP2A/PP2A_4E_BP 0 0 0 0.0 0 631752.727399 8.66821217762e-07 4.0 1.0 0 0 "" red 62 "" -13 -3 0
simundump kenz /kinetics/Phosphatase/PP2A/PP2A_4EBP 0 0 0 0.0 0 631752.727399 8.66821217762e-07 4.0 1.0 0 0 "" red 62 "" -13 -7 0
simundump kenz /kinetics/AKT_activation/PIP3_PDK1/phospho_thr308 0 0 0 0.0 0 631752.727399 0.000190712751081 40.0 10.0 0 0 "" red 9 "" -4 8 0
simundump kenz /kinetics/AKT_activation/PIP3_PDK2/phosp_AKTser473 0 0 0 0.0 0 631752.727399 0.000190703597161 80.0 20.0 0 0 "" red 39 "" 2 13 0
simundump kenz /kinetics/AKT_activation/PIP3_AKT_t308_s473/TSC2_phospho 0 0 0 0.0 0 631752.727399 4.44367850076e-06 24.0 6.0 0 0 "" red 25 "" 8 11 0
simundump kenz /kinetics/TrKB/BDNF_TrKB2_p_clx/PLC_g_phospho 0 0 0 0.0 0 631752.727399 1.27134544788e-05 2.0 0.5 0 0 "" red red "" -3 5 0
simundump kenz /kinetics/TrKB/BDNF_TrKB2_p_clx/SHC_phospho 0 0 0 0.0 0 631752.727399 2.74626727102e-06 1.2 0.3 0 0 "" red red "" -3 2 0
simundump kenz /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_PI3K_clx/Phospho 0 0 0 0.0 0 631752.727399 7.62825575955e-06 16.0 4.0 0 0 "" red brown "" 2 -4 0
simundump kenz /kinetics/PI3K_activation/PI3K_basal/basal_phosp 0 0 0 0.0 0 631752.727399 7.62823542565e-06 16.0 4.0 0 0 "" red 10 "" -3 -16 0
simundump kenz /kinetics/PLC_g/PLCg_basal/PLC_g_phospho 0 0 0 0.0 0 631752.727399 1.27138782747e-05 2.0 0.5 0 0 "" red 33 "" -3 10 0
simundump kenz /kinetics/TSC1_TSC2/TSC1_TSC2/TSC2phospho 0 0 0 0.0 0 631752.727399 0.00050855513099 80.0 20.0 0 0 "" red 51 "" 12 8 0
simundump kenz /kinetics/mTORC1/TOR_Rheb_GTP_clx/S6K_phospho 0 0 0 0.0 0 631752.727399 5.72138253242e-07 0.24 0.06 0 0 "" red 42 "" 12 -16 0
simundump kenz /kinetics/mTORC1/TOR_Rheb_GTP_clx/TOR_4E_BP_phospho 0 0 0 0.0 0 631752.727399 4.23789839879e-06 4.0 1.0 0 0 "" red 44 "" -6 -11 0
simundump kenz /kinetics/mTORC1/TOR_Rheb_GTP_clx/TOR_4E_BP_p 0 0 0 0.0 0 631752.727399 4.23789839879e-06 4.0 1.0 0 0 "" red 44 "" -2 -20 0
simundump kenz /kinetics/S6Kinase/S6K_thr_412/S6_phos 0 0 0 0.0 0 631752.727399 3.05126568936e-07 0.04 0.01 0 0 "" red 48 "" 7 -19 0
simundump kenz /kinetics/S6Kinase/S6K_thr_252/CaMKIII_phospho 0 0 0 0.0 0 631752.727399 7.62823542565e-06 4.0 1.0 0 0 "" red 6 "" -6 18 0
simundump kenz /kinetics/S6Kinase/S6K_thr_252/S6_phospho 0 0 0 0.0 0 631752.727399 3.05127586243e-06 0.4 0.1 0 0 "" red 4 "" -6 16 0
simundump kenz /kinetics/CaMKIII/CaMKIII_CaM_Ca4/phospho 0 0 0 0.0 0 631752.727399 3.81416348242e-05 40.0 10.0 0 0 "" red 58 "" 18 21 0
simundump kenz /kinetics/CaMKIII/CaMKIII_basal/eEF2thr56_basal 0 0 0 0.0 0 631752.727399 3.81416348242e-05 40.0 10.0 0 0 "" red 45 "" 18 15 0
simundump kenz /kinetics/S6Kinase/S6K_basal/CaMKIII_basal 0 0 0 0.0 0 631752.727399 7.62905927837e-05 40.0 10.0 0 0 "" red 45 "" 23 19 0
simundump kenz /kinetics/Translation_elongation/Translation_clx/pro_syn 0 0 0 0.0 0 631752.727399 2.77400365209e-06 0.08 0.02 0 0 "" red 52 "" 17 -1 0
simundump kenz /kinetics/Translation_elongation/Translation_clx/rad_pro_syn 0 0 0 0.0 0 631752.727399 2.54277565496e-06 0.08 0.02 0 0 "" red 52 "" 17 2 0
simundump kenz /kinetics/MAPK/MAPK_p_p/cluster_phospho_S6K 0 0 0 0.0 0 631752.727399 4.40944284322e-07 4.0 1.0 0 0 "" red red "" 0 6 0
simundump kenz /kinetics/MAPK/MAPK_p_p/MAPK_4E_BP_p_p 0 0 0 0.0 0 631752.727399 6.81857127891e-08 0.64 0.16 0 0 "" red orange "" -8 -10 0
simundump kenz /kinetics/MAPK/MAPK_p_p/MAPK_4E_BP_phospho 0 0 0 0.0 0 631752.727399 6.81857127891e-08 0.64 0.16 0 0 "" red 47 "" -9 -3 0
simundump kenz /kinetics/Ras/inact_GEF/basal_GEF_activity 0 0 0 0.0 0 631752.727399 1.51039665586e-08 0.08 0.02 0 0 "" red hotpink "" 12 20 0
simundump kenz /kinetics/Translation_elongation/Basal_Translation/basal_syn 0 0 0 0.0 0 631752.727399 2.77391211289e-06 0.08 0.02 0 0 "" red 53 "" 23 -6 0
simundump kenz /kinetics/Translation_elongation/Basal_Translation/rad_basal_syn 0 0 0 0.0 0 631752.727399 2.77391211289e-06 0.08 0.02 0 0 "" red 53 "" 27 -11 0
simundump kenz /kinetics/40S/40S_basal/basal 0 0 0 0.0 0 631752.727399 3.05127586243e-06 0.4 0.1 0 0 "" red 44 "" 20 4 0
simundump kenz /kinetics/PI3K_activation/PTEN/PIP3_dephosp 0 0 0 0.0 0 631752.727399 0.000524446334593 22.0 5.5 0 0 "" red 37 "" 1 -15 0
simundump kenz /kinetics/Ras/Ras_GTP_PI3K/PIP2_phospho_Ras_GTP 0 0 0 0.0 0 631752.727399 7.62823542565e-06 16.0 4.0 0 0 "" red 31 "" 5 -23 0
simundump kenz /kinetics/AKT_activation/PIP3_AKT_t308_s473/Enz 0 0 0 0.0 0 631752.727399 7.8275123716e-07 0.4 0.1 0 0 "" black 19 "" -2301 -2675 0
simundump kenz /kinetics/HomerPIKE/L.mGluR_p.Homer.PIKE_L.PI3K/Enz 0 0 0 0.0 0 631752.727399 7.60018882881e-06 16.0 4.0 0 0 "" 27 23 "" -1504 2394 0
simundump kenz /kinetics/barr2_signaling/GRK/GRK_binding 0 0 0 0.0 0 631752.727399 1.13950890759e-07 0.66 0.165 0 0 "" 20 black "" 922 -3618 0
simundump kenz /kinetics/Phosphatase/PP2A/mGluR_dephosph 0 0 0 0.0 0 631752.727399 9.02277770246e-08 0.5 0.125 0 0 "" 23 black "" -2074 -1229 0
simundump kenz /kinetics/MAPK/craf_1_p/MEK_phospho 0 0 0 0.0 0 631752.727399 4.79482487041e-06 0.42 0.105 0 0 "" 0 black "" -971 2276 0
simundump kenz /kinetics/MAPK/craf_1_p/MEKp_phospho 0 0 0 0.0 0 631752.727399 4.79482487041e-06 0.42 0.105 0 0 "" 63 black "" 177 2693 0
addmsg /kinetics/PKC/PKC_DAG_AA_p /kinetics/PKC/PKC_active SUMTOTAL n nInit
addmsg /kinetics/PKC/PKC_Ca_memb_p /kinetics/PKC/PKC_active SUMTOTAL n nInit
addmsg /kinetics/PKC/PKC_Ca_AA_p /kinetics/PKC/PKC_active SUMTOTAL n nInit
addmsg /kinetics/PKC/PKC_DAG_memb_p /kinetics/PKC/PKC_active SUMTOTAL n nInit
addmsg /kinetics/PKC/PKC_basal_p /kinetics/PKC/PKC_active SUMTOTAL n nInit
addmsg /kinetics/PKC/PKC_AA_p /kinetics/PKC/PKC_active SUMTOTAL n nInit
addmsg /kinetics/CaMKII/CaMKII_CaM /kinetics/CaMKII/tot_CaM_CaMKII SUMTOTAL n nInit
addmsg /kinetics/CaMKII/CaMKII_thr286_p_CaM /kinetics/CaMKII/tot_CaM_CaMKII SUMTOTAL n nInit
addmsg /kinetics/CaMKII/CaMKII_thr286 /kinetics/CaMKII/tot_autonomous_CaMKII SUMTOTAL n nInit
addmsg /kinetics/CaMKII/CaMKII_p_p_p /kinetics/CaMKII/tot_autonomous_CaMKII SUMTOTAL n nInit
addmsg /kinetics/PP2B/CaMCa4_CaNAB /kinetics/CaM/CaM(Ca)n_CaNAB SUMTOTAL n nInit
addmsg /kinetics/PP2B/CaMCa3_CaNAB /kinetics/CaM/CaM(Ca)n_CaNAB SUMTOTAL n nInit
addmsg /kinetics/PP2B/CaMCa2_CaNAB /kinetics/CaM/CaM(Ca)n_CaNAB SUMTOTAL n nInit
simundump xgraph /graphs/conc1 0 0 99 0.001 0.999 0
simundump xgraph /graphs/conc2 0 0 100 0 1 0
 simundump xplot /graphs/conc1/MAPK_p.Co 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" yellow 0 0 1
simundump xgraph /moregraphs/conc3 0 0 100 0 1 0
simundump xgraph /moregraphs/conc4 0 0 100 0 1 0
 simundump xcoredraw /edit/draw 0 -6 4 -2 6
simundump xtree /edit/draw/tree 0 \
  /kinetics/#[],/kinetics/#[]/#[],/kinetics/#[]/#[]/#[][TYPE!=proto],/kinetics/#[]/#[]/#[][TYPE!=linkinfo]/##[] "edit_elm.D <v>; drag_from_edit.w <d> <S> <x> <y> <z>" auto 0.6
simundump xtext /file/notes 0 1
addmsg /kinetics/PKC/PKC_cytosolic /kinetics/PKC/PKC_act_by_Ca SUBSTRATE n 
addmsg /kinetics/PKC/PKC_act_by_Ca /kinetics/PKC/PKC_cytosolic REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/PKC/PKC_act_by_Ca SUBSTRATE n 
addmsg /kinetics/PKC/PKC_act_by_Ca /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/PKC/PKC_Ca /kinetics/PKC/PKC_act_by_Ca PRODUCT n 
addmsg /kinetics/PKC/PKC_act_by_Ca /kinetics/PKC/PKC_Ca REAC B A
addmsg /kinetics/PKC/PKC_Ca /kinetics/PKC/PKC_act_by_DAG SUBSTRATE n 
addmsg /kinetics/PKC/PKC_act_by_DAG /kinetics/PKC/PKC_Ca REAC A B 
addmsg /kinetics/PKC/DAG /kinetics/PKC/PKC_act_by_DAG SUBSTRATE n 
addmsg /kinetics/PKC/PKC_act_by_DAG /kinetics/PKC/DAG REAC A B 
addmsg /kinetics/PKC/PKC_Ca_DAG /kinetics/PKC/PKC_act_by_DAG PRODUCT n 
addmsg /kinetics/PKC/PKC_act_by_DAG /kinetics/PKC/PKC_Ca_DAG REAC B A
addmsg /kinetics/PKC/PKC_Ca /kinetics/PKC/PKC_Ca_to_memb SUBSTRATE n 
addmsg /kinetics/PKC/PKC_Ca_to_memb /kinetics/PKC/PKC_Ca REAC A B 
addmsg /kinetics/PKC/PKC_Ca_memb_p /kinetics/PKC/PKC_Ca_to_memb PRODUCT n 
addmsg /kinetics/PKC/PKC_Ca_to_memb /kinetics/PKC/PKC_Ca_memb_p REAC B A
addmsg /kinetics/PKC/PKC_Ca_DAG /kinetics/PKC/PKC_DAG_to_memb SUBSTRATE n 
addmsg /kinetics/PKC/PKC_DAG_to_memb /kinetics/PKC/PKC_Ca_DAG REAC A B 
addmsg /kinetics/PKC/PKC_DAG_memb_p /kinetics/PKC/PKC_DAG_to_memb PRODUCT n 
addmsg /kinetics/PKC/PKC_DAG_to_memb /kinetics/PKC/PKC_DAG_memb_p REAC B A
addmsg /kinetics/PKC/PKC_Ca /kinetics/PKC/PKC_act_by_Ca_AA SUBSTRATE n 
addmsg /kinetics/PKC/PKC_act_by_Ca_AA /kinetics/PKC/PKC_Ca REAC A B 
addmsg /kinetics/PKC/Arachidonic_Acid /kinetics/PKC/PKC_act_by_Ca_AA SUBSTRATE n 
addmsg /kinetics/PKC/PKC_act_by_Ca_AA /kinetics/PKC/Arachidonic_Acid REAC A B 
addmsg /kinetics/PKC/PKC_Ca_AA_p /kinetics/PKC/PKC_act_by_Ca_AA PRODUCT n 
addmsg /kinetics/PKC/PKC_act_by_Ca_AA /kinetics/PKC/PKC_Ca_AA_p REAC B A
addmsg /kinetics/PKC/PKC_DAG_AA /kinetics/PKC/PKC_act_by_DAG_AA SUBSTRATE n 
addmsg /kinetics/PKC/PKC_act_by_DAG_AA /kinetics/PKC/PKC_DAG_AA REAC A B 
addmsg /kinetics/PKC/PKC_DAG_AA_p /kinetics/PKC/PKC_act_by_DAG_AA PRODUCT n 
addmsg /kinetics/PKC/PKC_act_by_DAG_AA /kinetics/PKC/PKC_DAG_AA_p REAC B A
addmsg /kinetics/PKC/PKC_cytosolic /kinetics/PKC/PKC_basal_act SUBSTRATE n 
addmsg /kinetics/PKC/PKC_basal_act /kinetics/PKC/PKC_cytosolic REAC A B 
addmsg /kinetics/PKC/PKC_basal_p /kinetics/PKC/PKC_basal_act PRODUCT n 
addmsg /kinetics/PKC/PKC_basal_act /kinetics/PKC/PKC_basal_p REAC B A
addmsg /kinetics/PKC/PKC_cytosolic /kinetics/PKC/PKC_act_by_AA SUBSTRATE n 
addmsg /kinetics/PKC/PKC_act_by_AA /kinetics/PKC/PKC_cytosolic REAC A B 
addmsg /kinetics/PKC/Arachidonic_Acid /kinetics/PKC/PKC_act_by_AA SUBSTRATE n 
addmsg /kinetics/PKC/PKC_act_by_AA /kinetics/PKC/Arachidonic_Acid REAC A B 
addmsg /kinetics/PKC/PKC_AA_p /kinetics/PKC/PKC_act_by_AA PRODUCT n 
addmsg /kinetics/PKC/PKC_act_by_AA /kinetics/PKC/PKC_AA_p REAC B A
addmsg /kinetics/PKC/PKC_cytosolic /kinetics/PKC/PKC_n_DAG SUBSTRATE n 
addmsg /kinetics/PKC/PKC_n_DAG /kinetics/PKC/PKC_cytosolic REAC A B 
addmsg /kinetics/PKC/DAG /kinetics/PKC/PKC_n_DAG SUBSTRATE n 
addmsg /kinetics/PKC/PKC_n_DAG /kinetics/PKC/DAG REAC A B 
addmsg /kinetics/PKC/PKC_DAG /kinetics/PKC/PKC_n_DAG PRODUCT n 
addmsg /kinetics/PKC/PKC_n_DAG /kinetics/PKC/PKC_DAG REAC B A
addmsg /kinetics/PKC/PKC_DAG /kinetics/PKC/PKC_n_DAG_AA SUBSTRATE n 
addmsg /kinetics/PKC/PKC_n_DAG_AA /kinetics/PKC/PKC_DAG REAC A B 
addmsg /kinetics/PKC/Arachidonic_Acid /kinetics/PKC/PKC_n_DAG_AA SUBSTRATE n 
addmsg /kinetics/PKC/PKC_n_DAG_AA /kinetics/PKC/Arachidonic_Acid REAC A B 
addmsg /kinetics/PKC/PKC_DAG_AA /kinetics/PKC/PKC_n_DAG_AA PRODUCT n 
addmsg /kinetics/PKC/PKC_n_DAG_AA /kinetics/PKC/PKC_DAG_AA REAC B A
addmsg /kinetics/PLA2/PLA2_cytosolic /kinetics/PLA2/PLA2_Ca_act SUBSTRATE n 
addmsg /kinetics/PLA2/PLA2_Ca_act /kinetics/PLA2/PLA2_cytosolic REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/PLA2/PLA2_Ca_act SUBSTRATE n 
addmsg /kinetics/PLA2/PLA2_Ca_act /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/PLA2/PLA2_Ca_p /kinetics/PLA2/PLA2_Ca_act PRODUCT n 
addmsg /kinetics/PLA2/PLA2_Ca_act /kinetics/PLA2/PLA2_Ca_p REAC B A
addmsg /kinetics/PLA2/PLA2_cytosolic /kinetics/PLA2/PIP2_PLA2_act SUBSTRATE n 
addmsg /kinetics/PLA2/PIP2_PLA2_act /kinetics/PLA2/PLA2_cytosolic REAC A B 
addmsg /kinetics/PI3K_activation/temp_PIP2 /kinetics/PLA2/PIP2_PLA2_act SUBSTRATE n 
addmsg /kinetics/PLA2/PIP2_PLA2_act /kinetics/PI3K_activation/temp_PIP2 REAC A B 
addmsg /kinetics/PLA2/PIP2_PLA2_p /kinetics/PLA2/PIP2_PLA2_act PRODUCT n 
addmsg /kinetics/PLA2/PIP2_PLA2_act /kinetics/PLA2/PIP2_PLA2_p REAC B A
addmsg /kinetics/PLA2/PLA2_Ca_p /kinetics/PLA2/PIP2_Ca_PLA2_act SUBSTRATE n 
addmsg /kinetics/PLA2/PIP2_Ca_PLA2_act /kinetics/PLA2/PLA2_Ca_p REAC A B 
addmsg /kinetics/PI3K_activation/temp_PIP2 /kinetics/PLA2/PIP2_Ca_PLA2_act SUBSTRATE n 
addmsg /kinetics/PLA2/PIP2_Ca_PLA2_act /kinetics/PI3K_activation/temp_PIP2 REAC A B 
addmsg /kinetics/PLA2/PIP2_Ca_PLA2_p /kinetics/PLA2/PIP2_Ca_PLA2_act PRODUCT n 
addmsg /kinetics/PLA2/PIP2_Ca_PLA2_act /kinetics/PLA2/PIP2_Ca_PLA2_p REAC B A
addmsg /kinetics/PKC/DAG /kinetics/PLA2/DAG_Ca_PLA2_act SUBSTRATE n 
addmsg /kinetics/PLA2/DAG_Ca_PLA2_act /kinetics/PKC/DAG REAC A B 
addmsg /kinetics/PLA2/PLA2_Ca_p /kinetics/PLA2/DAG_Ca_PLA2_act SUBSTRATE n 
addmsg /kinetics/PLA2/DAG_Ca_PLA2_act /kinetics/PLA2/PLA2_Ca_p REAC A B 
addmsg /kinetics/PLA2/DAG_Ca_PLA2_p /kinetics/PLA2/DAG_Ca_PLA2_act PRODUCT n 
addmsg /kinetics/PLA2/DAG_Ca_PLA2_act /kinetics/PLA2/DAG_Ca_PLA2_p REAC B A
addmsg /kinetics/PKC/Arachidonic_Acid /kinetics/PLA2/Degrade_AA SUBSTRATE n 
addmsg /kinetics/PLA2/Degrade_AA /kinetics/PKC/Arachidonic_Acid REAC A B 
addmsg /kinetics/PLA2/APC /kinetics/PLA2/Degrade_AA PRODUCT n 
addmsg /kinetics/PLA2/Degrade_AA /kinetics/PLA2/APC REAC B A
addmsg /kinetics/PLA2/PLA2_p /kinetics/PLA2/PLA2_p_Ca_act SUBSTRATE n 
addmsg /kinetics/PLA2/PLA2_p_Ca_act /kinetics/PLA2/PLA2_p REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/PLA2/PLA2_p_Ca_act SUBSTRATE n 
addmsg /kinetics/PLA2/PLA2_p_Ca_act /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/PLA2/PLA2_p_Ca /kinetics/PLA2/PLA2_p_Ca_act PRODUCT n 
addmsg /kinetics/PLA2/PLA2_p_Ca_act /kinetics/PLA2/PLA2_p_Ca REAC B A
addmsg /kinetics/PLA2/PLA2_p /kinetics/PLA2/dephosphorylate_PLA2_p SUBSTRATE n 
addmsg /kinetics/PLA2/dephosphorylate_PLA2_p /kinetics/PLA2/PLA2_p REAC A B 
addmsg /kinetics/PLA2/PLA2_cytosolic /kinetics/PLA2/dephosphorylate_PLA2_p PRODUCT n 
addmsg /kinetics/PLA2/dephosphorylate_PLA2_p /kinetics/PLA2/PLA2_cytosolic REAC B A
addmsg /kinetics/PLCbeta/PLC /kinetics/PLCbeta/Act_PLC_Ca SUBSTRATE n 
addmsg /kinetics/PLCbeta/Act_PLC_Ca /kinetics/PLCbeta/PLC REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/PLCbeta/Act_PLC_Ca SUBSTRATE n 
addmsg /kinetics/PLCbeta/Act_PLC_Ca /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/PLCbeta/PLC_Ca /kinetics/PLCbeta/Act_PLC_Ca PRODUCT n 
addmsg /kinetics/PLCbeta/Act_PLC_Ca /kinetics/PLCbeta/PLC_Ca REAC B A
addmsg /kinetics/PI3K_activation/IP3 /kinetics/PLCbeta/Degrade_IP3 SUBSTRATE n 
addmsg /kinetics/PLCbeta/Degrade_IP3 /kinetics/PI3K_activation/IP3 REAC A B 
addmsg /kinetics/PLCbeta/Inositol /kinetics/PLCbeta/Degrade_IP3 PRODUCT n 
addmsg /kinetics/PLCbeta/Degrade_IP3 /kinetics/PLCbeta/Inositol REAC B A
addmsg /kinetics/PKC/DAG /kinetics/PLCbeta/Degrade_DAG SUBSTRATE n 
addmsg /kinetics/PLCbeta/Degrade_DAG /kinetics/PKC/DAG REAC A B 
addmsg /kinetics/PC /kinetics/PLCbeta/Degrade_DAG PRODUCT n 
addmsg /kinetics/PLCbeta/Degrade_DAG /kinetics/PC REAC B A
addmsg /kinetics/PLCbeta/PLC_Ca /kinetics/PLCbeta/Act_PLC_by_Gq SUBSTRATE n 
addmsg /kinetics/PLCbeta/Act_PLC_by_Gq /kinetics/PLCbeta/PLC_Ca REAC A B 
addmsg /kinetics/Gprotein/G_pGTP /kinetics/PLCbeta/Act_PLC_by_Gq SUBSTRATE n 
addmsg /kinetics/PLCbeta/Act_PLC_by_Gq /kinetics/Gprotein/G_pGTP REAC A B 
addmsg /kinetics/PLCbeta/PLC_Ca_Gq /kinetics/PLCbeta/Act_PLC_by_Gq PRODUCT n 
addmsg /kinetics/PLCbeta/Act_PLC_by_Gq /kinetics/PLCbeta/PLC_Ca_Gq REAC B A
addmsg /kinetics/PLCbeta/PLC_Ca_Gq /kinetics/PLCbeta/Inact_PLC_Gq SUBSTRATE n 
addmsg /kinetics/PLCbeta/Inact_PLC_Gq /kinetics/PLCbeta/PLC_Ca_Gq REAC A B 
addmsg /kinetics/PLCbeta/PLC_Ca /kinetics/PLCbeta/Inact_PLC_Gq PRODUCT n 
addmsg /kinetics/PLCbeta/Inact_PLC_Gq /kinetics/PLCbeta/PLC_Ca REAC B A
addmsg /kinetics/Gprotein/G_pGDP /kinetics/PLCbeta/Inact_PLC_Gq PRODUCT n 
addmsg /kinetics/PLCbeta/Inact_PLC_Gq /kinetics/Gprotein/G_pGDP REAC B A
addmsg /kinetics/PLCbeta/PLC /kinetics/PLCbeta/PLC_bind_Gq SUBSTRATE n 
addmsg /kinetics/PLCbeta/PLC_bind_Gq /kinetics/PLCbeta/PLC REAC A B 
addmsg /kinetics/Gprotein/G_pGTP /kinetics/PLCbeta/PLC_bind_Gq SUBSTRATE n 
addmsg /kinetics/PLCbeta/PLC_bind_Gq /kinetics/Gprotein/G_pGTP REAC A B 
addmsg /kinetics/PLCbeta/PLC_Gq /kinetics/PLCbeta/PLC_bind_Gq PRODUCT n 
addmsg /kinetics/PLCbeta/PLC_bind_Gq /kinetics/PLCbeta/PLC_Gq REAC B A
addmsg /kinetics/PLCbeta/PLC_Gq /kinetics/PLCbeta/PLC_Gq_bind_Ca SUBSTRATE n 
addmsg /kinetics/PLCbeta/PLC_Gq_bind_Ca /kinetics/PLCbeta/PLC_Gq REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/PLCbeta/PLC_Gq_bind_Ca SUBSTRATE n 
addmsg /kinetics/PLCbeta/PLC_Gq_bind_Ca /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/PLCbeta/PLC_Ca_Gq /kinetics/PLCbeta/PLC_Gq_bind_Ca PRODUCT n 
addmsg /kinetics/PLCbeta/PLC_Gq_bind_Ca /kinetics/PLCbeta/PLC_Ca_Gq REAC B A
addmsg /kinetics/mGluR/Glutamate /kinetics/mGluR/RecLigandBinding SUBSTRATE n 
addmsg /kinetics/mGluR/RecLigandBinding /kinetics/mGluR/Glutamate REAC A B 
addmsg /kinetics/mGluR/mGluR /kinetics/mGluR/RecLigandBinding SUBSTRATE n 
addmsg /kinetics/mGluR/RecLigandBinding /kinetics/mGluR/mGluR REAC A B 
addmsg /kinetics/mGluR/Rec_Glu /kinetics/mGluR/RecLigandBinding PRODUCT n 
addmsg /kinetics/mGluR/RecLigandBinding /kinetics/mGluR/Rec_Glu REAC B A
addmsg /kinetics/Gprotein/G_GDP /kinetics/Gprotein/Basal_Act_Gq SUBSTRATE n 
addmsg /kinetics/Gprotein/Basal_Act_Gq /kinetics/Gprotein/G_GDP REAC A B 
addmsg /kinetics/Gprotein/BetaGamma /kinetics/Gprotein/Basal_Act_Gq PRODUCT n 
addmsg /kinetics/Gprotein/Basal_Act_Gq /kinetics/Gprotein/BetaGamma REAC B A
addmsg /kinetics/Gprotein/G_pGTP /kinetics/Gprotein/Basal_Act_Gq PRODUCT n 
addmsg /kinetics/Gprotein/Basal_Act_Gq /kinetics/Gprotein/G_pGTP REAC B A
addmsg /kinetics/Gprotein/BetaGamma /kinetics/Gprotein/Trimerize_G SUBSTRATE n 
addmsg /kinetics/Gprotein/Trimerize_G /kinetics/Gprotein/BetaGamma REAC A B 
addmsg /kinetics/Gprotein/G_pGDP /kinetics/Gprotein/Trimerize_G SUBSTRATE n 
addmsg /kinetics/Gprotein/Trimerize_G /kinetics/Gprotein/G_pGDP REAC A B 
addmsg /kinetics/Gprotein/G_GDP /kinetics/Gprotein/Trimerize_G PRODUCT n 
addmsg /kinetics/Gprotein/Trimerize_G /kinetics/Gprotein/G_GDP REAC B A
addmsg /kinetics/Gprotein/G_pGTP /kinetics/Gprotein/Inact_Gq SUBSTRATE n 
addmsg /kinetics/Gprotein/Inact_Gq /kinetics/Gprotein/G_pGTP REAC A B 
addmsg /kinetics/Gprotein/G_pGDP /kinetics/Gprotein/Inact_Gq PRODUCT n 
addmsg /kinetics/Gprotein/Inact_Gq /kinetics/Gprotein/G_pGDP REAC B A
addmsg /kinetics/Gprotein/G_GDP /kinetics/mGluR/Rec_Glu_bind_Gq SUBSTRATE n 
addmsg /kinetics/mGluR/Rec_Glu_bind_Gq /kinetics/Gprotein/G_GDP REAC A B 
addmsg /kinetics/mGluR/Rec_Glu /kinetics/mGluR/Rec_Glu_bind_Gq SUBSTRATE n 
addmsg /kinetics/mGluR/Rec_Glu_bind_Gq /kinetics/mGluR/Rec_Glu REAC A B 
addmsg /kinetics/mGluR/Rec_Glu_Gq /kinetics/mGluR/Rec_Glu_bind_Gq PRODUCT n 
addmsg /kinetics/mGluR/Rec_Glu_bind_Gq /kinetics/mGluR/Rec_Glu_Gq REAC B A
addmsg /kinetics/mGluR/Glutamate /kinetics/mGluR/Glu_bind_Rec_Gq SUBSTRATE n 
addmsg /kinetics/mGluR/Glu_bind_Rec_Gq /kinetics/mGluR/Glutamate REAC A B 
addmsg /kinetics/mGluR/Rec_Gq /kinetics/mGluR/Glu_bind_Rec_Gq SUBSTRATE n 
addmsg /kinetics/mGluR/Glu_bind_Rec_Gq /kinetics/mGluR/Rec_Gq REAC A B 
addmsg /kinetics/mGluR/Rec_Glu_Gq /kinetics/mGluR/Glu_bind_Rec_Gq PRODUCT n 
addmsg /kinetics/mGluR/Glu_bind_Rec_Gq /kinetics/mGluR/Rec_Glu_Gq REAC B A
addmsg /kinetics/mGluR/Rec_Glu_Gq /kinetics/mGluR/Activate_Gq SUBSTRATE n 
addmsg /kinetics/mGluR/Activate_Gq /kinetics/mGluR/Rec_Glu_Gq REAC A B 
addmsg /kinetics/Gprotein/BetaGamma /kinetics/mGluR/Activate_Gq PRODUCT n 
addmsg /kinetics/mGluR/Activate_Gq /kinetics/Gprotein/BetaGamma REAC B A
addmsg /kinetics/Gprotein/G_pGTP /kinetics/mGluR/Activate_Gq PRODUCT n 
addmsg /kinetics/mGluR/Activate_Gq /kinetics/Gprotein/G_pGTP REAC B A
addmsg /kinetics/mGluR/Rec_Glu /kinetics/mGluR/Activate_Gq PRODUCT n 
addmsg /kinetics/mGluR/Activate_Gq /kinetics/mGluR/Rec_Glu REAC B A
addmsg /kinetics/Gprotein/G_GDP /kinetics/mGluR/Rec_bind_Gq SUBSTRATE n 
addmsg /kinetics/mGluR/Rec_bind_Gq /kinetics/Gprotein/G_GDP REAC A B 
addmsg /kinetics/mGluR/mGluR /kinetics/mGluR/Rec_bind_Gq SUBSTRATE n 
addmsg /kinetics/mGluR/Rec_bind_Gq /kinetics/mGluR/mGluR REAC A B 
addmsg /kinetics/mGluR/Rec_Gq /kinetics/mGluR/Rec_bind_Gq PRODUCT n 
addmsg /kinetics/mGluR/Rec_bind_Gq /kinetics/mGluR/Rec_Gq REAC B A
addmsg /kinetics/mGluR/Rec_Gq /kinetics/mGluRAntag/Antag_bind_Rec_Gq SUBSTRATE n 
addmsg /kinetics/mGluRAntag/Antag_bind_Rec_Gq /kinetics/mGluR/Rec_Gq REAC A B 
addmsg /kinetics/mGluRAntag/mGluRAntag /kinetics/mGluRAntag/Antag_bind_Rec_Gq SUBSTRATE n 
addmsg /kinetics/mGluRAntag/Antag_bind_Rec_Gq /kinetics/mGluRAntag/mGluRAntag REAC A B 
addmsg /kinetics/mGluRAntag/Blocked_Rec_Gq /kinetics/mGluRAntag/Antag_bind_Rec_Gq PRODUCT n 
addmsg /kinetics/mGluRAntag/Antag_bind_Rec_Gq /kinetics/mGluRAntag/Blocked_Rec_Gq REAC B A
addmsg /kinetics/MAPK/craf_1_p /kinetics/Ras/Ras_act_craf SUBSTRATE n 
addmsg /kinetics/Ras/Ras_act_craf /kinetics/MAPK/craf_1_p REAC A B 
addmsg /kinetics/Ras/GTP_Ras /kinetics/Ras/Ras_act_craf SUBSTRATE n 
addmsg /kinetics/Ras/Ras_act_craf /kinetics/Ras/GTP_Ras REAC A B 
addmsg /kinetics/MAPK/Raf_p_GTP_Ras /kinetics/Ras/Ras_act_craf PRODUCT n 
addmsg /kinetics/Ras/Ras_act_craf /kinetics/MAPK/Raf_p_GTP_Ras REAC B A
addmsg /kinetics/Gprotein/BetaGamma /kinetics/Ras/bg_act_GEF SUBSTRATE n 
addmsg /kinetics/Ras/bg_act_GEF /kinetics/Gprotein/BetaGamma REAC A B 
addmsg /kinetics/Ras/inact_GEF /kinetics/Ras/bg_act_GEF SUBSTRATE n 
addmsg /kinetics/Ras/bg_act_GEF /kinetics/Ras/inact_GEF REAC A B 
addmsg /kinetics/Ras/GEF_Gprot_bg /kinetics/Ras/bg_act_GEF PRODUCT n 
addmsg /kinetics/Ras/bg_act_GEF /kinetics/Ras/GEF_Gprot_bg REAC B A
addmsg /kinetics/Ras/GEF_p /kinetics/Ras/dephosph_GEF SUBSTRATE n 
addmsg /kinetics/Ras/dephosph_GEF /kinetics/Ras/GEF_p REAC A B 
addmsg /kinetics/Ras/inact_GEF /kinetics/Ras/dephosph_GEF PRODUCT n 
addmsg /kinetics/Ras/dephosph_GEF /kinetics/Ras/inact_GEF REAC B A
addmsg /kinetics/Ras/GTP_Ras /kinetics/Ras/Ras_intrinsic_GTPase SUBSTRATE n 
addmsg /kinetics/Ras/Ras_intrinsic_GTPase /kinetics/Ras/GTP_Ras REAC A B 
addmsg /kinetics/Ras/GDP_Ras /kinetics/Ras/Ras_intrinsic_GTPase PRODUCT n 
addmsg /kinetics/Ras/Ras_intrinsic_GTPase /kinetics/Ras/GDP_Ras REAC B A
addmsg /kinetics/Ras/GAP_p /kinetics/Ras/dephosph_GAP SUBSTRATE n 
addmsg /kinetics/Ras/dephosph_GAP /kinetics/Ras/GAP_p REAC A B 
addmsg /kinetics/Ras/GAP /kinetics/Ras/dephosph_GAP PRODUCT n 
addmsg /kinetics/Ras/dephosph_GAP /kinetics/Ras/GAP REAC B A
addmsg /kinetics/Ras/inact_GEF /kinetics/Ras/CaM_bind_GEF SUBSTRATE n 
addmsg /kinetics/Ras/CaM_bind_GEF /kinetics/Ras/inact_GEF REAC A B 
addmsg /kinetics/CaM/CaM_Ca4 /kinetics/Ras/CaM_bind_GEF SUBSTRATE n 
addmsg /kinetics/Ras/CaM_bind_GEF /kinetics/CaM/CaM_Ca4 REAC A B 
addmsg /kinetics/Ras/CaM_GEF /kinetics/Ras/CaM_bind_GEF PRODUCT n 
addmsg /kinetics/Ras/CaM_bind_GEF /kinetics/Ras/CaM_GEF REAC B A
addmsg /kinetics/Ras/inact_GEF_p /kinetics/Ras/dephosph_inact_GEF_p SUBSTRATE n 
addmsg /kinetics/Ras/dephosph_inact_GEF_p /kinetics/Ras/inact_GEF_p REAC A B 
addmsg /kinetics/Ras/inact_GEF /kinetics/Ras/dephosph_inact_GEF_p PRODUCT n 
addmsg /kinetics/Ras/dephosph_inact_GEF_p /kinetics/Ras/inact_GEF REAC B A
addmsg /kinetics/EGFR/EGFR /kinetics/EGFR/act_EGFR SUBSTRATE n 
addmsg /kinetics/EGFR/act_EGFR /kinetics/EGFR/EGFR REAC A B 
addmsg /kinetics/EGFR/EGF /kinetics/EGFR/act_EGFR SUBSTRATE n 
addmsg /kinetics/EGFR/act_EGFR /kinetics/EGFR/EGF REAC A B 
addmsg /kinetics/EGFR/L.EGFR /kinetics/EGFR/act_EGFR PRODUCT n 
addmsg /kinetics/EGFR/act_EGFR /kinetics/EGFR/L.EGFR REAC B A
addmsg /kinetics/Sos/SHC_p /kinetics/Sos/SHC_p_dephospho SUBSTRATE n 
addmsg /kinetics/Sos/SHC_p_dephospho /kinetics/Sos/SHC_p REAC A B 
addmsg /kinetics/Sos/SHC /kinetics/Sos/SHC_p_dephospho PRODUCT n 
addmsg /kinetics/Sos/SHC_p_dephospho /kinetics/Sos/SHC REAC B A
addmsg /kinetics/EGFR/L.EGFR /kinetics/EGFR/Internalize SUBSTRATE n 
addmsg /kinetics/EGFR/Internalize /kinetics/EGFR/L.EGFR REAC A B 
addmsg /kinetics/EGFR/Internal_L.EGFR /kinetics/EGFR/Internalize PRODUCT n 
addmsg /kinetics/EGFR/Internalize /kinetics/EGFR/Internal_L.EGFR REAC B A
addmsg /kinetics/Sos/SHC_p /kinetics/Sos/SHC_bind_Sos.Grb2 SUBSTRATE n 
addmsg /kinetics/Sos/SHC_bind_Sos.Grb2 /kinetics/Sos/SHC_p REAC A B 
addmsg /kinetics/Sos/Sos.Grb2 /kinetics/Sos/SHC_bind_Sos.Grb2 SUBSTRATE n 
addmsg /kinetics/Sos/SHC_bind_Sos.Grb2 /kinetics/Sos/Sos.Grb2 REAC A B 
addmsg /kinetics/Sos/SHC_p.Sos.Grb2 /kinetics/Sos/SHC_bind_Sos.Grb2 PRODUCT n 
addmsg /kinetics/Sos/SHC_bind_Sos.Grb2 /kinetics/Sos/SHC_p.Sos.Grb2 REAC B A
addmsg /kinetics/Sos/Grb2 /kinetics/Sos/Grb2_bind_Sos_p SUBSTRATE n 
addmsg /kinetics/Sos/Grb2_bind_Sos_p /kinetics/Sos/Grb2 REAC A B 
addmsg /kinetics/Sos/Sos_p /kinetics/Sos/Grb2_bind_Sos_p SUBSTRATE n 
addmsg /kinetics/Sos/Grb2_bind_Sos_p /kinetics/Sos/Sos_p REAC A B 
addmsg /kinetics/Sos/Sos_p.Grb2 /kinetics/Sos/Grb2_bind_Sos_p PRODUCT n 
addmsg /kinetics/Sos/Grb2_bind_Sos_p /kinetics/Sos/Sos_p.Grb2 REAC B A
addmsg /kinetics/Sos/Sos_p /kinetics/Sos/dephosph_Sos SUBSTRATE n 
addmsg /kinetics/Sos/dephosph_Sos /kinetics/Sos/Sos_p REAC A B 
addmsg /kinetics/Sos/Sos /kinetics/Sos/dephosph_Sos PRODUCT n 
addmsg /kinetics/Sos/dephosph_Sos /kinetics/Sos/Sos REAC B A
addmsg /kinetics/Sos/Grb2 /kinetics/Sos/Grb2_bind_Sos SUBSTRATE n 
addmsg /kinetics/Sos/Grb2_bind_Sos /kinetics/Sos/Grb2 REAC A B 
addmsg /kinetics/Sos/Sos /kinetics/Sos/Grb2_bind_Sos SUBSTRATE n 
addmsg /kinetics/Sos/Grb2_bind_Sos /kinetics/Sos/Sos REAC A B 
addmsg /kinetics/Sos/Sos.Grb2 /kinetics/Sos/Grb2_bind_Sos PRODUCT n 
addmsg /kinetics/Sos/Grb2_bind_Sos /kinetics/Sos/Sos.Grb2 REAC B A
addmsg /kinetics/PLC_g/PLC_g /kinetics/PLC_g/Ca_act_PLC_g SUBSTRATE n 
addmsg /kinetics/PLC_g/Ca_act_PLC_g /kinetics/PLC_g/PLC_g REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/PLC_g/Ca_act_PLC_g SUBSTRATE n 
addmsg /kinetics/PLC_g/Ca_act_PLC_g /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/PLC_g/Ca.PLC_g /kinetics/PLC_g/Ca_act_PLC_g PRODUCT n 
addmsg /kinetics/PLC_g/Ca_act_PLC_g /kinetics/PLC_g/Ca.PLC_g REAC B A
addmsg /kinetics/PLC_g/PLC_g_p /kinetics/PLC_g/Ca_act_PLC_g_p SUBSTRATE n 
addmsg /kinetics/PLC_g/Ca_act_PLC_g_p /kinetics/PLC_g/PLC_g_p REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/PLC_g/Ca_act_PLC_g_p SUBSTRATE n 
addmsg /kinetics/PLC_g/Ca_act_PLC_g_p /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/PLC_g/Ca.PLC_g_p /kinetics/PLC_g/Ca_act_PLC_g_p PRODUCT n 
addmsg /kinetics/PLC_g/Ca_act_PLC_g_p /kinetics/PLC_g/Ca.PLC_g_p REAC B A
addmsg /kinetics/PLC_g/Ca.PLC_g_p /kinetics/PLC_g/dephosph_PLC_g SUBSTRATE n 
addmsg /kinetics/PLC_g/dephosph_PLC_g /kinetics/PLC_g/Ca.PLC_g_p REAC A B 
addmsg /kinetics/PLC_g/Ca.PLC_g /kinetics/PLC_g/dephosph_PLC_g PRODUCT n 
addmsg /kinetics/PLC_g/dephosph_PLC_g /kinetics/PLC_g/Ca.PLC_g REAC B A
addmsg /kinetics/CaM/CaM_Ca4 /kinetics/CaMKII/CaMKII_bind_CaM SUBSTRATE n 
addmsg /kinetics/CaMKII/CaMKII_bind_CaM /kinetics/CaM/CaM_Ca4 REAC A B 
addmsg /kinetics/CaMKII/CaMKII /kinetics/CaMKII/CaMKII_bind_CaM SUBSTRATE n 
addmsg /kinetics/CaMKII/CaMKII_bind_CaM /kinetics/CaMKII/CaMKII REAC A B 
addmsg /kinetics/CaMKII/CaMKII_CaM /kinetics/CaMKII/CaMKII_bind_CaM PRODUCT n 
addmsg /kinetics/CaMKII/CaMKII_bind_CaM /kinetics/CaMKII/CaMKII_CaM REAC B A
addmsg /kinetics/CaM/CaM_Ca4 /kinetics/CaMKII/CaMKII_thr286_bind_CaM SUBSTRATE n 
addmsg /kinetics/CaMKII/CaMKII_thr286_bind_CaM /kinetics/CaM/CaM_Ca4 REAC A B 
addmsg /kinetics/CaMKII/CaMKII_thr286 /kinetics/CaMKII/CaMKII_thr286_bind_CaM SUBSTRATE n 
addmsg /kinetics/CaMKII/CaMKII_thr286_bind_CaM /kinetics/CaMKII/CaMKII_thr286 REAC A B 
addmsg /kinetics/CaMKII/CaMKII_thr286_p_CaM /kinetics/CaMKII/CaMKII_thr286_bind_CaM PRODUCT n 
addmsg /kinetics/CaMKII/CaMKII_thr286_bind_CaM /kinetics/CaMKII/CaMKII_thr286_p_CaM REAC B A
addmsg /kinetics/CaMKII/CaMKII /kinetics/CaMKII/basal_activity SUBSTRATE n 
addmsg /kinetics/CaMKII/basal_activity /kinetics/CaMKII/CaMKII REAC A B 
addmsg /kinetics/CaMKII/CaMKII_thr286 /kinetics/CaMKII/basal_activity PRODUCT n 
addmsg /kinetics/CaMKII/basal_activity /kinetics/CaMKII/CaMKII_thr286 REAC B A
addmsg /kinetics/CaM/CaM /kinetics/CaM/CaM_TR2_bind_Ca SUBSTRATE n 
addmsg /kinetics/CaM/CaM_TR2_bind_Ca /kinetics/CaM/CaM REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/CaM/CaM_TR2_bind_Ca SUBSTRATE n 
addmsg /kinetics/CaM/CaM_TR2_bind_Ca /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/CaM/CaM_TR2_bind_Ca SUBSTRATE n 
addmsg /kinetics/CaM/CaM_TR2_bind_Ca /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/CaM/CaM_TR2_Ca2 /kinetics/CaM/CaM_TR2_bind_Ca PRODUCT n 
addmsg /kinetics/CaM/CaM_TR2_bind_Ca /kinetics/CaM/CaM_TR2_Ca2 REAC B A
addmsg /kinetics/CaM/CaM_TR2_Ca2 /kinetics/CaM/CaM_TR2_Ca2_bind_Ca SUBSTRATE n 
addmsg /kinetics/CaM/CaM_TR2_Ca2_bind_Ca /kinetics/CaM/CaM_TR2_Ca2 REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/CaM/CaM_TR2_Ca2_bind_Ca SUBSTRATE n 
addmsg /kinetics/CaM/CaM_TR2_Ca2_bind_Ca /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/CaM/CaM_Ca3 /kinetics/CaM/CaM_TR2_Ca2_bind_Ca PRODUCT n 
addmsg /kinetics/CaM/CaM_TR2_Ca2_bind_Ca /kinetics/CaM/CaM_Ca3 REAC B A
addmsg /kinetics/CaM/CaM_Ca3 /kinetics/CaM/CaM_Ca3_bind_Ca SUBSTRATE n 
addmsg /kinetics/CaM/CaM_Ca3_bind_Ca /kinetics/CaM/CaM_Ca3 REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/CaM/CaM_Ca3_bind_Ca SUBSTRATE n 
addmsg /kinetics/CaM/CaM_Ca3_bind_Ca /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/CaM/CaM_Ca4 /kinetics/CaM/CaM_Ca3_bind_Ca PRODUCT n 
addmsg /kinetics/CaM/CaM_Ca3_bind_Ca /kinetics/CaM/CaM_Ca4 REAC B A
addmsg /kinetics/CaM/CaM /kinetics/CaM/neurogranin_bind_CaM SUBSTRATE n 
addmsg /kinetics/CaM/neurogranin_bind_CaM /kinetics/CaM/CaM REAC A B 
addmsg /kinetics/CaM/neurogranin /kinetics/CaM/neurogranin_bind_CaM SUBSTRATE n 
addmsg /kinetics/CaM/neurogranin_bind_CaM /kinetics/CaM/neurogranin REAC A B 
addmsg /kinetics/CaM/neurogranin_CaM /kinetics/CaM/neurogranin_bind_CaM PRODUCT n 
addmsg /kinetics/CaM/neurogranin_bind_CaM /kinetics/CaM/neurogranin_CaM REAC B A
addmsg /kinetics/CaM/neurogranin_p /kinetics/CaM/dephosph_neurogranin SUBSTRATE n 
addmsg /kinetics/CaM/dephosph_neurogranin /kinetics/CaM/neurogranin_p REAC A B 
addmsg /kinetics/CaM/neurogranin /kinetics/CaM/dephosph_neurogranin PRODUCT n 
addmsg /kinetics/CaM/dephosph_neurogranin /kinetics/CaM/neurogranin REAC B A
addmsg /kinetics/PP1/PP1_active /kinetics/PP1/Inact_PP1 SUBSTRATE n 
addmsg /kinetics/PP1/Inact_PP1 /kinetics/PP1/PP1_active REAC A B 
addmsg /kinetics/PP1/I1_p /kinetics/PP1/Inact_PP1 SUBSTRATE n 
addmsg /kinetics/PP1/Inact_PP1 /kinetics/PP1/I1_p REAC A B 
addmsg /kinetics/PP1/PP1_I1_p /kinetics/PP1/Inact_PP1 PRODUCT n 
addmsg /kinetics/PP1/Inact_PP1 /kinetics/PP1/PP1_I1_p REAC B A
addmsg /kinetics/PP1/PP1_I1 /kinetics/PP1/dissoc_PP1_I1 SUBSTRATE n 
addmsg /kinetics/PP1/dissoc_PP1_I1 /kinetics/PP1/PP1_I1 REAC A B 
addmsg /kinetics/PP1/PP1_active /kinetics/PP1/dissoc_PP1_I1 PRODUCT n 
addmsg /kinetics/PP1/dissoc_PP1_I1 /kinetics/PP1/PP1_active REAC B A
addmsg /kinetics/PP1/I1 /kinetics/PP1/dissoc_PP1_I1 PRODUCT n 
addmsg /kinetics/PP1/dissoc_PP1_I1 /kinetics/PP1/I1 REAC B A
addmsg /kinetics/PP2B/CaNAB_Ca2 /kinetics/PP2B/Ca_bind_CaNAB_Ca2 SUBSTRATE n 
addmsg /kinetics/PP2B/Ca_bind_CaNAB_Ca2 /kinetics/PP2B/CaNAB_Ca2 REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/PP2B/Ca_bind_CaNAB_Ca2 SUBSTRATE n 
addmsg /kinetics/PP2B/Ca_bind_CaNAB_Ca2 /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/PP2B/Ca_bind_CaNAB_Ca2 SUBSTRATE n 
addmsg /kinetics/PP2B/Ca_bind_CaNAB_Ca2 /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/CaM/CaNAB_Ca4 /kinetics/PP2B/Ca_bind_CaNAB_Ca2 PRODUCT n 
addmsg /kinetics/PP2B/Ca_bind_CaNAB_Ca2 /kinetics/CaM/CaNAB_Ca4 REAC B A
addmsg /kinetics/PP2B/CaNAB /kinetics/PP2B/Ca_bind_CaNAB SUBSTRATE n 
addmsg /kinetics/PP2B/Ca_bind_CaNAB /kinetics/PP2B/CaNAB REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/PP2B/Ca_bind_CaNAB SUBSTRATE n 
addmsg /kinetics/PP2B/Ca_bind_CaNAB /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/PP2B/Ca_bind_CaNAB SUBSTRATE n 
addmsg /kinetics/PP2B/Ca_bind_CaNAB /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/PP2B/CaNAB_Ca2 /kinetics/PP2B/Ca_bind_CaNAB PRODUCT n 
addmsg /kinetics/PP2B/Ca_bind_CaNAB /kinetics/PP2B/CaNAB_Ca2 REAC B A
addmsg /kinetics/CaM/CaM_TR2_Ca2 /kinetics/PP2B/CaM_Ca2_bind_CaNAB SUBSTRATE n 
addmsg /kinetics/PP2B/CaM_Ca2_bind_CaNAB /kinetics/CaM/CaM_TR2_Ca2 REAC A B 
addmsg /kinetics/CaM/CaNAB_Ca4 /kinetics/PP2B/CaM_Ca2_bind_CaNAB SUBSTRATE n 
addmsg /kinetics/PP2B/CaM_Ca2_bind_CaNAB /kinetics/CaM/CaNAB_Ca4 REAC A B 
addmsg /kinetics/PP2B/CaMCa2_CaNAB /kinetics/PP2B/CaM_Ca2_bind_CaNAB PRODUCT n 
addmsg /kinetics/PP2B/CaM_Ca2_bind_CaNAB /kinetics/PP2B/CaMCa2_CaNAB REAC B A
addmsg /kinetics/CaM/CaM_Ca3 /kinetics/PP2B/CaMCa3_bind_CaNAB SUBSTRATE n 
addmsg /kinetics/PP2B/CaMCa3_bind_CaNAB /kinetics/CaM/CaM_Ca3 REAC A B 
addmsg /kinetics/CaM/CaNAB_Ca4 /kinetics/PP2B/CaMCa3_bind_CaNAB SUBSTRATE n 
addmsg /kinetics/PP2B/CaMCa3_bind_CaNAB /kinetics/CaM/CaNAB_Ca4 REAC A B 
addmsg /kinetics/PP2B/CaMCa3_CaNAB /kinetics/PP2B/CaMCa3_bind_CaNAB PRODUCT n 
addmsg /kinetics/PP2B/CaMCa3_bind_CaNAB /kinetics/PP2B/CaMCa3_CaNAB REAC B A
addmsg /kinetics/CaM/CaM_Ca4 /kinetics/PP2B/CaMCa4_bind_CaNAB SUBSTRATE n 
addmsg /kinetics/PP2B/CaMCa4_bind_CaNAB /kinetics/CaM/CaM_Ca4 REAC A B 
addmsg /kinetics/CaM/CaNAB_Ca4 /kinetics/PP2B/CaMCa4_bind_CaNAB SUBSTRATE n 
addmsg /kinetics/PP2B/CaMCa4_bind_CaNAB /kinetics/CaM/CaNAB_Ca4 REAC A B 
addmsg /kinetics/PP2B/CaMCa4_CaNAB /kinetics/PP2B/CaMCa4_bind_CaNAB PRODUCT n 
addmsg /kinetics/PP2B/CaMCa4_bind_CaNAB /kinetics/PP2B/CaMCa4_CaNAB REAC B A
addmsg /kinetics/PKA/R2C2 /kinetics/PKA/cAMP_bind_site_B1 SUBSTRATE n 
addmsg /kinetics/PKA/cAMP_bind_site_B1 /kinetics/PKA/R2C2 REAC A B 
addmsg /kinetics/AC/cAMP /kinetics/PKA/cAMP_bind_site_B1 SUBSTRATE n 
addmsg /kinetics/PKA/cAMP_bind_site_B1 /kinetics/AC/cAMP REAC A B 
addmsg /kinetics/PKA/R2C2_cAMP /kinetics/PKA/cAMP_bind_site_B1 PRODUCT n 
addmsg /kinetics/PKA/cAMP_bind_site_B1 /kinetics/PKA/R2C2_cAMP REAC B A
addmsg /kinetics/PKA/R2C2_cAMP /kinetics/PKA/cAMP_bind_site_B2 SUBSTRATE n 
addmsg /kinetics/PKA/cAMP_bind_site_B2 /kinetics/PKA/R2C2_cAMP REAC A B 
addmsg /kinetics/AC/cAMP /kinetics/PKA/cAMP_bind_site_B2 SUBSTRATE n 
addmsg /kinetics/PKA/cAMP_bind_site_B2 /kinetics/AC/cAMP REAC A B 
addmsg /kinetics/PKA/R2C2_cAMP2 /kinetics/PKA/cAMP_bind_site_B2 PRODUCT n 
addmsg /kinetics/PKA/cAMP_bind_site_B2 /kinetics/PKA/R2C2_cAMP2 REAC B A
addmsg /kinetics/PKA/R2C2_cAMP2 /kinetics/PKA/cAMP_bind_site_A1 SUBSTRATE n 
addmsg /kinetics/PKA/cAMP_bind_site_A1 /kinetics/PKA/R2C2_cAMP2 REAC A B 
addmsg /kinetics/AC/cAMP /kinetics/PKA/cAMP_bind_site_A1 SUBSTRATE n 
addmsg /kinetics/PKA/cAMP_bind_site_A1 /kinetics/AC/cAMP REAC A B 
addmsg /kinetics/PKA/R2C2_cAMP3 /kinetics/PKA/cAMP_bind_site_A1 PRODUCT n 
addmsg /kinetics/PKA/cAMP_bind_site_A1 /kinetics/PKA/R2C2_cAMP3 REAC B A
addmsg /kinetics/PKA/R2C2_cAMP3 /kinetics/PKA/cAMP_bind_site_A2 SUBSTRATE n 
addmsg /kinetics/PKA/cAMP_bind_site_A2 /kinetics/PKA/R2C2_cAMP3 REAC A B 
addmsg /kinetics/AC/cAMP /kinetics/PKA/cAMP_bind_site_A2 SUBSTRATE n 
addmsg /kinetics/PKA/cAMP_bind_site_A2 /kinetics/AC/cAMP REAC A B 
addmsg /kinetics/PKA/R2C2_cAMP4 /kinetics/PKA/cAMP_bind_site_A2 PRODUCT n 
addmsg /kinetics/PKA/cAMP_bind_site_A2 /kinetics/PKA/R2C2_cAMP4 REAC B A
addmsg /kinetics/PKA/R2C2_cAMP4 /kinetics/PKA/Release_C1 SUBSTRATE n 
addmsg /kinetics/PKA/Release_C1 /kinetics/PKA/R2C2_cAMP4 REAC A B 
addmsg /kinetics/PKA/PKA_active /kinetics/PKA/Release_C1 PRODUCT n 
addmsg /kinetics/PKA/Release_C1 /kinetics/PKA/PKA_active REAC B A
addmsg /kinetics/PKA/R2C_cAMP4 /kinetics/PKA/Release_C1 PRODUCT n 
addmsg /kinetics/PKA/Release_C1 /kinetics/PKA/R2C_cAMP4 REAC B A
addmsg /kinetics/PKA/R2C_cAMP4 /kinetics/PKA/Release_C2 SUBSTRATE n 
addmsg /kinetics/PKA/Release_C2 /kinetics/PKA/R2C_cAMP4 REAC A B 
addmsg /kinetics/PKA/PKA_active /kinetics/PKA/Release_C2 PRODUCT n 
addmsg /kinetics/PKA/Release_C2 /kinetics/PKA/PKA_active REAC B A
addmsg /kinetics/PKA/R2_cAMP4 /kinetics/PKA/Release_C2 PRODUCT n 
addmsg /kinetics/PKA/Release_C2 /kinetics/PKA/R2_cAMP4 REAC B A
addmsg /kinetics/PKA/PKA_active /kinetics/PKA/inhib_PKA SUBSTRATE n 
addmsg /kinetics/PKA/inhib_PKA /kinetics/PKA/PKA_active REAC A B 
addmsg /kinetics/PKA/PKA_inhibitor /kinetics/PKA/inhib_PKA SUBSTRATE n 
addmsg /kinetics/PKA/inhib_PKA /kinetics/PKA/PKA_inhibitor REAC A B 
addmsg /kinetics/PKA/inhibited_PKA /kinetics/PKA/inhib_PKA PRODUCT n 
addmsg /kinetics/PKA/inhib_PKA /kinetics/PKA/inhibited_PKA REAC B A
addmsg /kinetics/CaM/CaM_Ca4 /kinetics/AC/CaM_bind_AC1 SUBSTRATE n 
addmsg /kinetics/AC/CaM_bind_AC1 /kinetics/CaM/CaM_Ca4 REAC A B 
addmsg /kinetics/AC/AC1 /kinetics/AC/CaM_bind_AC1 SUBSTRATE n 
addmsg /kinetics/AC/CaM_bind_AC1 /kinetics/AC/AC1 REAC A B 
addmsg /kinetics/AC/AC1_CaM /kinetics/AC/CaM_bind_AC1 PRODUCT n 
addmsg /kinetics/AC/CaM_bind_AC1 /kinetics/AC/AC1_CaM REAC B A
addmsg /kinetics/AC/AC2_p /kinetics/AC/dephosph_AC2 SUBSTRATE n 
addmsg /kinetics/AC/dephosph_AC2 /kinetics/AC/AC2_p REAC A B 
addmsg /kinetics/AC/AC2 /kinetics/AC/dephosph_AC2 PRODUCT n 
addmsg /kinetics/AC/dephosph_AC2 /kinetics/AC/AC2 REAC B A
addmsg /kinetics/AC/AC2 /kinetics/AC/Gs_bind_AC2 SUBSTRATE n 
addmsg /kinetics/AC/Gs_bind_AC2 /kinetics/AC/AC2 REAC A B 
addmsg /kinetics/Gprotein/Gs_alpha /kinetics/AC/Gs_bind_AC2 SUBSTRATE n 
addmsg /kinetics/AC/Gs_bind_AC2 /kinetics/Gprotein/Gs_alpha REAC A B 
addmsg /kinetics/AC/AC2_Gs /kinetics/AC/Gs_bind_AC2 PRODUCT n 
addmsg /kinetics/AC/Gs_bind_AC2 /kinetics/AC/AC2_Gs REAC B A
addmsg /kinetics/AC/AC1 /kinetics/AC/Gs_bind_AC1 SUBSTRATE n 
addmsg /kinetics/AC/Gs_bind_AC1 /kinetics/AC/AC1 REAC A B 
addmsg /kinetics/Gprotein/Gs_alpha /kinetics/AC/Gs_bind_AC1 SUBSTRATE n 
addmsg /kinetics/AC/Gs_bind_AC1 /kinetics/Gprotein/Gs_alpha REAC A B 
addmsg /kinetics/AC/AC1_Gs /kinetics/AC/Gs_bind_AC1 PRODUCT n 
addmsg /kinetics/AC/Gs_bind_AC1 /kinetics/AC/AC1_Gs REAC B A
addmsg /kinetics/AC/AC2_p /kinetics/AC/Gs_bind_AC2_p SUBSTRATE n 
addmsg /kinetics/AC/Gs_bind_AC2_p /kinetics/AC/AC2_p REAC A B 
addmsg /kinetics/Gprotein/Gs_alpha /kinetics/AC/Gs_bind_AC2_p SUBSTRATE n 
addmsg /kinetics/AC/Gs_bind_AC2_p /kinetics/Gprotein/Gs_alpha REAC A B 
addmsg /kinetics/AC/AC2_p_Gs /kinetics/AC/Gs_bind_AC2_p PRODUCT n 
addmsg /kinetics/AC/Gs_bind_AC2_p /kinetics/AC/AC2_p_Gs REAC B A
addmsg /kinetics/AC/cAMP_PDE_p /kinetics/AC/dephosph_PDE SUBSTRATE n 
addmsg /kinetics/AC/dephosph_PDE /kinetics/AC/cAMP_PDE_p REAC A B 
addmsg /kinetics/AC/cAMP_PDE /kinetics/AC/dephosph_PDE PRODUCT n 
addmsg /kinetics/AC/dephosph_PDE /kinetics/AC/cAMP_PDE REAC B A
addmsg /kinetics/CaM/CaM_Ca4 /kinetics/AC/CaM_bind_PDE1 SUBSTRATE n 
addmsg /kinetics/AC/CaM_bind_PDE1 /kinetics/CaM/CaM_Ca4 REAC A B 
addmsg /kinetics/AC/PDE1 /kinetics/AC/CaM_bind_PDE1 SUBSTRATE n 
addmsg /kinetics/AC/CaM_bind_PDE1 /kinetics/AC/PDE1 REAC A B 
addmsg /kinetics/AC/CaM.PDE1 /kinetics/AC/CaM_bind_PDE1 PRODUCT n 
addmsg /kinetics/AC/CaM_bind_PDE1 /kinetics/AC/CaM.PDE1 REAC B A
addmsg /kinetics/PI3K_activation/PIP3 /kinetics/AKT_activation/PIP3_bind_AKT SUBSTRATE n 
addmsg /kinetics/AKT_activation/PIP3_bind_AKT /kinetics/PI3K_activation/PIP3 REAC A B 
addmsg /kinetics/AKT_activation/AKT /kinetics/AKT_activation/PIP3_bind_AKT SUBSTRATE n 
addmsg /kinetics/AKT_activation/PIP3_bind_AKT /kinetics/AKT_activation/AKT REAC A B 
addmsg /kinetics/AKT_activation/PIP3_AKT /kinetics/AKT_activation/PIP3_bind_AKT PRODUCT n 
addmsg /kinetics/AKT_activation/PIP3_bind_AKT /kinetics/AKT_activation/PIP3_AKT REAC B A
addmsg /kinetics/PI3K_activation/PIP3 /kinetics/AKT_activation/PIP3_bind_PDK1 SUBSTRATE n 
addmsg /kinetics/AKT_activation/PIP3_bind_PDK1 /kinetics/PI3K_activation/PIP3 REAC A B 
addmsg /kinetics/PI3K_activation/PDK1 /kinetics/AKT_activation/PIP3_bind_PDK1 SUBSTRATE n 
addmsg /kinetics/AKT_activation/PIP3_bind_PDK1 /kinetics/PI3K_activation/PDK1 REAC A B 
addmsg /kinetics/AKT_activation/PIP3_PDK1 /kinetics/AKT_activation/PIP3_bind_PDK1 PRODUCT n 
addmsg /kinetics/AKT_activation/PIP3_bind_PDK1 /kinetics/AKT_activation/PIP3_PDK1 REAC B A
addmsg /kinetics/TSC1_TSC2/TSC1_TSC2_p /kinetics/TSC1_TSC2/TSC1_TSC2_dephospho SUBSTRATE n 
addmsg /kinetics/TSC1_TSC2/TSC1_TSC2_dephospho /kinetics/TSC1_TSC2/TSC1_TSC2_p REAC A B 
addmsg /kinetics/TSC1_TSC2/TSC1_TSC2 /kinetics/TSC1_TSC2/TSC1_TSC2_dephospho PRODUCT n 
addmsg /kinetics/TSC1_TSC2/TSC1_TSC2_dephospho /kinetics/TSC1_TSC2/TSC1_TSC2 REAC B A
addmsg /kinetics/TrKB/BDNF_TrKB2_clx /kinetics/TrKB/Autophos_TrKB SUBSTRATE n 
addmsg /kinetics/TrKB/Autophos_TrKB /kinetics/TrKB/BDNF_TrKB2_clx REAC A B 
addmsg /kinetics/TrKB/BDNF_TrKB2_p_clx /kinetics/TrKB/Autophos_TrKB PRODUCT n 
addmsg /kinetics/TrKB/Autophos_TrKB /kinetics/TrKB/BDNF_TrKB2_p_clx REAC B A
addmsg /kinetics/TrKB/TrKB /kinetics/TrKB/Dimeriz_TrKB SUBSTRATE n 
addmsg /kinetics/TrKB/Dimeriz_TrKB /kinetics/TrKB/TrKB REAC A B 
addmsg /kinetics/TrKB/BDNF_TrKB_clx /kinetics/TrKB/Dimeriz_TrKB SUBSTRATE n 
addmsg /kinetics/TrKB/Dimeriz_TrKB /kinetics/TrKB/BDNF_TrKB_clx REAC A B 
addmsg /kinetics/TrKB/BDNF_TrKB2_clx /kinetics/TrKB/Dimeriz_TrKB PRODUCT n 
addmsg /kinetics/TrKB/Dimeriz_TrKB /kinetics/TrKB/BDNF_TrKB2_clx REAC B A
addmsg /kinetics/BDNF/BDNF /kinetics/TrKB/Ligand_binding SUBSTRATE n 
addmsg /kinetics/TrKB/Ligand_binding /kinetics/BDNF/BDNF REAC A B 
addmsg /kinetics/TrKB/TrKB /kinetics/TrKB/Ligand_binding SUBSTRATE n 
addmsg /kinetics/TrKB/Ligand_binding /kinetics/TrKB/TrKB REAC A B 
addmsg /kinetics/TrKB/BDNF_TrKB_clx /kinetics/TrKB/Ligand_binding PRODUCT n 
addmsg /kinetics/TrKB/Ligand_binding /kinetics/TrKB/BDNF_TrKB_clx REAC B A
addmsg /kinetics/PLC_g/PLC_g_p /kinetics/PLC_g/PLC_g_p_dephospho SUBSTRATE n 
addmsg /kinetics/PLC_g/PLC_g_p_dephospho /kinetics/PLC_g/PLC_g_p REAC A B 
addmsg /kinetics/PLC_g/PLC_g /kinetics/PLC_g/PLC_g_p_dephospho PRODUCT n 
addmsg /kinetics/PLC_g/PLC_g_p_dephospho /kinetics/PLC_g/PLC_g REAC B A
addmsg /kinetics/TrKB/BDNF_TrKB2_p_clx /kinetics/TrKB/LR_Internalize SUBSTRATE n 
addmsg /kinetics/TrKB/LR_Internalize /kinetics/TrKB/BDNF_TrKB2_p_clx REAC A B 
addmsg /kinetics/TrKB/Int_BDNF_TrKB2_p_clx /kinetics/TrKB/LR_Internalize PRODUCT n 
addmsg /kinetics/TrKB/LR_Internalize /kinetics/TrKB/Int_BDNF_TrKB2_p_clx REAC B A
addmsg /kinetics/TrKB/Int_BDNF_TrKB2_p_clx /kinetics/TrKB/LR_Internalize PRODUCT n 
addmsg /kinetics/TrKB/LR_Internalize /kinetics/TrKB/Int_BDNF_TrKB2_p_clx REAC B A
addmsg /kinetics/TrKB/Int_BDNF_TrKB2_p_clx /kinetics/TrKB/LR_cycling SUBSTRATE n 
addmsg /kinetics/TrKB/LR_cycling /kinetics/TrKB/Int_BDNF_TrKB2_p_clx REAC A B 
addmsg /kinetics/TrKB/TrKB /kinetics/TrKB/LR_cycling PRODUCT n 
addmsg /kinetics/TrKB/LR_cycling /kinetics/TrKB/TrKB REAC B A
addmsg /kinetics/Sos/Grb2 /kinetics/Sos/Grb2_bind_SHC SUBSTRATE n 
addmsg /kinetics/Sos/Grb2_bind_SHC /kinetics/Sos/Grb2 REAC A B 
addmsg /kinetics/Sos/SHC_p /kinetics/Sos/Grb2_bind_SHC SUBSTRATE n 
addmsg /kinetics/Sos/Grb2_bind_SHC /kinetics/Sos/SHC_p REAC A B 
addmsg /kinetics/Sos/SHC_p_Grb2_clx /kinetics/Sos/Grb2_bind_SHC PRODUCT n 
addmsg /kinetics/Sos/Grb2_bind_SHC /kinetics/Sos/SHC_p_Grb2_clx REAC B A
addmsg /kinetics/Sos/SHC_p_Grb2_clx /kinetics/PI3K_activation/bind_Gab1 SUBSTRATE n 
addmsg /kinetics/PI3K_activation/bind_Gab1 /kinetics/Sos/SHC_p_Grb2_clx REAC A B 
addmsg /kinetics/PI3K_activation/Gab1 /kinetics/PI3K_activation/bind_Gab1 SUBSTRATE n 
addmsg /kinetics/PI3K_activation/bind_Gab1 /kinetics/PI3K_activation/Gab1 REAC A B 
addmsg /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_clx /kinetics/PI3K_activation/bind_Gab1 PRODUCT n 
addmsg /kinetics/PI3K_activation/bind_Gab1 /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_clx REAC B A
addmsg /kinetics/PI3K_activation/PI3K /kinetics/PI3K_activation/PI3K_act SUBSTRATE n 
addmsg /kinetics/PI3K_activation/PI3K_act /kinetics/PI3K_activation/PI3K REAC A B 
addmsg /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_clx /kinetics/PI3K_activation/PI3K_act SUBSTRATE n 
addmsg /kinetics/PI3K_activation/PI3K_act /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_clx REAC A B 
addmsg /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_PI3K_clx /kinetics/PI3K_activation/PI3K_act PRODUCT n 
addmsg /kinetics/PI3K_activation/PI3K_act /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_PI3K_clx REAC B A
addmsg /kinetics/PI3K_activation/PI3K /kinetics/PI3K_activation/basal_PI3K_act SUBSTRATE n 
addmsg /kinetics/PI3K_activation/basal_PI3K_act /kinetics/PI3K_activation/PI3K REAC A B 
addmsg /kinetics/PI3K_activation/PI3K_basal /kinetics/PI3K_activation/basal_PI3K_act PRODUCT n 
addmsg /kinetics/PI3K_activation/basal_PI3K_act /kinetics/PI3K_activation/PI3K_basal REAC B A
addmsg /kinetics/mTORC1/Rheb_GTP /kinetics/mTORC1/Rheb_GTP_bind_TORclx SUBSTRATE n 
addmsg /kinetics/mTORC1/Rheb_GTP_bind_TORclx /kinetics/mTORC1/Rheb_GTP REAC A B 
addmsg /kinetics/mTORC1/TOR_clx /kinetics/mTORC1/Rheb_GTP_bind_TORclx SUBSTRATE n 
addmsg /kinetics/mTORC1/Rheb_GTP_bind_TORclx /kinetics/mTORC1/TOR_clx REAC A B 
addmsg /kinetics/mTORC1/TOR_Rheb_GTP_clx /kinetics/mTORC1/Rheb_GTP_bind_TORclx PRODUCT n 
addmsg /kinetics/mTORC1/Rheb_GTP_bind_TORclx /kinetics/mTORC1/TOR_Rheb_GTP_clx REAC B A
addmsg /kinetics/40S/40S /kinetics/S6Kinase/S6_dephosph SUBSTRATE n 
addmsg /kinetics/S6Kinase/S6_dephosph /kinetics/40S/40S REAC A B 
addmsg /kinetics/40S/40S_inact /kinetics/S6Kinase/S6_dephosph PRODUCT n 
addmsg /kinetics/S6Kinase/S6_dephosph /kinetics/40S/40S_inact REAC B A
addmsg /kinetics/Translation_initiation/eIF4E /kinetics/4E_BP/eIF4E_bind_BP2 SUBSTRATE n 
addmsg /kinetics/4E_BP/eIF4E_bind_BP2 /kinetics/Translation_initiation/eIF4E REAC A B 
addmsg /kinetics/4E_BP/4E_BP /kinetics/4E_BP/eIF4E_bind_BP2 SUBSTRATE n 
addmsg /kinetics/4E_BP/eIF4E_bind_BP2 /kinetics/4E_BP/4E_BP REAC A B 
addmsg /kinetics/4E_BP/eIF4E_BP /kinetics/4E_BP/eIF4E_bind_BP2 PRODUCT n 
addmsg /kinetics/4E_BP/eIF4E_bind_BP2 /kinetics/4E_BP/eIF4E_BP REAC B A
addmsg /kinetics/4E_BP/eIF4E_BP_t37_46_s65 /kinetics/4E_BP/eIF4E_BP2_disso SUBSTRATE n 
addmsg /kinetics/4E_BP/eIF4E_BP2_disso /kinetics/4E_BP/eIF4E_BP_t37_46_s65 REAC A B 
addmsg /kinetics/Translation_initiation/eIF4E /kinetics/4E_BP/eIF4E_BP2_disso PRODUCT n 
addmsg /kinetics/4E_BP/eIF4E_BP2_disso /kinetics/Translation_initiation/eIF4E REAC B A
addmsg /kinetics/4E_BP/4E_BP_t37_46_s65 /kinetics/4E_BP/eIF4E_BP2_disso PRODUCT n 
addmsg /kinetics/4E_BP/eIF4E_BP2_disso /kinetics/4E_BP/4E_BP_t37_46_s65 REAC B A
addmsg /kinetics/Translation_initiation/eIF4E /kinetics/Translation_initiation/eIF4F_clx SUBSTRATE n 
addmsg /kinetics/Translation_initiation/eIF4F_clx /kinetics/Translation_initiation/eIF4E REAC A B 
addmsg /kinetics/Translation_initiation/eIF4G_A_clx /kinetics/Translation_initiation/eIF4F_clx SUBSTRATE n 
addmsg /kinetics/Translation_initiation/eIF4F_clx /kinetics/Translation_initiation/eIF4G_A_clx REAC A B 
addmsg /kinetics/Translation_initiation/eIF4F /kinetics/Translation_initiation/eIF4F_clx PRODUCT n 
addmsg /kinetics/Translation_initiation/eIF4F_clx /kinetics/Translation_initiation/eIF4F REAC B A
addmsg /kinetics/Translation_initiation/eIF4A /kinetics/Translation_initiation/eIF4G_A_clx_formation SUBSTRATE n 
addmsg /kinetics/Translation_initiation/eIF4G_A_clx_formation /kinetics/Translation_initiation/eIF4A REAC A B 
addmsg /kinetics/Translation_initiation/eIF4G /kinetics/Translation_initiation/eIF4G_A_clx_formation SUBSTRATE n 
addmsg /kinetics/Translation_initiation/eIF4G_A_clx_formation /kinetics/Translation_initiation/eIF4G REAC A B 
addmsg /kinetics/Translation_initiation/eIF4G_A_clx /kinetics/Translation_initiation/eIF4G_A_clx_formation PRODUCT n 
addmsg /kinetics/Translation_initiation/eIF4G_A_clx_formation /kinetics/Translation_initiation/eIF4G_A_clx REAC B A
addmsg /kinetics/Translation_initiation/eIF4F /kinetics/Translation_initiation/eIF4F_mRNA_clx_formation SUBSTRATE n 
addmsg /kinetics/Translation_initiation/eIF4F_mRNA_clx_formation /kinetics/Translation_initiation/eIF4F REAC A B 
addmsg /kinetics/Translation_initiation/mRNA /kinetics/Translation_initiation/eIF4F_mRNA_clx_formation SUBSTRATE n 
addmsg /kinetics/Translation_initiation/eIF4F_mRNA_clx_formation /kinetics/Translation_initiation/mRNA REAC A B 
addmsg /kinetics/Translation_initiation/eIF4F_mRNA_clx /kinetics/Translation_initiation/eIF4F_mRNA_clx_formation PRODUCT n 
addmsg /kinetics/Translation_initiation/eIF4F_mRNA_clx_formation /kinetics/Translation_initiation/eIF4F_mRNA_clx REAC B A
addmsg /kinetics/40S/40S /kinetics/43S_complex/Q_binds_R SUBSTRATE n 
addmsg /kinetics/43S_complex/Q_binds_R /kinetics/40S/40S REAC A B 
addmsg /kinetics/43S_complex/Quaternary_clx /kinetics/43S_complex/Q_binds_R SUBSTRATE n 
addmsg /kinetics/43S_complex/Q_binds_R /kinetics/43S_complex/Quaternary_clx REAC A B 
addmsg /kinetics/43S_complex/Q.R /kinetics/43S_complex/Q_binds_R PRODUCT n 
addmsg /kinetics/43S_complex/Q_binds_R /kinetics/43S_complex/Q.R REAC B A
addmsg /kinetics/Translation_initiation/eIF4F_mRNA_clx /kinetics/43S_complex/QR_binds_M SUBSTRATE n 
addmsg /kinetics/43S_complex/QR_binds_M /kinetics/Translation_initiation/eIF4F_mRNA_clx REAC A B 
addmsg /kinetics/43S_complex/Q.R /kinetics/43S_complex/QR_binds_M SUBSTRATE n 
addmsg /kinetics/43S_complex/QR_binds_M /kinetics/43S_complex/Q.R REAC A B 
addmsg /kinetics/43S_complex/43Scomplex /kinetics/43S_complex/QR_binds_M PRODUCT n 
addmsg /kinetics/43S_complex/QR_binds_M /kinetics/43S_complex/43Scomplex REAC B A
addmsg /kinetics/40S/40S /kinetics/43S_complex/R_binds_M SUBSTRATE n 
addmsg /kinetics/43S_complex/R_binds_M /kinetics/40S/40S REAC A B 
addmsg /kinetics/Translation_initiation/eIF4F_mRNA_clx /kinetics/43S_complex/R_binds_M SUBSTRATE n 
addmsg /kinetics/43S_complex/R_binds_M /kinetics/Translation_initiation/eIF4F_mRNA_clx REAC A B 
addmsg /kinetics/43S_complex/RM /kinetics/43S_complex/R_binds_M PRODUCT n 
addmsg /kinetics/43S_complex/R_binds_M /kinetics/43S_complex/RM REAC B A
addmsg /kinetics/43S_complex/RM /kinetics/43S_complex/RM_binds_Q SUBSTRATE n 
addmsg /kinetics/43S_complex/RM_binds_Q /kinetics/43S_complex/RM REAC A B 
addmsg /kinetics/43S_complex/Quaternary_clx /kinetics/43S_complex/RM_binds_Q SUBSTRATE n 
addmsg /kinetics/43S_complex/RM_binds_Q /kinetics/43S_complex/Quaternary_clx REAC A B 
addmsg /kinetics/43S_complex/43Scomplex /kinetics/43S_complex/RM_binds_Q PRODUCT n 
addmsg /kinetics/43S_complex/RM_binds_Q /kinetics/43S_complex/43Scomplex REAC B A
addmsg /kinetics/CaM/CaM /kinetics/CaM/CaM_bind_Ca SUBSTRATE n 
addmsg /kinetics/CaM/CaM_bind_Ca /kinetics/CaM/CaM REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/CaM/CaM_bind_Ca SUBSTRATE n 
addmsg /kinetics/CaM/CaM_bind_Ca /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/CaM/CaM_Ca /kinetics/CaM/CaM_bind_Ca PRODUCT n 
addmsg /kinetics/CaM/CaM_bind_Ca /kinetics/CaM/CaM_Ca REAC B A
addmsg /kinetics/CaM/CaM_Ca2 /kinetics/CaM/CaM_Ca2_bind_Ca SUBSTRATE n 
addmsg /kinetics/CaM/CaM_Ca2_bind_Ca /kinetics/CaM/CaM_Ca2 REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/CaM/CaM_Ca2_bind_Ca SUBSTRATE n 
addmsg /kinetics/CaM/CaM_Ca2_bind_Ca /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/CaM/CaM_Ca3 /kinetics/CaM/CaM_Ca2_bind_Ca PRODUCT n 
addmsg /kinetics/CaM/CaM_Ca2_bind_Ca /kinetics/CaM/CaM_Ca3 REAC B A
addmsg /kinetics/CaM/CaM_Ca /kinetics/CaM/CaM_Ca_bind_Ca SUBSTRATE n 
addmsg /kinetics/CaM/CaM_Ca_bind_Ca /kinetics/CaM/CaM_Ca REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/CaM/CaM_Ca_bind_Ca SUBSTRATE n 
addmsg /kinetics/CaM/CaM_Ca_bind_Ca /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/CaM/CaM_Ca2 /kinetics/CaM/CaM_Ca_bind_Ca PRODUCT n 
addmsg /kinetics/CaM/CaM_Ca_bind_Ca /kinetics/CaM/CaM_Ca2 REAC B A
addmsg /kinetics/CaMKIII/CaMKIII_p /kinetics/CaMKIII/CaMKIII_dephospho SUBSTRATE n 
addmsg /kinetics/CaMKIII/CaMKIII_dephospho /kinetics/CaMKIII/CaMKIII_p REAC A B 
addmsg /kinetics/CaMKIII/CaMKIII /kinetics/CaMKIII/CaMKIII_dephospho PRODUCT n 
addmsg /kinetics/CaMKIII/CaMKIII_dephospho /kinetics/CaMKIII/CaMKIII REAC B A
addmsg /kinetics/Translation_elongation/eEF2 /kinetics/Translation_elongation/elongation SUBSTRATE n 
addmsg /kinetics/Translation_elongation/elongation /kinetics/Translation_elongation/eEF2 REAC A B 
addmsg /kinetics/Translation_elongation/80S_ribos_clx /kinetics/Translation_elongation/elongation SUBSTRATE n 
addmsg /kinetics/Translation_elongation/elongation /kinetics/Translation_elongation/80S_ribos_clx REAC A B 
addmsg /kinetics/Translation_elongation/Translation_clx /kinetics/Translation_elongation/elongation PRODUCT n 
addmsg /kinetics/Translation_elongation/elongation /kinetics/Translation_elongation/Translation_clx REAC B A
addmsg /kinetics/Translation_elongation/60S_R /kinetics/Translation_elongation/activation SUBSTRATE n 
addmsg /kinetics/Translation_elongation/activation /kinetics/Translation_elongation/60S_R REAC A B 
addmsg /kinetics/43S_complex/43Scomplex /kinetics/Translation_elongation/activation SUBSTRATE n 
addmsg /kinetics/Translation_elongation/activation /kinetics/43S_complex/43Scomplex REAC A B 
addmsg /kinetics/Translation_elongation/80S_ribos_clx /kinetics/Translation_elongation/activation PRODUCT n 
addmsg /kinetics/Translation_elongation/activation /kinetics/Translation_elongation/80S_ribos_clx REAC B A
addmsg /kinetics/CaM/CaM_Ca4 /kinetics/CaM/CaMKIII_bind_CaM_Ca4 SUBSTRATE n 
addmsg /kinetics/CaM/CaMKIII_bind_CaM_Ca4 /kinetics/CaM/CaM_Ca4 REAC A B 
addmsg /kinetics/CaMKIII/CaMKIII /kinetics/CaM/CaMKIII_bind_CaM_Ca4 SUBSTRATE n 
addmsg /kinetics/CaM/CaMKIII_bind_CaM_Ca4 /kinetics/CaMKIII/CaMKIII REAC A B 
addmsg /kinetics/CaMKIII/CaMKIII_CaM_Ca4 /kinetics/CaM/CaMKIII_bind_CaM_Ca4 PRODUCT n 
addmsg /kinetics/CaM/CaMKIII_bind_CaM_Ca4 /kinetics/CaMKIII/CaMKIII_CaM_Ca4 REAC B A
addmsg /kinetics/protein/peptide /kinetics/protein/pep_elongation SUBSTRATE n 
addmsg /kinetics/protein/pep_elongation /kinetics/protein/peptide REAC A B 
addmsg /kinetics/protein/protein /kinetics/protein/pep_elongation PRODUCT n 
addmsg /kinetics/protein/pep_elongation /kinetics/protein/protein REAC B A
addmsg /kinetics/protein/protein /kinetics/protein/protein_deg SUBSTRATE n 
addmsg /kinetics/protein/protein_deg /kinetics/protein/protein REAC A B 
addmsg /kinetics/protein/degraded_protein /kinetics/protein/protein_deg PRODUCT n 
addmsg /kinetics/protein/protein_deg /kinetics/protein/degraded_protein REAC B A
addmsg /kinetics/mTORC1/Rheb_GDP /kinetics/mTORC1/GDP_to_GTP SUBSTRATE n 
addmsg /kinetics/mTORC1/GDP_to_GTP /kinetics/mTORC1/Rheb_GDP REAC A B 
addmsg /kinetics/mTORC1/Rheb_GTP /kinetics/mTORC1/GDP_to_GTP PRODUCT n 
addmsg /kinetics/mTORC1/GDP_to_GTP /kinetics/mTORC1/Rheb_GTP REAC B A
addmsg /kinetics/4E_BP/eIF4E_BP_thr37_46 /kinetics/4E_BP/eIF4E_BP_disso SUBSTRATE n 
addmsg /kinetics/4E_BP/eIF4E_BP_disso /kinetics/4E_BP/eIF4E_BP_thr37_46 REAC A B 
addmsg /kinetics/Translation_initiation/eIF4E /kinetics/4E_BP/eIF4E_BP_disso PRODUCT n 
addmsg /kinetics/4E_BP/eIF4E_BP_disso /kinetics/Translation_initiation/eIF4E REAC B A
addmsg /kinetics/4E_BP/4E_BP_t37_46 /kinetics/4E_BP/eIF4E_BP_disso PRODUCT n 
addmsg /kinetics/4E_BP/eIF4E_BP_disso /kinetics/4E_BP/4E_BP_t37_46 REAC B A
addmsg /kinetics/S6Kinase/S6K /kinetics/S6Kinase/basal_S6K SUBSTRATE n 
addmsg /kinetics/S6Kinase/basal_S6K /kinetics/S6Kinase/S6K REAC A B 
addmsg /kinetics/S6Kinase/S6K_p /kinetics/S6Kinase/basal_S6K PRODUCT n 
addmsg /kinetics/S6Kinase/basal_S6K /kinetics/S6Kinase/S6K_p REAC B A
addmsg /kinetics/protein/rad_peptide /kinetics/protein/rad_pep_elongation SUBSTRATE n 
addmsg /kinetics/protein/rad_pep_elongation /kinetics/protein/rad_peptide REAC A B 
addmsg /kinetics/protein/rad_protein /kinetics/protein/rad_pep_elongation PRODUCT n 
addmsg /kinetics/protein/rad_pep_elongation /kinetics/protein/rad_protein REAC B A
addmsg /kinetics/protein/rad_protein /kinetics/protein/rad_protein_deg SUBSTRATE n 
addmsg /kinetics/protein/rad_protein_deg /kinetics/protein/rad_protein REAC A B 
addmsg /kinetics/protein/rad_deg_pro /kinetics/protein/rad_protein_deg PRODUCT n 
addmsg /kinetics/protein/rad_protein_deg /kinetics/protein/rad_deg_pro REAC B A
addmsg /kinetics/protein/AA /kinetics/protein/labelling SUBSTRATE n 
addmsg /kinetics/protein/labelling /kinetics/protein/AA REAC A B 
addmsg /kinetics/protein/rad_AA /kinetics/protein/labelling PRODUCT n 
addmsg /kinetics/protein/labelling /kinetics/protein/rad_AA REAC B A
addmsg /kinetics/PI3K_activation/PI3K /kinetics/Ras/PI3K_bind_Ras_GTP SUBSTRATE n 
addmsg /kinetics/Ras/PI3K_bind_Ras_GTP /kinetics/PI3K_activation/PI3K REAC A B 
addmsg /kinetics/Ras/GTP_Ras /kinetics/Ras/PI3K_bind_Ras_GTP SUBSTRATE n 
addmsg /kinetics/Ras/PI3K_bind_Ras_GTP /kinetics/Ras/GTP_Ras REAC A B 
addmsg /kinetics/Ras/Ras_GTP_PI3K /kinetics/Ras/PI3K_bind_Ras_GTP PRODUCT n 
addmsg /kinetics/Ras/PI3K_bind_Ras_GTP /kinetics/Ras/Ras_GTP_PI3K REAC B A
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
addmsg /kinetics/barr2_signaling/barr2 /kinetics/barr2_signaling/mGluR_barr2_assoc SUBSTRATE n 
addmsg /kinetics/barr2_signaling/mGluR_barr2_assoc /kinetics/barr2_signaling/barr2 REAC A B 
addmsg /kinetics/barr2_signaling/L.mGluR_p /kinetics/barr2_signaling/mGluR_barr2_assoc SUBSTRATE n 
addmsg /kinetics/barr2_signaling/mGluR_barr2_assoc /kinetics/barr2_signaling/L.mGluR_p REAC A B 
addmsg /kinetics/barr2_signaling/L.mGluR_p.barr2 /kinetics/barr2_signaling/mGluR_barr2_assoc PRODUCT n 
addmsg /kinetics/barr2_signaling/mGluR_barr2_assoc /kinetics/barr2_signaling/L.mGluR_p.barr2 REAC B A
addmsg /kinetics/barr2_signaling/mGluR_p.barr2 /kinetics/barr2_signaling/mGluR_internalize SUBSTRATE n 
addmsg /kinetics/barr2_signaling/mGluR_internalize /kinetics/barr2_signaling/mGluR_p.barr2 REAC A B 
addmsg /kinetics/barr2_signaling/Internal_mGluR_p.barr2 /kinetics/barr2_signaling/mGluR_internalize PRODUCT n 
addmsg /kinetics/barr2_signaling/mGluR_internalize /kinetics/barr2_signaling/Internal_mGluR_p.barr2 REAC B A
addmsg /kinetics/barr2_signaling/Internal_mGluR_p.barr2 /kinetics/barr2_signaling/barr2_dissoc SUBSTRATE n 
addmsg /kinetics/barr2_signaling/barr2_dissoc /kinetics/barr2_signaling/Internal_mGluR_p.barr2 REAC A B 
addmsg /kinetics/barr2_signaling/Internal_mGluR_p /kinetics/barr2_signaling/barr2_dissoc PRODUCT n 
addmsg /kinetics/barr2_signaling/barr2_dissoc /kinetics/barr2_signaling/Internal_mGluR_p REAC B A
addmsg /kinetics/barr2_signaling/barr2 /kinetics/barr2_signaling/barr2_dissoc PRODUCT n 
addmsg /kinetics/barr2_signaling/barr2_dissoc /kinetics/barr2_signaling/barr2 REAC B A
addmsg /kinetics/barr2_signaling/Internal_mGluR /kinetics/barr2_signaling/mGluR_recycling SUBSTRATE n 
addmsg /kinetics/barr2_signaling/mGluR_recycling /kinetics/barr2_signaling/Internal_mGluR REAC A B 
addmsg /kinetics/mGluR/mGluR /kinetics/barr2_signaling/mGluR_recycling PRODUCT n 
addmsg /kinetics/barr2_signaling/mGluR_recycling /kinetics/mGluR/mGluR REAC B A
addmsg /kinetics/barr2_signaling/L.mGluR_p.barr2 /kinetics/barr2_signaling/ligand_dissoc SUBSTRATE n 
addmsg /kinetics/barr2_signaling/ligand_dissoc /kinetics/barr2_signaling/L.mGluR_p.barr2 REAC A B 
addmsg /kinetics/barr2_signaling/mGluR_p.barr2 /kinetics/barr2_signaling/ligand_dissoc PRODUCT n 
addmsg /kinetics/barr2_signaling/ligand_dissoc /kinetics/barr2_signaling/mGluR_p.barr2 REAC B A
addmsg /kinetics/mGluR/Glutamate /kinetics/barr2_signaling/ligand_dissoc PRODUCT n 
addmsg /kinetics/barr2_signaling/ligand_dissoc /kinetics/mGluR/Glutamate REAC B A
addmsg /kinetics/MAPK/craf_1 /kinetics/MAPK/mGluR_barr2_Raf_scaffolding SUBSTRATE n 
addmsg /kinetics/MAPK/mGluR_barr2_Raf_scaffolding /kinetics/MAPK/craf_1 REAC A B 
addmsg /kinetics/barr2_signaling/Internal_mGluR_p.barr2 /kinetics/MAPK/mGluR_barr2_Raf_scaffolding SUBSTRATE n 
addmsg /kinetics/MAPK/mGluR_barr2_Raf_scaffolding /kinetics/barr2_signaling/Internal_mGluR_p.barr2 REAC A B 
addmsg /kinetics/MAPK/craf_1_p /kinetics/MAPK/mGluR_barr2_Raf_scaffolding PRODUCT n 
addmsg /kinetics/MAPK/mGluR_barr2_Raf_scaffolding /kinetics/MAPK/craf_1_p REAC B A
addmsg /kinetics/MAPK/craf_1 /kinetics/PKC/PKC_active/PKC_act_raf SUBSTRATE n 
addmsg /kinetics/PKC/PKC_active/PKC_act_raf /kinetics/MAPK/craf_1 REAC sA B 
addmsg /kinetics/PKC/PKC_active/PKC_act_raf /kinetics/MAPK/craf_1_p MM_PRD pA
addmsg /kinetics/PKC/PKC_active /kinetics/PKC/PKC_active/PKC_act_raf ENZYME n
addmsg /kinetics/PKC/PKC_active/PKC_act_raf /kinetics/PKC/PKC_active REAC eA B
addmsg /kinetics/Ras/GAP /kinetics/PKC/PKC_active/PKC_inact_GAP SUBSTRATE n 
addmsg /kinetics/PKC/PKC_active/PKC_inact_GAP /kinetics/Ras/GAP REAC sA B 
addmsg /kinetics/PKC/PKC_active/PKC_inact_GAP /kinetics/Ras/GAP_p MM_PRD pA
addmsg /kinetics/PKC/PKC_active /kinetics/PKC/PKC_active/PKC_inact_GAP ENZYME n
addmsg /kinetics/PKC/PKC_active/PKC_inact_GAP /kinetics/PKC/PKC_active REAC eA B
addmsg /kinetics/Ras/inact_GEF /kinetics/PKC/PKC_active/PKC_act_GEF SUBSTRATE n 
addmsg /kinetics/PKC/PKC_active/PKC_act_GEF /kinetics/Ras/inact_GEF REAC sA B 
addmsg /kinetics/PKC/PKC_active/PKC_act_GEF /kinetics/Ras/GEF_p MM_PRD pA
addmsg /kinetics/PKC/PKC_active /kinetics/PKC/PKC_active/PKC_act_GEF ENZYME n
addmsg /kinetics/PKC/PKC_active/PKC_act_GEF /kinetics/PKC/PKC_active REAC eA B
addmsg /kinetics/CaM/neurogranin /kinetics/PKC/PKC_active/PKC_phosph_neurogranin SUBSTRATE n 
addmsg /kinetics/PKC/PKC_active/PKC_phosph_neurogranin /kinetics/CaM/neurogranin REAC sA B 
addmsg /kinetics/PKC/PKC_active/PKC_phosph_neurogranin /kinetics/CaM/neurogranin_p MM_PRD pA
addmsg /kinetics/PKC/PKC_active /kinetics/PKC/PKC_active/PKC_phosph_neurogranin ENZYME n
addmsg /kinetics/PKC/PKC_active/PKC_phosph_neurogranin /kinetics/PKC/PKC_active REAC eA B
addmsg /kinetics/CaM/neurogranin_CaM /kinetics/PKC/PKC_active/PKC_phosph_ng_CaM SUBSTRATE n 
addmsg /kinetics/PKC/PKC_active/PKC_phosph_ng_CaM /kinetics/CaM/neurogranin_CaM REAC sA B 
addmsg /kinetics/PKC/PKC_active/PKC_phosph_ng_CaM /kinetics/CaM/CaM MM_PRD pA
addmsg /kinetics/PKC/PKC_active/PKC_phosph_ng_CaM /kinetics/CaM/neurogranin_p MM_PRD pA
addmsg /kinetics/PKC/PKC_active /kinetics/PKC/PKC_active/PKC_phosph_ng_CaM ENZYME n
addmsg /kinetics/PKC/PKC_active/PKC_phosph_ng_CaM /kinetics/PKC/PKC_active REAC eA B
addmsg /kinetics/AC/AC2 /kinetics/PKC/PKC_active/phosph_AC2 SUBSTRATE n 
addmsg /kinetics/PKC/PKC_active/phosph_AC2 /kinetics/AC/AC2 REAC sA B 
addmsg /kinetics/PKC/PKC_active/phosph_AC2 /kinetics/AC/AC2_p MM_PRD pA
addmsg /kinetics/PKC/PKC_active /kinetics/PKC/PKC_active/phosph_AC2 ENZYME n
addmsg /kinetics/PKC/PKC_active/phosph_AC2 /kinetics/PKC/PKC_active REAC eA B
addmsg /kinetics/PLA2/APC /kinetics/PLA2/PLA2_Ca_p/kenz SUBSTRATE n 
addmsg /kinetics/PLA2/PLA2_Ca_p/kenz /kinetics/PLA2/APC REAC sA B 
addmsg /kinetics/PLA2/PLA2_Ca_p/kenz /kinetics/PKC/Arachidonic_Acid MM_PRD pA
addmsg /kinetics/PLA2/PLA2_Ca_p /kinetics/PLA2/PLA2_Ca_p/kenz ENZYME n
addmsg /kinetics/PLA2/PLA2_Ca_p/kenz /kinetics/PLA2/PLA2_Ca_p REAC eA B
addmsg /kinetics/PLA2/APC /kinetics/PLA2/PIP2_PLA2_p/kenz SUBSTRATE n 
addmsg /kinetics/PLA2/PIP2_PLA2_p/kenz /kinetics/PLA2/APC REAC sA B 
addmsg /kinetics/PLA2/PIP2_PLA2_p/kenz /kinetics/PKC/Arachidonic_Acid MM_PRD pA
addmsg /kinetics/PLA2/PIP2_PLA2_p /kinetics/PLA2/PIP2_PLA2_p/kenz ENZYME n
addmsg /kinetics/PLA2/PIP2_PLA2_p/kenz /kinetics/PLA2/PIP2_PLA2_p REAC eA B
addmsg /kinetics/PLA2/APC /kinetics/PLA2/PIP2_Ca_PLA2_p/kenz SUBSTRATE n 
addmsg /kinetics/PLA2/PIP2_Ca_PLA2_p/kenz /kinetics/PLA2/APC REAC sA B 
addmsg /kinetics/PLA2/PIP2_Ca_PLA2_p/kenz /kinetics/PKC/Arachidonic_Acid MM_PRD pA
addmsg /kinetics/PLA2/PIP2_Ca_PLA2_p /kinetics/PLA2/PIP2_Ca_PLA2_p/kenz ENZYME n
addmsg /kinetics/PLA2/PIP2_Ca_PLA2_p/kenz /kinetics/PLA2/PIP2_Ca_PLA2_p REAC eA B
addmsg /kinetics/PLA2/APC /kinetics/PLA2/DAG_Ca_PLA2_p/kenz SUBSTRATE n 
addmsg /kinetics/PLA2/DAG_Ca_PLA2_p/kenz /kinetics/PLA2/APC REAC sA B 
addmsg /kinetics/PLA2/DAG_Ca_PLA2_p/kenz /kinetics/PKC/Arachidonic_Acid MM_PRD pA
addmsg /kinetics/PLA2/DAG_Ca_PLA2_p /kinetics/PLA2/DAG_Ca_PLA2_p/kenz ENZYME n
addmsg /kinetics/PLA2/DAG_Ca_PLA2_p/kenz /kinetics/PLA2/DAG_Ca_PLA2_p REAC eA B
addmsg /kinetics/PLA2/APC /kinetics/PLA2/PLA2_p_Ca/kenz SUBSTRATE n 
addmsg /kinetics/PLA2/PLA2_p_Ca/kenz /kinetics/PLA2/APC REAC sA B 
addmsg /kinetics/PLA2/PLA2_p_Ca/kenz /kinetics/PKC/Arachidonic_Acid MM_PRD pA
addmsg /kinetics/PLA2/PLA2_p_Ca /kinetics/PLA2/PLA2_p_Ca/kenz ENZYME n
addmsg /kinetics/PLA2/PLA2_p_Ca/kenz /kinetics/PLA2/PLA2_p_Ca REAC eA B
addmsg /kinetics/PLA2/PLA2_cytosolic /kinetics/MAPK/MAPK_p_p/MAPK_p_p SUBSTRATE n 
addmsg /kinetics/MAPK/MAPK_p_p/MAPK_p_p /kinetics/PLA2/PLA2_cytosolic REAC sA B 
addmsg /kinetics/MAPK/MAPK_p_p/MAPK_p_p /kinetics/PLA2/PLA2_p MM_PRD pA
addmsg /kinetics/MAPK/MAPK_p_p /kinetics/MAPK/MAPK_p_p/MAPK_p_p ENZYME n
addmsg /kinetics/MAPK/MAPK_p_p/MAPK_p_p /kinetics/MAPK/MAPK_p_p REAC eA B
addmsg /kinetics/MAPK/craf_1_p /kinetics/MAPK/MAPK_p_p/MAPK_p_p_feedback SUBSTRATE n 
addmsg /kinetics/MAPK/MAPK_p_p/MAPK_p_p_feedback /kinetics/MAPK/craf_1_p REAC sA B 
addmsg /kinetics/MAPK/MAPK_p_p/MAPK_p_p_feedback /kinetics/MAPK/craf_1_p_p MM_PRD pA
addmsg /kinetics/MAPK/MAPK_p_p /kinetics/MAPK/MAPK_p_p/MAPK_p_p_feedback ENZYME n
addmsg /kinetics/MAPK/MAPK_p_p/MAPK_p_p_feedback /kinetics/MAPK/MAPK_p_p REAC eA B
addmsg /kinetics/Sos/Sos /kinetics/MAPK/MAPK_p_p/phosph_Sos SUBSTRATE n 
addmsg /kinetics/MAPK/MAPK_p_p/phosph_Sos /kinetics/Sos/Sos REAC sA B 
addmsg /kinetics/MAPK/MAPK_p_p/phosph_Sos /kinetics/Sos/Sos_p MM_PRD pA
addmsg /kinetics/MAPK/MAPK_p_p /kinetics/MAPK/MAPK_p_p/phosph_Sos ENZYME n
addmsg /kinetics/MAPK/MAPK_p_p/phosph_Sos /kinetics/MAPK/MAPK_p_p REAC eA B
addmsg /kinetics/PI3K_activation/PIP2 /kinetics/PLCbeta/PLC_Ca/PLC_Ca SUBSTRATE n 
addmsg /kinetics/PLCbeta/PLC_Ca/PLC_Ca /kinetics/PI3K_activation/PIP2 REAC sA B 
addmsg /kinetics/PLCbeta/PLC_Ca/PLC_Ca /kinetics/PKC/DAG MM_PRD pA
addmsg /kinetics/PLCbeta/PLC_Ca/PLC_Ca /kinetics/PI3K_activation/IP3 MM_PRD pA
addmsg /kinetics/PLCbeta/PLC_Ca /kinetics/PLCbeta/PLC_Ca/PLC_Ca ENZYME n
addmsg /kinetics/PLCbeta/PLC_Ca/PLC_Ca /kinetics/PLCbeta/PLC_Ca REAC eA B
addmsg /kinetics/PI3K_activation/PIP2 /kinetics/PLCbeta/PLC_Ca_Gq/PLCb_Ca_Gq SUBSTRATE n 
addmsg /kinetics/PLCbeta/PLC_Ca_Gq/PLCb_Ca_Gq /kinetics/PI3K_activation/PIP2 REAC sA B 
addmsg /kinetics/PLCbeta/PLC_Ca_Gq/PLCb_Ca_Gq /kinetics/PKC/DAG MM_PRD pA
addmsg /kinetics/PLCbeta/PLC_Ca_Gq/PLCb_Ca_Gq /kinetics/PI3K_activation/IP3 MM_PRD pA
addmsg /kinetics/PLCbeta/PLC_Ca_Gq /kinetics/PLCbeta/PLC_Ca_Gq/PLCb_Ca_Gq ENZYME n
addmsg /kinetics/PLCbeta/PLC_Ca_Gq/PLCb_Ca_Gq /kinetics/PLCbeta/PLC_Ca_Gq REAC eA B
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
addmsg /kinetics/MAPK/MAPK_p /kinetics/Phosphatase/MKP_1/MKP1_tyr_deph SUBSTRATE n 
addmsg /kinetics/Phosphatase/MKP_1/MKP1_tyr_deph /kinetics/MAPK/MAPK_p REAC sA B 
addmsg /kinetics/Phosphatase/MKP_1/MKP1_tyr_deph /kinetics/MAPK/MAPK MM_PRD pA
addmsg /kinetics/Phosphatase/MKP_1 /kinetics/Phosphatase/MKP_1/MKP1_tyr_deph ENZYME n
addmsg /kinetics/Phosphatase/MKP_1/MKP1_tyr_deph /kinetics/Phosphatase/MKP_1 REAC eA B
addmsg /kinetics/MAPK/MAPK_p_p /kinetics/Phosphatase/MKP_1/MKP1_thr_deph SUBSTRATE n 
addmsg /kinetics/Phosphatase/MKP_1/MKP1_thr_deph /kinetics/MAPK/MAPK_p_p REAC sA B 
addmsg /kinetics/Phosphatase/MKP_1/MKP1_thr_deph /kinetics/MAPK/MAPK_p MM_PRD pA
addmsg /kinetics/Phosphatase/MKP_1 /kinetics/Phosphatase/MKP_1/MKP1_thr_deph ENZYME n
addmsg /kinetics/Phosphatase/MKP_1/MKP1_thr_deph /kinetics/Phosphatase/MKP_1 REAC eA B
addmsg /kinetics/MAPK/craf_1_p /kinetics/Phosphatase/PPhosphatase2A/craf_dephospho SUBSTRATE n 
addmsg /kinetics/Phosphatase/PPhosphatase2A/craf_dephospho /kinetics/MAPK/craf_1_p REAC sA B 
addmsg /kinetics/Phosphatase/PPhosphatase2A/craf_dephospho /kinetics/MAPK/craf_1 MM_PRD pA
addmsg /kinetics/Phosphatase/PPhosphatase2A /kinetics/Phosphatase/PPhosphatase2A/craf_dephospho ENZYME n
addmsg /kinetics/Phosphatase/PPhosphatase2A/craf_dephospho /kinetics/Phosphatase/PPhosphatase2A REAC eA B
addmsg /kinetics/MAPK/MAPKK_p_p /kinetics/Phosphatase/PPhosphatase2A/MAPKK_dephospho SUBSTRATE n 
addmsg /kinetics/Phosphatase/PPhosphatase2A/MAPKK_dephospho /kinetics/MAPK/MAPKK_p_p REAC sA B 
addmsg /kinetics/Phosphatase/PPhosphatase2A/MAPKK_dephospho /kinetics/MAPK/MAPKK_p MM_PRD pA
addmsg /kinetics/Phosphatase/PPhosphatase2A /kinetics/Phosphatase/PPhosphatase2A/MAPKK_dephospho ENZYME n
addmsg /kinetics/Phosphatase/PPhosphatase2A/MAPKK_dephospho /kinetics/Phosphatase/PPhosphatase2A REAC eA B
addmsg /kinetics/MAPK/MAPKK_p /kinetics/Phosphatase/PPhosphatase2A/MAPKK_dephospho_ser SUBSTRATE n 
addmsg /kinetics/Phosphatase/PPhosphatase2A/MAPKK_dephospho_ser /kinetics/MAPK/MAPKK_p REAC sA B 
addmsg /kinetics/Phosphatase/PPhosphatase2A/MAPKK_dephospho_ser /kinetics/MAPK/MAPKK MM_PRD pA
addmsg /kinetics/Phosphatase/PPhosphatase2A /kinetics/Phosphatase/PPhosphatase2A/MAPKK_dephospho_ser ENZYME n
addmsg /kinetics/Phosphatase/PPhosphatase2A/MAPKK_dephospho_ser /kinetics/Phosphatase/PPhosphatase2A REAC eA B
addmsg /kinetics/MAPK/craf_1_p_p /kinetics/Phosphatase/PPhosphatase2A/craf_p_p_dephospho SUBSTRATE n 
addmsg /kinetics/Phosphatase/PPhosphatase2A/craf_p_p_dephospho /kinetics/MAPK/craf_1_p_p REAC sA B 
addmsg /kinetics/Phosphatase/PPhosphatase2A/craf_p_p_dephospho /kinetics/MAPK/craf_1_p MM_PRD pA
addmsg /kinetics/Phosphatase/PPhosphatase2A /kinetics/Phosphatase/PPhosphatase2A/craf_p_p_dephospho ENZYME n
addmsg /kinetics/Phosphatase/PPhosphatase2A/craf_p_p_dephospho /kinetics/Phosphatase/PPhosphatase2A REAC eA B
addmsg /kinetics/Ras/GDP_Ras /kinetics/Ras/GEF_Gprot_bg/GEF_bg_act_Ras SUBSTRATE n 
addmsg /kinetics/Ras/GEF_Gprot_bg/GEF_bg_act_Ras /kinetics/Ras/GDP_Ras REAC sA B 
addmsg /kinetics/Ras/GEF_Gprot_bg/GEF_bg_act_Ras /kinetics/Ras/GTP_Ras MM_PRD pA
addmsg /kinetics/Ras/GEF_Gprot_bg /kinetics/Ras/GEF_Gprot_bg/GEF_bg_act_Ras ENZYME n
addmsg /kinetics/Ras/GEF_Gprot_bg/GEF_bg_act_Ras /kinetics/Ras/GEF_Gprot_bg REAC eA B
addmsg /kinetics/Ras/GDP_Ras /kinetics/Ras/GEF_p/GEF_p_act_Ras SUBSTRATE n 
addmsg /kinetics/Ras/GEF_p/GEF_p_act_Ras /kinetics/Ras/GDP_Ras REAC sA B 
addmsg /kinetics/Ras/GEF_p/GEF_p_act_Ras /kinetics/Ras/GTP_Ras MM_PRD pA
addmsg /kinetics/Ras/GEF_p /kinetics/Ras/GEF_p/GEF_p_act_Ras ENZYME n
addmsg /kinetics/Ras/GEF_p/GEF_p_act_Ras /kinetics/Ras/GEF_p REAC eA B
addmsg /kinetics/Ras/GTP_Ras /kinetics/Ras/GAP/GAP_inact_Ras SUBSTRATE n 
addmsg /kinetics/Ras/GAP/GAP_inact_Ras /kinetics/Ras/GTP_Ras REAC sA B 
addmsg /kinetics/Ras/GAP/GAP_inact_Ras /kinetics/Ras/GDP_Ras MM_PRD pA
addmsg /kinetics/Ras/GAP /kinetics/Ras/GAP/GAP_inact_Ras ENZYME n
addmsg /kinetics/Ras/GAP/GAP_inact_Ras /kinetics/Ras/GAP REAC eA B
addmsg /kinetics/Ras/GDP_Ras /kinetics/Ras/CaM_GEF/CaM_GEF_act_Ras SUBSTRATE n 
addmsg /kinetics/Ras/CaM_GEF/CaM_GEF_act_Ras /kinetics/Ras/GDP_Ras REAC sA B 
addmsg /kinetics/Ras/CaM_GEF/CaM_GEF_act_Ras /kinetics/Ras/GTP_Ras MM_PRD pA
addmsg /kinetics/Ras/CaM_GEF /kinetics/Ras/CaM_GEF/CaM_GEF_act_Ras ENZYME n
addmsg /kinetics/Ras/CaM_GEF/CaM_GEF_act_Ras /kinetics/Ras/CaM_GEF REAC eA B
addmsg /kinetics/Ras/inact_GEF /kinetics/PKA/PKA_active/PKA_phosph_GEF SUBSTRATE n 
addmsg /kinetics/PKA/PKA_active/PKA_phosph_GEF /kinetics/Ras/inact_GEF REAC sA B 
addmsg /kinetics/PKA/PKA_active/PKA_phosph_GEF /kinetics/Ras/inact_GEF_p MM_PRD pA
addmsg /kinetics/PKA/PKA_active /kinetics/PKA/PKA_active/PKA_phosph_GEF ENZYME n
addmsg /kinetics/PKA/PKA_active/PKA_phosph_GEF /kinetics/PKA/PKA_active REAC eA B
addmsg /kinetics/PP1/I1 /kinetics/PKA/PKA_active/PKA_phosph_I1 SUBSTRATE n 
addmsg /kinetics/PKA/PKA_active/PKA_phosph_I1 /kinetics/PP1/I1 REAC sA B 
addmsg /kinetics/PKA/PKA_active/PKA_phosph_I1 /kinetics/PP1/I1_p MM_PRD pA
addmsg /kinetics/PKA/PKA_active /kinetics/PKA/PKA_active/PKA_phosph_I1 ENZYME n
addmsg /kinetics/PKA/PKA_active/PKA_phosph_I1 /kinetics/PKA/PKA_active REAC eA B
addmsg /kinetics/AC/cAMP_PDE /kinetics/PKA/PKA_active/phosph_PDE SUBSTRATE n 
addmsg /kinetics/PKA/PKA_active/phosph_PDE /kinetics/AC/cAMP_PDE REAC sA B 
addmsg /kinetics/PKA/PKA_active/phosph_PDE /kinetics/AC/cAMP_PDE_p MM_PRD pA
addmsg /kinetics/PKA/PKA_active /kinetics/PKA/PKA_active/phosph_PDE ENZYME n
addmsg /kinetics/PKA/PKA_active/phosph_PDE /kinetics/PKA/PKA_active REAC eA B
addmsg /kinetics/Ras/GDP_Ras /kinetics/Sos/SHC_p.Sos.Grb2/Sos.Ras_GEF SUBSTRATE n 
addmsg /kinetics/Sos/SHC_p.Sos.Grb2/Sos.Ras_GEF /kinetics/Ras/GDP_Ras REAC sA B 
addmsg /kinetics/Sos/SHC_p.Sos.Grb2/Sos.Ras_GEF /kinetics/Ras/GTP_Ras MM_PRD pA
addmsg /kinetics/Sos/SHC_p.Sos.Grb2 /kinetics/Sos/SHC_p.Sos.Grb2/Sos.Ras_GEF ENZYME n
addmsg /kinetics/Sos/SHC_p.Sos.Grb2/Sos.Ras_GEF /kinetics/Sos/SHC_p.Sos.Grb2 REAC eA B
addmsg /kinetics/PLC_g/Ca.PLC_g /kinetics/EGFR/L.EGFR/Ca.PLC_g_phospho SUBSTRATE n 
addmsg /kinetics/EGFR/L.EGFR/Ca.PLC_g_phospho /kinetics/PLC_g/Ca.PLC_g REAC sA B 
addmsg /kinetics/EGFR/L.EGFR/Ca.PLC_g_phospho /kinetics/PLC_g/Ca.PLC_g_p MM_PRD pA
addmsg /kinetics/EGFR/L.EGFR /kinetics/EGFR/L.EGFR/Ca.PLC_g_phospho ENZYME n
addmsg /kinetics/EGFR/L.EGFR/Ca.PLC_g_phospho /kinetics/EGFR/L.EGFR REAC eA B
addmsg /kinetics/Sos/SHC /kinetics/EGFR/L.EGFR/SHC_phospho SUBSTRATE n 
addmsg /kinetics/EGFR/L.EGFR/SHC_phospho /kinetics/Sos/SHC REAC sA B 
addmsg /kinetics/EGFR/L.EGFR/SHC_phospho /kinetics/Sos/SHC_p MM_PRD pA
addmsg /kinetics/EGFR/L.EGFR /kinetics/EGFR/L.EGFR/SHC_phospho ENZYME n
addmsg /kinetics/EGFR/L.EGFR/SHC_phospho /kinetics/EGFR/L.EGFR REAC eA B
addmsg /kinetics/PI3K_activation/PIP2 /kinetics/PLC_g/Ca.PLC_g/PIP2_hydrolysis SUBSTRATE n 
addmsg /kinetics/PLC_g/Ca.PLC_g/PIP2_hydrolysis /kinetics/PI3K_activation/PIP2 REAC sA B 
addmsg /kinetics/PLC_g/Ca.PLC_g/PIP2_hydrolysis /kinetics/PKC/DAG MM_PRD pA 
addmsg /kinetics/PLC_g/Ca.PLC_g/PIP2_hydrolysis /kinetics/PI3K_activation/IP3 MM_PRD pA 
addmsg /kinetics/PLC_g/Ca.PLC_g /kinetics/PLC_g/Ca.PLC_g/PIP2_hydrolysis ENZYME n 
addmsg /kinetics/PI3K_activation/PIP2 /kinetics/PLC_g/Ca.PLC_g_p/PIP2_hydrolysis SUBSTRATE n 
addmsg /kinetics/PLC_g/Ca.PLC_g_p/PIP2_hydrolysis /kinetics/PI3K_activation/PIP2 REAC sA B 
addmsg /kinetics/PLC_g/Ca.PLC_g_p/PIP2_hydrolysis /kinetics/PKC/DAG MM_PRD pA 
addmsg /kinetics/PLC_g/Ca.PLC_g_p/PIP2_hydrolysis /kinetics/PI3K_activation/IP3 MM_PRD pA 
addmsg /kinetics/PLC_g/Ca.PLC_g_p /kinetics/PLC_g/Ca.PLC_g_p/PIP2_hydrolysis ENZYME n 
addmsg /kinetics/CaMKII/CaMKII_thr286 /kinetics/CaMKII/tot_CaM_CaMKII/CaM_act_305 SUBSTRATE n 
addmsg /kinetics/CaMKII/tot_CaM_CaMKII/CaM_act_305 /kinetics/CaMKII/CaMKII_thr286 REAC sA B 
addmsg /kinetics/CaMKII/tot_CaM_CaMKII/CaM_act_305 /kinetics/CaMKII/CaMKII_p_p_p MM_PRD pA
addmsg /kinetics/CaMKII/tot_CaM_CaMKII /kinetics/CaMKII/tot_CaM_CaMKII/CaM_act_305 ENZYME n
addmsg /kinetics/CaMKII/tot_CaM_CaMKII/CaM_act_305 /kinetics/CaMKII/tot_CaM_CaMKII REAC eA B
addmsg /kinetics/CaMKII/CaMKII_CaM /kinetics/CaMKII/tot_CaM_CaMKII/CaM_act_286 SUBSTRATE n 
addmsg /kinetics/CaMKII/tot_CaM_CaMKII/CaM_act_286 /kinetics/CaMKII/CaMKII_CaM REAC sA B 
addmsg /kinetics/CaMKII/tot_CaM_CaMKII/CaM_act_286 /kinetics/CaMKII/CaMKII_thr286_p_CaM MM_PRD pA
addmsg /kinetics/CaMKII/tot_CaM_CaMKII /kinetics/CaMKII/tot_CaM_CaMKII/CaM_act_286 ENZYME n
addmsg /kinetics/CaMKII/tot_CaM_CaMKII/CaM_act_286 /kinetics/CaMKII/tot_CaM_CaMKII REAC eA B
addmsg /kinetics/CaMKII/CaMKII_thr286 /kinetics/CaMKII/tot_autonomous_CaMKII/auton_305 SUBSTRATE n 
addmsg /kinetics/CaMKII/tot_autonomous_CaMKII/auton_305 /kinetics/CaMKII/CaMKII_thr286 REAC sA B 
addmsg /kinetics/CaMKII/tot_autonomous_CaMKII/auton_305 /kinetics/CaMKII/CaMKII_p_p_p MM_PRD pA
addmsg /kinetics/CaMKII/tot_autonomous_CaMKII /kinetics/CaMKII/tot_autonomous_CaMKII/auton_305 ENZYME n
addmsg /kinetics/CaMKII/tot_autonomous_CaMKII/auton_305 /kinetics/CaMKII/tot_autonomous_CaMKII REAC eA B
addmsg /kinetics/CaMKII/CaMKII_CaM /kinetics/CaMKII/tot_autonomous_CaMKII/auton_286 SUBSTRATE n 
addmsg /kinetics/CaMKII/tot_autonomous_CaMKII/auton_286 /kinetics/CaMKII/CaMKII_CaM REAC sA B 
addmsg /kinetics/CaMKII/tot_autonomous_CaMKII/auton_286 /kinetics/CaMKII/CaMKII_thr286_p_CaM MM_PRD pA
addmsg /kinetics/CaMKII/tot_autonomous_CaMKII /kinetics/CaMKII/tot_autonomous_CaMKII/auton_286 ENZYME n
addmsg /kinetics/CaMKII/tot_autonomous_CaMKII/auton_286 /kinetics/CaMKII/tot_autonomous_CaMKII REAC eA B
addmsg /kinetics/CaMKII/CaMKII_thr286_p_CaM /kinetics/PP1/PP1_active/Deph_thr286 SUBSTRATE n 
addmsg /kinetics/PP1/PP1_active/Deph_thr286 /kinetics/CaMKII/CaMKII_thr286_p_CaM REAC sA B 
addmsg /kinetics/PP1/PP1_active/Deph_thr286 /kinetics/CaMKII/CaMKII_CaM MM_PRD pA
addmsg /kinetics/PP1/PP1_active /kinetics/PP1/PP1_active/Deph_thr286 ENZYME n
addmsg /kinetics/PP1/PP1_active/Deph_thr286 /kinetics/PP1/PP1_active REAC eA B
addmsg /kinetics/CaMKII/CaMKII_p_p_p /kinetics/PP1/PP1_active/Deph_thr305 SUBSTRATE n 
addmsg /kinetics/PP1/PP1_active/Deph_thr305 /kinetics/CaMKII/CaMKII_p_p_p REAC sA B 
addmsg /kinetics/PP1/PP1_active/Deph_thr305 /kinetics/CaMKII/CaMKII_thr286 MM_PRD pA
addmsg /kinetics/PP1/PP1_active /kinetics/PP1/PP1_active/Deph_thr305 ENZYME n
addmsg /kinetics/PP1/PP1_active/Deph_thr305 /kinetics/PP1/PP1_active REAC eA B
addmsg /kinetics/CaMKII/CaMKII_thr306 /kinetics/PP1/PP1_active/Deph_thr306 SUBSTRATE n 
addmsg /kinetics/PP1/PP1_active/Deph_thr306 /kinetics/CaMKII/CaMKII_thr306 REAC sA B 
addmsg /kinetics/PP1/PP1_active/Deph_thr306 /kinetics/CaMKII/CaMKII MM_PRD pA
addmsg /kinetics/PP1/PP1_active /kinetics/PP1/PP1_active/Deph_thr306 ENZYME n
addmsg /kinetics/PP1/PP1_active/Deph_thr306 /kinetics/PP1/PP1_active REAC eA B
addmsg /kinetics/CaMKII/CaMKII_p_p_p /kinetics/PP1/PP1_active/Deph_thr286c SUBSTRATE n 
addmsg /kinetics/PP1/PP1_active/Deph_thr286c /kinetics/CaMKII/CaMKII_p_p_p REAC sA B 
addmsg /kinetics/PP1/PP1_active/Deph_thr286c /kinetics/CaMKII/CaMKII_thr306 MM_PRD pA
addmsg /kinetics/PP1/PP1_active /kinetics/PP1/PP1_active/Deph_thr286c ENZYME n
addmsg /kinetics/PP1/PP1_active/Deph_thr286c /kinetics/PP1/PP1_active REAC eA B
addmsg /kinetics/CaMKII/CaMKII_thr286 /kinetics/PP1/PP1_active/Deph_thr286b SUBSTRATE n 
addmsg /kinetics/PP1/PP1_active/Deph_thr286b /kinetics/CaMKII/CaMKII_thr286 REAC sA B 
addmsg /kinetics/PP1/PP1_active/Deph_thr286b /kinetics/CaMKII/CaMKII MM_PRD pA
addmsg /kinetics/PP1/PP1_active /kinetics/PP1/PP1_active/Deph_thr286b ENZYME n
addmsg /kinetics/PP1/PP1_active/Deph_thr286b /kinetics/PP1/PP1_active REAC eA B
addmsg /kinetics/CaM/neurogranin_p /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_neurogranin SUBSTRATE n 
addmsg /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_neurogranin /kinetics/CaM/neurogranin_p REAC sA B 
addmsg /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_neurogranin /kinetics/CaM/neurogranin MM_PRD pA
addmsg /kinetics/CaM/CaM(Ca)n_CaNAB /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_neurogranin ENZYME n
addmsg /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_neurogranin /kinetics/CaM/CaM(Ca)n_CaNAB REAC eA B
addmsg /kinetics/PP1/I1_p /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_inhib1 SUBSTRATE n 
addmsg /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_inhib1 /kinetics/PP1/I1_p REAC sA B 
addmsg /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_inhib1 /kinetics/PP1/I1 MM_PRD pA
addmsg /kinetics/CaM/CaM(Ca)n_CaNAB /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_inhib1 ENZYME n
addmsg /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_inhib1 /kinetics/CaM/CaM(Ca)n_CaNAB REAC eA B
addmsg /kinetics/PP1/PP1_I1_p /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_PP1_I_p SUBSTRATE n 
addmsg /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_PP1_I_p /kinetics/PP1/PP1_I1_p REAC sA B 
addmsg /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_PP1_I_p /kinetics/PP1/PP1_I1 MM_PRD pA
addmsg /kinetics/CaM/CaM(Ca)n_CaNAB /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_PP1_I_p ENZYME n
addmsg /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_PP1_I_p /kinetics/CaM/CaM(Ca)n_CaNAB REAC eA B
addmsg /kinetics/PP1/I1_p /kinetics/Phosphatase/PP2A/PP2A_dephospho_I1 SUBSTRATE n 
addmsg /kinetics/Phosphatase/PP2A/PP2A_dephospho_I1 /kinetics/PP1/I1_p REAC sA B 
addmsg /kinetics/Phosphatase/PP2A/PP2A_dephospho_I1 /kinetics/PP1/I1 MM_PRD pA
addmsg /kinetics/Phosphatase/PP2A /kinetics/Phosphatase/PP2A/PP2A_dephospho_I1 ENZYME n
addmsg /kinetics/Phosphatase/PP2A/PP2A_dephospho_I1 /kinetics/Phosphatase/PP2A REAC eA B
addmsg /kinetics/PP1/PP1_I1_p /kinetics/Phosphatase/PP2A/PP2A_dephospho_PP1_I_p SUBSTRATE n 
addmsg /kinetics/Phosphatase/PP2A/PP2A_dephospho_PP1_I_p /kinetics/PP1/PP1_I1_p REAC sA B 
addmsg /kinetics/Phosphatase/PP2A/PP2A_dephospho_PP1_I_p /kinetics/PP1/PP1_I1 MM_PRD pA
addmsg /kinetics/Phosphatase/PP2A /kinetics/Phosphatase/PP2A/PP2A_dephospho_PP1_I_p ENZYME n
addmsg /kinetics/Phosphatase/PP2A/PP2A_dephospho_PP1_I_p /kinetics/Phosphatase/PP2A REAC eA B
addmsg /kinetics/PP1/I1_p /kinetics/CaM/CaNAB_Ca4/dephosph_inhib1_noCaM SUBSTRATE n 
addmsg /kinetics/CaM/CaNAB_Ca4/dephosph_inhib1_noCaM /kinetics/PP1/I1_p REAC sA B 
addmsg /kinetics/CaM/CaNAB_Ca4/dephosph_inhib1_noCaM /kinetics/PP1/I1 MM_PRD pA
addmsg /kinetics/CaM/CaNAB_Ca4 /kinetics/CaM/CaNAB_Ca4/dephosph_inhib1_noCaM ENZYME n
addmsg /kinetics/CaM/CaNAB_Ca4/dephosph_inhib1_noCaM /kinetics/CaM/CaNAB_Ca4 REAC eA B
addmsg /kinetics/AC/ATP /kinetics/AC/AC1_CaM/kenz SUBSTRATE n 
addmsg /kinetics/AC/AC1_CaM/kenz /kinetics/AC/ATP REAC sA B 
addmsg /kinetics/AC/AC1_CaM/kenz /kinetics/AC/cAMP MM_PRD pA 
addmsg /kinetics/AC/AC1_CaM /kinetics/AC/AC1_CaM/kenz ENZYME n 
addmsg /kinetics/AC/ATP /kinetics/AC/AC2_p/kenz SUBSTRATE n 
addmsg /kinetics/AC/AC2_p/kenz /kinetics/AC/ATP REAC sA B 
addmsg /kinetics/AC/AC2_p/kenz /kinetics/AC/cAMP MM_PRD pA 
addmsg /kinetics/AC/AC2_p /kinetics/AC/AC2_p/kenz ENZYME n 
addmsg /kinetics/AC/ATP /kinetics/AC/AC2_Gs/kenz SUBSTRATE n 
addmsg /kinetics/AC/AC2_Gs/kenz /kinetics/AC/ATP REAC sA B 
addmsg /kinetics/AC/AC2_Gs/kenz /kinetics/AC/cAMP MM_PRD pA 
addmsg /kinetics/AC/AC2_Gs /kinetics/AC/AC2_Gs/kenz ENZYME n 
addmsg /kinetics/AC/ATP /kinetics/AC/AC1_Gs/kenz SUBSTRATE n 
addmsg /kinetics/AC/AC1_Gs/kenz /kinetics/AC/ATP REAC sA B 
addmsg /kinetics/AC/AC1_Gs/kenz /kinetics/AC/cAMP MM_PRD pA 
addmsg /kinetics/AC/AC1_Gs /kinetics/AC/AC1_Gs/kenz ENZYME n 
addmsg /kinetics/AC/ATP /kinetics/AC/AC2_p_Gs/kenz SUBSTRATE n 
addmsg /kinetics/AC/AC2_p_Gs/kenz /kinetics/AC/ATP REAC sA B 
addmsg /kinetics/AC/AC2_p_Gs/kenz /kinetics/AC/cAMP MM_PRD pA 
addmsg /kinetics/AC/AC2_p_Gs /kinetics/AC/AC2_p_Gs/kenz ENZYME n 
addmsg /kinetics/AC/cAMP /kinetics/AC/cAMP_PDE/PDE SUBSTRATE n 
addmsg /kinetics/AC/cAMP_PDE/PDE /kinetics/AC/cAMP REAC sA B 
addmsg /kinetics/AC/cAMP_PDE/PDE /kinetics/AMP MM_PRD pA
addmsg /kinetics/AC/cAMP_PDE /kinetics/AC/cAMP_PDE/PDE ENZYME n
addmsg /kinetics/AC/cAMP_PDE/PDE /kinetics/AC/cAMP_PDE REAC eA B
addmsg /kinetics/AC/cAMP /kinetics/AC/cAMP_PDE_p/PDE_p SUBSTRATE n 
addmsg /kinetics/AC/cAMP_PDE_p/PDE_p /kinetics/AC/cAMP REAC sA B 
addmsg /kinetics/AC/cAMP_PDE_p/PDE_p /kinetics/AMP MM_PRD pA
addmsg /kinetics/AC/cAMP_PDE_p /kinetics/AC/cAMP_PDE_p/PDE_p ENZYME n
addmsg /kinetics/AC/cAMP_PDE_p/PDE_p /kinetics/AC/cAMP_PDE_p REAC eA B
addmsg /kinetics/AC/cAMP /kinetics/AC/PDE1/PDE1 SUBSTRATE n 
addmsg /kinetics/AC/PDE1/PDE1 /kinetics/AC/cAMP REAC sA B 
addmsg /kinetics/AC/PDE1/PDE1 /kinetics/AMP MM_PRD pA
addmsg /kinetics/AC/PDE1 /kinetics/AC/PDE1/PDE1 ENZYME n
addmsg /kinetics/AC/PDE1/PDE1 /kinetics/AC/PDE1 REAC eA B
addmsg /kinetics/AC/cAMP /kinetics/AC/CaM.PDE1/CaM.PDE1 SUBSTRATE n 
addmsg /kinetics/AC/CaM.PDE1/CaM.PDE1 /kinetics/AC/cAMP REAC sA B 
addmsg /kinetics/AC/CaM.PDE1/CaM.PDE1 /kinetics/AMP MM_PRD pA
addmsg /kinetics/AC/CaM.PDE1 /kinetics/AC/CaM.PDE1/CaM.PDE1 ENZYME n
addmsg /kinetics/AC/CaM.PDE1/CaM.PDE1 /kinetics/AC/CaM.PDE1 REAC eA B
addmsg /kinetics/S6Kinase/S6K_thr_412 /kinetics/PI3K_activation/PDK1/S6K_phospho SUBSTRATE n 
addmsg /kinetics/PI3K_activation/PDK1/S6K_phospho /kinetics/S6Kinase/S6K_thr_412 REAC sA B 
addmsg /kinetics/PI3K_activation/PDK1/S6K_phospho /kinetics/S6Kinase/S6K_thr_252 MM_PRD pA
addmsg /kinetics/PI3K_activation/PDK1 /kinetics/PI3K_activation/PDK1/S6K_phospho ENZYME n
addmsg /kinetics/PI3K_activation/PDK1/S6K_phospho /kinetics/PI3K_activation/PDK1 REAC eA B
addmsg /kinetics/S6Kinase/S6K_p /kinetics/Phosphatase/PP2A/dephos_clus_S6K SUBSTRATE n 
addmsg /kinetics/Phosphatase/PP2A/dephos_clus_S6K /kinetics/S6Kinase/S6K_p REAC sA B 
addmsg /kinetics/Phosphatase/PP2A/dephos_clus_S6K /kinetics/S6Kinase/S6K MM_PRD pA
addmsg /kinetics/Phosphatase/PP2A /kinetics/Phosphatase/PP2A/dephos_clus_S6K ENZYME n
addmsg /kinetics/Phosphatase/PP2A/dephos_clus_S6K /kinetics/Phosphatase/PP2A REAC eA B
addmsg /kinetics/S6Kinase/S6K_thr_412 /kinetics/Phosphatase/PP2A/dephos_S6K SUBSTRATE n 
addmsg /kinetics/Phosphatase/PP2A/dephos_S6K /kinetics/S6Kinase/S6K_thr_412 REAC sA B 
addmsg /kinetics/Phosphatase/PP2A/dephos_S6K /kinetics/S6Kinase/S6K_p MM_PRD pA
addmsg /kinetics/Phosphatase/PP2A /kinetics/Phosphatase/PP2A/dephos_S6K ENZYME n
addmsg /kinetics/Phosphatase/PP2A/dephos_S6K /kinetics/Phosphatase/PP2A REAC eA B
addmsg /kinetics/S6Kinase/S6K_thr_252 /kinetics/Phosphatase/PP2A/dephosp_S6K SUBSTRATE n 
addmsg /kinetics/Phosphatase/PP2A/dephosp_S6K /kinetics/S6Kinase/S6K_thr_252 REAC sA B 
addmsg /kinetics/Phosphatase/PP2A/dephosp_S6K /kinetics/S6Kinase/S6K_thr_412 MM_PRD pA
addmsg /kinetics/Phosphatase/PP2A /kinetics/Phosphatase/PP2A/dephosp_S6K ENZYME n
addmsg /kinetics/Phosphatase/PP2A/dephosp_S6K /kinetics/Phosphatase/PP2A REAC eA B
addmsg /kinetics/AKT_activation/PIP3_AKT_t308_s473 /kinetics/Phosphatase/PP2A/Dephos_AKTser473 SUBSTRATE n 
addmsg /kinetics/Phosphatase/PP2A/Dephos_AKTser473 /kinetics/AKT_activation/PIP3_AKT_t308_s473 REAC sA B 
addmsg /kinetics/Phosphatase/PP2A/Dephos_AKTser473 /kinetics/AKT_activation/PIP3_AKT_thr308 MM_PRD pA
addmsg /kinetics/Phosphatase/PP2A /kinetics/Phosphatase/PP2A/Dephos_AKTser473 ENZYME n
addmsg /kinetics/Phosphatase/PP2A/Dephos_AKTser473 /kinetics/Phosphatase/PP2A REAC eA B
addmsg /kinetics/AKT_activation/PIP3_AKT_thr308 /kinetics/Phosphatase/PP2A/Dephosph_AKTthr308 SUBSTRATE n 
addmsg /kinetics/Phosphatase/PP2A/Dephosph_AKTthr308 /kinetics/AKT_activation/PIP3_AKT_thr308 REAC sA B 
addmsg /kinetics/Phosphatase/PP2A/Dephosph_AKTthr308 /kinetics/AKT_activation/PIP3_AKT MM_PRD pA
addmsg /kinetics/Phosphatase/PP2A /kinetics/Phosphatase/PP2A/Dephosph_AKTthr308 ENZYME n
addmsg /kinetics/Phosphatase/PP2A/Dephosph_AKTthr308 /kinetics/Phosphatase/PP2A REAC eA B
addmsg /kinetics/Translation_elongation/eEFthr_56 /kinetics/Phosphatase/PP2A/eEF2thr_56_dephospho SUBSTRATE n 
addmsg /kinetics/Phosphatase/PP2A/eEF2thr_56_dephospho /kinetics/Translation_elongation/eEFthr_56 REAC sA B 
addmsg /kinetics/Phosphatase/PP2A/eEF2thr_56_dephospho /kinetics/Translation_elongation/eEF2 MM_PRD pA
addmsg /kinetics/Phosphatase/PP2A /kinetics/Phosphatase/PP2A/eEF2thr_56_dephospho ENZYME n
addmsg /kinetics/Phosphatase/PP2A/eEF2thr_56_dephospho /kinetics/Phosphatase/PP2A REAC eA B
addmsg /kinetics/4E_BP/4E_BP_t37_46_s65 /kinetics/Phosphatase/PP2A/PP2A_4E_BP_p_p SUBSTRATE n 
addmsg /kinetics/Phosphatase/PP2A/PP2A_4E_BP_p_p /kinetics/4E_BP/4E_BP_t37_46_s65 REAC sA B 
addmsg /kinetics/Phosphatase/PP2A/PP2A_4E_BP_p_p /kinetics/4E_BP/4E_BP_t37_46 MM_PRD pA
addmsg /kinetics/Phosphatase/PP2A /kinetics/Phosphatase/PP2A/PP2A_4E_BP_p_p ENZYME n
addmsg /kinetics/Phosphatase/PP2A/PP2A_4E_BP_p_p /kinetics/Phosphatase/PP2A REAC eA B
addmsg /kinetics/4E_BP/4E_BP_t37_46 /kinetics/Phosphatase/PP2A/PP2A_4E_BP_p SUBSTRATE n 
addmsg /kinetics/Phosphatase/PP2A/PP2A_4E_BP_p /kinetics/4E_BP/4E_BP_t37_46 REAC sA B 
addmsg /kinetics/Phosphatase/PP2A/PP2A_4E_BP_p /kinetics/4E_BP/4E_BP MM_PRD pA
addmsg /kinetics/Phosphatase/PP2A /kinetics/Phosphatase/PP2A/PP2A_4E_BP_p ENZYME n
addmsg /kinetics/Phosphatase/PP2A/PP2A_4E_BP_p /kinetics/Phosphatase/PP2A REAC eA B
addmsg /kinetics/4E_BP/eIF4E_BP_t37_46_s65 /kinetics/Phosphatase/PP2A/PP2A_4E_BP SUBSTRATE n 
addmsg /kinetics/Phosphatase/PP2A/PP2A_4E_BP /kinetics/4E_BP/eIF4E_BP_t37_46_s65 REAC sA B 
addmsg /kinetics/Phosphatase/PP2A/PP2A_4E_BP /kinetics/4E_BP/eIF4E_BP_thr37_46 MM_PRD pA
addmsg /kinetics/Phosphatase/PP2A /kinetics/Phosphatase/PP2A/PP2A_4E_BP ENZYME n
addmsg /kinetics/Phosphatase/PP2A/PP2A_4E_BP /kinetics/Phosphatase/PP2A REAC eA B
addmsg /kinetics/4E_BP/eIF4E_BP_thr37_46 /kinetics/Phosphatase/PP2A/PP2A_4EBP SUBSTRATE n 
addmsg /kinetics/Phosphatase/PP2A/PP2A_4EBP /kinetics/4E_BP/eIF4E_BP_thr37_46 REAC sA B 
addmsg /kinetics/Phosphatase/PP2A/PP2A_4EBP /kinetics/4E_BP/eIF4E_BP MM_PRD pA
addmsg /kinetics/Phosphatase/PP2A /kinetics/Phosphatase/PP2A/PP2A_4EBP ENZYME n
addmsg /kinetics/Phosphatase/PP2A/PP2A_4EBP /kinetics/Phosphatase/PP2A REAC eA B
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
addmsg /kinetics/TSC1_TSC2/TSC1_TSC2 /kinetics/AKT_activation/PIP3_AKT_t308_s473/TSC2_phospho SUBSTRATE n 
addmsg /kinetics/AKT_activation/PIP3_AKT_t308_s473/TSC2_phospho /kinetics/TSC1_TSC2/TSC1_TSC2 REAC sA B 
addmsg /kinetics/AKT_activation/PIP3_AKT_t308_s473/TSC2_phospho /kinetics/TSC1_TSC2/TSC1_TSC2_p MM_PRD pA
addmsg /kinetics/AKT_activation/PIP3_AKT_t308_s473 /kinetics/AKT_activation/PIP3_AKT_t308_s473/TSC2_phospho ENZYME n
addmsg /kinetics/AKT_activation/PIP3_AKT_t308_s473/TSC2_phospho /kinetics/AKT_activation/PIP3_AKT_t308_s473 REAC eA B
addmsg /kinetics/PLC_g/PLC_g /kinetics/TrKB/BDNF_TrKB2_p_clx/PLC_g_phospho SUBSTRATE n 
addmsg /kinetics/TrKB/BDNF_TrKB2_p_clx/PLC_g_phospho /kinetics/PLC_g/PLC_g REAC sA B 
addmsg /kinetics/TrKB/BDNF_TrKB2_p_clx/PLC_g_phospho /kinetics/PLC_g/PLC_g_p MM_PRD pA
addmsg /kinetics/TrKB/BDNF_TrKB2_p_clx /kinetics/TrKB/BDNF_TrKB2_p_clx/PLC_g_phospho ENZYME n
addmsg /kinetics/TrKB/BDNF_TrKB2_p_clx/PLC_g_phospho /kinetics/TrKB/BDNF_TrKB2_p_clx REAC eA B
addmsg /kinetics/Sos/SHC /kinetics/TrKB/BDNF_TrKB2_p_clx/SHC_phospho SUBSTRATE n 
addmsg /kinetics/TrKB/BDNF_TrKB2_p_clx/SHC_phospho /kinetics/Sos/SHC REAC sA B 
addmsg /kinetics/TrKB/BDNF_TrKB2_p_clx/SHC_phospho /kinetics/Sos/SHC_p MM_PRD pA
addmsg /kinetics/TrKB/BDNF_TrKB2_p_clx /kinetics/TrKB/BDNF_TrKB2_p_clx/SHC_phospho ENZYME n
addmsg /kinetics/TrKB/BDNF_TrKB2_p_clx/SHC_phospho /kinetics/TrKB/BDNF_TrKB2_p_clx REAC eA B
addmsg /kinetics/PI3K_activation/PIP2 /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_PI3K_clx/Phospho SUBSTRATE n 
addmsg /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_PI3K_clx/Phospho /kinetics/PI3K_activation/PIP2 REAC sA B 
addmsg /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_PI3K_clx/Phospho /kinetics/PI3K_activation/PIP3 MM_PRD pA
addmsg /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_PI3K_clx /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_PI3K_clx/Phospho ENZYME n
addmsg /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_PI3K_clx/Phospho /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_PI3K_clx REAC eA B
addmsg /kinetics/PI3K_activation/PIP2 /kinetics/PI3K_activation/PI3K_basal/basal_phosp SUBSTRATE n 
addmsg /kinetics/PI3K_activation/PI3K_basal/basal_phosp /kinetics/PI3K_activation/PIP2 REAC sA B 
addmsg /kinetics/PI3K_activation/PI3K_basal/basal_phosp /kinetics/PI3K_activation/PIP3 MM_PRD pA
addmsg /kinetics/PI3K_activation/PI3K_basal /kinetics/PI3K_activation/PI3K_basal/basal_phosp ENZYME n
addmsg /kinetics/PI3K_activation/PI3K_basal/basal_phosp /kinetics/PI3K_activation/PI3K_basal REAC eA B
addmsg /kinetics/PLC_g/PLC_g /kinetics/PLC_g/PLCg_basal/PLC_g_phospho SUBSTRATE n 
addmsg /kinetics/PLC_g/PLCg_basal/PLC_g_phospho /kinetics/PLC_g/PLC_g REAC sA B 
addmsg /kinetics/PLC_g/PLCg_basal/PLC_g_phospho /kinetics/PLC_g/PLC_g_p MM_PRD pA
addmsg /kinetics/PLC_g/PLCg_basal /kinetics/PLC_g/PLCg_basal/PLC_g_phospho ENZYME n
addmsg /kinetics/PLC_g/PLCg_basal/PLC_g_phospho /kinetics/PLC_g/PLCg_basal REAC eA B
addmsg /kinetics/mTORC1/Rheb_GTP /kinetics/TSC1_TSC2/TSC1_TSC2/TSC2phospho SUBSTRATE n 
addmsg /kinetics/TSC1_TSC2/TSC1_TSC2/TSC2phospho /kinetics/mTORC1/Rheb_GTP REAC sA B 
addmsg /kinetics/TSC1_TSC2/TSC1_TSC2/TSC2phospho /kinetics/mTORC1/Rheb_GDP MM_PRD pA
addmsg /kinetics/TSC1_TSC2/TSC1_TSC2 /kinetics/TSC1_TSC2/TSC1_TSC2/TSC2phospho ENZYME n
addmsg /kinetics/TSC1_TSC2/TSC1_TSC2/TSC2phospho /kinetics/TSC1_TSC2/TSC1_TSC2 REAC eA B
addmsg /kinetics/S6Kinase/S6K_p /kinetics/mTORC1/TOR_Rheb_GTP_clx/S6K_phospho SUBSTRATE n 
addmsg /kinetics/mTORC1/TOR_Rheb_GTP_clx/S6K_phospho /kinetics/S6Kinase/S6K_p REAC sA B 
addmsg /kinetics/mTORC1/TOR_Rheb_GTP_clx/S6K_phospho /kinetics/S6Kinase/S6K_thr_412 MM_PRD pA
addmsg /kinetics/mTORC1/TOR_Rheb_GTP_clx /kinetics/mTORC1/TOR_Rheb_GTP_clx/S6K_phospho ENZYME n
addmsg /kinetics/mTORC1/TOR_Rheb_GTP_clx/S6K_phospho /kinetics/mTORC1/TOR_Rheb_GTP_clx REAC eA B
addmsg /kinetics/4E_BP/eIF4E_BP /kinetics/mTORC1/TOR_Rheb_GTP_clx/TOR_4E_BP_phospho SUBSTRATE n 
addmsg /kinetics/mTORC1/TOR_Rheb_GTP_clx/TOR_4E_BP_phospho /kinetics/4E_BP/eIF4E_BP REAC sA B 
addmsg /kinetics/mTORC1/TOR_Rheb_GTP_clx/TOR_4E_BP_phospho /kinetics/4E_BP/eIF4E_BP_thr37_46 MM_PRD pA
addmsg /kinetics/mTORC1/TOR_Rheb_GTP_clx /kinetics/mTORC1/TOR_Rheb_GTP_clx/TOR_4E_BP_phospho ENZYME n
addmsg /kinetics/mTORC1/TOR_Rheb_GTP_clx/TOR_4E_BP_phospho /kinetics/mTORC1/TOR_Rheb_GTP_clx REAC eA B
addmsg /kinetics/4E_BP/4E_BP /kinetics/mTORC1/TOR_Rheb_GTP_clx/TOR_4E_BP_p SUBSTRATE n 
addmsg /kinetics/mTORC1/TOR_Rheb_GTP_clx/TOR_4E_BP_p /kinetics/4E_BP/4E_BP REAC sA B 
addmsg /kinetics/mTORC1/TOR_Rheb_GTP_clx/TOR_4E_BP_p /kinetics/4E_BP/4E_BP_t37_46 MM_PRD pA
addmsg /kinetics/mTORC1/TOR_Rheb_GTP_clx /kinetics/mTORC1/TOR_Rheb_GTP_clx/TOR_4E_BP_p ENZYME n
addmsg /kinetics/mTORC1/TOR_Rheb_GTP_clx/TOR_4E_BP_p /kinetics/mTORC1/TOR_Rheb_GTP_clx REAC eA B
addmsg /kinetics/40S/40S_inact /kinetics/S6Kinase/S6K_thr_412/S6_phos SUBSTRATE n 
addmsg /kinetics/S6Kinase/S6K_thr_412/S6_phos /kinetics/40S/40S_inact REAC sA B 
addmsg /kinetics/S6Kinase/S6K_thr_412/S6_phos /kinetics/40S/40S MM_PRD pA
addmsg /kinetics/S6Kinase/S6K_thr_412 /kinetics/S6Kinase/S6K_thr_412/S6_phos ENZYME n
addmsg /kinetics/S6Kinase/S6K_thr_412/S6_phos /kinetics/S6Kinase/S6K_thr_412 REAC eA B
addmsg /kinetics/CaMKIII/CaMKIII /kinetics/S6Kinase/S6K_thr_252/CaMKIII_phospho SUBSTRATE n 
addmsg /kinetics/S6Kinase/S6K_thr_252/CaMKIII_phospho /kinetics/CaMKIII/CaMKIII REAC sA B 
addmsg /kinetics/S6Kinase/S6K_thr_252/CaMKIII_phospho /kinetics/CaMKIII/CaMKIII_p MM_PRD pA
addmsg /kinetics/S6Kinase/S6K_thr_252 /kinetics/S6Kinase/S6K_thr_252/CaMKIII_phospho ENZYME n
addmsg /kinetics/S6Kinase/S6K_thr_252/CaMKIII_phospho /kinetics/S6Kinase/S6K_thr_252 REAC eA B
addmsg /kinetics/40S/40S_inact /kinetics/S6Kinase/S6K_thr_252/S6_phospho SUBSTRATE n 
addmsg /kinetics/S6Kinase/S6K_thr_252/S6_phospho /kinetics/40S/40S_inact REAC sA B 
addmsg /kinetics/S6Kinase/S6K_thr_252/S6_phospho /kinetics/40S/40S MM_PRD pA
addmsg /kinetics/S6Kinase/S6K_thr_252 /kinetics/S6Kinase/S6K_thr_252/S6_phospho ENZYME n
addmsg /kinetics/S6Kinase/S6K_thr_252/S6_phospho /kinetics/S6Kinase/S6K_thr_252 REAC eA B
addmsg /kinetics/Translation_elongation/eEF2 /kinetics/CaMKIII/CaMKIII_CaM_Ca4/phospho SUBSTRATE n 
addmsg /kinetics/CaMKIII/CaMKIII_CaM_Ca4/phospho /kinetics/Translation_elongation/eEF2 REAC sA B 
addmsg /kinetics/CaMKIII/CaMKIII_CaM_Ca4/phospho /kinetics/Translation_elongation/eEFthr_56 MM_PRD pA
addmsg /kinetics/CaMKIII/CaMKIII_CaM_Ca4 /kinetics/CaMKIII/CaMKIII_CaM_Ca4/phospho ENZYME n
addmsg /kinetics/CaMKIII/CaMKIII_CaM_Ca4/phospho /kinetics/CaMKIII/CaMKIII_CaM_Ca4 REAC eA B
addmsg /kinetics/Translation_elongation/eEF2 /kinetics/CaMKIII/CaMKIII_basal/eEF2thr56_basal SUBSTRATE n 
addmsg /kinetics/CaMKIII/CaMKIII_basal/eEF2thr56_basal /kinetics/Translation_elongation/eEF2 REAC sA B 
addmsg /kinetics/CaMKIII/CaMKIII_basal/eEF2thr56_basal /kinetics/Translation_elongation/eEFthr_56 MM_PRD pA
addmsg /kinetics/CaMKIII/CaMKIII_basal /kinetics/CaMKIII/CaMKIII_basal/eEF2thr56_basal ENZYME n
addmsg /kinetics/CaMKIII/CaMKIII_basal/eEF2thr56_basal /kinetics/CaMKIII/CaMKIII_basal REAC eA B
addmsg /kinetics/CaMKIII/CaMKIII /kinetics/S6Kinase/S6K_basal/CaMKIII_basal SUBSTRATE n 
addmsg /kinetics/S6Kinase/S6K_basal/CaMKIII_basal /kinetics/CaMKIII/CaMKIII REAC sA B 
addmsg /kinetics/S6Kinase/S6K_basal/CaMKIII_basal /kinetics/CaMKIII/CaMKIII_p MM_PRD pA
addmsg /kinetics/S6Kinase/S6K_basal /kinetics/S6Kinase/S6K_basal/CaMKIII_basal ENZYME n
addmsg /kinetics/S6Kinase/S6K_basal/CaMKIII_basal /kinetics/S6Kinase/S6K_basal REAC eA B
addmsg /kinetics/protein/AA /kinetics/Translation_elongation/Translation_clx/pro_syn SUBSTRATE n 
addmsg /kinetics/Translation_elongation/Translation_clx/pro_syn /kinetics/protein/AA REAC sA B 
addmsg /kinetics/Translation_elongation/Translation_clx/pro_syn /kinetics/protein/peptide MM_PRD pA
addmsg /kinetics/Translation_elongation/Translation_clx /kinetics/Translation_elongation/Translation_clx/pro_syn ENZYME n
addmsg /kinetics/Translation_elongation/Translation_clx/pro_syn /kinetics/Translation_elongation/Translation_clx REAC eA B
addmsg /kinetics/protein/rad_AA /kinetics/Translation_elongation/Translation_clx/rad_pro_syn SUBSTRATE n 
addmsg /kinetics/Translation_elongation/Translation_clx/rad_pro_syn /kinetics/protein/rad_AA REAC sA B 
addmsg /kinetics/Translation_elongation/Translation_clx/rad_pro_syn /kinetics/protein/rad_peptide MM_PRD pA
addmsg /kinetics/Translation_elongation/Translation_clx /kinetics/Translation_elongation/Translation_clx/rad_pro_syn ENZYME n
addmsg /kinetics/Translation_elongation/Translation_clx/rad_pro_syn /kinetics/Translation_elongation/Translation_clx REAC eA B
addmsg /kinetics/S6Kinase/S6K /kinetics/MAPK/MAPK_p_p/cluster_phospho_S6K SUBSTRATE n 
addmsg /kinetics/MAPK/MAPK_p_p/cluster_phospho_S6K /kinetics/S6Kinase/S6K REAC sA B 
addmsg /kinetics/MAPK/MAPK_p_p/cluster_phospho_S6K /kinetics/S6Kinase/S6K_p MM_PRD pA
addmsg /kinetics/MAPK/MAPK_p_p /kinetics/MAPK/MAPK_p_p/cluster_phospho_S6K ENZYME n
addmsg /kinetics/MAPK/MAPK_p_p/cluster_phospho_S6K /kinetics/MAPK/MAPK_p_p REAC eA B
addmsg /kinetics/4E_BP/4E_BP_t37_46 /kinetics/MAPK/MAPK_p_p/MAPK_4E_BP_p_p SUBSTRATE n 
addmsg /kinetics/MAPK/MAPK_p_p/MAPK_4E_BP_p_p /kinetics/4E_BP/4E_BP_t37_46 REAC sA B 
addmsg /kinetics/MAPK/MAPK_p_p/MAPK_4E_BP_p_p /kinetics/4E_BP/4E_BP_t37_46_s65 MM_PRD pA
addmsg /kinetics/MAPK/MAPK_p_p /kinetics/MAPK/MAPK_p_p/MAPK_4E_BP_p_p ENZYME n
addmsg /kinetics/MAPK/MAPK_p_p/MAPK_4E_BP_p_p /kinetics/MAPK/MAPK_p_p REAC eA B
addmsg /kinetics/4E_BP/eIF4E_BP_thr37_46 /kinetics/MAPK/MAPK_p_p/MAPK_4E_BP_phospho SUBSTRATE n 
addmsg /kinetics/MAPK/MAPK_p_p/MAPK_4E_BP_phospho /kinetics/4E_BP/eIF4E_BP_thr37_46 REAC sA B 
addmsg /kinetics/MAPK/MAPK_p_p/MAPK_4E_BP_phospho /kinetics/4E_BP/eIF4E_BP_t37_46_s65 MM_PRD pA
addmsg /kinetics/MAPK/MAPK_p_p /kinetics/MAPK/MAPK_p_p/MAPK_4E_BP_phospho ENZYME n
addmsg /kinetics/MAPK/MAPK_p_p/MAPK_4E_BP_phospho /kinetics/MAPK/MAPK_p_p REAC eA B
addmsg /kinetics/Ras/GDP_Ras /kinetics/Ras/inact_GEF/basal_GEF_activity SUBSTRATE n 
addmsg /kinetics/Ras/inact_GEF/basal_GEF_activity /kinetics/Ras/GDP_Ras REAC sA B 
addmsg /kinetics/Ras/inact_GEF/basal_GEF_activity /kinetics/Ras/GTP_Ras MM_PRD pA
addmsg /kinetics/Ras/inact_GEF /kinetics/Ras/inact_GEF/basal_GEF_activity ENZYME n
addmsg /kinetics/Ras/inact_GEF/basal_GEF_activity /kinetics/Ras/inact_GEF REAC eA B
addmsg /kinetics/protein/AA /kinetics/Translation_elongation/Basal_Translation/basal_syn SUBSTRATE n 
addmsg /kinetics/Translation_elongation/Basal_Translation/basal_syn /kinetics/protein/AA REAC sA B 
addmsg /kinetics/Translation_elongation/Basal_Translation/basal_syn /kinetics/protein/peptide MM_PRD pA
addmsg /kinetics/Translation_elongation/Basal_Translation /kinetics/Translation_elongation/Basal_Translation/basal_syn ENZYME n
addmsg /kinetics/Translation_elongation/Basal_Translation/basal_syn /kinetics/Translation_elongation/Basal_Translation REAC eA B
addmsg /kinetics/protein/rad_AA /kinetics/Translation_elongation/Basal_Translation/rad_basal_syn SUBSTRATE n 
addmsg /kinetics/Translation_elongation/Basal_Translation/rad_basal_syn /kinetics/protein/rad_AA REAC sA B 
addmsg /kinetics/Translation_elongation/Basal_Translation/rad_basal_syn /kinetics/protein/peptide MM_PRD pA
addmsg /kinetics/Translation_elongation/Basal_Translation /kinetics/Translation_elongation/Basal_Translation/rad_basal_syn ENZYME n
addmsg /kinetics/Translation_elongation/Basal_Translation/rad_basal_syn /kinetics/Translation_elongation/Basal_Translation REAC eA B
addmsg /kinetics/40S/40S_inact /kinetics/40S/40S_basal/basal SUBSTRATE n 
addmsg /kinetics/40S/40S_basal/basal /kinetics/40S/40S_inact REAC sA B 
addmsg /kinetics/40S/40S_basal/basal /kinetics/40S/40S MM_PRD pA
addmsg /kinetics/40S/40S_basal /kinetics/40S/40S_basal/basal ENZYME n
addmsg /kinetics/40S/40S_basal/basal /kinetics/40S/40S_basal REAC eA B
addmsg /kinetics/PI3K_activation/PIP3 /kinetics/PI3K_activation/PTEN/PIP3_dephosp SUBSTRATE n 
addmsg /kinetics/PI3K_activation/PTEN/PIP3_dephosp /kinetics/PI3K_activation/PIP3 REAC sA B 
addmsg /kinetics/PI3K_activation/PTEN/PIP3_dephosp /kinetics/PI3K_activation/PIP2 MM_PRD pA
addmsg /kinetics/PI3K_activation/PTEN /kinetics/PI3K_activation/PTEN/PIP3_dephosp ENZYME n
addmsg /kinetics/PI3K_activation/PTEN/PIP3_dephosp /kinetics/PI3K_activation/PTEN REAC eA B
addmsg /kinetics/PI3K_activation/PIP2 /kinetics/Ras/Ras_GTP_PI3K/PIP2_phospho_Ras_GTP SUBSTRATE n 
addmsg /kinetics/Ras/Ras_GTP_PI3K/PIP2_phospho_Ras_GTP /kinetics/PI3K_activation/PIP2 REAC sA B 
addmsg /kinetics/Ras/Ras_GTP_PI3K/PIP2_phospho_Ras_GTP /kinetics/PI3K_activation/PIP3 MM_PRD pA
addmsg /kinetics/Ras/Ras_GTP_PI3K /kinetics/Ras/Ras_GTP_PI3K/PIP2_phospho_Ras_GTP ENZYME n
addmsg /kinetics/Ras/Ras_GTP_PI3K/PIP2_phospho_Ras_GTP /kinetics/Ras/Ras_GTP_PI3K REAC eA B
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
addmsg /kinetics/mGluR/Rec_Glu /kinetics/barr2_signaling/GRK/GRK_binding SUBSTRATE n 
addmsg /kinetics/barr2_signaling/GRK/GRK_binding /kinetics/mGluR/Rec_Glu REAC sA B 
addmsg /kinetics/barr2_signaling/GRK/GRK_binding /kinetics/barr2_signaling/L.mGluR_p MM_PRD pA
addmsg /kinetics/barr2_signaling/GRK /kinetics/barr2_signaling/GRK/GRK_binding ENZYME n
addmsg /kinetics/barr2_signaling/GRK/GRK_binding /kinetics/barr2_signaling/GRK REAC eA B
addmsg /kinetics/barr2_signaling/Internal_mGluR_p /kinetics/Phosphatase/PP2A/mGluR_dephosph SUBSTRATE n 
addmsg /kinetics/Phosphatase/PP2A/mGluR_dephosph /kinetics/barr2_signaling/Internal_mGluR_p REAC sA B 
addmsg /kinetics/Phosphatase/PP2A/mGluR_dephosph /kinetics/barr2_signaling/Internal_mGluR MM_PRD pA
addmsg /kinetics/Phosphatase/PP2A /kinetics/Phosphatase/PP2A/mGluR_dephosph ENZYME n
addmsg /kinetics/Phosphatase/PP2A/mGluR_dephosph /kinetics/Phosphatase/PP2A REAC eA B
addmsg /kinetics/MAPK/MAPKK /kinetics/MAPK/craf_1_p/MEK_phospho SUBSTRATE n 
addmsg /kinetics/MAPK/craf_1_p/MEK_phospho /kinetics/MAPK/MAPKK REAC sA B 
addmsg /kinetics/MAPK/craf_1_p/MEK_phospho /kinetics/MAPK/MAPKK_p MM_PRD pA
addmsg /kinetics/MAPK/craf_1_p /kinetics/MAPK/craf_1_p/MEK_phospho ENZYME n
addmsg /kinetics/MAPK/craf_1_p/MEK_phospho /kinetics/MAPK/craf_1_p REAC eA B
addmsg /kinetics/MAPK/MAPKK_p /kinetics/MAPK/craf_1_p/MEKp_phospho SUBSTRATE n 
addmsg /kinetics/MAPK/craf_1_p/MEKp_phospho /kinetics/MAPK/MAPKK_p REAC sA B 
addmsg /kinetics/MAPK/craf_1_p/MEKp_phospho /kinetics/MAPK/MAPKK_p_p MM_PRD pA
addmsg /kinetics/MAPK/craf_1_p /kinetics/MAPK/craf_1_p/MEKp_phospho ENZYME n
addmsg /kinetics/MAPK/craf_1_p/MEKp_phospho /kinetics/MAPK/craf_1_p REAC eA B
addmsg /kinetics/MAPK/MAPK_p_p /graphs/conc1/MAPK_p.Co PLOT Co *MAPK_p_p *orange

enddump
 // End of dump
call /kinetics/PKC/PKC_DAG/notes LOAD \ 
"CoInit was .0624"
call /kinetics/PKC/PKC_cytosolic/notes LOAD \ 
"Marquez et al J. Immun 149,2560(92) est 1e6/cell for chromaffin cells We will use 1 uM as our initial concen"
call /kinetics/PLA2/PLA2_cytosolic/notes LOAD \ 
"Calculated cytosolic was 20 nm from Wijkander and Sundler However, Leslie and Channon use about 400 nM. Need to confirm, but this is the value I use here. Another recalc of W&S gives 1uM"
call /kinetics/PLA2/APC/notes LOAD \ 
"arachodonylphosphatidylcholine is the favoured substrate from Wijkander and Sundler, JBC 202 pp 873-880, 1991. Their assay used 30 uM substrate, which is what the kinetics in this model are based on. For the later model we should locate a more realistic value for APC."
call /kinetics/PLA2/PLA2_p_Ca/notes LOAD \ 
"Phosphorylated form of PLA2. Still need to hook it up using kinases. PKA: Wightman et al JBC 257 pp6650 1982 PKC: Many refs, eg Gronich et al JBC 263 pp 16645, 1988 but see Lin etal MAPK: Lin et al, Cell 72 pp 269, 1993. Show 3x with MAPK but not PKC alone Do not know if there is a Ca requirement for active phosphorylated state."
call /kinetics/PI3K_activation/temp_PIP2/notes LOAD \ 
"This isn't explicitly present in the M&L model, but is obviously needed. I assume its conc is fixed at 1uM for now, which is a bit high. PLA2 is stim 7x by PIP2 @ 0.5 uM (Leslie and Channon BBA 1045:261(1990) Leslie and Channon say PIP2 is present at 0.1 - 0.2mol% range in membs, which comes to 50 nM. Ref is Majerus et al Cell 37 pp 701-703 1984 Lets use a lower level of 30 nM, same ref...."
call /kinetics/PI3K_activation/IP3/notes LOAD \ 
"Peak IP3 is perhaps 15 uM, basal <= 0.2 uM."
call /kinetics/mGluR/Glutamate/notes LOAD \ 
"Varying the amount of (steady state) glu between .01 uM and up, the final amount of G*GTP complex does not change much. This means that the system should be reasonably robust wr to the amount of glu in the synaptic cleft. It would be nice to know how fast it is removed."
call /kinetics/PLCbeta/PLC/notes LOAD \ 
"Total PLC = 0.8 uM see Ryu et al JBC 262 (26) pp 12511 1987"
call /kinetics/PC/notes LOAD \ 
"Phosphatidylcholine is the main (around 55%) metabolic product of DAG, follwed by PE (around 25%). Ref is Welsh and Cabot, JCB35:231-245(1987)"
call /kinetics/PLCbeta/PLC_Ca_Gq/notes LOAD \ 
"This should really be labelled PLC-G*GTP-Ca. This is the activated form of the enzyme. Mahama and Linderman assume that the IP3 precursors are not rate-limiting, but I will include those for completeness as they may be needed later."
call /kinetics/Gprotein/BetaGamma/notes LOAD \ 
"These exist in a nebulous sense in this model, basically only to balance the conservation equations. The details of their reassociation with G-GDP are not modeled Resting level =0.0094, stim level =.0236 from all42.g ish."
call /kinetics/Gprotein/G_pGTP/notes LOAD \ 
"Activated G protein. Berstein et al indicate that about 20-40% of the total Gq alpha should bind GTP at steady stim. This sim gives more like 65%."
call /kinetics/Gprotein/G_GDP/notes LOAD \ 
"From M&L, total Gprot = 1e5molecules/cell At equil, 92340 are here, 400 are in G*GTP, and another 600 are assoc with the PLC and 6475 are as G*GDP. This is OK. From Pang and Sternweis JBC 265:30 18707-12 1990 we get conc est 1.6 uM to 0.8 uM. A number of other factors are involved too."
call /kinetics/mGluR/mGluR/notes LOAD \ 
"From M&L, Total # of receptors/cell = 1900 Vol of cell = 1e-15 (10 um cube). Navogadro = 6.023e23 so conversion from n to conc in uM is n/vol*nA * 1e3 = 1.66e-6 However, for typical synaptic channels the density is likely to be very high at the synapse. Use an estimate of 0.1 uM for now. this gives a total of about 60K receptors/cell, which is in line with Fay et at."
call /kinetics/mGluR/Rec_Glu/notes LOAD \ 
"This acts like an enzyme to activate the g proteins Assume cell has vol 1e-15 m^3 (10 uM cube), conversion factor to conc in uM is 6e5"
call /kinetics/mGluR/Rec_Gq/notes LOAD \ 
"Fraction of Rec-Gq is 44% of rec, from Fay et al. Since this is not the same receptor, this value is a bit doubtful. Still, we adjust the rate consts in Rec-bind-Gq to match."
call /kinetics/mGluRAntag/mGluRAntag/notes LOAD \ 
"I am implementing this as acting only on the Rec-Gq complex, based on a more complete model PLC_Gq48.g which showed that the binding to the rec alone contributed only a small amount."
call /kinetics/MAPK/craf_1/notes LOAD \ 
"Couldn't find any ref to the actual conc of craf-1 but I should try Strom et al Oncogene 5 pp 345 In line with the other kinases in the cascade, I estimate the conc to be 0.2 uM. To init we use 0.15, which is close to equil"
call /kinetics/MAPK/MAPKK/notes LOAD \ 
"Conc is from Seger et al JBC 267:20 pp14373 (1992) mwt is 45/46 Kd We assume that phosphorylation on both ser and thr is needed for activiation. See Kyriakis et al Nature 358 417 1992 Init conc of total is 0.18"
call /kinetics/MAPK/MAPK/notes LOAD \ 
"conc is from Sanghera et al JBC 265 pp 52 (1990) A second calculation gives 3.1 uM, from same paper. They est MAPK is 1e-4x total protein, and protein is 15% of cell wt, so MAPK is 1.5e-5g/ml = 0.36uM. which is closer to our first estimate. Lets use this."
call /kinetics/MAPK/craf_1_p_p/notes LOAD \ 
"Negative feedback by MAPK* by hyperphosphorylating craf-1* gives rise to this pool. Ueki et al JBC 269(22):15756-15761, 1994"
call /kinetics/MAPK/MAPK_p/notes LOAD \ 
"Haystead et al FEBS Lett. 306(1) pp 17-22 show that phosphorylation is strictly sequential, first tyr185 then thr183."
call /kinetics/MAPK/MAPKK_p_p/notes LOAD \ 
"MAPKK phosphorylates MAPK on both the tyr and thr residues, first tyr then thr. Refs: Seger et al JBC267:20 pp 14373 1992 The MAPKK itself is phosphorylated on ser as well as thr residues. Let us assume that the ser goes first, and that the sequential phosphorylation is needed. See Kyriakis et al Nature 358 417-421 1992"
call /kinetics/MAPK/MAPKK_p/notes LOAD \ 
"Intermediately phophorylated, assumed inactive, form of MAPKK"
call /kinetics/Phosphatase/MKP_1/notes LOAD \ 
"MKP-1 dephosphoryates and inactivates MAPK in vivo: Sun et al Cell 75 487-493 1993. Levels of MKP-1 are regulated, and rise in 1 hour. Kinetics from Charles et al PNAS 90:5292-5296 1993. They refer to Charles et al Oncogene 7 187-190 who show that half-life of MKP1/3CH134 is 40 min. 80% deph of MAPK in 20 min Sep 17 1997: CoInit now 0.4x to 0.0032. See parm searches from jun96 on."
call /kinetics/Phosphatase/PPhosphatase2A/notes LOAD \ 
"Refs: Pato et al Biochem J 293:35-41(93); Takai&Mieskes Biochem J 275:233-239 k1=1.46e-4, k2=1000,k3=250. these use kcat values for calponin. Also, units of kcat may be in min! revert to Vmax base: k3=6, k2=25,k1=3.3e-6 or 6,6,1e-6 CoInit assumed 0.1 uM. See NOTES for MAPK_Ras50.g. CoInit now 0.08 Sep 17 1997: Raise CoInt 1.4x to 0.224, see parm searches from jun 96 on."
call /kinetics/Ras/GEF_Gprot_bg/notes LOAD \ 
"Guanine nucleotide exchange factor. This activates raf by exchanging bound GDP with GTP. I have left the GDP/GTP out of this reaction, it would be trivial to put them in. See Boguski & McCormick. Possible candidate molecules: RasGRF, smgGDS, Vav (in dispute). rasGRF: Kcat= 1.2/min Km = 680 nM smgGDS: Kcat: 0.37 /min, Km = 220 nM. vav: Turnover up over baseline by 10X,"
call /kinetics/Ras/inact_GEF/notes LOAD \ 
"Assume that SoS is present only at 50 nM. Revised to 100 nM to get equil to experimentally known levels."
call /kinetics/Ras/GEF_p/notes LOAD \ 
"phosphorylated and thereby activated form of GEF. See, e.g. Orita et al JBC 268:34 25542-25546 1993, Gulbins et al. It is not clear whether there is major specificity for tyr or ser/thr."
call /kinetics/Ras/GTP_Ras/notes LOAD \ 
"Only a very small fraction (7% unstim, 15% stim) of ras is GTP-bound. Gibbs et al JBC 265(33) 20437"
call /kinetics/Ras/GDP_Ras/notes LOAD \ 
"GDP bound form. See Rosen et al Neuron 12 1207-1221 June 1994. the activation loop is based on Boguski and McCormick Nature 366 643-654 93 Assume Ras is present at about the same level as craf-1, 0.2 uM. Hallberg et al JBC 269:6 3913-3916 1994 estimate upto 5-10% of cellular Raf is assoc with Ras. Given that only 5-10% of Ras is GTP-bound, we need similar amounts of Ras as Raf."
call /kinetics/Ras/GAP/notes LOAD \ 
"GTPase-activating proteins. See Boguski and McCormick. Turn off Ras by helping to hydrolyze bound GTP. This one is probably NF1, ie., Neurofibromin as it is inhibited by AA and lipids, and expressed in neural cells. p120-GAP is also a possible candidate, but is less regulated. Both may exist at similar levels. See Eccleston et al JBC 268(36) pp27012-19 Level=.002"
call /kinetics/Ras/inact_GEF_p/notes LOAD \ 
"Phosphorylation-inactivated form of GEF. See Hordijk et al JBC 269:5 3534-3538 1994 and Buregering et al EMBO J 12:11 4211-4220 1993"
call /kinetics/Ras/CaM_GEF/notes LOAD \ 
"See Farnsworth et al Nature 376 524-527 1995"
call /kinetics/EGFR/EGFR/notes LOAD \ 
"Berkers et al JBC 266 say 22K hi aff recs. Sherrill and Kyte Biochemistry 35 use range 4-200 nM. These match, lets use them."
call /kinetics/EGFR/L.EGFR/notes LOAD \ 
"This is terribly simplified: there are many interesting intermediate stages, including dimerization and assoc with adapter molecules like Shc, that contribute to the activation of the EGFR."
call /kinetics/Sos/SHC/notes LOAD \ 
"There are 2 isoforms: 52 KDa and 46 KDa (See Okada et al JBC 270:35 pp 20737 1995). They are acted up on by the EGFR in very similar ways, and apparently both bind Grb2 similarly, so we'll bundle them together here. Sasaoka et al JBC 269:51 pp 32621 1994 show immunoprecs where it looks like there is at least as much Shc as Grb2. So we'll tentatively say there is 1 uM of Shc."
call /kinetics/Sos/Grb2/notes LOAD \ 
"There is probably a lot of it in the cell: it is also known as Ash (abundant src homology protein I think). Also Waters et al JBC 271:30 18224 1996 say that only a small fraction of cellular Grb is precipitated out when SoS is precipitated. As most of the Sos seems to be associated with Grb2, it would seem like there is a lot of the latter. Say 1 uM. I haven't been able to find a decent...."
call /kinetics/Sos/Sos/notes LOAD \ 
"I have tried using low (0.02 uM) initial concs, but these give a very flat response to EGF stim although the overall activation of Ras is not too bad. I am reverting to 0.1 because we expect a sharp initial response, followed by a decline. Sep 17 1997: The transient activation curve looks better with [Sos] = 0.05. Apr 26 1998: Some error there, it is better where it was at 0.1"
call /kinetics/PLC_g/PLC_g/notes LOAD \ 
"Amount from Homma et al JBC 263:14 6592-6598 1988"
call /kinetics/CaMKII/CaMKII/notes LOAD \ 
"Huge conc of CaMKII. In PSD it is 20-40% of protein, so we assume it is around 2.5% of protein in spine as a whole. This level is so high it is unlikely to matter much if we are off a bit. This comes to about 70 uM."
call /kinetics/CaMKII/CaMKII_thr286_p_CaM/notes LOAD \ 
"From Hanson and Schulman, the thr286 is responsible for autonomous activation of CaMKII."
call /kinetics/CaMKII/CaMKII_p_p_p/notes LOAD \ 
"From Hanson and Schulman, the CaMKII does a lot of autophosphorylation just after the CaM is released. This prevents further CaM binding and renders the enzyme quite independent of Ca."
call /kinetics/CaMKII/CaMKII_thr286/notes LOAD \ 
"I am not sure if we need to endow this one with a lot of enzs. It is likely to be a short-lived intermediate, since it will be phosphorylated further as soon as the CAM falls off."
call /kinetics/CaMKII/CaMKII_thr306/notes LOAD \ 
"This forms due to basal autophosphorylation, but I think it has to be considered as a pathway even if some CaM is floating around. In either case it will tend to block further binding of CaM, and will not display any enzyme activity. See Hanson and Schulman JBC 267:24 pp17216-17224 1992"
call /kinetics/PP1/PP1_active/notes LOAD \ 
"Cohen et al Meth Enz 159 390-408 is main source of info conc = 1.8 uM"
call /kinetics/CaM/CaM/notes LOAD \ 
"There is a LOT of this in the cell: upto 1% of total protein mass. (Alberts et al) Say 25 uM. Meyer et al Science 256 1199-1202 1992 refer to studies saying it is comparable to CaMK levels."
call /kinetics/CaM/neurogranin_p/notes LOAD \ 
"The phosph form does not bind CaM (Huang et al ABB 305:2 570-580 1993)"
call /kinetics/CaM/neurogranin/notes LOAD \ 
"Also known as RC3 and p17 and BICKS. Conc in brain >> 2 uM from Martzen and Slemmon J neurosci 64 92-100 1995 but others say less without any #s. Conc in dend spines is much higher than overall, so it could be anywhere from 2 uM to 50. We will estimate 10 uM as a starting point. Gerendasy et al JBC 269:35 22420-22426 1994 have a skeleton model (no numbers) indicating CaM-Ca(n) binding ...."
call /kinetics/CaM/CaM_TR2_Ca2/notes LOAD \ 
"This is the intermediate where the TR2 end (the high-affinity end) has bound the Ca but the TR1 end has not."
call /kinetics/PP1/I1/notes LOAD \ 
"I1 is a 'mixed' inhibitor, but at high enz concs it looks like a non-compet inhibitor (Foulkes et al Eur J Biochem 132 309-313 9183). We treat it as non-compet, so it just turns the enz off without interacting with the binding site. Cohen et al ann rev bioch refer to results where conc is 1.5 to 1.8 uM. In order to get complete inhib of PP1, which is at 1.8 uM, we need >= 1.8 uM."
call /kinetics/PP1/I1_p/notes LOAD \ 
"Dephosph is mainly by PP2B"
call /kinetics/PP2B/CaNAB/notes LOAD \ 
"We assume that the A and B subunits of PP2B are always bound under physiol conditions. Up to 1% of brain protein = 25 uM. I need to work out how it is distributed between cytosolic and particulate fractions. Tallant and Cheung '83 Biochem 22 3630-3635 have conc in many species, average for mammalian brain is around 1 uM."
call /kinetics/PKA/R2C2/notes LOAD \ 
"This is the R2C2 complex, consisting of 2 catalytic (C) subunits, and the R-dimer. See Taylor et al Ann Rev Biochem 1990 59:971-1005 for a review. The Doskeland and Ogreid review is better for numbers. Amount of PKA is about .5 uM."
call /kinetics/PKA/R2C2_cAMP/notes LOAD \ 
"CoInit was .0624"
call /kinetics/PKA/R2_cAMP4/notes LOAD \ 
"Starts at 0.15 for the test of fig 6 in Smith et al, but we aren't using that paper any more."
call /kinetics/PKA/PKA_inhibitor/notes LOAD \ 
"About 25% of PKA C subunit is dissociated in resting cells without having any noticable activity. Doskeland and Ogreid Int J biochem 13 pp1-19 suggest that this is because there is a corresponding amount of inhibitor protein."
call /kinetics/AC/cAMP/notes LOAD \ 
"The conc of this has been a problem. Schaecter and Benowitz use 50 uM, but Shinomura et al have < 5. So I have altered the cAMP-dependent rates in the PKA model to reflect this."
call /kinetics/AC/ATP/notes LOAD \ 
"ATP is present in all cells between 2 and 10 mM. See Lehninger."
call /kinetics/AC/AC1_CaM/notes LOAD \ 
"This version of cyclase is Calmodulin activated. Gs stims it but betagamma inhibits."
call /kinetics/AC/AC1/notes LOAD \ 
"Starting conc at 20 nM."
call /kinetics/AC/AC2_p/notes LOAD \ 
"This version is activated by Gs and by a betagamma and phosphorylation."
call /kinetics/AC/AC2/notes LOAD \ 
"Starting at 0.015 uM."
call /kinetics/AC/cAMP_PDE/notes LOAD \ 
"The levels of the PDE are not known at this time. However, enough kinetic info and info about steady-state levels of cAMP etc are around to make it possible to estimate this."
call /kinetics/AC/cAMP_PDE_p/notes LOAD \ 
"This form has about 2X activity as plain PDE. See Sette et al JBC 269:28 18271-18274 1994."
call /kinetics/AC/PDE1/notes LOAD \ 
"CaM-Dependent PDE. Amount calculated from total rate in brain vs. specific rate."
call /kinetics/AC/CaM.PDE1/notes LOAD \ 
"Activity up 6x following Ca-CaM binding."
call /kinetics/AKT_activation/PIP3_AKT_t308_s473/notes LOAD \ 
"aaa"
call /kinetics/43S_complex/Q.R/notes LOAD \ 
"Q.R= Quaternary complex.Ribosome"
call /kinetics/43S_complex/Quaternary_clx/notes LOAD \ 
"Q= Quaternary complex"
call /kinetics/43S_complex/43Scomplex/notes LOAD \ 
"40S_complex consist of Quaternary complex, mRNA complex, 40S Ribosomes."
call /kinetics/CaM/CaM_Ca2/notes LOAD \ 
"This is the intermediate where the TR2 end (the high-affinity end) has bound the Ca but the TR1 end has not."
call /kinetics/CaM/CaM_Ca/notes LOAD \ 
"This is the intermediate where the TR2 end (the high-affinity end) has bound the Ca but the TR1 end has not."
call /kinetics/Translation_elongation/Basal_Translation/notes LOAD \ 
"It will contribute to mTOR independent translation."
call /kinetics/40S/40S_inact/notes LOAD \ 
"Inactivated form of S6K"
call /kinetics/40S/40S/notes LOAD \ 
"Activated form of S6"
call /kinetics/barr2_signaling/GRK/notes LOAD \ 
"Bychkov et al., 2011. 150ng/mg *0.5mg/ml /65000g/mol = 1.155385nM (which is too low, therefore increasing the concentration arbitrarily by 1000 fold)"
call /kinetics/barr2_signaling/barr2/notes LOAD \ 
"Bychkov et al., 2011. 30ng/mg *0.5mg/ml /40000g/mol = 0.375nM (which is too low, therefore increasing the concentration arbitrarily by 1000 fold)"
call /kinetics/PKC/PKC_act_by_Ca/notes LOAD \ 
"Need est of rate of assoc of Ca and PKC. Assume it is fast The original parameter-searched kf of 439.4 has been scaled by 1/6e8 to account for change of units to n. Kf now 8.16e-7, kb=.6085 Raised kf to 1e-6 to match Ca curve, kb to .5"
call /kinetics/PKC/PKC_act_by_DAG/notes LOAD \ 
"Need est of rate. Assume it is fast Obtained from param search kf raised 10 X : see Shinomura et al PNAS 88 5149-5153 1991. kf changed from 3.865e-7 to 2.0e-7 in line with closer analysis of Shinomura data. 26 June 1996: Corrected DAG data: reduce kf 15x from 2e-7 to 1.333e-8"
call /kinetics/PKC/PKC_DAG_to_memb/notes LOAD \ 
"Raise kb from .087 to 0.1 to match data from Shinomura et al. Lower kf from 1.155 to 1.0 to match data from Shinomura et al."
call /kinetics/PKC/PKC_act_by_Ca_AA/notes LOAD \ 
"Schaechter and Benowitz We have to increase Kf for conc scaling Changed kf to 2e-9 on Sept 19, 94. This gives better match."
call /kinetics/PKC/PKC_act_by_DAG_AA/notes LOAD \ 
"Assume slowish too. Schaechter and Benowitz"
call /kinetics/PKC/PKC_basal_act/notes LOAD \ 
"Initial basal levels were set by kf = 1, kb = 20. In model, though, the basal levels of PKC activity are higher."
call /kinetics/PKC/PKC_act_by_AA/notes LOAD \ 
"Raise kf from 1.667e-10 to 2e-10 to get better match to data."
call /kinetics/PKC/PKC_n_DAG/notes LOAD \ 
"kf raised 10 X based on Shinomura et al PNAS 88 5149-5153 1991 closer analysis of Shinomura et al: kf now 1e-8 (was 1.66e-8). Further tweak. To get sufficient AA synergy, increase kf to 1.5e-8 26 June 1996: Corrected DAG levels: reduce kf by 15x from 1.5e-8 to 1e-9"
call /kinetics/PKC/PKC_n_DAG_AA/notes LOAD \ 
"Reduced kf to 0.66X to match Shinomura et al data. Initial: kf = 3.3333e-9 New: 2e-9 Newer: 2e-8 kb was 0.2 now 2."
call /kinetics/PLA2/PLA2_Ca_act/notes LOAD \ 
"Leslie and Channon BBA 1045 (1990) 261-270 fig6 pp267."
call /kinetics/PLA2/DAG_Ca_PLA2_act/notes LOAD \ 
"27 June 1996 Scaled kf down by 0.015 from 3.33e-7 to 5e-9 to fit with revised DAG estimates and use of mole-fraction to calculate eff on PLA2."
call /kinetics/PLA2/Degrade_AA/notes LOAD \ 
"I need to check if the AA degradation pathway really leads back to APC. Anyway, it is a convenient buffered pool to dump it back into. For the purposes of the full model we use a rate of degradation of 0.2/sec Raised decay to 0.4 : see PLA35.g notes for Feb17"
call /kinetics/PLA2/PLA2_p_Ca_act/notes LOAD \ 
"To start off, same kinetics as the PLA2-Ca-act direct pathway. Oops ! Missed out the Ca input to this pathway first time round. Let's raise the forward rate about 3x to 5e-6. This will let us reduce the rather high rates we have used for the kenz on PLA2*-Ca. In fact, it may be that the rates are not that different, just that this pathway for getting the PLA2 to the memb is more efficien...."
call /kinetics/PLCbeta/Act_PLC_Ca/notes LOAD \ 
"Affinity for Ca = 1uM without AlF, 0.1 with: from Smrcka et al science 251 pp 804-807 1991 so [Ca].kf = kb so kb/kf = 1 * 6e5 = 1/1.66e-6 11 June 1996: Raised affinity to 5e-6 to maintain balance. See notes."
call /kinetics/PLCbeta/Degrade_IP3/notes LOAD \ 
"The enzyme is IP3 5-phosphomonesterase. about 45K. Actual products are Ins(1,4)P2, and cIns(1:2,4,5)P3. review in Majerus et al Science 234 1519-1526, 1986. Meyer and Stryer 1988 PNAS 85:5051-5055 est decay of IP3 at 1-3/sec"
call /kinetics/PLCbeta/Degrade_DAG/notes LOAD \ 
"These rates are the same as for degrading IP3, but I am sure that they could be improved. Lets double kf to 0.2, since the amount of DAG in the cell should be <= 1uM. Need to double it again, for the same reason. kf now 0.5 27 June 1996 kf is now 0.02 to get 50 sec time course 30 Aug 1997: Raised kf to 0.11 to accomodate PLC_gamma 27 Mar 1998: kf now 0.15 for PLC_gamma"
call /kinetics/PLCbeta/Act_PLC_by_Gq/notes LOAD \ 
"Affinity for Gq is > 20 nM (Smrcka et al Science251 804-807 1991) so [Gq].kf = kb so 40nM * 6e5 = kb/kf = 24e3 so kf = 4.2e-5, kb =1"
call /kinetics/PLCbeta/Inact_PLC_Gq/notes LOAD \ 
"This process is assumed to be directly caused by the inactivation of the G*GTP to G*GDP. Hence, kf = .013 /sec = 0.8/min, same as the rate for Inact-G. kb = 0 since this is irreversible. We may be interested in studying the role of PLC as a GAP. If so, the kf would be faster here than in Inact-G"
call /kinetics/PLCbeta/PLC_bind_Gq/notes LOAD \ 
"this binding does not produce active PLC. This step was needed to implement the described (Smrcka et al) increase in affinity for Ca by PLC once Gq was bound. The kinetics are the same as the binding step for Ca-PLC to Gq. June 1996: Changed the kf to 4.2e-5 to 4.2e-6 to preserve balance around the reactions."
call /kinetics/PLCbeta/PLC_Gq_bind_Ca/notes LOAD \ 
"this step has a high affinity for Ca, from Smrcka et al. 0.1uM so kf /kb = 1/6e4 = 1.666e-5:1. See the Act-PLC-by-Gq reac. 11 Jun 1996: Raised kf to 5e-5 based on match to conc-eff curves from Smrcka et al."
call /kinetics/mGluR/RecLigandBinding/notes LOAD \ 
"kf = kf from text = 1e7 / M / sec = 10 /uM/sec = 10 / 6e5 / # / sec = 1.67e-5 kb = kr from text = 60 / sec Note that we continue to use uM here since [phenylephrine] is also in uM. From Martin et al FEBS Lett 316:2 191-196 1993 we have Kd = 600 nM Assuming kb = 10/sec, we get kf = 10/(0.6 uM * 6e5) = 2.8e-5 1/sec/#"
call /kinetics/Gprotein/Basal_Act_Gq/notes LOAD \ 
"kf = kg1 = 0.01/sec, kb = 0. This is the basal exchange of GTP for GDP."
call /kinetics/Gprotein/Trimerize_G/notes LOAD \ 
"kf == kg3 = 1e-5 /cell/sec. As usual, there is no back-reaction kb = 0"
call /kinetics/Gprotein/Inact_Gq/notes LOAD \ 
"From Berstein et al JBC 267:12 8081-8088 1992, kcat for GTPase activity of Gq is only 0.8/min"
call /kinetics/mGluR/Rec_Glu_bind_Gq/notes LOAD \ 
"This is the k1-k2 equivalent for enzyme complex formation in the binding of Rec-Glu to Gq. See Fay et al Biochem 30 5066-5075 1991. kf = 5e-5 which is nearly the same as calculated by Fay et al. (4.67e-5) kb = .04 June 1996: Closer reading of Fay et al suggests that kb <= 0.0001, so kf = 1e-8 by detailed balance. This reaction appears to be neglible."
call /kinetics/mGluR/Glu_bind_Rec_Gq/notes LOAD \ 
"From Fay et al kb3 = kb = 1.06e-3 which is rather slow. k+1 = kf = 2.8e7 /M/sec= 4.67e-5/sec use 5e-5. However, the Kd from Martin et al may be more appropriate, as this is Glu not the system from Fay. kf = 2.8e-5, kb = 10 Let us compromise. since we have the Fay model, keep kf = k+1 = 2.8e-5. But kb (k-3) is .01 * k-1 from Fay. Scaling by .01, kb = .01 * 10 = 0.1"
call /kinetics/mGluR/Activate_Gq/notes LOAD \ 
"This is the kcat==k3 stage of the Rec-Glu ezymatic activation of Gq. From Berstein et al actiation is at .35 - 0.7/min From Fay et al Biochem 30 5066-5075 1991 kf = .01/sec From Nakamura et al J physiol Lond 474:1 35-41 1994 see time courses. Also (Berstein) 15-40% of gprot is in GTP-bound form on stim."
call /kinetics/mGluR/Rec_bind_Gq/notes LOAD \ 
"Lets try out the same kinetics as the Rec-Glu-bind-Gq This is much too forward. We know that the steady-state amount of Rec-Gq should be 40% of the total amount of receptor. This is for a different receptor, still we can try to match the value. kf = 1e-6 and kb = 1 give 0.333:0.8 which is pretty close."
call /kinetics/mGluRAntag/Antag_bind_Rec_Gq/notes LOAD \ 
"The rate consts give a total binding affinity of only"
call /kinetics/Ras/Ras_act_craf/notes LOAD \ 
"Assume the binding is fast and limited only by the amount of Ras* available. So kf=kb/[craf-1] If kb is 1/sec, then kf = 1/0.2 uM = 1/(0.2 * 6e5) = 8.3e-6 Later: Raise it by 10 X to 4e-5 From Hallberg et al JBC 269:6 3913-3916 1994, 3% of cellular Raf is complexed with Ras. So we raise kb 4x to 4 This step needed to memb-anchor and activate Raf: Leevers et al Nature 369 411-414 (I don't...."
call /kinetics/Ras/bg_act_GEF/notes LOAD \ 
"SoS/GEF is present at 50 nM ie 3e4/cell. BetaGamma maxes out at 9e4. Assume we have 1/3 of the GEF active when the BetaGamma is 1.5e4. so 1e4 * kb = 2e4 * 1.5e4 * kf, so kf/kb = 3e-5. The rate of this equil should be reasonably fast, say 1/sec"
call /kinetics/Ras/Ras_intrinsic_GTPase/notes LOAD \ 
"This is extremely slow (1e-4), but it is significant as so little GAP actually gets complexed with it that the total GTP turnover rises only by 2-3 X (see Gibbs et al, JBC 265(33) 20437-20422) and Eccleston et al JBC 268(36) 27012-27019 kf = 1e-4"
call /kinetics/Ras/dephosph_GAP/notes LOAD \ 
"Assume a reasonably good rate for dephosphorylating it, 1/sec"
call /kinetics/Ras/CaM_bind_GEF/notes LOAD \ 
"We have no numbers for this. It is probably between the two extremes represented by the CaMKII phosph states, and I have used guesses based on this. kf=1e-4 kb=1 The reaction is based on Farnsworth et al Nature 376 524-527 1995"
call /kinetics/EGFR/act_EGFR/notes LOAD \ 
"Affinity of EGFR for EGF is complex: depends on [EGFR]. We'll assume fixed [EGFR] and use exptal affinity ~20 nM (see Sherrill and Kyte Biochem 1996 35 5705-5718, Berkers et al JBC 266:2 922-927 1991, Sorokin et al JBC 269:13 9752-9759 1994). Tau =~2 min (Davis et al JBC 263:11 5373-5379 1988) or Berkers Kass = 6.2e5/M/sec, Kdiss=3.5e-4/sec. Sherrill and Kyte have Hill Coeff=1.7"
call /kinetics/Sos/SHC_p_dephospho/notes LOAD \ 
"Time course of decline of phosph is 20 min. Part of this is the turnoff time of the EGFR itself. Lets assume a tau of 10 min for this dephosph. It may be wildly off."
call /kinetics/EGFR/Internalize/notes LOAD \ 
"See Helin and Beguinot JBC 266:13 1991 pg 8363-8368. In Fig 3 they have internalization tau about 10 min, equil at about 20% EGF available. So kf = 4x kb, and 1/(kf + kb) = 600 sec so kb = 1/3K = 3.3e-4, and kf = 1.33e-3. This doesn't take into account the unbound receptor, so we need to push the kf up a bit, to 0.002"
call /kinetics/Sos/SHC_bind_Sos.Grb2/notes LOAD \ 
"Sasaoka et al JBC 269:51 pp 32621 1994, table on pg 32623 indicates that this pathway accounts for about 50% of the GEF activation. (88% - 39%). Error is large, about 20%. Fig 1 is most useful in constraining rates. Chook et al JBC 271:48 pp 30472, 1996 say that the Kd is 0.2 uM for Shc binding to EGFR. The Kd for Grb direct binding is 0.7, so we'll ignore it."
call /kinetics/Sos/Grb2_bind_Sos_p/notes LOAD \ 
"Same rates as Grb2_bind_Sos: Porfiri and McCormick JBC 271:10 pp 5871 1996 show that the binding is not affected by the phosph."
call /kinetics/Sos/dephosph_Sos/notes LOAD \ 
"The only clue I have to these rates is from the time courses of the EGF activation, which is around 1 to 5 min. The dephosph would be expected to be of the same order, perhaps a bit longer. Lets use 0.002 which is about 8 min. Sep 17: The transient activation curve matches better with kf = 0.001"
call /kinetics/Sos/Grb2_bind_Sos/notes LOAD \ 
"As there are 2 SH3 domains, this reaction could be 2nd order. I have a Kd of 22 uM from peptide binding (Lemmon et al JBC 269:50 pg 31653). However, Chook et al JBC 271:48 pg30472 say it is 0.4uM with purified proteins, so we believe them. They say it is 1:1 binding."
call /kinetics/PLC_g/Ca_act_PLC_g/notes LOAD \ 
"Nice curves from Homma et al JBC 263:14 6592-6598 1988 Fig 5c. The activity falls above 10 uM, but that is too high to reach physiologically anyway, so we'll ignore the higher pts and match the lower ones only. Half-max at 1 uM. But Wahl et al JBC 267:15 10447-10456 1992 have half-max at 56 nM which is what I'll use."
call /kinetics/PLC_g/Ca_act_PLC_g_p/notes LOAD \ 
"Again, we refer to Homma et al and Wahl et al, for preference using Wahl. Half-Max of the phosph form is at 316 nM. Use kb of 10 as this is likely to be pretty fast. Did some curve comparisons, and instead of 316 nM giving a kf of 5.27e-5, we will use 8e-5 for kf. 16 Sep 97. As we are now phosphorylating the Ca-bound form, equils have shifted. kf should now be 2e-5 to match the curves."
call /kinetics/CaMKII/CaMKII_bind_CaM/notes LOAD \ 
"This is tricky. There is some cooperativity here arising from interactions between the subunits of the CAMKII holoenzyme. However, the stoichiometry is 1. Kb/Kf = 6e4 #/cell. Rate is fast (see Hanson et al Neuron 12 943-956 1994) so lets say kb = 10. This gives kf = 1.6667e-4 H&S AnnRev Biochem 92 give tau for dissoc as 0.2 sec at low Ca, 0.4 at high. Low Ca = 100 nM = physiol."
call /kinetics/CaMKII/CaMKII_thr286_bind_CaM/notes LOAD \ 
"Affinity is up 1000X. Time to release is about 20 sec, so the kb is OK at 0.1 This makes Kf around 1.6666e-3"
call /kinetics/CaMKII/basal_activity/notes LOAD \ 
"This reaction represents one of the big unknowns in CaMK-II biochemistry: what maintains the basal level of phosphorylation on thr 286 ? See Hanson and Schulman Ann Rev Biochem 1992 61:559-601, specially pg 580, for review. I have not been able to find any compelling mechanism in the literature, but fortunately the level of basal activity is well documented."
call /kinetics/CaM/CaM_TR2_bind_Ca/notes LOAD \ 
"Lets use the fast rate consts here. Since the rates are so different, I am not sure whether the order is relevant. These correspond to the TR2C fragment. We use the Martin et al rates here, plus the Drabicowski binding consts. All are scaled by 3X to cell temp. kf = 2e-10 kb = 72 Stemmer & Klee: K1=.9, K2=1.1. Assume 1.0uM for both. kb/kf=3.6e11. If kb=72, kf = 2e-10 (Exactly the same !)...."
call /kinetics/CaM/CaM_TR2_Ca2_bind_Ca/notes LOAD \ 
"K3 = 21.5, K4 = 2.8. Assuming that the K4 step happens first, we get kb/kf = 2.8 uM = 1.68e6 so kf =6e-6 assuming kb = 10"
call /kinetics/CaM/CaM_Ca3_bind_Ca/notes LOAD \ 
"Use K3 = 21.5 uM here from Stemmer and Klee table 3. kb/kf =21.5 * 6e5 so kf = 7.75e-7, kb = 10"
call /kinetics/CaM/neurogranin_bind_CaM/notes LOAD \ 
"Surprisingly, no direct info on rates from neurogranin at this time. These rates are based on GAP-43 binding studies. As GAP-43 and neurogranin share near identity in the CaM/PKC binding regions, and also similarity in phosph and dephosph rates, I am borrowing GAP-43 kinetic info. See Alexander et al JBC 262:13 6108-6113 1987"
call /kinetics/CaM/dephosph_neurogranin/notes LOAD \ 
"This is put in to keep the basal levels of neurogranin* experimentally reasonable. From various papers, specially Ramakers et al JBC 270:23 1995 13892-13898, it looks like the basal level of phosph is between 20 and 40%. I est around 25 % The kf of 0.005 gives around this level at basal PKC activity levels of 0.1 uM active PKC."
call /kinetics/PP1/Inact_PP1/notes LOAD \ 
"K inhib = 1nM from Cohen Ann Rev Bioch 1989, 4 nM from Foukes et al Assume 2 nM. kf /kb = 8.333e-4"
call /kinetics/PP1/dissoc_PP1_I1/notes LOAD \ 
"Let us assume that the equil in this case is very far over to the right. This is probably safe."
call /kinetics/PP2B/Ca_bind_CaNAB_Ca2/notes LOAD \ 
"This process is probably much more complicated and involves CaM. However, as I can't find detailed info I am bundling this into a single step. Based on Steemer and Klee pg 6863, the Kact is 0.5 uM. kf/kb = 1/(0.5 * 6e5)^2 = 1.11e-11"
call /kinetics/PP2B/Ca_bind_CaNAB/notes LOAD \ 
"going on the experience with CaM, we put the fast (high affinity) sites first. We only know (Stemmer and Klee) that the affinity is < 70 nM. Assuming 10 nM at first, we get kf = 2.78e-8, kb = 1. Try 20 nM. kf = 7e-9, kb = 1"
call /kinetics/PP2B/CaM_Ca2_bind_CaNAB/notes LOAD \ 
"Disabled. See notes for PP2B7.g"
call /kinetics/PKA/cAMP_bind_site_B1/notes LOAD \ 
"Hasler et al FASEB J 6:2734-2741 1992 say Kd =1e-7M for type II, 5.6e-8 M for type I. Take mean which comes to 2e-13 #/cell Smith et al PNAS USA 78:3 1591-1595 1981 have better data. First kf/kb=2.1e7/M = 3.5e-5 (#/cell). Ogreid and Doskeland Febs Lett 129:2 287-292 1981 have figs suggesting time course of complete assoc is < 1 min."
call /kinetics/PKA/cAMP_bind_site_B2/notes LOAD \ 
"For now let us set this to the same Km (1e-7M) as site B. This gives kf/kb = .7e-7M * 1e6 / (6e5^2) : 1/(6e5^2) = 2e-13:2.77e-12 Smith et al have better values. They say that this is cooperative, so the consts are now kf/kb =8.3e-4"
call /kinetics/PKA/Release_C1/notes LOAD \ 
"This has to be fast, as the activation of PKA by cAMP is also fast. kf was 10"
call /kinetics/PKA/inhib_PKA/notes LOAD \ 
"This has to be set to zero for matching the expts in vitro. In vivo we need to consider the inhibition though. kf = 1e-5 kb = 1"
call /kinetics/AC/CaM_bind_AC1/notes LOAD \ 
"Half-max at 20 nM CaM (Tang et al JBC 266:13 8595-8603 1991 kb/kf = 20 nM = 12000 #/cell so kf = kb/12000 = kb * 8.333e-5"
call /kinetics/AC/dephosph_AC2/notes LOAD \ 
"Random rate."
call /kinetics/AC/Gs_bind_AC2/notes LOAD \ 
"Half-max at around 3nM = kb/kf from fig 5 in Feinstein et al PNAS USA 88 10173-10177 1991 kf = kb/1800 = 5.56e-4 kb Ofer's thesis data indicates it is more like 2 nM. kf = kb/1200 = 8.33e-4"
call /kinetics/AC/Gs_bind_AC1/notes LOAD \ 
"Half-max 8nM from Tang et al JBC266:13 8595-8603 kb/kf = 8 nM = 4800#/cell so kf = kb * 2.08e-4"
call /kinetics/AC/Gs_bind_AC2_p/notes LOAD \ 
"kb/kf = 1.2 nM so kf = kb/720 = 1.3888 * kb."
call /kinetics/AC/dephosph_PDE/notes LOAD \ 
"The rates for this are poorly constrained. In adipocytes (probably a different PDE) the dephosphorylation is complete within 15 min, but there are no intermediate time points so it could be much faster. Identity of phosphatase etc is still unknown."
call /kinetics/AC/CaM_bind_PDE1/notes LOAD \ 
"For olf epi PDE1, affinity is 7 nM. Assume same for brain. Reaction should be pretty fast. Assume kb = 5/sec. Then kf = 5 / (0.007 * 6e5) = 1.2e-3"
call /kinetics/CaM/CaM_bind_Ca/notes LOAD \ 
"Lets use the fast rate consts here. Since the rates are so different, I am not sure whether the order is relevant. These correspond to the TR2C fragment. We use the Martin et al rates here, plus the Drabicowski binding consts. All are scaled by 3X to cell temp. kf = 2e-10 kb = 72 Stemmer & Klee: K1=.9, K2=1.1. Assume 1.0uM for both. kb/kf=3.6e11. If kb=72, kf = 2e-10 (Exactly the same !) 19 May 2006. Splitting the old CaM-TR2-bind-Ca reaction into two steps, each binding 1 Ca. This improves numerical stability and is conceptually better too. Overall rates are the same, so each kf and kb is the square root of the earlier ones. So kf = 1.125e-4, kb = 8.4853"
call /kinetics/CaM/CaM_Ca2_bind_Ca/notes LOAD \ 
"K3 = 21.5, K4 = 2.8. Assuming that the K4 step happens first, we get kb/kf = 2.8 uM = 1.68e6 so kf =6e-6 assuming kb = 10"
call /kinetics/CaM/CaM_Ca_bind_Ca/notes LOAD \ 
"Lets use the fast rate consts here. Since the rates are so different, I am not sure whether the order is relevant. These correspond to the TR2C fragment. We use the Martin et al rates here, plus the Drabicowski binding consts. All are scaled by 3X to cell temp. kf = 2e-10 kb = 72 Stemmer & Klee: K1=.9, K2=1.1. Assume 1.0uM for both. kb/kf=3.6e11. If kb=72, kf = 2e-10 (Exactly the same !) 19 May 2006. Splitting the old CaM-TR2-bind-Ca reaction into two steps, each binding 1 Ca. This improves numerical stability and is conceptually better too. Overall rates are the same, so each kf and kb is the square root of the earlier ones. So kf = 1.125e-4, kb = 8.4853"
call /kinetics/barr2_signaling/mGluR_barr2_assoc/notes LOAD \ 
"Heitzler,2012"
call /kinetics/barr2_signaling/mGluR_internalize/notes LOAD \ 
"Rate based on internalization time after beta-arrestin binding. According to Mundell SJ et al., 2001, t(1/2) ~ 1.9(+/-)0.4 min. Therefore, kf =0.005 to 0.0077/s"
call /kinetics/barr2_signaling/ligand_dissoc/notes LOAD \ 
"Navarro DL et al., Amino Acids (2005). Kd for glutamte-mGluR for rat fetus is 599 (+/-) 89.7 nM and for mothers is 534.3 (+/-) 89.7 nM. Therefore, assuming Kd = 595nM"
call /kinetics/PKC/PKC_active/PKC_act_raf/notes LOAD \ 
"Rate consts from Chen et al Biochem 32, 1032 (1993) k3 = k2 = 4 k1 = 9e-5 recalculated gives 1.666e-5, which is not very different. Looks like k3 is rate-limiting in this case: there is a huge amount of craf locked up in the enz complex. Let us assume a 10x higher Km, ie, lower affinity. k1 drops by 10x. Also changed k2 to 4x k3. Lowerd k1 to 1e-6 to balance 10X DAG sensitivity of PKC"
call /kinetics/PKC/PKC_active/PKC_inact_GAP/notes LOAD \ 
"Rate consts copied from PCK-act-raf This reaction inactivates GAP. The idea is from the Boguski and McCormick review."
call /kinetics/PKC/PKC_active/PKC_act_GEF/notes LOAD \ 
"Rate consts from PKC-act-raf. This reaction activates GEF. It can lead to at least 2X stim of ras, and a 2X stim of MAPK over and above that obtained via direct phosph of c-raf. Note that it is a push-pull reaction, and there is also a contribution through the phosphorylation and inactivation of GAPs. The original PKC-act-raf rate consts are too fast. We lower K1 by 10 X"
call /kinetics/PKC/PKC_active/PKC_phosph_neurogranin/notes LOAD \ 
"Rates from Huang et al ABB 305:2 570-580 1993"
call /kinetics/PKC/PKC_active/PKC_phosph_ng_CaM/notes LOAD \ 
"Rates are 60% those of PKC-phosph-neurogranin. See Huang et al ABB 305:2 570-580 1993"
call /kinetics/PKC/PKC_active/phosph_AC2/notes LOAD \ 
"Phorbol esters have little effect on AC1 or on the Gs-stimulation of AC2. So in this model we are only dealing with the increase in basal activation of AC2 induced by PKC k1 = 1.66e-6 k2 = 16 k3 =4"
call /kinetics/PLA2/PLA2_Ca_p/kenz/notes LOAD \ 
"10 x raise oct22 12 x oct 24, set k2 = 4 * k3"
call /kinetics/PLA2/PIP2_PLA2_p/kenz/notes LOAD \ 
"10 X raise oct 22 12 X further raise oct 24 to allow for correct conc of enzyme"
call /kinetics/PLA2/PIP2_Ca_PLA2_p/kenz/notes LOAD \ 
"10 x raise oct 22 12 x and rescale for k2 = 4 * k3 convention oct 24 Increase further to get the match to expt, which was spoilt due to large accumulation of PLA2 in the enzyme complexed forms. Lets raise k3, leaving the others at k1 = 1.5e-5 and k2 = 144 since they are large already."
call /kinetics/PLA2/DAG_Ca_PLA2_p/kenz/notes LOAD \ 
"10 X raise oct 22 12 X raise oct 24 + conversion to k2 =4 * k3"
call /kinetics/PLA2/PLA2_p_Ca/kenz/notes LOAD \ 
"This form should be 3 to 6 times as fast as the Ca-only form. I have scaled by 4x which seems to give a 5x rise. 10x raise Oct 22 12 x oct 24, changed k2 = 4 * k3"
call /kinetics/MAPK/MAPK_p_p/MAPK_p_p/notes LOAD \ 
"Km = 25uM @ 50 uM ATP and 1mg/ml MBP (huge XS of substrate) Vmax = 4124 pmol/min/ml at a conc of 125 pmol/ml of enz, so: k3 = .5/sec (rate limiting) k1 = (k2 + k3)/Km = (.5 + 0)/(25*6e5) = 2e-8 (#/cell)^-1 #s from Sanghera et al JBC 265 pp 52 , 1990. From Nemenoff et al JBC 268(3):1960-1964 - using Sanghera's 1e-4 ratio of MAPK to protein, we get k3 = 7/sec from 1000 pmol/min/mg fig 5"
call /kinetics/MAPK/MAPK_p_p/MAPK_p_p_feedback/notes LOAD \ 
"Ueki et al JBC 269(22):15756-15761 show the presence of this step, but not the rate consts, which are derived from Sanghera et al JBC 265(1):52-57, 1990, see the deriv in the MAPK* notes."
call /kinetics/MAPK/MAPK_p_p/phosph_Sos/notes LOAD \ 
"See Porfiri and McCormick JBC 271:10 pp5871 1996 for the existence of this step. We'll take the rates from the ones used for the phosph of Raf by MAPK. Sep 17 1997: The transient activation curve matches better with k1 up by 10 x."
call /kinetics/PLCbeta/PLC_Ca/PLC_Ca/notes LOAD \ 
"From Sternweis et al Phil Trans R Soc Lond 1992, also matched by Homma et al. k1 = 1.5e-5, now 4.2e-6 k2 = 70/sec; now 40/sec k3 = 17.5/sec; now 10/sec Note that the wording in Sternweis et al is ambiguous re the Km."
call /kinetics/PLCbeta/PLC_Ca_Gq/PLCb_Ca_Gq/notes LOAD \ 
"From Sternweis et al, Phil Trans R Soc Lond 1992, and the values from other refs eg Homma et al JBC 263(14) pp6592 1988 match. k1 = 5e-5/sec k2 = 240/sec; now 120/sec k3 = 60/sec; now 30/sec Note that the wording in Sternweis et al is ambiguous wr. to the Km for Gq vs non-Gq states of PLC. K1 is still a bit too low. Raise to 7e-5 9 Jun 1996: k1 was 0.0002, changed to 5e-5"
call /kinetics/MAPK/MAPKK_p_p/MAPKKtyr/notes LOAD \ 
"The actual MAPKK is 2 forms from Seger et al JBC 267:20 14373(1992) Vmax = 150nmol/min/mg From Haystead et al FEBS 306(1):17-22 we get Km=46.6nM for at least one of the phosphs. Putting these together: k3=0.15/sec, scale to get k2=0.6. k1=0.75/46.6nM=2.7e-5"
call /kinetics/MAPK/MAPKK_p_p/MAPKKthr/notes LOAD \ 
"Rate consts same as for MAPKKtyr."
call /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.1/notes LOAD \ 
"Kinetics are the same as for the craf-1* activity, ie., k1=1.1e-6, k2=.42, k3 =0.105 These are based on Force et al PNAS USA 91 1270-1274 1994. These parms cannot reach the observed 4X stim of MAPK. So lets increase the affinity, ie, raise k1 10X to 1.1e-5 Lets take it back down to where it was. Back up to 5X: 5.5e-6"
call /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.2/notes LOAD \ 
"Same kinetics as other c-raf activated forms. See Force et al PNAS 91 1270-1274 1994. k1 = 1.1e-6, k2 = .42, k3 = 1.05 raise k1 to 5.5e-6"
call /kinetics/Phosphatase/MKP_1/MKP1_tyr_deph/notes LOAD \ 
"The original kinetics have been modified to obey the k2 = 4 * k3 rule, while keeping kcat and Km fixed. As noted in the NOTES, the only constraining data point is the time course of MAPK dephosphorylation, which this model satisfies. It would be nice to have more accurate estimates of rate consts and MKP-1 levels from the literature. Effective Km : 67 nM kcat = 1.43 umol/min/mg"
call /kinetics/Phosphatase/MKP_1/MKP1_thr_deph/notes LOAD \ 
"See MKP1-tyr-deph"
call /kinetics/Phosphatase/PPhosphatase2A/craf_dephospho/notes LOAD \ 
"See parent PPhosphatase2A for parms"
call /kinetics/Phosphatase/PPhosphatase2A/MAPKK_dephospho/notes LOAD \ 
"See: Kyriakis et al Nature 358 pp 417-421 1992 Ahn et al Curr Op Cell Biol 4:992-999 1992 for this pathway. See parent PPhosphatase2A for parms."
call /kinetics/Phosphatase/PPhosphatase2A/craf_p_p_dephospho/notes LOAD \ 
"Ueki et al JBC 269(22) pp 15756-15761 1994 show hyperphosphorylation of craf, so this is there to dephosphorylate it. Identity of phosphatase is not known to me, but it may be PP2A like the rest, so I have made it so."
call /kinetics/Ras/GEF_Gprot_bg/GEF_bg_act_Ras/notes LOAD \ 
"Kinetics based on the activation of Gq by the receptor complex in the Gq model (in turn based on the Mahama and Linderman model) k1 = 2e-5, k2 = 1e-10, k3 = 10 (I do not know why they even bother with k2). Lets put k1 at 2e-6 to get a reasonable equilibrium More specific values from, eg.g: Orita et al JBC 268(34) 25542-25546 from rasGRF and smgGDS: k1=3.3e-7; k2 = 0.08, k3 = 0.02"
call /kinetics/Ras/GEF_p/GEF_p_act_Ras/notes LOAD \ 
"Kinetics same as GEF-bg-act-ras"
call /kinetics/Ras/GAP/GAP_inact_Ras/notes LOAD \ 
"From Eccleston et al JBC 268(36)pp27012-19 get Kd < 2uM, kcat - 10/sec From Martin et al Cell 63 843-849 1990 get Kd ~ 250 nM, kcat = 20/min I will go with the Eccleston figures as there are good error bars (10%). In general the values are reasonably close. k1 = 1.666e-3/sec, k2 = 1000/sec, k3 = 10/sec (note k3 is rate-limiting) 5 Nov 2002: Changed ratio term to 4 from 100. Now we have k1=8.25e-5; k2=40, k3=10. k3 is still rate-limiting."
call /kinetics/Ras/CaM_GEF/CaM_GEF_act_Ras/notes LOAD \ 
"Kinetics same as GEF-bg_act-ras"
call /kinetics/PKA/PKA_active/PKA_phosph_GEF/notes LOAD \ 
"This pathway inhibits Ras when cAMP is elevated. See: Hordijk et al JBC 269:5 3534-3538 1994 Burgering et al EMBO J 12:11 4211-4220 1993 The rates are the same as used in PKA-phosph-I1"
call /kinetics/PKA/PKA_active/PKA_phosph_I1/notes LOAD \ 
"#s from Bramson et al CRC crit rev Biochem 15:2 93-124. They have a huge list of peptide substrates and I have chosen high-ish rates. These consts give too much PKA activity, so lower Vmax 1/3. Now, k1 = 3e-5, k2 = 36, k3 = 9 (still pretty fast). Also lower Km 1/3 so k1 = 1e-5 Cohen et al FEBS Lett 76:182-86 1977 say rate =30% PKA act on phosphokinase beta."
call /kinetics/PKA/PKA_active/phosph_PDE/notes LOAD \ 
"Same rates as PKA-phosph-I1"
call /kinetics/EGFR/L.EGFR/Ca.PLC_g_phospho/notes LOAD \ 
"Hsu et al JBC 266:1 603-608 1991 Km = 385 +- 100 uM, Vm = 5.1 +-1 pmol/min/ug for PLC-771. Other sites have similar range, but are not stim as much by EGF. k1 = 2.8e-2/385/6e5 = 1.2e-10. Phenomenally slow. But Sherrill and Kyte say turnover # for angiotensin II is 5/min for cell extt, and 2/min for placental. Also see Okada et al for Shc rates which are much faster."
call /kinetics/EGFR/L.EGFR/SHC_phospho/notes LOAD \ 
"Rates from Okada et al JBC 270:35 pp 20737 1995 Km = 0.70 to 0.85 uM, Vmax = 4.4 to 5.0 pmol/min. Unfortunately the amount of enzyme is not known, the prep is only partially purified. Time course of phosph is max within 30 sec, falls back within 20 min. Ref: Sasaoka et al JBC 269:51 32621 1994. Use k3 = 0.1 based on this tau."
call /kinetics/PLC_g/Ca.PLC_g/PIP2_hydrolysis/notes LOAD \ 
"Mainly Homma et al JBC 263:14 1988 pp 6592, but these parms are the Ca-stimulated form. It is not clear whether the enzyme is activated by tyrosine phosphorylation at this point or not. Wahl et al JBC 267:15 10447-10456 1992 say that the Ca_stim and phosph form has 7X higher affinity for substrate than control. This is close to Wahl's figure 7, which I am using as reference."
call /kinetics/PLC_g/Ca.PLC_g_p/PIP2_hydrolysis/notes LOAD \ 
"Mainly Homma et al JBC 263:14 1988 pp 6592, but these parms are the Ca-stimulated form. It is not clear whether the enzyme is activated by tyrosine phosphorylation at this point or not. Wahl et al JBC 267:15 10447-10456 1992 say that this has 7X higher affinity for substrate than control."
call /kinetics/CaMKII/tot_CaM_CaMKII/CaM_act_305/notes LOAD \ 
"Rates from autocamtide phosphorylation, from Hanson and Schulman JBC 267:24 17216-17224 1992. Jan 1 1998: Speed up 12x to match fig 5."
call /kinetics/CaMKII/tot_autonomous_CaMKII/auton_305/notes LOAD \ 
"See Hanson and Schulman again, for afterburst rates of phosph."
call /kinetics/PP1/PP1_active/Deph_thr286/notes LOAD \ 
"The rates are from Stralfors et al Eur J Biochem 149 295-303 giving Vmax = 5.7 umol/min giving k3 = 3.5/sec and k2 = 14. Foulkes et al Eur J Biochem 132 309-313 1983 give Km = 5.1 uM so k1 becomes 5.72e-6 Simonelli 1984 (Grad Thesis, CUNY) showed that other substrates are about 1/10 rate of phosphorylase a, so we reduce k1,k2,k3 by 10 to 5.72e-7, 1.4, 0.35"
call /kinetics/PP1/PP1_active/Deph_thr306/notes LOAD \ 
"See Cohen et al"
call /kinetics/CaM/CaM(Ca)n_CaNAB/dephosph_neurogranin/notes LOAD \ 
"From Seki et al ABB 316(2):673-679"
call /kinetics/Phosphatase/PP2A/PP2A_dephospho_I1/notes LOAD \ 
"PP2A does most of the dephosph of I1 at basal Ca levels. See the review by Cohen in Ann Rev Biochem 1989. For now, lets halve Km. k1 was 3.3e-6, now 6.6e-6"
call /kinetics/Phosphatase/PP2A/PP2A_dephospho_PP1_I_p/notes LOAD \ 
"k1 changed from 3.3e-6 to 6.6e-6"
call /kinetics/CaM/CaNAB_Ca4/dephosph_inhib1_noCaM/notes LOAD \ 
"The rates here are so slow I do not know if we should even bother with this enz reacn. These numbers are from Liu and Storm. Other refs suggest that the Km stays the same but the Vmax goes to 10% of the CaM stim levels. Prev: k1=2.2e-9, k2 = 0.0052, k3 = 0.0013 New : k1=5.7e-8, k2=.136, k3=.034"
call /kinetics/AC/AC2_p/kenz/notes LOAD \ 
"Reduced Km to match expt data for basal activation of AC2 by PKC. Now k1 = 2.9e-6, k2 = 72, k3 = 18"
call /kinetics/AC/cAMP_PDE/PDE/notes LOAD \ 
"Best rates are from Conti et al Biochem 34 7979-7987 1995. Though these are for the Sertoli cell form, it looks like they carry nicely into alternatively spliced brain form. See Sette et al JBC 269:28 18271-18274 Km ~2 uM, Vmax est ~ 10 umol/min/mg for pure form. Brain protein is 93 kD but this was 67. So k3 ~10, k2 ~40, k1 ~4.2e-6"
call /kinetics/AC/cAMP_PDE_p/PDE_p/notes LOAD \ 
"This form has about twice the activity of the unphosphorylated form. See Sette et al JBC 269:28 18271-18274 1994. We'll ignore cGMP effects for now."
call /kinetics/AC/PDE1/PDE1/notes LOAD \ 
"Rate is 1/6 of the CaM stim form. We'll just reduce all lf k1, k2, k3 so that the Vmax goes down 1/6."
call /kinetics/AC/CaM.PDE1/CaM.PDE1/notes LOAD \ 
"Max activity ~10umol/min/mg in presence of lots of CaM. Affinity is low, 40 uM. k3 = 10, k2 = 40, k1 = (50/40) / 6e5."
complete_loading
