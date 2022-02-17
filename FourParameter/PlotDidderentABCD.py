import numpy as np
import matplotlib
import matplotlib as mpl
# mpl.use("pgf")
#from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
### for Palatino and other serif fonts use:
##rc('font',**{'family':'serif','serif':['Palatino']})
#rc('text', usetex=True)
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
matplotlib.rcParams['text.latex.preamble'] = [
       '\\usepackage{CJK}',
       r'\AtBeginDocument{\begin{CJK}{UTF8}{gbsn}}',
       r'\AtEndDocument{\end{CJK}}',
]

# pgf_with_rc_fonts = {
# 	"font.family": "serif",
# 	"font.serif": [],                   # use latex default serif font
# 	"font.sans-serif": ["SimHei"], # use a specific sans-serif font
# }
# mpl.rcParams.update(pgf_with_rc_fonts)
#matplotlib.rcParams['text.latex.preamble'] = [
#	   '\\usepackage{CJK}',
#	   r'\AtBeginDocument{\begin{CJK}{UTF8}{gbsn}}',
#	   r'\AtEndDocument{\end{CJK}}',
#]
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy import optimize
from adjustText import adjust_text
# from moviepy.editor import VideoClip
# from moviepy.video.io.bindings import mplfig_to_npimage
# import moviepy.editor as mpy

def func_A(x):
	a,b,c,d,e,f,g,h,i = 0.,-0.00610833,0.00150847,5.77749,0.77655055,0.000265084,0.00189221,0.0320232,0.520944
	return (a * x ** 2 + b * x + c) / (1 + np.exp(-d * (x - e))) + (f * x ** 2 + g * x + h) / (1 + np.exp(-i * (x - e)))


def func_B(x):
	a,b,c,d,e,f,g,h,i = -0.0380714,-0.389742,0.832097,0.11715,1.00594,0.0430202,0.115392,-0.217208,5.14202
	return (a * x ** 2 + b * x + c) / (1 + np.exp(-d * (x - e))) + (f * x ** 2 + g * x + h) / (1 + np.exp(-i * (x - e)))



def func_C(x):
	a,b,c,d,e,f,g,h,i = -0.000632976,-0.00186678,0.748577,5.49769,0.9,-0.0266069,0.114567,0.574344,-5.51776
	return (a * x ** 2 + b * x + c) / (1 + np.exp(-d * (x - e))) + (f * x ** 2 + g * x + h) / (1 + np.exp(-i * (x - e)))


def func_D(x):
	a,b,c,d,e,f,g,h,i = 0.,-0.00148349,0.470459,0.0483721,0.8,0.,-0.00542422,0.0156325,4.15415   
	return (a * x ** 2 + b * x + c) / (1 + np.exp(-d * (x - e))) + (f * x ** 2 + g * x + h) / (1 + np.exp(-i * (x - e)))

def equiv_strain(ABCD, s):
	'''根据应变值计算等效应变
	'''
	s1 = s[0]
	s2 = s[1]
	s3 = s[2]
	a = ABCD[0]
	b = ABCD[1]
	c = ABCD[2]
	d = ABCD[3]
	i1 = np.sum(s)
	j2 = ((s1 - s2) ** 2 + (s1 - s3) ** 2 + (s2 - s3) ** 2) / 6
	fa = 1.0
	fb = -(b * np.sqrt(j2) + c * s1 + d * i1)
	fc = -a * j2
	estrain = (-fb + np.sqrt(fb ** 2 - 4 * fa * fc)) / (2 * fa)
	return estrain

def force_2_strain(e, mu, f):
	"""
	in:
		f is np.array
	out:
		epsilon is np.array
	"""
	poisson = np.array([[1, -mu, -mu],
						[-mu, 1, -mu],
						[-mu, -mu, 1]])
	strain = np.dot(poisson, f) / e
	return strain

def get_strain(beta,e,mu,ft,ct,curve):
	'''根据beta值返回应变值
	'''
	if curve == 1:
		f = np.array([ft,0,0])
		if beta <= 1.0:
			def fun(x):
				return 1.2 * x - 0.2 * x ** 6 - beta
			sol = optimize.root(fun,beta)
			x = sol.x
		elif beta > 1.0:
			def fun(x):
				return x / (2.723 * (x - 1) ** 1.7 + x) - (2.0 - beta)
			sol = optimize.root(fun,beta)
			x = sol.x
			beta = 2.0 - beta
	elif curve == 2:
		f = np.array([[0], [0], [-ft / ct]])
		if beta <= 1.0:
			def fun(x):
				return 1.746 * x - 0.492 * x ** 2 - 0.254 * x ** 3 - beta

			sol = optimize.root(fun, beta)
			x = sol.x
			beta = beta
		else:
			def fun(x):
				return x / (1.635 * (x - 1) ** 2 + x) - (2.0 - beta)

			sol = optimize.root(fun, beta)
			x = sol.x
			beta = 2.0 - beta

	
	s = force_2_strain(e,mu,f)
	s = np.multiply(s,x)

	return s,x

def strain_stress(x):
	if x <= 1.0:
		return 1.2 * x - 0.2 * x ** 6
	else:
		return x / (2.723 * (x - 1) ** 1.7 + x)

if __name__ == "__main__":
	e = 3.14e10
	mu = 0.167
	ft = 3.47e6
	ct = 0.126
	beta = 1.0
	e0 = ft / e

	#plt.rc('text',usetex=True)
	#plt.rc('font',family='serif')

	#f = open("FourParameter\\FITABCD.data",'r')
	#lines = f.readlines()

	#x = []
	#fa = []
	#fb = []
	#fc = []
	#fd = []
	#i = 0
	#for iline in lines:
	#	i += 1
	#	if i > 1:
	#		data = list(map(float,iline.split()))
	#		x.append(data[0])
	#		fa.append(data[1])
	#		fb.append(data[2])
	#		fc.append(data[3])
	#		fd.append(data[4])
	plt.figure(figsize=(4,3))
	#计算假定点的等效应力和等效应变
	beta = 1.2
	tarbeta = get_strain(beta,e,mu,ft,ct,1)[1]
	#绘制假定点的x
	plt.axvline(x=tarbeta,linestyle='-.',linewidth=0.5)
	plt.axhline(y=0.8,linestyle='-.',linewidth=0.5)
	nabcd = 10
	ndiv = 100

	#绘制利用不同等效应变对应的参数计算出来的等效应变值
	betas = [1.0,1.2,1.4]

	for ibeta in betas:
		xbeta = get_strain(ibeta,e,mu,ft,ct,1)[1]
		print(xbeta)
		a = func_A(xbeta)
		b = func_B(xbeta)
		c = func_C(xbeta)
		d = func_D(xbeta)
		abcd = np.array([a,b,c,d])
		es = []
		y = []
		for idiv in range(ndiv):
			beta = 0.5 * idiv / ndiv + 1.0   #1.0-1.5范围内的x
			s = get_strain(beta,e,mu,ft,ct,2)[0]
			es.append(equiv_strain(abcd,s) / e0)
			y.append(2.0 - beta)
		plt.plot(es,y,"-.",linewidth=0.5,label=r'$\beta={0:.3f}$'.format(float(2-ibeta)))
		#plt.annotate('$β={0:.3f}$'.format(float(xbeta)),xy=(1,1),xytext=(1.8,0.8),arrowprops=dict(arrowstyle="->"))
		#beta = 1.2
		#s = get_strain(beta,e,mu,ft,ct,2)[0]
		#es = equiv_strain(abcd,s)/e0
		#plt.scatter(es,2.0-beta)
	
	es = []
	y = []
	for idiv in range(ndiv):
		beta = 0.5 * idiv / ndiv + 1.0
		ybeta = get_strain(beta,e,mu,ft,ct,1)[1]
		s = get_strain(beta,e,mu,ft,ct,2)[0]
		a = func_A(ybeta)
		b = func_B(ybeta)
		c = func_C(ybeta)
		d = func_D(ybeta)
		abcd = np.array([a,b,c,d])
		es.append(equiv_strain(abcd,s) / e0)
		y.append(2.0 - beta)
	plt.plot(es,y,linewidth=1.0,label=u"变参数")
	plt.text(0.8,0.6,r"$A=f(\beta),B=f(\beta),C=f(\beta),D=f(\beta)$")
	t = r"$\varepsilon^* = f(A,B,C,D)$"
	plt.text(0.8,0.55,t)
	plt.xlabel(r'$\varepsilon^*/\varepsilon_0$')
	plt.ylabel(r'$\sigma^*/f_t$')
	plt.legend()
	plt.tight_layout()
	# plt.savefig("FourParameter\\Figs\\DifferentABCD.pdf")
	plt.show()
	# plt.close()

	

	