from classy import Class

teste = '/home/vitor-petri/projects/cobaya/chains/teste.1.txt'

with open(teste,'r') as file:
    lines = file.readlines()
    cabecalho = lines[0].split()
    first_line = lines[1].split()
    del cabecalho[0]

dado_teste = {}
for i in range(0,len(cabecalho)):
    dado_teste[cabecalho[i]] = float(first_line[i])

keys = ['n_s','theta_s_100','omega_b','omega_cdm','w0_int','wa_int','tau_reio','A_s']

cosmo = {k: dado_teste[k] for k in keys}
cosmo['m_ncdm'] = 0.06

INT = Class()
INT.set(cosmo)
INT.set({'z_max_pk':2,'output':'tCl,lCl,mPk,mTk','k_output_values':0.05,'gauge':'newtonian','non linear':'hmcode','nonlinear_min_k_max':20,'N_ncdm': 1, 'N_ur': 2.0328})
INT.compute()

print(f'Diferença entre os H0: {100*INT.h() - dado_teste['H0']}')
print(f'Diferença entre os Sigma8: {INT.sigma8() - dado_teste['sigma8']}')

teste2 = '/home/vitor-petri/projects/cobaya/coding/vitor-cobaya-int/chains/int.1.txt'

with open(teste2,'r') as file:
    lines = file.readlines()
    cabecalho = lines[0].split()
    first_line = lines[1].split()
    del cabecalho[0]

dado_teste = {}
for i in range(0,len(cabecalho)):
    dado_teste[cabecalho[i]] = float(first_line[i])

keys = ['n_s','theta_s_100','omega_b','omega_cdm','w0_int','wa_int','tau_reio','A_s']

cosmo = {k: dado_teste[k] for k in keys}
cosmo['m_ncdm'] = 0.06

INT = Class()
INT.set(cosmo)
INT.set({'z_max_pk':2,'output':'tCl,lCl,mPk,mTk','k_output_values':0.05,'gauge':'newtonian','non linear':'hmcode','nonlinear_min_k_max':20,'N_ncdm': 1, 'N_ur': 2.0328})
INT.compute()

print('Teste 2')
print(f'Diferença entre os H0: {100*INT.h() - dado_teste['H0']}')
print(f'Diferença entre os Sigma8: {INT.sigma8() - dado_teste['sigma8']}')