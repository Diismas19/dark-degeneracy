from getdist import loadMCSamples

lcdm_samples=loadMCSamples('/home/vitor-petri/projects/cobaya/coding/vitor-cobaya-lcdm/chains/lcdm')
fld_samples=loadMCSamples('/home/vitor-petri/projects/cobaya/coding/vitor-cobaya-fld/chains/fld')
int_samples=loadMCSamples('/home/vitor-petri/projects/cobaya/coding/vitor-cobaya-int/chains/int')

print('LCDM')
print(lcdm_samples.getLikeStats())
print('\n')
print('FLD')
print(fld_samples.getLikeStats())
print('\n')
print('INT')
print(int_samples.getLikeStats())

