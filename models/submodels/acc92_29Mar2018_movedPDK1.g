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
DEFAULT_VOL = 1.02231269881e-15
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
simundump geometry /kinetics/geometry 0 1.02231269881e-15 3 sphere  "" white black -12 34 0
simundump group /kinetics/AKT_activation 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/TrKB 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/PI3K_activation 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/mTORC1 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/S6Kinase 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/4E_BP 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/43S_complex 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/CaM 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/MAPK 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/Ras 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/Sos 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/PKC 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/protein 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/PLC_g 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/BDNF 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/Phosphatase 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/Ca 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/CaMKIII 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/Translation_initiation 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/Translation_elongation 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/40S 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump group /kinetics/TSC1_TSC2 0 blue green x 0 0 "" defaultfile \
  defaultfile.g 0 0 0 -15 34 0
simundump kpool /kinetics/BDNF/BDNF 0 0.0 0 0 0 30.7825586473 0 0 615651.172948 4 /kinetics/geometry 44 black -14 16 0
simundump kpool /kinetics/PLC_g/PLC_g 0 0.0 0 0 0 61567.1695337 0 0 615651.172948 0 /kinetics/geometry cyan black -3 7 0
simundump kpool /kinetics/PLC_g/PLC_g_p 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry hot pink 0 -1 0
simundump kpool /kinetics/PI3K_activation/PIP3 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 43 black -3 -11 0
simundump kpool /kinetics/PI3K_activation/PDK1 0 0.0 0 0 0 615671.695337 0 0 615651.172948 0 /kinetics/geometry 37 black 3 6 0
simundump kpool /kinetics/Phosphatase/PP2A 0 0.0 0 0 0 92350.7543005 0 0 615651.172948 0 /kinetics/geometry 4 black 11 1 0
simundump kpool /kinetics/AKT_activation/PIP3_AKT 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 53 yellow -8 4 0
simundump kpool /kinetics/AKT_activation/PIP3_PDK1 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 9 yellow -4 10 0
simundump kpool /kinetics/AKT_activation/PIP3_PDK2 0 0.0 0 0 0 1847.01508602 0 0 615651.172948 0 /kinetics/geometry 39 yellow 2 10 0
simundump kpool /kinetics/AKT_activation/PIP3_AKT_thr308 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 60 yellow -4 4 0
simundump kpool /kinetics/AKT_activation/PIP3_AKT_t308_s473 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 25 yellow 4 11 0
simundump kpool /kinetics/AKT_activation/AKT 0 0.0 0 0 0 123134.339066 0 0 615651.172948 0 /kinetics/geometry 4 yellow -11 1 0
simundump kpool /kinetics/TSC1_TSC2/TSC1_TSC2_p 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 40 yellow 5 2 0
simundump kpool /kinetics/TrKB/Int_BDNF_TrKB2_p_clx 0 0.0 0 0 0 153917.923835 0 0 615651.172948 4 /kinetics/geometry yellow white -9 12 0
simundump kpool /kinetics/TrKB/TrKB 0 0.0 0 0 0 153907.662639 0 0 615651.172948 0 /kinetics/geometry 3 white -7 3 0
simundump kpool /kinetics/TrKB/BDNF_TrKB2_clx 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 38 white -5 3 0
simundump kpool /kinetics/TrKB/BDNF_TrKB_clx 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 45 white -6 -3 0
simundump kpool /kinetics/TrKB/BDNF_TrKB2_p_clx 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry red white -3 3 0
simundump kpool /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_PI3K_clx 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry brown white 2 -3 0
simundump kpool /kinetics/PI3K_activation/PI3K 0 0.0 0 0 0 61565.1172948 0 0 615651.172948 0 /kinetics/geometry cyan brown 4 -18 0
simundump kpool /kinetics/PI3K_activation/PI3K_basal 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 10 brown -3 -17 0
simundump kpool /kinetics/PI3K_activation/PIP2 0 0.0 0 0 0 4309701.86735 0 0 615651.172948 4 /kinetics/geometry orange brown 1 -11 0
simundump kpool /kinetics/Sos/SHC 0 0.0 0 0 0 307835.847668 0 0 615651.172948 0 /kinetics/geometry 5 brown -3 -6 0
simundump kpool /kinetics/Sos/SHC_p_Grb2_clx 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 42 brown 2 -7 0
simundump kpool /kinetics/PI3K_activation/Gab1 0 0.0 0 0 0 430970.186735 0 0 615651.172948 0 /kinetics/geometry 44 brown 2 -5 0
simundump kpool /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_clx 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 50 brown 6 -9 0
simundump kpool /kinetics/PLC_g/PLCg_basal 0 0.0 0 0 0 430.970186735 0 0 615651.172948 0 /kinetics/geometry 33 black -3 11 0
simundump kpool /kinetics/TSC1_TSC2/TSC1_TSC2 0 0.0 0 0 0 615671.695337 0 0 615651.172948 0 /kinetics/geometry 51 black 12 9 0
simundump kpool /kinetics/Translation_initiation/eIF4E 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 42 black -15 1 0
simundump kpool /kinetics/mTORC1/Rheb_GTP 0 0.0 0 0 0 615671.695337 0 0 615651.172948 0 /kinetics/geometry 28 black 20 10 0
simundump kpool /kinetics/mTORC1/Rheb_GDP 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 39 black 15 4 0
simundump kpool /kinetics/mTORC1/TOR_clx 0 0.0 0 0 0 369403.017202 0 0 615651.172948 0 /kinetics/geometry 25 8 10 -13 0
simundump kpool /kinetics/mTORC1/TOR_Rheb_GTP_clx 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 44 black 12 -19 0
simundump kpool /kinetics/S6Kinase/S6K_p 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 46 6 3 4 0
simundump kpool /kinetics/S6Kinase/S6K 0 0.0 0 0 0 769589.619171 0 0 615651.172948 0 /kinetics/geometry Pink 6 0 3 0
simundump kpool /kinetics/S6Kinase/S6K_thr_412 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 48 6 7 -16 0
simundump kpool /kinetics/40S/40S_inact 0 0.0 0 0 0 12313.4339066 0 0 615651.172948 4 /kinetics/geometry 3 6 16 12 0
simundump kpool /kinetics/4E_BP/4E_BP 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 47 white -11 -18 0
simundump kpool /kinetics/4E_BP/4E_BP_t37_46_s65 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 59 white -11 -13 0
simundump kpool /kinetics/4E_BP/eIF4E_BP 0 0.0 0 0 0 123134.339066 0 0 615651.172948 0 /kinetics/geometry 52 white -13 -11 0
simundump kpool /kinetics/4E_BP/eIF4E_BP_thr37_46 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 56 white -11 -5 0
simundump kpool /kinetics/4E_BP/eIF4E_BP_t37_46_s65 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 39 white -11 -1 0
simundump kpool /kinetics/40S/40S 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 7 black -11 15 0
simundump kpool /kinetics/Translation_initiation/eIF4G_A_clx 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry cyan black -6 4 0
simundump kpool /kinetics/Translation_initiation/eIF4A 0 0.0 0 0 0 123134.339066 0 0 615651.172948 0 /kinetics/geometry pink black -1 15 0
simundump kpool /kinetics/Translation_initiation/eIF4G 0 0.0 0 0 0 24626.8678136 0 0 615651.172948 0 /kinetics/geometry 21 black 0 14 0
simundump kpool /kinetics/Translation_initiation/eIF4F 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 6 black 2 -2 0
simundump kpool /kinetics/Translation_initiation/mRNA 0 0.0 0 0 0 49252.7095075 0 0 615651.172948 0 /kinetics/geometry 60 black 7 3 0
simundump kpool /kinetics/Translation_initiation/eIF4F_mRNA_clx 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 59 black 13 -5 0
simundump kpool /kinetics/43S_complex/Q.R 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry blue yellow 5 14 0
simundump kpool /kinetics/43S_complex/RM 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry pink yellow -7 3 0
simundump kpool /kinetics/43S_complex/Quaternary_clx 0 0.0 0 0 0 28936.569681 0 0 615651.172948 0 /kinetics/geometry 28 yellow -5 11 0
simundump kpool /kinetics/S6Kinase/S6K_thr_252 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 6 black -6 17 0
simundump kpool /kinetics/CaM/CaM_Ca4 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry blue yellow 4 27 0
simundump kpool /kinetics/CaMKIII/CaMKIII 0 0.0 0 0 0 36940.3017202 0 0 615651.172948 0 /kinetics/geometry 32 black -2 18 0
simundump kpool /kinetics/CaMKIII/CaMKIII_CaM_Ca4 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 58 black 18 22 0
simundump kpool /kinetics/Translation_elongation/eEF2 0 0.0 0 0 0 307835.847668 0 0 615651.172948 0 /kinetics/geometry 27 black 26 18 0
simundump kpool /kinetics/Translation_elongation/eEFthr_56 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry white black 15 15 0
simundump kpool /kinetics/CaM/CaM 0 0.0 0 0 0 12313433.9066 0 0 615651.172948 0 /kinetics/geometry pink blue 7 29 0
simundump kpool /kinetics/CaM/CaM_Ca3 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry hotpink blue 21 17 0
simundump kpool /kinetics/CaM/CaM_Ca2 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry pink blue 16 30 0
simundump kpool /kinetics/CaM/CaM_Ca 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry pink blue 11 29 0
simundump kpool /kinetics/Ca/Ca 0 0.0 0 0 0 49253.7356269 0 0 615651.172948 0 /kinetics/geometry red black -7 30 0
simundump kpool /kinetics/CaMKIII/CaMKIII_basal 0 0.0 0 0 0 6.15671695337 0 0 615651.172948 0 /kinetics/geometry 45 black 10 11 0
simundump kpool /kinetics/CaMKIII/CaMKIII_p 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 57 black 2 11 0
simundump kpool /kinetics/S6Kinase/S6K_basal 0 0.0 0 0 0 615.671695337 0 0 615651.172948 0 /kinetics/geometry 45 black 24 21 0
simundump kpool /kinetics/Translation_elongation/60S_R 0 0.0 0 0 0 41865.675283 0 0 615651.172948 4 /kinetics/geometry 46 black 22 15 0
simundump kpool /kinetics/Translation_elongation/Translation_clx 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 52 black 17 0 0
simundump kpool /kinetics/protein/AA 0 0.0 0 0 0 61567.1695337 0 0 615651.172948 4 /kinetics/geometry cyan black 22 -1 0
simundump kpool /kinetics/protein/peptide 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry brown black 16 -6 0
simundump kpool /kinetics/protein/degraded_protein 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry white black 25 -18 0
simundump kpool /kinetics/protein/protein 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry red black 16 -18 0
simundump kpool /kinetics/Translation_elongation/80S_ribos_clx 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry blue black 19 7 0
simundump kpool /kinetics/Sos/Grb2 0 0.0 0 0 0 615671.695337 0 0 615651.172948 0 /kinetics/geometry orange yellow 15 33 0
simundump kpool /kinetics/Sos/SHC_p 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry orange yellow 9 29 0
simundump kpool /kinetics/MAPK/MAPK_p_p 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry orange yellow 13 1 0
simundump kpool /kinetics/PKC/PKC_active 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry yellow black 2 8 0
simundump kpool /kinetics/MAPK/craf_1 0 0.0 0 0 0 307835.847668 0 0 615651.172948 0 /kinetics/geometry pink brown 6 9 0
simundump kpool /kinetics/MAPK/craf_1_p 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry pink brown 9 8 0
simundump kpool /kinetics/MAPK/MAPKK 0 0.0 0 0 0 307835.847668 0 0 615651.172948 0 /kinetics/geometry pink brown 6 4 0
simundump kpool /kinetics/MAPK/MAPK 0 0.0 0 0 0 2216418.10322 0 0 615651.172948 0 /kinetics/geometry pink brown 6 1 0
simundump kpool /kinetics/MAPK/craf_1_p_p 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry hotpink brown 14 8 0
simundump kpool /kinetics/MAPK/MAPK_p 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry orange brown 9 1 0
simundump kpool /kinetics/MAPK/MAPKK_p_p 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry pink brown 13 4 0
simundump kpool /kinetics/MAPK/MAPKK_p 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry pink brown 9 4 0
simundump kpool /kinetics/MAPK/Raf_p_GTP_Ras 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry red brown 5 5 0
simundump kpool /kinetics/Phosphatase/MKP_1 0 0.0 0 0 0 12313.4339066 0 0 615651.172948 0 /kinetics/geometry hotpink black 4 2 0
simundump kpool /kinetics/Phosphatase/PPhosphatase2A 0 0.0 0 0 0 615671.695337 0 0 615651.172948 0 /kinetics/geometry hotpink yellow 9 9 0
simundump kpool /kinetics/Ras/inact_GEF 0 0.0 0 0 0 61567.1695337 0 0 615651.172948 0 /kinetics/geometry hotpink blue 12 21 0
simundump kpool /kinetics/Ras/GEF_p 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry hotpink blue 6 17 0
simundump kpool /kinetics/Ras/GTP_Ras 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry orange blue 14 14 0
simundump kpool /kinetics/Ras/GDP_Ras 0 0.0 0 0 0 307835.847668 0 0 615651.172948 0 /kinetics/geometry pink blue 6 14 0
simundump kpool /kinetics/Ras/GAP_p 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry red blue 3 13 0
simundump kpool /kinetics/Ras/GAP 0 0.0 0 0 0 6156.71695337 0 0 615651.172948 0 /kinetics/geometry red blue 6 12 0
simundump kpool /kinetics/Ras/CaM_GEF 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry pink blue 5 19 0
simundump kpool /kinetics/Sos/SHC_p.Sos.Grb2 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry brown yellow 11 27 0
simundump kpool /kinetics/Sos/Sos_p.Grb2 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry orange blue 13 30 0
simundump kpool /kinetics/Sos/Sos.Grb2 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry orange blue 15 19 0
simundump kpool /kinetics/Sos/Sos_p 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry red blue 16 29 0
simundump kpool /kinetics/Sos/Sos 0 0.0 0 0 0 61567.1695337 0 0 615651.172948 0 /kinetics/geometry red blue 18 25 0
simundump kpool /kinetics/43S_complex/43Scomplex 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry hotpink black 18 13 0
simundump kpool /kinetics/PKC/PKC_Ca 0 0.0 0 0 0 2.29081176641e-11 0 0 615651.172948 0 /kinetics/geometry red black -4 1 0
simundump kpool /kinetics/PKC/PKC_DAG_AA_p 0 0.0 0 0 0 3.02520548699e-12 0 0 615651.172948 0 /kinetics/geometry cyan blue 0 5 0
simundump kpool /kinetics/PKC/PKC_Ca_AA_p 0 0.0 0 0 0 1.07742546684e-10 0 0 615651.172948 0 /kinetics/geometry orange blue 0 6 0
simundump kpool /kinetics/PKC/PKC_Ca_memb_p 0 0.0 0 0 0 8.5553738784e-12 0 0 615651.172948 0 /kinetics/geometry pink blue -2 6 0
simundump kpool /kinetics/PKC/PKC_DAG_memb_p 0 0.0 0 0 0 5.80896505743e-15 0 0 615651.172948 0 /kinetics/geometry yellow blue -1 5 0
simundump kpool /kinetics/PKC/PKC_basal_p 0 0.0 0 0 0 12313.4339066 0 0 615651.172948 0 /kinetics/geometry pink blue -4 5 0
simundump kpool /kinetics/PKC/PKC_AA_p 0 0.0 0 0 0 1.11641800753e-11 0 0 615651.172948 0 /kinetics/geometry cyan blue 1 6 0
simundump kpool /kinetics/PKC/PKC_Ca_DAG 0 0.0 0 0 0 5.21053216957e-17 0 0 615651.172948 0 /kinetics/geometry white blue 0 1 0
simundump kpool /kinetics/PKC/PKC_DAG 0 0.0 0 0 0 7.14805099481e-11 0 0 615651.172948 0 /kinetics/geometry white blue 0 -1 0
simundump kpool /kinetics/PKC/PKC_DAG_AA 0 0.0 0 0 0 1.55077438861e-13 0 0 615651.172948 0 /kinetics/geometry white blue 0 0 0
simundump kpool /kinetics/PKC/PKC_cytosolic 0 0.0 0 0 0 615671.695337 0 0 615651.172948 0 /kinetics/geometry white blue -6 0 0
simundump kpool /kinetics/PKC/DAG 0 0.0 0 0 0 6772388.64871 0 0 615651.172948 4 /kinetics/geometry green black -3 -4 0
simundump kpool /kinetics/PKC/Arachidonic_Acid 0 0.0 0 0 0 3078358.47668 0 0 615651.172948 4 /kinetics/geometry darkgreen black -3 -9 0
simundump kpool /kinetics/Translation_elongation/Basal_Translation 0 0.0 0 0 0 123.134339066 0 0 615651.172948 0 /kinetics/geometry 53 black 22 -7 0
simundump kpool /kinetics/protein/rad_AA 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 45 black 27 -4 0
simundump kpool /kinetics/protein/rad_peptide 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 1 black 18 -8 0
simundump kpool /kinetics/protein/rad_protein 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 47 black 19 -14 0
simundump kpool /kinetics/protein/rad_deg_pro 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 2 black 27 -14 0
simundump kpool /kinetics/40S/40S_basal 0 0.0 0 0 0 61.5671695337 0 0 615651.172948 0 /kinetics/geometry 44 black 20 3 0
simundump kpool /kinetics/4E_BP/4E_BP_t37_46 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 60 black -7 -14 0
simundump kpool /kinetics/PI3K_activation/PTEN 0 0.0 0 0 0 166231.35774 0 0 615651.172948 0 /kinetics/geometry 37 black 1 -16 0
simundump kpool /kinetics/Ras/Ras_GTP_PI3K 0 0.0 0 0 0 0.0 0 0 615651.172948 0 /kinetics/geometry 31 black 5 -24 0
simundump kreac /kinetics/AKT_activation/PIP3_bind_AKT 0 7.30938263702e-05 0.089 "" white yellow -11 4 0
simundump kreac /kinetics/AKT_activation/PIP3_bind_PDK1 0 1.13700208293e-06 0.98 "" white yellow -8 6 0
simundump kreac /kinetics/TSC1_TSC2/TSC1_TSC2_dephospho 0 0.01 0.0 "" white yellow 10 7 0
simundump kreac /kinetics/TrKB/Autophos_TrKB 0 0.02 0.0 "" white white -4 -2 0
simundump kreac /kinetics/TrKB/Dimeriz_TrKB 0 1.62427476782e-06 0.02 "" white white -7 0 0
simundump kreac /kinetics/TrKB/Ligand_binding 0 1.62437222236e-06 0.05 "" white white -9 0 0
simundump kreac /kinetics/PLC_g/PLC_g_p_dephospho 0 0.07 0.0 "" white white -1 12 0
simundump kreac /kinetics/TrKB/LR_Internalize 0 0.01 0.0 "" white white -5 9 0
simundump kreac /kinetics/TrKB/LR_cycling 0 0.001 0.001 "" white white -9 9 0
simundump kreac /kinetics/Sos/SHC_p_dephospho 0 0.2 0.0 "" white brown -2 -9 0
simundump kreac /kinetics/Sos/Grb2_bind_SHC 0 1.62427476782e-06 1.0 "" white brown 0 -4 0
simundump kreac /kinetics/PI3K_activation/bind_Gab1 0 4.87272684895e-07 1.0 "" white brown 5 -5 0
simundump kreac /kinetics/PI3K_activation/PI3K_act 0 8.12147129367e-06 0.08 "" white brown 4 -13 0
simundump kreac /kinetics/PI3K_activation/basal_PI3K_act 0 0.00068 0.45 "" white brown 1 -19 0
simundump kreac /kinetics/mTORC1/Rheb_GTP_bind_TORclx 0 9.74545369788e-06 3.0 "" white 8 13 -7 0
simundump kreac /kinetics/S6Kinase/S6_dephosph 0 0.01 0.0 "" white 6 14 5 0
simundump kreac /kinetics/4E_BP/eIF4E_bind_BP2 0 8.12117893006e-05 0.15 "" white white -14 -18 0
simundump kreac /kinetics/4E_BP/eIF4E_BP2_disso 0 4.0 1.62427476782e-06 "" white white -16 -17 0
simundump kreac /kinetics/Translation_initiation/eIF4F_clx 0 4.87282430347e-05 0.1 "" white black -15 10 0
simundump kreac /kinetics/Translation_initiation/eIF4G_A_clx_formation 0 4.87282430347e-07 1.0 "" white black -7 9 0
simundump kreac /kinetics/Translation_initiation/eIF4F_mRNA_clx_formation 0 3.24854953566e-07 0.077 "" white black 9 -4 0
simundump kreac /kinetics/43S_complex/Q_binds_R 0 7.79636295829e-07 0.5 "" white yellow -4 13 0
simundump kreac /kinetics/43S_complex/QR_binds_M 0 7.95881967145e-07 0.0045 "" white yellow 6 11 0
simundump kreac /kinetics/43S_complex/R_binds_M 0 2.07899763737e-06 0.719 "" white yellow -3 4 0
simundump kreac /kinetics/43S_complex/RM_binds_Q 0 1.59172495247e-07 0.00169 "" white yellow -6 7 0
simundump kreac /kinetics/CaM/CaM_Ca3_bind_Ca 0 7.55282407038e-07 10.0 "" white blue 10 17 0
simundump kreac /kinetics/CaM/CaM_bind_Ca 0 1.37810460741e-05 8.4853 "" white blue 7 26 0
simundump kreac /kinetics/CaM/CaM_Ca2_bind_Ca 0 5.84736967326e-06 10.0 "" white blue 13 26 0
simundump kreac /kinetics/CaM/CaM_Ca_bind_Ca 0 1.37810460741e-05 8.4853 "" white blue 19 26 0
simundump kreac /kinetics/CaMKIII/CaMKIII_dephospho 0 0.07 0.0 "" white black 1 20 0
simundump kreac /kinetics/Translation_elongation/elongation 0 6.49700161676e-05 10.0 "" white black 25 2 0
simundump kreac /kinetics/Translation_elongation/activation 0 1.62427476782e-06 0.9 "" white black 23 10 0
simundump kreac /kinetics/Ras/Ras_act_craf 0 1.62417731328e-05 0.5 "" white black 5 11 0
simundump kreac /kinetics/Ras/dephosph_GEF 0 1.0 0.0 "" white blue 9 17 0
simundump kreac /kinetics/Ras/Ras_intrinsic_GTPase 0 0.0001 0.0 "" white blue 9 13 0
simundump kreac /kinetics/Ras/dephosph_GAP 0 0.1 0.0 "" white blue 4 15 0
simundump kreac /kinetics/Ras/CaM_bind_GEF 0 0.000324845208113 1.0 "" white blue 2 21 0
simundump kreac /kinetics/Sos/SHC_bind_Sos.Grb2 0 8.12078911191e-07 0.1 "" white blue 11 19 0
simundump kreac /kinetics/Sos/Grb2_bind_Sos_p 0 4.06063819228e-08 0.0168 "" white blue 11 27 0
simundump kreac /kinetics/Sos/dephosph_Sos 0 0.001 0.0 "" white blue 14 26 0
simundump kreac /kinetics/Sos/Grb2_bind_Sos 0 4.06063819228e-08 0.0168 "" white blue 17 24 0
simundump kreac /kinetics/CaM/CaMKIII_bind_CaM_Ca4 0 0.000160799986015 0.09 "" white black -8 20 0
simundump kreac /kinetics/protein/pep_elongation 0 0.1 0.001 "" white black 16 -11 0
simundump kreac /kinetics/protein/protein_deg 0 1.0 0.0 "" white black 20 -17 0
simundump kreac /kinetics/mTORC1/GDP_to_GTP 0 0.2 0.0 "" white black 15 1 0
simundump kreac /kinetics/PKC/PKC_act_by_Ca 0 9.74545369788e-07 0.5 "" white blue -4 0 0
simundump kreac /kinetics/PKC/PKC_act_by_DAG 0 1.29936134153e-08 8.6348 "" white blue -2 0 0
simundump kreac /kinetics/PKC/PKC_Ca_to_memb 0 1.2705 3.5026 "" white blue -3 4 0
simundump kreac /kinetics/PKC/PKC_DAG_to_memb 0 1.0 0.1 "" white blue -2 2 0
simundump kreac /kinetics/PKC/PKC_act_by_Ca_AA 0 1.94909073959e-09 0.1 "" white blue 0 3 0
simundump kreac /kinetics/PKC/PKC_act_by_DAG_AA 0 2.0 0.2 "" white blue 1 3 0
simundump kreac /kinetics/PKC/PKC_basal_act 0 1.0 50.0 "" white blue -4 3 0
simundump kreac /kinetics/PKC/PKC_act_by_AA 0 1.94909073959e-10 0.1 "" white blue -4 -1 0
simundump kreac /kinetics/PKC/PKC_n_DAG 0 9.74545369788e-10 0.1 "" white blue -3 -1 0
simundump kreac /kinetics/PKC/PKC_n_DAG_AA 0 2.92363610936e-08 2.0 "" white blue -1 -2 0
simundump kreac /kinetics/4E_BP/eIF4E_BP_disso 0 1.0 1.62427476782e-07 "" white black -7 -5 0
simundump kreac /kinetics/S6Kinase/basal_S6K 0 0.01 0.0 "" white black 4 -1 0
simundump kreac /kinetics/protein/rad_pep_elongation 0 0.1 0.001 "" white black 22 -10 0
simundump kreac /kinetics/protein/rad_protein_deg 0 1.0 0.0 "" white black 23 -14 0
simundump kreac /kinetics/protein/labelling 0 0.0 0.0 "" white black 27 1 0
simundump kreac /kinetics/Ras/PI3K_bind_Ras_GTP 0 2.92363610936e-06 5.0 "" white black 13 -24 0
simundump kenz /kinetics/PI3K_activation/PDK1/S6K_phospho 0 0 0 0.0 0 615651.172948 7.91472114753e-07 4.0 1.0 0 0 "" 37 red "" 7 -7 0
simundump kenz /kinetics/Phosphatase/PP2A/dephos_clus_S6K 0 0 0 0.0 0 615651.172948 8.99394518123e-07 4.0 1.0 0 0 "" 25 red "" 3 1 0
simundump kenz /kinetics/Phosphatase/PP2A/dephos_S6K 0 0 0 0.0 0 615651.172948 8.99394518123e-07 4.0 1.0 0 0 "" 25 red "" 9 -2 0
simundump kenz /kinetics/Phosphatase/PP2A/dephosp_S6K 0 0 0 0.0 0 615651.172948 8.99394518123e-07 4.0 1.0 0 0 "" 25 red "" 13 -2 0
simundump kenz /kinetics/Phosphatase/PP2A/Dephos_AKTser473 0 0 0 0.0 0 615651.172948 2.96803230247e-06 7.2 1.8 0 0 "" 46 red "" 3 -8 0
simundump kenz /kinetics/Phosphatase/PP2A/Dephosph_AKTthr308 0 0 0 0.0 0 615651.172948 2.96793732541e-06 7.2 1.8 0 0 "" 46 red "" 0 -8 0
simundump kenz /kinetics/Phosphatase/PP2A/eEF2thr_56_dephospho 0 0 0 0.0 0 615651.172948 4.2270478609e-07 1.88 0.47 0 0 "" 4 red "" 23 8 0
simundump kenz /kinetics/Phosphatase/PP2A/PP2A_4E_BP_p_p 0 0 0 0.0 0 615651.172948 8.99404015826e-07 4.0 1.0 0 0 "" 4 red "" -11 -10 0
simundump kenz /kinetics/Phosphatase/PP2A/PP2A_4E_BP_p 0 0 0 0.0 0 615651.172948 8.99404015826e-07 4.0 1.0 0 0 "" 4 red "" -9 -17 0
simundump kenz /kinetics/Phosphatase/PP2A/PP2A_4E_BP 0 0 0 0.0 0 615651.172948 8.99375522717e-07 4.0 1.0 0 0 "" 62 red "" -13 -3 0
simundump kenz /kinetics/Phosphatase/PP2A/PP2A_4EBP 0 0 0 0.0 0 615651.172948 8.99375522717e-07 4.0 1.0 0 0 "" 62 red "" -13 -7 0
simundump kenz /kinetics/AKT_activation/PIP3_PDK1/phospho_thr308 0 0 0 0.0 0 615651.172948 0.000197875151967 40.0 10.0 0 0 "" 9 red "" -4 8 0
simundump kenz /kinetics/AKT_activation/PIP3_PDK2/phosp_AKTser473 0 0 0 0.0 0 615651.172948 0.000197865654262 80.0 20.0 0 0 "" 39 red "" 2 13 0
simundump kenz /kinetics/AKT_activation/PIP3_AKT_t308_s473/TSC2_phospho 0 0 0 0.0 0 615651.172948 4.6105651229e-06 24.0 6.0 0 0 "" 25 red "" 8 11 0
simundump kenz /kinetics/TrKB/BDNF_TrKB2_p_clx/PLC_g_phospho 0 0 0 0.0 0 615651.172948 1.31909204956e-05 2.0 0.5 0 0 "" red red "" -3 5 0
simundump kenz /kinetics/TrKB/BDNF_TrKB2_p_clx/SHC_phospho 0 0 0 0.0 0 615651.172948 2.84940598106e-06 1.2 0.3 0 0 "" red red "" -3 2 0
simundump kenz /kinetics/PI3K_activation/SHC_p_Grb2_Gab1_PI3K_clx/Phospho 0 0 0 0.0 0 615651.172948 7.9147422451e-06 16.0 4.0 0 0 "" brown red "" 2 -4 0
simundump kenz /kinetics/PI3K_activation/PI3K_basal/basal_phosp 0 0 0 0.0 0 615651.172948 7.91472114753e-06 16.0 4.0 0 0 "" 10 red "" -3 -16 0
simundump kenz /kinetics/PLC_g/PLCg_basal/PLC_g_phospho 0 0 0 0.0 0 615651.172948 1.31913602076e-05 2.0 0.5 0 0 "" 33 red "" -3 10 0
simundump kenz /kinetics/TSC1_TSC2/TSC1_TSC2/TSC2phospho 0 0 0 0.0 0 615651.172948 0.000527654408305 80.0 20.0 0 0 "" 51 red "" 12 8 0
simundump kenz /kinetics/mTORC1/TOR_Rheb_GTP_clx/S6K_phospho 0 0 0 0.0 0 615651.172948 5.93625455898e-07 0.24 0.06 0 0 "" 42 red "" 12 -16 0
simundump kenz /kinetics/mTORC1/TOR_Rheb_GTP_clx/TOR_4E_BP_phospho 0 0 0 0.0 0 615651.172948 4.39705675118e-06 4.0 1.0 0 0 "" 44 red "" -6 -11 0
simundump kenz /kinetics/mTORC1/TOR_Rheb_GTP_clx/TOR_4E_BP_p 0 0 0 0.0 0 615651.172948 4.39705675118e-06 4.0 1.0 0 0 "" 44 red "" -2 -20 0
simundump kenz /kinetics/S6Kinase/S6K_thr_412/S6_phos 0 0 0 0.0 0 615651.172948 3.16585890849e-07 0.04 0.01 0 0 "" 48 red "" 7 -19 0
simundump kenz /kinetics/S6Kinase/S6K_thr_252/CaMKIII_phospho 0 0 0 0.0 0 615651.172948 7.91472114753e-06 4.0 1.0 0 0 "" 6 red "" -6 18 0
simundump kenz /kinetics/S6Kinase/S6K_thr_252/S6_phospho 0 0 0 0.0 0 615651.172948 3.16586946361e-06 0.4 0.1 0 0 "" 4 red "" -6 16 0
simundump kenz /kinetics/CaMKIII/CaMKIII_CaM_Ca4/phospho 0 0 0 0.0 0 615651.172948 3.95740806229e-05 40.0 10.0 0 0 "" 58 red "" 18 21 0
simundump kenz /kinetics/CaMKIII/CaMKIII_basal/eEF2thr56_basal 0 0 0 0.0 0 615651.172948 3.95740806229e-05 40.0 10.0 0 0 "" 45 red "" 18 15 0
simundump kenz /kinetics/S6Kinase/S6K_basal/CaMKIII_basal 0 0 0 0.0 0 615651.172948 7.91557594083e-05 40.0 10.0 0 0 "" 45 red "" 23 19 0
simundump kenz /kinetics/Translation_elongation/Translation_clx/pro_syn 0 0 0 0.0 0 615651.172948 2.8781840286e-06 0.08 0.02 0 0 "" 52 red "" 17 -1 0
simundump kenz /kinetics/Translation_elongation/Translation_clx/rad_pro_syn 0 0 0 0.0 0 615651.172948 2.63827204153e-06 0.08 0.02 0 0 "" 52 red "" 17 2 0
simundump kenz /kinetics/MAPK/MAPK_p_p/cluster_phospho_S6K 0 0 0 0.0 0 615651.172948 4.5750437123e-07 4.0 1.0 0 0 "" red red "" 0 6 0
simundump kenz /kinetics/MAPK/MAPK_p_p/MAPK_p_p_feedback 0 0 0 0.0 0 615651.172948 3.08675359455e-06 40.0 10.0 0 0 "" orange red "" 10 10 0
simundump kenz /kinetics/MAPK/MAPK_p_p/phosph_Sos 0 0 0 0.0 0 615651.172948 3.08675359455e-05 40.0 10.0 0 0 "" orange red "" 20 30 0
simundump kenz /kinetics/MAPK/MAPK_p_p/MAPK_4E_BP_p_p 0 0 0 0.0 0 615651.172948 7.07464928465e-08 0.64 0.16 0 0 "" orange red "" -8 -10 0
simundump kenz /kinetics/MAPK/MAPK_p_p/MAPK_4E_BP_phospho 0 0 0 0.0 0 615651.172948 7.07464928465e-08 0.64 0.16 0 0 "" 47 red "" -9 -3 0
simundump kenz /kinetics/PKC/PKC_active/PKC_act_raf 0 0 0 0.0 0 615651.172948 1.58288724329e-06 16.0 4.0 0 0 "" yellow red "" 11 12 0
simundump kenz /kinetics/PKC/PKC_active/PKC_inact_GAP 0 0 0 0.0 0 615651.172948 9.49770336787e-06 16.0 4.0 0 0 "" yellow red "" 9 16 0
simundump kenz /kinetics/PKC/PKC_active/PKC_act_GEF 0 0 0 0.0 0 615651.172948 9.49770336787e-06 16.0 4.0 0 0 "" yellow red "" 7 19 0
simundump kenz /kinetics/MAPK/MAPKK_p_p/MAPKKtyr 0 0 0 0.0 0 615651.172948 5.12875981865e-05 1.2 0.3 0 0 "" pink red "" 8 3 0
simundump kenz /kinetics/MAPK/MAPKK_p_p/MAPKKthr 0 0 0 0.0 0 615651.172948 5.12875981865e-05 1.2 0.3 0 0 "" pink red "" 13 3 0
simundump kenz /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.1 0 0 0 0.0 0 615651.172948 1.49246910723e-05 1.2 0.3 0 0 "" red red "" 8 5 0
simundump kenz /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.2 0 0 0 0.0 0 615651.172948 1.49246910723e-05 1.2 0.3 0 0 "" red red "" 11 5 0
simundump kenz /kinetics/Phosphatase/MKP_1/MKP1_tyr_deph 0 0 0 0.0 0 615651.172948 4.52271136673e-06 16.0 4.0 0 0 "" hotpink red "" 5 3 0
simundump kenz /kinetics/Phosphatase/MKP_1/MKP1_thr_deph 0 0 0 0.0 0 615651.172948 4.52271136673e-06 16.0 4.0 0 0 "" hotpink red "" 10 3 0
simundump kenz /kinetics/Phosphatase/PPhosphatase2A/craf_dephospho 0 0 0 0.0 0 615651.172948 3.03309157053e-06 24.0 6.0 0 0 "" hotpink red "" 8 10 0
simundump kenz /kinetics/Phosphatase/PPhosphatase2A/MAPKK_dephospho 0 0 0 0.0 0 615651.172948 3.03309157053e-06 24.0 6.0 0 0 "" hotpink red "" 11 7 0
simundump kenz /kinetics/Phosphatase/PPhosphatase2A/MAPKK_dephospho_ser 0 0 0 0.0 0 615651.172948 3.03309157053e-06 24.0 6.0 0 0 "" hotpink red "" 8 7 0
simundump kenz /kinetics/Phosphatase/PPhosphatase2A/craf_p_p_dephospho 0 0 0 0.0 0 615651.172948 3.03309157053e-06 24.0 6.0 0 0 "" hotpink red "" 12 10 0
simundump kenz /kinetics/Ras/inact_GEF/basal_GEF_activity 0 0 0 0.0 0 615651.172948 1.56712105569e-08 0.08 0.02 0 0 "" hotpink red "" 12 20 0
simundump kenz /kinetics/Ras/GEF_p/GEF_p_act_Ras 0 0 0 0.0 0 615651.172948 3.13424211139e-07 0.08 0.02 0 0 "" hotpink red "" 7 16 0
simundump kenz /kinetics/Ras/GAP/GAP_inact_Ras 0 0 0 0.0 0 615651.172948 7.83332582968e-05 40.0 10.0 0 0 "" red red "" 9 12 0
simundump kenz /kinetics/Ras/CaM_GEF/CaM_GEF_act_Ras 0 0 0 0.0 0 615651.172948 3.13424211139e-06 0.8 0.2 0 0 "" pink red "" 5 18 0
simundump kenz /kinetics/Sos/SHC_p.Sos.Grb2/Sos.Ras_GEF 0 0 0 0.0 0 615651.172948 3.13424211139e-06 0.8 0.2 0 0 "" brown red "" 11 24 0
simundump kenz /kinetics/Translation_elongation/Basal_Translation/basal_syn 0 0 0 0.0 0 615651.172948 2.87808905156e-06 0.08 0.02 0 0 "" 53 red "" 23 -6 0
simundump kenz /kinetics/Translation_elongation/Basal_Translation/rad_basal_syn 0 0 0 0.0 0 615651.172948 2.87808905156e-06 0.08 0.02 0 0 "" 53 red "" 27 -11 0
simundump kenz /kinetics/40S/40S_basal/basal 0 0 0 0.0 0 615651.172948 3.16586946361e-06 0.4 0.1 0 0 "" 44 red "" 20 4 0
simundump kenz /kinetics/PI3K_activation/PTEN/PIP3_dephosp 0 0 0 0.0 0 615651.172948 0.000544142421352 22.0 5.5 0 0 "" 37 red "" 1 -15 0
simundump kenz /kinetics/Ras/Ras_GTP_PI3K/PIP2_phospho_Ras_GTP 0 0 0 0.0 0 615651.172948 7.91472114753e-06 16.0 4.0 0 0 "" 31 red "" 5 -23 0
addmsg /kinetics/PKC/PKC_DAG_AA_p /kinetics/PKC/PKC_active SUMTOTAL n nInit
addmsg /kinetics/PKC/PKC_Ca_memb_p /kinetics/PKC/PKC_active SUMTOTAL n nInit
addmsg /kinetics/PKC/PKC_Ca_AA_p /kinetics/PKC/PKC_active SUMTOTAL n nInit
addmsg /kinetics/PKC/PKC_DAG_memb_p /kinetics/PKC/PKC_active SUMTOTAL n nInit
addmsg /kinetics/PKC/PKC_basal_p /kinetics/PKC/PKC_active SUMTOTAL n nInit
addmsg /kinetics/PKC/PKC_AA_p /kinetics/PKC/PKC_active SUMTOTAL n nInit
simundump xgraph /graphs/conc1 0 0 99 0.001 0.999 0
simundump xgraph /graphs/conc2 0 0 100 0 1 0
 simundump xplot /graphs/conc1/40S.Co 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" black 0 0 1
simundump xplot /graphs/conc1/protein.Co 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" black 0 0 1
simundump xplot /graphs/conc1/MAPK_star.Co 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" yellow 0 0 1
simundump xplot /graphs/conc1/eIF4E.Co 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" black 0 0 1
simundump xplot /graphs/conc1/eIF4F_dash_mRNA_clx.Co 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" black 0 0 1
simundump xplot /graphs/conc1/eIF4F.Co 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" black 0 0 1
simundump xplot /graphs/conc1/S6K_thr_dash_252.Co 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" black 0 0 1
simundump xplot /graphs/conc1/TSC1_dash_TSC2_star.Co 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" yellow 0 0 1
simundump xplot /graphs/conc2/BDNF_TrkB2_star_clx.Co 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" white 0 0 1
simundump xplot /graphs/conc2/43Scomplex.Co 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" black 0 0 1
simundump xplot /graphs/conc2/PIP3_AKT_dash_t308_s473.Co 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" yellow 0 0 1
simundump xplot /graphs/conc2/degraded_protein.Co 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" black 0 0 1
simundump xplot /graphs/conc2/eIF4E_dash_BP.Co 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" white 0 0 1
simundump xplot /graphs/conc2/eIF4E_4E_dash_BP_t37_46_s65.Co 3 524288 \
"delete_plot.w <s> <d>; edit_plot.D <w>" white 0 0 1
simundump xgraph /moregraphs/conc3 0 0 100 0 1 0
simundump xgraph /moregraphs/conc4 0 0 100 0 1 0
 simundump xcoredraw /edit/draw 0 -6 4 -2 6
simundump xtree /edit/draw/tree 0 \
  /kinetics/#[],/kinetics/#[]/#[],/kinetics/#[]/#[]/#[][TYPE!=proto],/kinetics/#[]/#[]/#[][TYPE!=linkinfo]/##[] "edit_elm.D <v>; drag_from_edit.w <d> <S> <x> <y> <z>" auto 0.6
simundump xtext /file/notes 0 1
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
addmsg /kinetics/Sos/SHC_p /kinetics/Sos/SHC_p_dephospho SUBSTRATE n 
addmsg /kinetics/Sos/SHC_p_dephospho /kinetics/Sos/SHC_p REAC A B 
addmsg /kinetics/Sos/SHC /kinetics/Sos/SHC_p_dephospho PRODUCT n 
addmsg /kinetics/Sos/SHC_p_dephospho /kinetics/Sos/SHC REAC B A
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
addmsg /kinetics/CaM/CaM_Ca3 /kinetics/CaM/CaM_Ca3_bind_Ca SUBSTRATE n 
addmsg /kinetics/CaM/CaM_Ca3_bind_Ca /kinetics/CaM/CaM_Ca3 REAC A B 
addmsg /kinetics/Ca/Ca /kinetics/CaM/CaM_Ca3_bind_Ca SUBSTRATE n 
addmsg /kinetics/CaM/CaM_Ca3_bind_Ca /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/CaM/CaM_Ca4 /kinetics/CaM/CaM_Ca3_bind_Ca PRODUCT n 
addmsg /kinetics/CaM/CaM_Ca3_bind_Ca /kinetics/CaM/CaM_Ca4 REAC B A
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
addmsg /kinetics/MAPK/craf_1_p /kinetics/Ras/Ras_act_craf SUBSTRATE n 
addmsg /kinetics/Ras/Ras_act_craf /kinetics/MAPK/craf_1_p REAC A B 
addmsg /kinetics/Ras/GTP_Ras /kinetics/Ras/Ras_act_craf SUBSTRATE n 
addmsg /kinetics/Ras/Ras_act_craf /kinetics/Ras/GTP_Ras REAC A B 
addmsg /kinetics/MAPK/Raf_p_GTP_Ras /kinetics/Ras/Ras_act_craf PRODUCT n 
addmsg /kinetics/Ras/Ras_act_craf /kinetics/MAPK/Raf_p_GTP_Ras REAC B A
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
addmsg /kinetics/CaM/CaM_Ca4 /kinetics/Ras/CaM_bind_GEF SUBSTRATE n 
addmsg /kinetics/Ras/CaM_bind_GEF /kinetics/CaM/CaM_Ca4 REAC A B 
addmsg /kinetics/Ras/inact_GEF /kinetics/Ras/CaM_bind_GEF SUBSTRATE n 
addmsg /kinetics/Ras/CaM_bind_GEF /kinetics/Ras/inact_GEF REAC A B 
addmsg /kinetics/Ras/CaM_GEF /kinetics/Ras/CaM_bind_GEF PRODUCT n 
addmsg /kinetics/Ras/CaM_bind_GEF /kinetics/Ras/CaM_GEF REAC B A
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
addmsg /kinetics/Ca/Ca /kinetics/PKC/PKC_act_by_Ca SUBSTRATE n 
addmsg /kinetics/PKC/PKC_act_by_Ca /kinetics/Ca/Ca REAC A B 
addmsg /kinetics/PKC/PKC_cytosolic /kinetics/PKC/PKC_act_by_Ca SUBSTRATE n 
addmsg /kinetics/PKC/PKC_act_by_Ca /kinetics/PKC/PKC_cytosolic REAC A B 
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
addmsg /kinetics/Ras/GDP_Ras /kinetics/Ras/inact_GEF/basal_GEF_activity SUBSTRATE n 
addmsg /kinetics/Ras/inact_GEF/basal_GEF_activity /kinetics/Ras/GDP_Ras REAC sA B 
addmsg /kinetics/Ras/inact_GEF/basal_GEF_activity /kinetics/Ras/GTP_Ras MM_PRD pA
addmsg /kinetics/Ras/inact_GEF /kinetics/Ras/inact_GEF/basal_GEF_activity ENZYME n
addmsg /kinetics/Ras/inact_GEF/basal_GEF_activity /kinetics/Ras/inact_GEF REAC eA B
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
addmsg /kinetics/Ras/GDP_Ras /kinetics/Sos/SHC_p.Sos.Grb2/Sos.Ras_GEF SUBSTRATE n 
addmsg /kinetics/Sos/SHC_p.Sos.Grb2/Sos.Ras_GEF /kinetics/Ras/GDP_Ras REAC sA B 
addmsg /kinetics/Sos/SHC_p.Sos.Grb2/Sos.Ras_GEF /kinetics/Ras/GTP_Ras MM_PRD pA
addmsg /kinetics/Sos/SHC_p.Sos.Grb2 /kinetics/Sos/SHC_p.Sos.Grb2/Sos.Ras_GEF ENZYME n
addmsg /kinetics/Sos/SHC_p.Sos.Grb2/Sos.Ras_GEF /kinetics/Sos/SHC_p.Sos.Grb2 REAC eA B
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
addmsg /kinetics/40S/40S /graphs/conc1/40S.Co PLOT Co *40S *7
addmsg /kinetics/protein/protein /graphs/conc1/protein.Co PLOT Co *protein *red
addmsg /kinetics/MAPK/MAPK_p_p /graphs/conc1/MAPK_star.Co PLOT Co *MAPK_p_p *orange
addmsg /kinetics/Translation_initiation/eIF4E /graphs/conc1/eIF4E.Co PLOT Co *eIF4E *42
addmsg /kinetics/Translation_initiation/eIF4F_mRNA_clx /graphs/conc1/eIF4F_dash_mRNA_clx.Co PLOT Co *eIF4F_mRNA_clx *59
addmsg /kinetics/Translation_initiation/eIF4F /graphs/conc1/eIF4F.Co PLOT Co *eIF4F *6
addmsg /kinetics/S6Kinase/S6K_thr_252 /graphs/conc1/S6K_thr_dash_252.Co PLOT Co *S6K_thr_252 *6
addmsg /kinetics/TSC1_TSC2/TSC1_TSC2_p /graphs/conc1/TSC1_dash_TSC2_star.Co PLOT Co *TSC1_TSC2_p *40
addmsg /kinetics/TrKB/BDNF_TrKB2_p_clx /graphs/conc2/BDNF_TrkB2_star_clx.Co PLOT Co *BDNF_TrKB2_p_clx *red
addmsg /kinetics/43S_complex/43Scomplex /graphs/conc2/43Scomplex.Co PLOT Co *43Scomplex *hotpink
addmsg /kinetics/AKT_activation/PIP3_AKT_t308_s473 /graphs/conc2/PIP3_AKT_dash_t308_s473.Co PLOT Co *PIP3_AKT_t308_s473 *25
addmsg /kinetics/protein/degraded_protein /graphs/conc2/degraded_protein.Co PLOT Co *degraded_protein *white
addmsg /kinetics/4E_BP/eIF4E_BP /graphs/conc2/eIF4E_dash_BP.Co PLOT Co *eIF4E_BP *52
addmsg /kinetics/4E_BP/eIF4E_BP_t37_46_s65 /graphs/conc2/eIF4E_4E_dash_BP_t37_46_s65.Co PLOT Co *eIF4E_BP_t37_46_s65 *39

enddump
 // End of dump
call /kinetics/Phosphatase/PP2A/notes LOAD \ 
"Protein Phosphatase"
call /kinetics/AKT_activation/PIP3_AKT_t308_s473/notes LOAD \ 
"aaa"
call /kinetics/40S/40S_inact/notes LOAD \ 
"Inactivated form of S6K"
call /kinetics/40S/40S/notes LOAD \ 
"Activated form of S6"
call /kinetics/43S_complex/Q.R/notes LOAD \ 
"Q.R= Quaternary complex.Ribosome"
call /kinetics/43S_complex/Quaternary_clx/notes LOAD \ 
"Q= Quaternary complex"
call /kinetics/CaM/CaM/notes LOAD \ 
"There is a LOT of this in the cell: upto 1% of total protein mass. (Alberts et al) Say 25 uM. Meyer et al Science 256 1199-1202 1992 refer to studies saying it is comparable to CaMK levels."
call /kinetics/CaM/CaM_Ca2/notes LOAD \ 
"This is the intermediate where the TR2 end (the high-affinity end) has bound the Ca but the TR1 end has not."
call /kinetics/CaM/CaM_Ca/notes LOAD \ 
"This is the intermediate where the TR2 end (the high-affinity end) has bound the Ca but the TR1 end has not."
call /kinetics/Sos/Grb2/notes LOAD \ 
"There is probably a lot of it in the cell: it is also known as Ash (abundant src homology protein I think). Also Waters et al JBC 271:30 18224 1996 say that only a small fraction of cellular Grb is precipitated out when SoS is precipitated. As most of the Sos seems to be associated with Grb2, it would seem like there is a lot of the latter. Say 1 uM. I haven't been able to find a decent...."
call /kinetics/PKC/PKC_active/notes LOAD \ 
"Conc of PKC in brain is about 1 uM (?)"
call /kinetics/MAPK/craf_1/notes LOAD \ 
"Couldn't find any ref to the actual conc of craf-1 but I should try Strom et al Oncogene 5 pp 345 In line with the other kinases in the cascade, I estimate the conc to be 0.2 uM. To init we use 0.15, which is close to equil 16 May 2003: Changing to synaptic levels. Increasing 2.5 fold to 0.5 uM. See Mihaly et al 1991 Brain Res 547(2):309-14 and Morice et al 1999 Eur J Neurosci 11(6):1995-2006"
call /kinetics/MAPK/MAPKK/notes LOAD \ 
"Conc is from Seger et al JBC 267:20 pp14373 (1992) mwt is 45/46 Kd We assume that phosphorylation on both ser and thr is needed for activiation. See Kyriakis et al Nature 358 417 1992 Init conc of total is 0.18 Ortiz et al 1995 J Neurosci 15(2):1285-1297 suggest that levels are higher in hippocampus than other brain regions, and further elevated in synapses. Estimate 3x higher levels than before, at 0.5 uM. Similar results from Schipper et al 1999 Neuroscience 93(2):585-595 but again lacking in quantitation."
call /kinetics/MAPK/MAPK/notes LOAD \ 
"conc is from Sanghera et al JBC 265 pp 52 (1990) A second calculation gives 3.1 uM, from same paper. They est MAPK is 1e-4x total protein, and protein is 15% of cell wt, so MAPK is 1.5e-5g/ml = 0.36uM. which is closer to our first estimate. Lets use this. Updated 16 May 2003. Ortiz et al 1995 J Neurosci 15(2):1285-1297 provide estimates of ERK2 levels in hippocampus: 1009 ng/mg. This comes to about 3.6uM, which may still be an underestimate of synaptic levels."
call /kinetics/MAPK/craf_1_p_p/notes LOAD \ 
"Negative feedback by MAPK_star by hyperphosphorylating craf-1_star gives rise to this pool. Ueki et al JBC 269(22):15756-15761, 1994"
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
call /kinetics/Ras/inact_GEF/notes LOAD \ 
"Assume that SoS is present only at 50 nM. Revised to 100 nM to get equil to experimentally known levels."
call /kinetics/Ras/GEF_p/notes LOAD \ 
"phosphorylated and thereby activated form of GEF. See, e.g. Orita et al JBC 268:34 25542-25546 1993, Gulbins et al. It is not clear whether there is major specificity for tyr or ser/thr."
call /kinetics/Ras/GTP_Ras/notes LOAD \ 
"Only a very small fraction (7% unstim, 15% stim) of ras is GTP-bound. Gibbs et al JBC 265(33) 20437"
call /kinetics/Ras/GDP_Ras/notes LOAD \ 
"GDP bound form. See Rosen et al Neuron 12 1207-1221 June 1994. the activation loop is based on Boguski and McCormick Nature 366 643-654 93 Assume Ras is present at about the same level as craf-1, 0.2 uM. Hallberg et al JBC 269:6 3913-3916 1994 estimate upto 5-10% of cellular Raf is assoc with Ras. Given that only 5-10% of Ras is GTP-bound, we need similar amounts of Ras as Raf."
call /kinetics/Ras/GAP/notes LOAD \ 
"GTPase-activating proteins. See Boguski and McCormick. Turn off Ras by helping to hydrolyze bound GTP. This one is probably NF1, ie., Neurofibromin as it is inhibited by AA and lipids, and expressed in neural cells. p120-GAP is also a possible candidate, but is less regulated. Both may exist at similar levels. See Eccleston et al JBC 268(36) pp27012-19 Level=.002 16 May 2003: Increased level to 0.0036, in line with other concentration raises at the synapse."
call /kinetics/Ras/CaM_GEF/notes LOAD \ 
"See Farnsworth et al Nature 376 524-527 1995"
call /kinetics/Sos/Sos/notes LOAD \ 
"I have tried using low (0.02 uM) initial concs, but these give a very flat response to EGF stim although the overall activation of Ras is not too bad. I am reverting to 0.1 because we expect a sharp initial response, followed by a decline. Sep 17 1997: The transient activation curve looks better with [Sos] = 0.05. Apr 26 1998: Some error there, it is better where it was at 0.1"
call /kinetics/43S_complex/43Scomplex/notes LOAD \ 
"40S_complex consist of Quaternary complex, mRNA complex, 40S Ribosomes."
call /kinetics/PKC/PKC_DAG/notes LOAD \ 
"CoInit was .0624"
call /kinetics/PKC/PKC_cytosolic/notes LOAD \ 
"Marquez et al J. Immun 149,2560(92) est 1e6/cell for chromaffin cells We will use 1 uM as our initial concen"
call /kinetics/PKC/DAG/notes LOAD \ 
"The conc of this has been a problem. Schaecter and Benowitz use 50 uM, but Shinomura et al have < 5. So I have altered the DAG-dependent rates in the PKC model to reflect this."
call /kinetics/Translation_elongation/Basal_Translation/notes LOAD \ 
"It will contribute to mTOR independent translation."
call /kinetics/CaM/CaM_Ca3_bind_Ca/notes LOAD \ 
"Use K3 = 21.5 uM here from Stemmer and Klee table 3. kb/kf =21.5 * 6e5 so kf = 7.75e-7, kb = 10"
call /kinetics/CaM/CaM_bind_Ca/notes LOAD \ 
"Lets use the fast rate consts here. Since the rates are so different, I am not sure whether the order is relevant. These correspond to the TR2C fragment. We use the Martin et al rates here, plus the Drabicowski binding consts. All are scaled by 3X to cell temp. kf = 2e-10 kb = 72 Stemmer & Klee: K1=.9, K2=1.1. Assume 1.0uM for both. kb/kf=3.6e11. If kb=72, kf = 2e-10 (Exactly the same !) 19 May 2006. Splitting the old CaM-TR2-bind-Ca reaction into two steps, each binding 1 Ca. This improves numerical stability and is conceptually better too. Overall rates are the same, so each kf and kb is the square root of the earlier ones. So kf = 1.125e-4, kb = 8.4853"
call /kinetics/CaM/CaM_Ca2_bind_Ca/notes LOAD \ 
"K3 = 21.5, K4 = 2.8. Assuming that the K4 step happens first, we get kb/kf = 2.8 uM = 1.68e6 so kf =6e-6 assuming kb = 10"
call /kinetics/CaM/CaM_Ca_bind_Ca/notes LOAD \ 
"Lets use the fast rate consts here. Since the rates are so different, I am not sure whether the order is relevant. These correspond to the TR2C fragment. We use the Martin et al rates here, plus the Drabicowski binding consts. All are scaled by 3X to cell temp. kf = 2e-10 kb = 72 Stemmer & Klee: K1=.9, K2=1.1. Assume 1.0uM for both. kb/kf=3.6e11. If kb=72, kf = 2e-10 (Exactly the same !) 19 May 2006. Splitting the old CaM-TR2-bind-Ca reaction into two steps, each binding 1 Ca. This improves numerical stability and is conceptually better too. Overall rates are the same, so each kf and kb is the square root of the earlier ones. So kf = 1.125e-4, kb = 8.4853"
call /kinetics/Ras/Ras_act_craf/notes LOAD \ 
"Assume the binding is fast and limited only by the amount of Ras_star available. So kf=kb/[craf-1] If kb is 1/sec, then kf = 1/0.2 uM = 1/(0.2 * 6e5) = 8.3e-6 Later: Raise it by 10 X to 4e-5 From Hallberg et al JBC 269:6 3913-3916 1994, 3% of cellular Raf is complexed with Ras. So we raise kb 4x to 4 This step needed to memb-anchor and activate Raf: Leevers et al Nature 369 411-414 May 16, 2003 Changed Ras and Raf to synaptic levels, an increase of about 2x for each. To maintain the percentage of complexed Raf, reduced the kf by 2.4 fold to 10."
call /kinetics/Ras/Ras_intrinsic_GTPase/notes LOAD \ 
"This is extremely slow (1e-4), but it is significant as so little GAP actually gets complexed with it that the total GTP turnover rises only by 2-3 X (see Gibbs et al, JBC 265(33) 20437-20422) and Eccleston et al JBC 268(36) 27012-27019 kf = 1e-4"
call /kinetics/Ras/dephosph_GAP/notes LOAD \ 
"Assume a reasonably good rate for dephosphorylating it, 1/sec"
call /kinetics/Ras/CaM_bind_GEF/notes LOAD \ 
"We have no numbers for this. It is probably between the two extremes represented by the CaMKII phosph states, and I have used guesses based on this. kf=1e-4 kb=1 The reaction is based on Farnsworth et al Nature 376 524-527 1995"
call /kinetics/Sos/SHC_bind_Sos.Grb2/notes LOAD \ 
"Sasaoka et al JBC 269:51 pp 32621 1994, table on pg 32623 indicates that this pathway accounts for about 50% of the GEF activation. (88% - 39%). Error is large, about 20%. Fig 1 is most useful in constraining rates. Chook et al JBC 271:48 pp 30472, 1996 say that the Kd is 0.2 uM for Shc binding to EGFR. The Kd for Grb direct binding is 0.7, so we'll ignore it."
call /kinetics/Sos/Grb2_bind_Sos_p/notes LOAD \ 
"Same rates as Grb2_bind_Sos: Porfiri and McCormick JBC 271:10 pp 5871 1996 show that the binding is not affected by the phosph."
call /kinetics/Sos/dephosph_Sos/notes LOAD \ 
"The only clue I have to these rates is from the time courses of the EGF activation, which is around 1 to 5 min. The dephosph would be expected to be of the same order, perhaps a bit longer. Lets use 0.002 which is about 8 min. Sep 17: The transient activation curve matches better with kf = 0.001"
call /kinetics/Sos/Grb2_bind_Sos/notes LOAD \ 
"As there are 2 SH3 domains, this reaction could be 2nd order. I have a Kd of 22 uM from peptide binding (Lemmon et al JBC 269:50 pg 31653). However, Chook et al JBC 271:48 pg30472 say it is 0.4uM with purified proteins, so we believe them. They say it is 1:1 binding."
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
call /kinetics/MAPK/MAPK_p_p/MAPK_p_p_feedback/notes LOAD \ 
"Ueki et al JBC 269(22):15756-15761 show the presence of this step, but not the rate consts, which are derived from Sanghera et al JBC 265(1):52-57, 1990, see the deriv in the MAPK_star notes."
call /kinetics/MAPK/MAPK_p_p/phosph_Sos/notes LOAD \ 
"See Porfiri and McCormick JBC 271:10 pp5871 1996 for the existence of this step. We'll take the rates from the ones used for the phosph of Raf by MAPK. Sep 17 1997: The transient activation curve matches better with k1 up by 10 x."
call /kinetics/PKC/PKC_active/PKC_act_raf/notes LOAD \ 
"Rate consts from Chen et al Biochem 32, 1032 (1993) k3 = k2 = 4 k1 = 9e-5 recalculated gives 1.666e-5, which is not very different. Looks like k3 is rate-limiting in this case: there is a huge amount of craf locked up in the enz complex. Let us assume a 10x higher Km, ie, lower affinity. k1 drops by 10x. Also changed k2 to 4x k3. Lowerd k1 to 1e-6 to balance 10X DAG sensitivity of PKC"
call /kinetics/PKC/PKC_active/PKC_inact_GAP/notes LOAD \ 
"Rate consts copied from PCK-act-raf This reaction inactivates GAP. The idea is from the Boguski and McCormick review."
call /kinetics/PKC/PKC_active/PKC_act_GEF/notes LOAD \ 
"Rate consts from PKC-act-raf. This reaction activates GEF. It can lead to at least 2X stim of ras, and a 2X stim of MAPK over and above that obtained via direct phosph of c-raf. Note that it is a push-pull reaction, and there is also a contribution through the phosphorylation and inactivation of GAPs. The original PKC-act-raf rate consts are too fast. We lower K1 by 10 X"
call /kinetics/MAPK/MAPKK_p_p/MAPKKtyr/notes LOAD \ 
"The actual MAPKK is 2 forms from Seger et al JBC 267:20 14373(1992) Vmax = 150nmol/min/mg From Haystead et al FEBS 306(1):17-22 we get Km=46.6nM for at least one of the phosphs. Putting these together: k3=0.15/sec, scale to get k2=0.6. k1=0.75/46.6nM=2.7e-5"
call /kinetics/MAPK/MAPKK_p_p/MAPKKthr/notes LOAD \ 
"Rate consts same as for MAPKKtyr."
call /kinetics/MAPK/Raf_p_GTP_Ras/Raf_p_GTP_Ras.1/notes LOAD \ 
"Kinetics are the same as for the craf-1_star activity, ie., k1=1.1e-6, k2=.42, k3 =0.105 These are based on Force et al PNAS USA 91 1270-1274 1994. These parms cannot reach the observed 4X stim of MAPK. So lets increase the affinity, ie, raise k1 10X to 1.1e-5 Lets take it back down to where it was. Back up to 5X: 5.5e-6"
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
call /kinetics/Ras/GEF_p/GEF_p_act_Ras/notes LOAD \ 
"Kinetics same as GEF-bg-act-ras"
call /kinetics/Ras/GAP/GAP_inact_Ras/notes LOAD \ 
"From Eccleston et al JBC 268(36)pp27012-19 get Kd < 2uM, kcat - 10/sec From Martin et al Cell 63 843-849 1990 get Kd ~ 250 nM, kcat = 20/min I will go with the Eccleston figures as there are good error bars (10%). In general the values are reasonably close. k1 = 1.666e-3/sec, k2 = 1000/sec, k3 = 10/sec (note k3 is rate-limiting) 5 Nov 2002: Changed ratio term to 4 from 100. Now we have k1=8.25e-5; k2=40, k3=10. k3 is still rate-limiting."
call /kinetics/Ras/CaM_GEF/CaM_GEF_act_Ras/notes LOAD \ 
"Kinetics same as GEF-bg_act-ras"
complete_loading
