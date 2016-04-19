load("./BSPHighPWMScoreNonBinding/TFHelTs.RData")
names<-names(TFHelTs)
list1<-c(2,3,5,6,7,9,10,11,12,13,14,15,16,18,19,20) #8_30 mer samples 3, integrate prediction 6
list2<-c(1,4,5,6,7,8,11,13,14,15,16,20) #8_30 mer samples 4, integrate prediction 7
list3<-c(1,3,5,7,8,9,10,11,12,13,14,15,16,17) #8_30 mer samples 5, integrate prediction 8
list4<-c(4,6,7,8,12,15,16,19) #8_30 mer samples 6, integrate prediction 9
list5<-c(1,4,5,6,10,13,15,16) #8_30 mer samples 7, integrate prediction 10
list6<-c(22,37,69,94,98,109) #8_30 mer samples 8, integrate prediction 11
list7<-c(1,3,4,5,7,8,9,12,13,14,15,16,17,18,19) #8_30 mer samples 2, integrate prediction 4
usednames<-c(names[list1],names[list2+20],names[list3+40],
	names[list4+60],names[list5+80],names[list7+99])

source.path<-'/media/saens/0A57743A4B30AD0C/works/RamseyLab/projects/BSP/TFBSshape data/'
mainDir <- "./bindingsites/"
subDir <- "outputDirectory"

for(i in 1:length(usednames)){
	TF<-usednames[i]
	source.file<-paste(source.path,TF,'/binding_sites',sep="")
	subDir<-TF
	dir.create(file.path(mainDir, subDir), showWarnings = FALSE)

	target.file<-paste(file.path(mainDir, subDir),'/binding_sites_',TF,sep="")
	file.copy(from = source.file, to = target.file)
}