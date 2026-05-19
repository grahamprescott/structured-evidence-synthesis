# VBAC working controlled vocabulary

Seeded from `context/Claude VBAC generic.rtf`. Extended as papers are processed. Novel codes flagged `[UNVERIFIED]` at first appearance; harmonised entries below carry no flag.

## subject_codes (predictors of VBAC outcomes)

| code | definition | also covers |
|---|---|---|
| prior_vaginal_birth | Any prior vaginal delivery before the index pregnancy. | prior VD, previous vaginal delivery |
| prior_successful_vbac | Specifically a prior successful VBAC. | previous VBAC, prior TOLAC success |
| prior_caesarean_count | Number of prior caesarean deliveries. | parity of prior CS, number of prior CD |
| prior_caesarean_indication_recurring | Prior CS for an indication likely to recur (e.g. CPD, arrest of dilation, failure to progress). | dystocia indication, CPD, FTP |
| prior_caesarean_indication_non_recurring | Prior CS for a non-recurring indication (e.g. breech, fetal distress, malpresentation). | breech indication, non-recurrent indication |
| spontaneous_labour_onset | Labour starts spontaneously without induction. | spontaneous labour |
| induction_of_labour | Pharmacological or mechanical induction of labour. | induced labour, IOL |
| labour_augmentation | Augmentation of labour with oxytocin or other means. | oxytocin augmentation |
| prostaglandin_use | Use of prostaglandins for cervical ripening/induction. | PGE2, misoprostol |
| oxytocin_use | Use of oxytocin (for induction or augmentation). | syntocinon |
| bishop_score | Bishop score / cervical favourability at admission. | favourable cervix, cervical ripeness |
| cervical_dilation_at_admission | Cervical dilatation in cm at hospital admission. | admission dilatation |
| maternal_age | Maternal age (often advanced maternal age >35 or >40). | age >40, AMA |
| maternal_bmi | Maternal body mass index, often categorised as obesity. | BMI, obesity, maternal weight |
| inter_delivery_interval | Time between previous caesarean and current delivery. | interpregnancy interval, IDI |
| gestational_age | Gestational age at delivery (often >40 weeks marked as risk). | GA, post-dates |
| macrosomia | Estimated or actual fetal weight >4000g (or >4500g). | birthweight >4000g, large for gestational age |
| preeclampsia | Pregnancy-induced hypertension / preeclampsia. | PIH, hypertensive disorders of pregnancy |
| gestational_diabetes | Gestational diabetes mellitus. | GDM |
| prior_uterine_incision_type | Type of uterine incision in prior CS (low transverse vs classical/T). | type of scar, low transverse incision |
| maternal_height | Maternal height (cm or in). | short stature, height <160 cm |
| parity | Parity (number of prior births of any kind). | gravidity, multiparity |
| ethnicity | Maternal ethnicity / race. | race, ethnic group |
| socioeconomic_status | SES, education, insurance, area-level deprivation. | SES, deprivation |
| mfmu_calculator_score | Grobman / MFMU VBAC success calculator score. | Grobman score, VBAC calculator |
| station_at_admission | Fetal station at admission. | station, engagement |
| uterine_scar_thickness | Sonographic lower-uterine-segment thickness. | LUS thickness, scar thickness |
| epidural_analgesia | Use of epidural analgesia in labour. | epidural, regional analgesia |

## object_codes (VBAC outcomes)

| code | definition | also covers |
|---|---|---|
| vbac_success | Successful vaginal birth after caesarean (the index TOLAC ends in vaginal delivery). | successful VBAC, vaginal delivery after CS |
| tolac_failure | TOLAC that ends in repeat caesarean. | failed TOLAC, repeat caesarean after trial of labour |
| uterine_rupture | Complete uterine rupture during TOLAC. | uterine rupture, full-thickness scar disruption |
| uterine_dehiscence | Asymptomatic / incomplete uterine scar separation. | scar dehiscence, asymptomatic separation |
| maternal_morbidity | Composite or specific adverse maternal outcomes (e.g. hysterectomy, sepsis, ICU). | maternal complication, composite maternal outcome |
| maternal_mortality | Maternal death attributable to TOLAC. | maternal death |
| neonatal_morbidity | Composite or specific neonatal adverse outcomes. | composite neonatal outcome, neonatal complication |
| neonatal_mortality | Perinatal or neonatal death. | perinatal mortality, neonatal death |
| apgar_score | Apgar score (at 1 or 5 min). | Apgar <7 |
| nicu_admission | Admission to neonatal intensive care unit. | NICU |
| hysterectomy | Peripartum hysterectomy. | postpartum hysterectomy |
| transfusion | Blood transfusion requirement. | blood transfusion |
| endometritis | Postpartum endometritis. | puerperal endometritis |
| postpartum_haemorrhage | Postpartum haemorrhage. | PPH, blood loss |
| fetal_injury | Birth-related fetal/neonatal injury (e.g. instrumental delivery trauma). | birth trauma, vacuum injury |
| hypoxic_ischaemic_encephalopathy | HIE attributable to intrapartum events. | HIE, neonatal encephalopathy |

## Revision log

| date | change | rationale |
|---|---|---|
| 2026-05-19 | Seeded vocabulary from VBAC context note. | Initial pass before extraction. |
