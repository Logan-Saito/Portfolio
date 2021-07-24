cap log close
cd "C:\Users\logan\OneDrive\Desktop\CIF Final Project"
log using FinalProject.log, replace

use CCES_Panel_Full3waves_VV_V4.dta, clear

gen faminc_sort_10 = 10000 * faminc_10 if (faminc_10 < 19)
gen faminc_sort_12 = 10000 * faminc_12 if (faminc_12 < 19)
gen faminc_sort_14 = 10000 * faminc_14 if (faminc_14 < 19)
summarize faminc_sort_10 faminc_sort_12 faminc_sort_14

gen party_republican_10 = 0 
replace party_republican_10 = 1 if (CC10_390 == 2)
replace party_republican_10 = . if (CC10_390 > 3)

gen party_republican_12 = 0 
replace party_republican_12 = 1 if (CC12_390 == 2)
replace party_republican_12 = . if (CC12_390 > 3)

gen party_republican_14 = 0 
replace party_republican_14 = 1 if (CC14_390 == 2)
replace party_republican_14 = . if (CC14_390 > 3)

gen id = _n
reshape long faminc_sort_ party_republican_ employ_ StateAbbr_, i(id) j(year)


est clear
eststo: reg faminc_sort party_republican_
eststo: areg faminc_sort_ party_republican_, absorb(id)
eststo: areg faminc_sort_ party_republican_, absorb(year)
eststo: areg faminc_sort_ party_republican_ i.year, absorb(id)
esttab using FinalPanelProject.csv, se r2 replace

gen dummy_employ = 0
replace dummy_employ = 1 if (employ_ == 4)
tabulate dummy_employ

est clear
eststo: reg faminc_sort party_republican_ dummy_employ
eststo: areg faminc_sort party_republican_ dummy_employ, absorb(id)
eststo: areg faminc_sort party_republican_ dummy_employ, absorb(year)
eststo: areg faminc_sort_ party_republican_ i.year dummy_employ, absorb(id)
esttab using FinalPanelProjectEmploy.csv, se r2 replace

est clear
eststo: areg faminc_sort party_republican_ , absorb(StateAbbr_)
eststo: areg faminc_sort_ party_republican_ i.year, absorb(StateAbbr_)
esttab using FinalPanelProjectLoc.csv, se r2 replace

tabulate StateAbbr_
stop